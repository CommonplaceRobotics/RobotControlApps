#include "AppClient.h"

#include <grpcpp/create_channel.h>

#include <exception>
#include <iostream>

namespace App
{

/**
 * @brief Constructor, sets up the connection
 * @param appName app name
 * @param target connection target in the following format: "hostname:port" or "ip:port", e.g. "localhost:5000"
 */
AppClient::AppClient(const std::string& appName, const std::string& target) : m_appName(appName)
{
    std::shared_ptr<grpc::Channel> channel = grpc::CreateChannel(target, grpc::InsecureChannelCredentials());
    m_grpcStub = robotcontrolapp::RobotControlApp::NewStub(channel);
}

/**
 * @brief Destructor
 */
AppClient::~AppClient()
{
    Disconnect();
}

/**
 * @brief Connects the app
 */
void AppClient::Connect()
{
    std::unique_lock<std::recursive_mutex> threadLock(m_threadMutex);
    if (!m_stopThreads)
    {
        std::cout << "Connecting app '" << GetAppName() << '\'' << std::endl;
        m_stopThreads = false;

        // clear queue
        std::unique_lock<std::mutex> actionsLock(m_actionsMutex);
        m_actionsQueue = std::queue<robotcontrolapp::AppAction>();
        actionsLock.unlock();

        // Send an empty action at startup (this is queued and sent later by the thread)
        SendAction(robotcontrolapp::AppAction());

        // Start threads
        m_grpcStream =
            std::shared_ptr<grpc::ClientReaderWriter<robotcontrolapp::AppAction, robotcontrolapp::Event>>(m_grpcStub->RecieveActions(&m_grpcStreamContext));
        m_eventReaderThread = std::thread(&AppClient::EventReaderThread, this);
        m_actionsWriterThread = std::thread(&AppClient::ActionsWriterThread, this);
    }
    else
    {
        std::cerr << "Connect requested for app '" << GetAppName() << "' but it is still connected. Please call disconnect first!" << std::endl;
    }
}

/**
 * @brief Disconnects the app
 */
void AppClient::Disconnect()
{
    std::unique_lock<std::recursive_mutex> lock(m_threadMutex);
    if (m_grpcStream)
    {
        std::cout << "Disconnecting app '" << GetAppName() << '\'' << std::endl;
        m_stopThreads = true;
        if (m_eventReaderThread.joinable()) m_eventReaderThread.join();
        if (m_actionsWriterThread.joinable()) m_actionsWriterThread.join();
        if (m_grpcStream)
        {
            grpc::Status status = m_grpcStream->Finish();
            if (!status.ok())
            {
                std::cerr << "Stream status not okay";
                if (!status.error_message().empty()) std::cerr << ": " << status.error_message();
                std::cerr << std::endl;
            }
        }
        m_grpcStream = nullptr;
        std::cout << "App '" << GetAppName() << "' disconnected" << std::endl;
    }
}

/**
 * @brief Thread method for the event reader. This is used for UI events.
 * @param stream GRPC stream
 */
void AppClient::EventReaderThread()
{
    try
    {
        robotcontrolapp::Event m_Event;
        while (!m_stopThreads)
        {
            if (m_grpcStream->Read(&m_Event))
            {
                // Read UI events and call handler
                // std::cout << "Event recived (ui updates:" << event.ui_updates_size() << ")" << std::endl;
                std::map<std::string, const robotcontrolapp::AppUIElement*> updates;
                for (int i = 0; i < m_Event.ui_updates_size(); i += 1) updates[m_Event.ui_updates(i).element_name()] = &m_Event.ui_updates(i);
                if (!updates.empty()) UiUpdateHandler(updates);

                // Call handler for app function events
                if (m_Event.has_function()) AppFunctionHandler(m_Event.function());

                // Handler for disconnect requests
                if (m_Event.has_disconnect_request())
                {
                    std::cout << "Server requested disconnect, reason: " << m_Event.disconnect_request().reason() << std::endl;
                    m_stopThreads = true;
                    return;
                }
            }
            else
            {
                std::cout << "Read stream closed" << std::endl;
                m_stopThreads = true;
            }
        }
    }
    catch (std::exception& ex)
    {
        std::cerr << "Exception in EventReaderThread: " << ex.what() << std::endl;
    }
    m_stopThreads = true;
}

/**
 * @brief Thread method for the actions writer
 * @param stream GRPC stream
 */
void AppClient::ActionsWriterThread()
{
    try
    {
        while (!m_stopThreads)
        {
            std::unique_lock<std::mutex> lock(m_actionsMutex);
            if (!m_actionsQueue.empty())
            {
                // Send actions
                robotcontrolapp::AppAction actionToSend = m_actionsQueue.front();
                m_actionsQueue.pop();
                lock.unlock();
                actionToSend.set_app_name(GetAppName());
                if (!m_grpcStream->Write(actionToSend))
                {
                    std::cout << "Write stream closed" << std::endl;
                    m_stopThreads = true;
                }
            }
            else
            {
                lock.unlock();
                std::this_thread::sleep_for(std::chrono::milliseconds(5));
            }
        }
        m_grpcStream->WritesDone();
    }
    catch (std::exception& ex)
    {
        std::cerr << "Exception in ActionsWriterThread: " << ex.what() << std::endl;
    }
    m_stopThreads = true;
}

/**
 * @brief Queues an action to be sent to the robot control
 * @param action app action
 */
void AppClient::SendAction(const robotcontrolapp::AppAction& action)
{
    if (!m_stopThreads)
    {
        std::unique_lock<std::mutex> lock(m_actionsMutex);
        m_actionsQueue.push(action);
    }
}

/**
 * @brief Gets the tool center point position and orientation
 * @return TCP matrix
 */
DataTypes::Matrix44 AppClient::GetTcp()
{
    if (!IsConnected()) throw std::runtime_error("not connected");

    grpc::ClientContext context;
    robotcontrolapp::GetTCPRequest request;
    request.set_app_name(GetAppName());
    robotcontrolapp::Matrix44 response;
    grpc::Status status = m_grpcStub->GetTCP(&context, request, &response);
    if (!status.ok())
    {
        throw std::runtime_error("request GetTCP failed: " + status.error_message());
    }

    return DataTypes::Matrix44(response);
}

/**
 * @brief Gets the program variable, throws exception on error, e.g. if the variable does not exist
 * @param variableName name of the variable
 * @return NumberVariable or PositionVariable
 */
std::shared_ptr<DataTypes::ProgramVariable> AppClient::GetProgramVariable(const std::string& variableName)
{
    if (variableName.empty()) throw std::runtime_error("requested variable with empty name");

    std::set<std::string> names{variableName};
    auto result = GetProgramVariables({variableName});
    if (result.find(variableName) == result.end()) throw std::runtime_error("failed to get variable '" + variableName + "': variable does not exist");
    return result[variableName];
}

/**
 * @brief Gets the given number variable, throws on error, e.g. if the variable does not exist or is of a different type
 * @param variableName name of the variable
 * @return number variable
 */
std::shared_ptr<DataTypes::NumberVariable> AppClient::GetNumberVariable(const std::string& variableName)
{
    std::shared_ptr<DataTypes::NumberVariable> variable = std::dynamic_pointer_cast<DataTypes::NumberVariable>(GetProgramVariable(variableName));
    if (variable == nullptr) throw std::runtime_error("requested variable '" + variableName + "' is no number variable");
    return variable;
}

/**
 * @brief Gets the given position variable, throws on error, e.g. if the variable does not exist or is of a different type
 * @param variableName name of the variable
 * @return position variable
 */
std::shared_ptr<DataTypes::PositionVariable> AppClient::GetPositionVariable(const std::string& variableName)
{
    std::shared_ptr<DataTypes::PositionVariable> variable = std::dynamic_pointer_cast<DataTypes::PositionVariable>(GetProgramVariable(variableName));
    if (variable == nullptr) throw std::runtime_error("requested variable '" + variableName + "' is no position variable");
    return variable;
}

/**
 * @brief Gets program variables
 * @param variableNames set of program variables to request
 * @return map of program variables, key is the variable name
 */
std::map<std::string, std::shared_ptr<DataTypes::ProgramVariable>> AppClient::GetProgramVariables(const std::unordered_set<std::string>& variableNames)
{
    if (!IsConnected()) throw std::runtime_error("not connected");

    std::map<std::string, std::shared_ptr<DataTypes::ProgramVariable>> result;

    grpc::ClientContext context;
    robotcontrolapp::ProgramVariablesRequest request;
    request.set_app_name(GetAppName());
    for (const std::string& varName : variableNames) request.add_variable_names(varName.c_str());

    auto variablesReader = m_grpcStub->GetProgramVariables(&context, request);
    robotcontrolapp::ProgramVariable response;

    while (variablesReader->Read(&response))
    {
        switch (response.value_case())
        {
            case robotcontrolapp::ProgramVariable::kNumber:
                result[response.name()] = std::make_shared<DataTypes::NumberVariable>(response.name(), response.number());
                break;
            case robotcontrolapp::ProgramVariable::kPosition:
                switch (response.position().value_case())
                {
                    case robotcontrolapp::ProgramVariable_ProgramVariablePosition::kRobotJoints:
                    {
                        std::array<double, DataTypes::PositionVariable::ROBOT_AXES_COUNT> robotAxes = {0};
                        std::array<double, DataTypes::PositionVariable::EXTERNAL_AXES_COUNT> externalAxes = {0};
                        for (int i = 0; i < response.position().robot_joints().joints_size() && i < (int)robotAxes.size(); i++)
                        {
                            robotAxes[i] = response.position().robot_joints().joints(i);
                        }
                        for (int i = 0; i < response.position().external_joints_size() && i < (int)externalAxes.size(); i++)
                        {
                            externalAxes[i] = response.position().external_joints(i);
                        }
                        result[response.name()] = std::make_shared<DataTypes::PositionVariable>(response.name(), robotAxes, externalAxes);
                    }
                    break;
                    case robotcontrolapp::ProgramVariable_ProgramVariablePosition::kBoth:
                    {
                        std::array<double, DataTypes::PositionVariable::ROBOT_AXES_COUNT> robotAxes = {0};
                        std::array<double, DataTypes::PositionVariable::EXTERNAL_AXES_COUNT> externalAxes = {0};
                        for (int i = 0; i < response.position().both().robot_joints().joints_size() && i < (int)robotAxes.size(); i++)
                        {
                            robotAxes[i] = response.position().both().robot_joints().joints(i);
                        }
                        for (int i = 0; i < response.position().external_joints_size() && i < (int)externalAxes.size(); i++)
                        {
                            externalAxes[i] = response.position().external_joints(i);
                        }
                        DataTypes::Matrix44 cartesian(response.position().both().cartesian());
                        result[response.name()] = std::make_shared<DataTypes::PositionVariable>(response.name(), cartesian, robotAxes, externalAxes);
                    }
                    break;
                    case robotcontrolapp::ProgramVariable_ProgramVariablePosition::kCartesian:
                    {
                        std::array<double, DataTypes::PositionVariable::EXTERNAL_AXES_COUNT> externalAxes = {0};
                        for (int i = 0; i < response.position().external_joints_size() && i < (int)externalAxes.size(); i++)
                        {
                            externalAxes[i] = response.position().external_joints(i);
                        }
                        DataTypes::Matrix44 cartesian(response.position().cartesian());
                        result[response.name()] = std::make_shared<DataTypes::PositionVariable>(response.name(), cartesian, externalAxes);
                    }
                    break;
                    default:
                        std::cerr << "received unknown variable value type" << std::endl;
                        break;
                }
                break;
            default:
                std::cerr << "received unknown variable type" << std::endl;
                break;
        }
    }
    return result;
}

/**
 * @brief Sets a number variable
 * @param name name of the variable
 * @param value value to set
 */
void AppClient::SetNumberVariable(const std::string& name, double value)
{
    if (!IsConnected()) throw std::runtime_error("not connected");

    grpc::ClientContext context;
    robotcontrolapp::SetProgramVariablesRequest request;
    request.set_app_name(GetAppName());
    auto variable = request.add_variables();
    variable->set_name(name);
    variable->set_number(value);
    robotcontrolapp::SetProgramVariablesResponse response;
    grpc::Status status = m_grpcStub->SetProgramVariables(&context, request, &response);
    if (!status.ok())
    {
        throw std::runtime_error("request SetProgramVariables failed: " + status.error_message());
    }
}

/**
 * @brief Sets a position variable with joint angles. The robot control will try to convert these to cartesian.
 * @param name name of the variable
 * @param a1 position of robot axis 1 in degrees or mm
 * @param a2 position of robot axis 2 in degrees or mm
 * @param a3 position of robot axis 3 in degrees or mm
 * @param a4 position of robot axis 4 in degrees or mm
 * @param a5 position of robot axis 5 in degrees or mm
 * @param a6 position of robot axis 6 in degrees or mm
 * @param e1 position of external axis 1 in degrees, mm or user defined units
 * @param e2 position of external axis 2 in degrees, mm or user defined units
 * @param e3 position of external axis 3 in degrees, mm or user defined units
 */
void AppClient::SetPositionVariable(const std::string& name, double a1, double a2, double a3, double a4, double a5, double a6, double e1, double e2, double e3)
{
    if (!IsConnected()) throw std::runtime_error("not connected");

    grpc::ClientContext context;
    robotcontrolapp::SetProgramVariablesRequest request;
    request.set_app_name(GetAppName());
    auto variable = request.add_variables();
    variable->set_name(name);
    auto position = variable->mutable_position();
    position->mutable_robot_joints()->add_joints(a1);
    position->mutable_robot_joints()->add_joints(a2);
    position->mutable_robot_joints()->add_joints(a3);
    position->mutable_robot_joints()->add_joints(a4);
    position->mutable_robot_joints()->add_joints(a5);
    position->mutable_robot_joints()->add_joints(a6);
    position->add_external_joints(e1);
    position->add_external_joints(e2);
    position->add_external_joints(e3);
    robotcontrolapp::SetProgramVariablesResponse response;
    grpc::Status status = m_grpcStub->SetProgramVariables(&context, request, &response);
    if (!status.ok())
    {
        throw std::runtime_error("request SetProgramVariables failed: " + status.error_message());
    }
}

/**
 * @brief Sets a position variable with a cartesian position. The robot control will try to convert this to joint angles.
 * @param name name of the variable
 * @param cartesianPosition cartesian position and orientation
 * @param e1 position of external axis 1 in degrees, mm or user defined units
 * @param e2 position of external axis 2 in degrees, mm or user defined units
 * @param e3 position of external axis 3 in degrees, mm or user defined units
 */
void AppClient::SetPositionVariable(const std::string& name, DataTypes::Matrix44 cartesianPosition, double e1, double e2, double e3)
{
    if (!IsConnected()) throw std::runtime_error("not connected");

    grpc::ClientContext context;
    robotcontrolapp::SetProgramVariablesRequest request;
    request.set_app_name(GetAppName());
    auto variable = request.add_variables();
    variable->set_name(name);
    auto position = variable->mutable_position();
    *position->mutable_cartesian() = cartesianPosition.ToGrpc();
    position->add_external_joints(e1);
    position->add_external_joints(e2);
    position->add_external_joints(e3);
    robotcontrolapp::SetProgramVariablesResponse response;
    grpc::Status status = m_grpcStub->SetProgramVariables(&context, request, &response);
    if (!status.ok())
    {
        throw std::runtime_error("request SetProgramVariables failed: " + status.error_message());
    }
}

/**
 * @brief Sets a position variable with joint angles and cartesian position. Warning: joint angles and cartesian may refer to different positions!
 * @param name name of the variable
 * @param cartesianPosition cartesian position and orientation
 * @param a1 position of robot axis 1 in degrees or mm
 * @param a2 position of robot axis 2 in degrees or mm
 * @param a3 position of robot axis 3 in degrees or mm
 * @param a4 position of robot axis 4 in degrees or mm
 * @param a5 position of robot axis 5 in degrees or mm
 * @param a6 position of robot axis 6 in degrees or mm
 * @param e1 position of external axis 1 in degrees, mm or user defined units
 * @param e2 position of external axis 2 in degrees, mm or user defined units
 * @param e3 position of external axis 3 in degrees, mm or user defined units
 */
void AppClient::SetPositionVariable(const std::string& name, DataTypes::Matrix44 cartesianPosition, double a1, double a2, double a3, double a4, double a5,
                                    double a6, double e1, double e2, double e3)
{
    if (!IsConnected()) throw std::runtime_error("not connected");

    grpc::ClientContext context;
    robotcontrolapp::SetProgramVariablesRequest request;
    request.set_app_name(GetAppName());
    auto variable = request.add_variables();
    variable->set_name(name);
    auto position = variable->mutable_position();
    *position->mutable_cartesian() = cartesianPosition.ToGrpc();
    position->mutable_robot_joints()->add_joints(a1);
    position->mutable_robot_joints()->add_joints(a2);
    position->mutable_robot_joints()->add_joints(a3);
    position->mutable_robot_joints()->add_joints(a4);
    position->mutable_robot_joints()->add_joints(a5);
    position->mutable_robot_joints()->add_joints(a6);
    position->add_external_joints(e1);
    position->add_external_joints(e2);
    position->add_external_joints(e3);
    robotcontrolapp::SetProgramVariablesResponse response;
    grpc::Status status = m_grpcStub->SetProgramVariables(&context, request, &response);
    if (!status.ok())
    {
        throw std::runtime_error("request SetProgramVariables failed: " + status.error_message());
    }
}

/**
 * @brief Announces to the robot control that the app function call finished. This allows the robot program to continue with the next command.
 * @param callId function call ID from the function call request
 */
void AppClient::SendFunctionDone(int64_t callId)
{
    robotcontrolapp::AppAction response;
    response.add_done_functions(callId);
    SendAction(response);
}

/**
 * @brief Requests the state of a UI element. The robot control will respond with a call of UiUpdateHandler() if the element exists and if it was changed after
 * start up
 * @param elementName ID of the requested UI element
 */
void AppClient::RequestUIElementState(const std::string& elementName)
{
    robotcontrolapp::AppAction request;
    request.add_request_ui_state(elementName);
    SendAction(request);
}
/**
 * @brief Requests the state of several UI elements. The robot control will respond with a call of UiUpdateHandler() if the element exists and if it was changed
 * after start up
 * @param elementNames set of UI element names
 */
void AppClient::RequestUIElementStates(const std::unordered_set<std::string>& elementNames)
{
    robotcontrolapp::AppAction request;
    for (const std::string& name : elementNames) request.add_request_ui_state(name);
    SendAction(request);
}

/**
 * @brief Sets a UI element visible or hidden
 * @param elementName ID of the UI element
 * @param visible true to set the element visible or false to hide it
 */
void AppClient::SetUIVisibility(const std::string& elementName, bool visible)
{
    robotcontrolapp::AppAction request;
    robotcontrolapp::AppUIElement& uiElement = *request.add_ui_changes();
    uiElement.set_element_name(elementName);
    uiElement.set_is_visible(visible);
    SendAction(request);
}

/**
 * @brief Set a list of UI element visible or hidden
 * @param elements list of elements and visibility (key is the element name, value is the visibility state)
 */
void AppClient::SetUIVisibility(const std::unordered_map<std::string, bool>& elements)
{
    robotcontrolapp::AppAction request;
    for (auto& element : elements)
    {
        robotcontrolapp::AppUIElement& uiElement = *request.add_ui_changes();
        uiElement.set_element_name(element.first);
        uiElement.set_is_visible(element.second);
    }
    SendAction(request);
}

/**
 * @brief Sets the checked state of a checkbox
 * @param elementName ID of the UI element
 * @param isChecked if true the check box will be checked
 */
void AppClient::SetCheckboxState(const std::string& elementName, bool isChecked)
{
    robotcontrolapp::AppAction request;
    robotcontrolapp::AppUIElement& uiElement = *request.add_ui_changes();
    uiElement.set_element_name(elementName);
    uiElement.mutable_state()->set_checkbox_state(isChecked ? robotcontrolapp::CHECKED : robotcontrolapp::UNCHECKED);
    SendAction(request);
}

/**
 * @brief Sets the selected value of a drop down box
 * @param elementName ID of the UI element
 * @param selectedValue selected value
 */
void AppClient::SetDropDownState(const std::string& elementName, const std::string& selectedValue)
{
    SetText(elementName, selectedValue);
}

/**
 * @brief Sets the selected value and the list of selectable values of a drop down box
 * @param elementName ID of the UI element
 * @param selectedValue selected value
 * @param selectableEntries selectable values. If empty the current list will be kept.
 */
void AppClient::SetDropDownState(const std::string& elementName, const std::string& selectedValue, const std::list<std::string>& selectableEntries)
{
    robotcontrolapp::AppAction request;
    robotcontrolapp::AppUIElement& uiElement = *request.add_ui_changes();
    uiElement.set_element_name(elementName);
    uiElement.mutable_state()->mutable_dropdown_state()->set_selected_option(selectedValue);
    for (const std::string& entry : selectableEntries)
    {
        *uiElement.mutable_state()->mutable_dropdown_state()->add_options() = entry;
    }
    SendAction(request);
}

/**
 * @brief Sets the text of a text box, label, etc.
 * @param elementName ID of the UI element
 * @param value text
 */
void AppClient::SetText(const std::string& elementName, const std::string& value)
{
    robotcontrolapp::AppAction request;
    robotcontrolapp::AppUIElement& uiElement = *request.add_ui_changes();
    uiElement.set_element_name(elementName);
    uiElement.mutable_state()->mutable_textfield_state()->set_current_text(value);
    SendAction(request);
}

/**
 * @brief Sets the number value of a number box, text box, label, etc.
 * @param elementName ID of the UI element
 * @param value number
 */
void AppClient::SetNumber(const std::string& elementName, double value)
{
    robotcontrolapp::AppAction request;
    robotcontrolapp::AppUIElement& uiElement = *request.add_ui_changes();
    uiElement.set_element_name(elementName);
    uiElement.mutable_state()->mutable_numberfield_state()->set_current_number(value);
    SendAction(request);
}

/**
 * @brief Sets the image of an image element in the UI
 * @param elementName ID of the UI element
 * @param imageWidth width of the image UI element (does not need to be equal to the image width, image will be scaled)
 * @param imageHeight height of the image UI element (does not need to be equal to the image height, image will be scaled)
 * @param imageData binary image data
 * @param imageDataLength length of the image data
 * @param encoding image format
 */
void AppClient::SetImage(const std::string& elementName, unsigned uiWidth, unsigned uiHeight, uint8_t* imageData, size_t imageDataLength,
                         robotcontrolapp::ImageState::ImageData::ImageEncoding encoding)
{
    robotcontrolapp::AppAction request;
    robotcontrolapp::AppUIElement& uiElement = *request.add_ui_changes();
    uiElement.set_element_name(elementName);
    uiElement.mutable_state()->mutable_image_state()->mutable_image_data()->set_height(uiHeight);
    uiElement.mutable_state()->mutable_image_state()->mutable_image_data()->set_width(uiWidth);
    uiElement.mutable_state()->mutable_image_state()->mutable_image_data()->set_encoding(encoding);
    uiElement.mutable_state()->mutable_image_state()->mutable_image_data()->set_data(imageData, imageDataLength);
    SendAction(request);
}

} // namespace App
