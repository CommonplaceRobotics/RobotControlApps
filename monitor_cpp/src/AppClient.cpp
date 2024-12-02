#include "AppClient.h"

#include <grpcpp/create_channel.h>

#include <exception>
#include <fstream>
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
        StopRobotStateStream();
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
 * @brief Resets hardware errors and disables the motors
 */
void AppClient::ResetErrors() {
    if (!IsConnected()) throw std::runtime_error("not connected");

    robotcontrolapp::ResetErrorsRequest request;
    request.set_app_name(GetAppName());

    robotcontrolapp::ResetErrorsResponse response;
    grpc::ClientContext context;
    auto status = m_grpcStub->ResetErrors(&context, request, &response);
    if (!status.ok())
    {
        throw std::runtime_error("request ResetErrors failed: " + status.error_message());
    }
}

/**
 * @brief Resets hardware errors and enables the motors
 */
void AppClient::EnableMotors()
{
    if (!IsConnected()) throw std::runtime_error("not connected");

    robotcontrolapp::EnableMotorsRequest request;
    request.set_app_name(GetAppName());
    request.set_enable(true);

    robotcontrolapp::EnableMotorsResponse response;
    grpc::ClientContext context;
    auto status = m_grpcStub->EnableMotors(&context, request, &response);
    if (!status.ok())
    {
        throw std::runtime_error("request EnableMotors failed: " + status.error_message());
    }
}

/**
 * @brief Disables the motors and IO
 */
void AppClient::DisableMotors()
{
    if (!IsConnected()) throw std::runtime_error("not connected");

    robotcontrolapp::EnableMotorsRequest request;
    request.set_app_name(GetAppName());
    request.set_enable(false);

    robotcontrolapp::EnableMotorsResponse response;
    grpc::ClientContext context;
    auto status = m_grpcStub->EnableMotors(&context, request, &response);
    if (!status.ok())
    {
        throw std::runtime_error("request EnableMotors failed: " + status.error_message());
    }
}

/**
 * @brief Starts referencing all joints
 * @param withReferencingProgram if true: call referencing program after referencing, then reference again
 */
void AppClient::ReferenceAllJoints(bool withReferencingProgram)
{
    if (!IsConnected()) throw std::runtime_error("not connected");

    robotcontrolapp::ReferenceJointsRequest request;
    request.set_app_name(GetAppName());
    request.set_reference_all(true);
    request.set_referencing_program(withReferencingProgram);

    robotcontrolapp::ReferenceJointsResponse response;
    grpc::ClientContext context;
    auto status = m_grpcStub->ReferenceJoints(&context, request, &response);
    if (!status.ok())
    {
        throw std::runtime_error("request ReferenceJoints failed: " + status.error_message());
    }
}

/**
 * @brief Runs the referencing program, then references again. Does not reference before calling the program.
 */
void AppClient::ReferencingProgram()
{
    if (!IsConnected()) throw std::runtime_error("not connected");

    robotcontrolapp::ReferenceJointsRequest request;
    request.set_app_name(GetAppName());
    request.set_reference_all(false);
    request.set_referencing_program(true);

    robotcontrolapp::ReferenceJointsResponse response;
    grpc::ClientContext context;
    auto status = m_grpcStub->ReferenceJoints(&context, request, &response);
    if (!status.ok())
    {
        throw std::runtime_error("request ReferencingProgram failed: " + status.error_message());
    }
}

/**
 * @brief Starts referencing a robot joint
 * @param n joint number 0..6
 */
void AppClient::ReferenceRobotJoint(unsigned n)
{
    if (!IsConnected()) throw std::runtime_error("not connected");

    robotcontrolapp::ReferenceJointsRequest request;
    request.set_app_name(GetAppName());
    request.set_reference_all(false);
    request.set_referencing_program(false);
    request.add_reference_robot_joints(n);

    robotcontrolapp::ReferenceJointsResponse response;
    grpc::ClientContext context;
    auto status = m_grpcStub->ReferenceJoints(&context, request, &response);
    if (!status.ok())
    {
        throw std::runtime_error("request ReferenceJoints failed: " + status.error_message());
    }
}

/**
 * @brief Starts referencing an external joint
 * @param n joint number 0..3
 */
void AppClient::ReferenceExternalJoint(unsigned n)
{
    if (!IsConnected()) throw std::runtime_error("not connected");

    robotcontrolapp::ReferenceJointsRequest request;
    request.set_app_name(GetAppName());
    request.set_reference_all(false);
    request.set_referencing_program(false);
    request.add_reference_external_joints(n);

    robotcontrolapp::ReferenceJointsResponse response;
    grpc::ClientContext context;
    auto status = m_grpcStub->ReferenceJoints(&context, request, &response);
    if (!status.ok())
    {
        throw std::runtime_error("request ReferenceJoints failed: " + status.error_message());
    }
}

/**
 * @brief Starts referencing robot and external joints without delay
 * @param robotJoints set of robot joint numbers 0..6
 * @param externalJoints set of external joint numbers 0..3
 */
void AppClient::ReferenceJoints(std::set<int> robotJoints, std::set<int> externalJoints)
{
    if (!IsConnected()) throw std::runtime_error("not connected");

    robotcontrolapp::ReferenceJointsRequest request;
    request.set_app_name(GetAppName());
    request.set_reference_all(false);
    request.set_referencing_program(false);
    for (int n : robotJoints) request.add_reference_robot_joints(n);
    for (int n : externalJoints) request.add_reference_external_joints(n);

    robotcontrolapp::ReferenceJointsResponse response;
    grpc::ClientContext context;
    auto status = m_grpcStub->ReferenceJoints(&context, request, &response);
    if (!status.ok())
    {
        throw std::runtime_error("request ReferenceJoints failed: " + status.error_message());
    }
}

/**
 * @brief Starts streaming the robot state
 */
void AppClient::StartRobotStateStream() {
    if (!IsConnected()) throw std::runtime_error("not connected");

    std::unique_lock<std::recursive_mutex> lock(m_threadMutex);
    if (m_robotStateThread.joinable()) StopRobotStateStream();
    m_robotStateStreamActive = true;
    m_robotStateThread = std::thread(&AppClient::RobotStateThread, this);
}

/**
 * @brief Stops streaming the robot state
 */
void AppClient::StopRobotStateStream() {
    std::unique_lock<std::recursive_mutex> lock(m_threadMutex);
    m_robotStateStreamActive = true;
    if (m_robotStateThread.joinable()) m_robotStateThread.join();
}

/**
 * @brief Thread method for the RobotState reader
 */
void AppClient::RobotStateThread()
{
    try
    {
        grpc::ClientContext context;
        robotcontrolapp::RobotStateRequest request;
        request.set_app_name(GetAppName());

        auto reader = m_grpcStub->GetRobotStateStream(&context, request);
        robotcontrolapp::RobotState response;

        while (m_robotStateStreamActive && IsConnected())
        {
            if (reader->Read(&response))
            {
                OnRobotStateUpdated(response);
            }
            else
            {
                std::cerr << "RobotState read stream closed" << std::endl;
                m_stopThreads = true;
                break;
            }
        }
    }
    catch (std::exception& ex)
    {
        std::cerr << "Exception in RobotStateThread: " << ex.what() << std::endl;
    }
    m_robotStateStreamActive = false;
}

/**
 * @brief Gets the current state
 * @return robot state
 */
DataTypes::RobotState AppClient::GetRobotState()
{
    if (!IsConnected()) throw std::runtime_error("not connected");

    robotcontrolapp::RobotStateRequest request;
    request.set_app_name(GetAppName());
    
    robotcontrolapp::RobotState response;
    grpc::ClientContext context;
    auto status = m_grpcStub->GetRobotState(&context, request, &response);
    if (!status.ok())
    {
        throw std::runtime_error("request GetRobotState failed: " + status.error_message());
    }

    return DataTypes::RobotState(response);
}

/**
 * @brief Sets the state of a digital input (only in simulation)
 * @param number input number (0-63)
 * @param state target state
 */
void AppClient::SetDigitalInput(unsigned number, bool state) {
    robotcontrolapp::IOStateRequest request;
    request.set_app_name(GetAppName());

    auto din = request.add_dins();
    din->set_id(number);
    din->set_state(state ? robotcontrolapp::DIOState::HIGH : robotcontrolapp::DIOState::LOW);

    robotcontrolapp::IOStateResponse response;
    grpc::ClientContext context;
    auto status = m_grpcStub->SetIOState(&context, request, &response);
    if (!status.ok())
    {
        throw std::runtime_error("request SetIOState failed: " + status.error_message());
    }
}

/**
 * @brief Sets the states of the digital inputs (only in simulation)
 * @param inputs set of digital inputs to set
 */
void AppClient::SetDigitalInputs(const std::set<std::pair<unsigned, bool>>& inputs) 
{
    robotcontrolapp::IOStateRequest request;
    request.set_app_name(GetAppName());

    for (const auto& input : inputs)
    {
        auto din = request.add_dins();
        din->set_id(input.first);
        din->set_state(input.second ? robotcontrolapp::DIOState::HIGH : robotcontrolapp::DIOState::LOW);
    }

    robotcontrolapp::IOStateResponse response;
    grpc::ClientContext context;
    auto status = m_grpcStub->SetIOState(&context, request, &response);
    if (!status.ok())
    {
        throw std::runtime_error("request SetIOState failed: " + status.error_message());
    }
}

/**
 * @brief Sets the state of a digital output
 * @param number output number (0-63)
 * @param state target state
 */
void AppClient::SetDigitalOutput(unsigned number, bool state) {
    robotcontrolapp::IOStateRequest request;
    request.set_app_name(GetAppName());

    auto dout = request.add_douts();
    dout->set_id(number);
    dout->set_target_state(state ? robotcontrolapp::DIOState::HIGH : robotcontrolapp::DIOState::LOW);

    robotcontrolapp::IOStateResponse response;
    grpc::ClientContext context;
    auto status = m_grpcStub->SetIOState(&context, request, &response);
    if (!status.ok())
    {
        throw std::runtime_error("request SetIOState failed: " + status.error_message());
    }
}

/**
 * @brief Sets the states of the digital outputs
 * @param outputs set of digital outputs to set
 */
void AppClient::SetDigitalOutputs(const std::set<std::pair<unsigned, bool>>& outputs) {
    robotcontrolapp::IOStateRequest request;
    request.set_app_name(GetAppName());

    for (const auto& output : outputs)
    {
        auto dout = request.add_douts();
        dout->set_id(output.first);
        dout->set_target_state(output.second ? robotcontrolapp::DIOState::HIGH : robotcontrolapp::DIOState::LOW);
    }

    robotcontrolapp::IOStateResponse response;
    grpc::ClientContext context;
    auto status = m_grpcStub->SetIOState(&context, request, &response);
    if (!status.ok())
    {
        throw std::runtime_error("request SetIOState failed: " + status.error_message());
    }
}

/**
 * @brief Sets the state of a global signal
 * @param number global signal number (0-99)
 * @param state target state
 */
void AppClient::SetGlobalSignal(unsigned number, bool state) {
    robotcontrolapp::IOStateRequest request;
    request.set_app_name(GetAppName());

    auto gsig = request.add_gsigs();
    gsig->set_id(number);
    gsig->set_target_state(state ? robotcontrolapp::DIOState::HIGH : robotcontrolapp::DIOState::LOW);

    robotcontrolapp::IOStateResponse response;
    grpc::ClientContext context;
    auto status = m_grpcStub->SetIOState(&context, request, &response);
    if (!status.ok())
    {
        throw std::runtime_error("request SetIOState failed: " + status.error_message());
    }
}

/**
 * @brief Sets the states of the global signals
 * @param outputs set of global signals to set
 */
void AppClient::SetGlobalSignals(const std::set<std::pair<unsigned, bool>>& signals) {
    robotcontrolapp::IOStateRequest request;
    request.set_app_name(GetAppName());

    for (const auto& signal : signals)
    {
        auto gsig = request.add_gsigs();
        gsig->set_id(signal.first);
        gsig->set_target_state(signal.second ? robotcontrolapp::DIOState::HIGH : robotcontrolapp::DIOState::LOW);
    }

    robotcontrolapp::IOStateResponse response;
    grpc::ClientContext context;
    auto status = m_grpcStub->SetIOState(&context, request, &response);
    if (!status.ok())
    {
        throw std::runtime_error("request SetIOState failed: " + status.error_message());
    }
}

/**
 * @brief Gets the current motion state (program execution etc)
 * @return
 */
DataTypes::MotionState AppClient::GetMotionState()
{
    if (!IsConnected()) throw std::runtime_error("not connected");

    robotcontrolapp::GetMotionStateRequest request;
    request.set_app_name(GetAppName());

    robotcontrolapp::MotionState response;
    grpc::ClientContext context;
    auto status = m_grpcStub->GetMotionState(&context, request, &response);
    if (!status.ok())
    {
        throw std::runtime_error("request GetMotionState failed: " + status.error_message());
    }

    return DataTypes::MotionState(response);
}

/**
 * @brief Loads a motion program
 * @param program program to load, relative to the Data/Programs directory
 */
DataTypes::MotionState AppClient::LoadMotionProgram(const std::string& program)
{
    if (!IsConnected()) throw std::runtime_error("not connected");

    robotcontrolapp::MotionInterpolatorRequest request;
    request.set_app_name(GetAppName());
    request.set_main_program(program);

    robotcontrolapp::MotionState response;
    grpc::ClientContext context;
    auto status = m_grpcStub->SetMotionInterpolator(&context, request, &response);
    if (!status.ok())
    {
        throw std::runtime_error("request SetMotionInterpolator failed: " + status.error_message());
    }

    return DataTypes::MotionState(response);
}

/**
 * @brief Unloads the motion program
 */
DataTypes::MotionState AppClient::UnloadMotionProgram()
{
    return LoadMotionProgram("");
}

/**
 * @brief Starts or continues the motion program
 */
DataTypes::MotionState AppClient::StartMotionProgram()
{
    if (!IsConnected()) throw std::runtime_error("not connected");

    robotcontrolapp::MotionInterpolatorRequest request;
    request.set_app_name(GetAppName());
    request.set_runstate(robotcontrolapp::RunState::RUNNING);

    robotcontrolapp::MotionState response;
    grpc::ClientContext context;
    auto status = m_grpcStub->SetMotionInterpolator(&context, request, &response);
    if (!status.ok())
    {
        throw std::runtime_error("request SetMotionInterpolator failed: " + status.error_message());
    }

    return DataTypes::MotionState(response);
}

/**
 * @brief Starts or continues the motion program at a specific command
 * @param commandIdx command index within the current (sub-)program
 * @param subProgram sub-program or empty for main program
 */
DataTypes::MotionState AppClient::StartMotionProgramAt(unsigned commandIdx, const std::string& subProgram)
{
    if (!IsConnected()) throw std::runtime_error("not connected");

    robotcontrolapp::MotionInterpolatorRequest request;
    request.set_app_name(GetAppName());
    request.set_runstate(robotcontrolapp::RunState::RUNNING);
    if (!subProgram.empty()) request.mutable_start_at()->set_program(subProgram);
    request.mutable_start_at()->set_command(commandIdx);

    robotcontrolapp::MotionState response;
    grpc::ClientContext context;
    auto status = m_grpcStub->SetMotionInterpolator(&context, request, &response);
    if (!status.ok())
    {
        throw std::runtime_error("request SetMotionInterpolator failed: " + status.error_message());
    }

    return DataTypes::MotionState(response);
}

/**
 * @brief Pauses the motion program
 */
DataTypes::MotionState AppClient::PauseMotionProgram()
{
    if (!IsConnected()) throw std::runtime_error("not connected");

    robotcontrolapp::MotionInterpolatorRequest request;
    request.set_app_name(GetAppName());
    request.set_runstate(robotcontrolapp::RunState::PAUSED);

    robotcontrolapp::MotionState response;
    grpc::ClientContext context;
    auto status = m_grpcStub->SetMotionInterpolator(&context, request, &response);
    if (!status.ok())
    {
        throw std::runtime_error("request SetMotionInterpolator failed: " + status.error_message());
    }

    return DataTypes::MotionState(response);
}

/**
 * @brief Stops the motion program
 */
DataTypes::MotionState AppClient::StopMotionProgram()
{
    if (!IsConnected()) throw std::runtime_error("not connected");

    robotcontrolapp::MotionInterpolatorRequest request;
    request.set_app_name(GetAppName());
    request.set_runstate(robotcontrolapp::RunState::NOT_RUNNING);

    robotcontrolapp::MotionState response;
    grpc::ClientContext context;
    auto status =m_grpcStub->SetMotionInterpolator(&context, request, &response);
    if (!status.ok())
    {
        throw std::runtime_error("request SetMotionInterpolator failed: " + status.error_message());
    }

    return DataTypes::MotionState(response);
}

/**
 * @brief Sets the motion program to run once
 * @return
 */
DataTypes::MotionState AppClient::SetMotionProgramSingle()
{
    if (!IsConnected()) throw std::runtime_error("not connected");

    robotcontrolapp::MotionInterpolatorRequest request;
    request.set_app_name(GetAppName());
    request.set_replay_mode(robotcontrolapp::ReplayMode::SINGLE);

    robotcontrolapp::MotionState response;
    grpc::ClientContext context;
    auto status = m_grpcStub->SetMotionInterpolator(&context, request, &response);
    if (!status.ok())
    {
        throw std::runtime_error("request SetMotionInterpolator failed: " + status.error_message());

    }
    return DataTypes::MotionState(response);
}

/**
 * @brief Sets the motion program to repeat
 * @return
 */
DataTypes::MotionState AppClient::SetMotionProgramRepeat()
{
    if (!IsConnected()) throw std::runtime_error("not connected");

    robotcontrolapp::MotionInterpolatorRequest request;
    request.set_app_name(GetAppName());
    request.set_replay_mode(robotcontrolapp::ReplayMode::REPEAT);

    robotcontrolapp::MotionState response;
    grpc::ClientContext context;
    auto status = m_grpcStub->SetMotionInterpolator(&context, request, &response);
    if (!status.ok())
    {
        throw std::runtime_error("request SetMotionInterpolator failed: " + status.error_message());
    }

    return DataTypes::MotionState(response);
}

/**
 * @brief Sets the motion program to pause after each step
 * @return
 */
DataTypes::MotionState AppClient::SetMotionProgramStep()
{
    if (!IsConnected()) throw std::runtime_error("not connected");

    robotcontrolapp::MotionInterpolatorRequest request;
    request.set_app_name(GetAppName());
    request.set_replay_mode(robotcontrolapp::ReplayMode::STEP);

    robotcontrolapp::MotionState response;
    grpc::ClientContext context;
    auto status = m_grpcStub->SetMotionInterpolator(&context, request, &response);
    if (!status.ok())
    {
        throw std::runtime_error("request SetMotionInterpolator failed: " + status.error_message());
    }

    return DataTypes::MotionState(response);
}

/**
 * @brief Loads and starts a logic program
 * @param program program to load, relative to the Data/Programs directory
 */
DataTypes::MotionState AppClient::LoadLogicProgram(const std::string& program)
{
    if (!IsConnected()) throw std::runtime_error("not connected");

    robotcontrolapp::LogicInterpolatorRequest request;
    request.set_app_name(GetAppName());
    request.set_main_program(program);
    
    robotcontrolapp::MotionState response;
    grpc::ClientContext context;
    auto status = m_grpcStub->SetLogicInterpolator(&context, request, &response);
    if (!status.ok())
    {
        throw std::runtime_error("request SetLogicInterpolator failed: " + status.error_message());
    }

    return DataTypes::MotionState(response);
}

/**
 * @brief Unloads the logic program
 */
DataTypes::MotionState AppClient::UnloadLogicProgram()
{
    return LoadLogicProgram("");
}

/**
 * @brief Starts a joint motion to the given position
 * @param velocityPercent velocity in percent, 0.0..100.0
 * @param acceleration acceleration in percent, currently not used
 * @param a1 A1 target in degrees or mm
 * @param a2 A2 target in degrees or mm
 * @param a3 A3 target in degrees or mm
 * @param a4 A4 target in degrees or mm
 * @param a5 A5 target in degrees or mm
 * @param a6 A6 target in degrees or mm
 * @param e1 E1 target in degrees, mm or user defined units
 * @param e2 E2 target in degrees, mm or user defined units
 * @param e3 E3 target in degrees, mm or user defined units
 */
DataTypes::MotionState AppClient::MoveToJoint(float velocityPercent, float acceleration, double a1, double a2, double a3, double a4, double a5, double a6,
                                              double e1,
                                              double e2, double e3)
{
    if (!IsConnected()) throw std::runtime_error("not connected");

    robotcontrolapp::MoveToRequest request;
    request.set_app_name(GetAppName());
    robotcontrolapp::MoveToRequest_MoveToJoint* joint = new robotcontrolapp::MoveToRequest_MoveToJoint();
    joint->add_robot_joints(a1);
    joint->add_robot_joints(a2);
    joint->add_robot_joints(a3);
    joint->add_robot_joints(a4);
    joint->add_robot_joints(a5);
    joint->add_robot_joints(a6);
    joint->add_external_joints(e1);
    joint->add_external_joints(e2);
    joint->add_external_joints(e3);
    joint->set_velocity(velocityPercent);
    joint->set_acceleration(acceleration);
    request.set_allocated_joint(joint);

    robotcontrolapp::MotionState response;
    grpc::ClientContext context;
    auto status = m_grpcStub->MoveTo(&context, request, &response);
    if (!status.ok())
    {
        throw std::runtime_error("request MoveTo failed: " + status.error_message());
    }

    return DataTypes::MotionState(response);
}

/**
 * @brief Starts a relative joint motion to the given position
 * @param velocityPercent velocity in percent, 0.0..100.0
 * @param acceleration acceleration in percent, currently not used
 * @param a1 A1 target in degrees or mm
 * @param a2 A2 target in degrees or mm
 * @param a3 A3 target in degrees or mm
 * @param a4 A4 target in degrees or mm
 * @param a5 A5 target in degrees or mm
 * @param a6 A6 target in degrees or mm
 * @param e1 E1 target in degrees, mm or user defined units
 * @param e2 E2 target in degrees, mm or user defined units
 * @param e3 E3 target in degrees, mm or user defined units
 */
DataTypes::MotionState AppClient::MoveToJointRelative(float velocityPercent, float acceleration, double a1, double a2, double a3, double a4, double a5,
                                                      double a6,
                                                      double e1, double e2, double e3)
{
    if (!IsConnected()) throw std::runtime_error("not connected");

    robotcontrolapp::MoveToRequest request;
    request.set_app_name(GetAppName());
    robotcontrolapp::MoveToRequest_MoveToJoint* joint = new robotcontrolapp::MoveToRequest_MoveToJoint();
    joint->add_robot_joints(a1);
    joint->add_robot_joints(a2);
    joint->add_robot_joints(a3);
    joint->add_robot_joints(a4);
    joint->add_robot_joints(a5);
    joint->add_robot_joints(a6);
    joint->add_external_joints(e1);
    joint->add_external_joints(e2);
    joint->add_external_joints(e3);
    joint->set_velocity(velocityPercent);
    joint->set_acceleration(acceleration);
    request.set_allocated_joint_relative(joint);

    robotcontrolapp::MotionState response;
    grpc::ClientContext context;
    auto status = m_grpcStub->MoveTo(&context, request, &response);
    if (!status.ok())
    {
        throw std::runtime_error("request MoveTo failed: " + status.error_message());
    }

    return DataTypes::MotionState(response);
}

/**
 * @brief Starts a linear motion to the given position
 * @param velocityMms velocity in mm/s
 * @param acceleration acceleration in percent, currently not used
 * @param x X position in mm
 * @param y Y position in mm
 * @param z Z position in mm
 * @param a A orientation in mm
 * @param b B orientation in mm
 * @param c C orientation in mm
 * @param e1 E1 target in degrees, mm or user defined units
 * @param e2 E2 target in degrees, mm or user defined units
 * @param e3 E3 target in degrees, mm or user defined units
 * @param frame user frame or empty for base frame
 */
DataTypes::MotionState AppClient::MoveToLinear(float velocityMms, float acceleration, double x, double y, double z, double a, double b, double c, double e1,
                                               double e2,
                                               double e3, const std::string& frame)
{
    if (!IsConnected()) throw std::runtime_error("not connected");

    robotcontrolapp::MoveToRequest request;
    request.set_app_name(GetAppName());
    robotcontrolapp::MoveToRequest_MoveToCart* cart = new robotcontrolapp::MoveToRequest_MoveToCart();
    cart->mutable_position()->set_x(x);
    cart->mutable_position()->set_y(y);
    cart->mutable_position()->set_z(z);
    cart->mutable_orientation()->set_x(a);
    cart->mutable_orientation()->set_y(b);
    cart->mutable_orientation()->set_z(c);
    cart->add_external_joints(e1);
    cart->add_external_joints(e2);
    cart->add_external_joints(e3);
    cart->set_velocity(velocityMms);
    cart->set_acceleration(acceleration);
    cart->set_frame(frame);
    request.set_allocated_cart(cart);

    robotcontrolapp::MotionState response;
    grpc::ClientContext context;
    auto status = m_grpcStub->MoveTo(&context, request, &response);
    if (!status.ok())
    {
        throw std::runtime_error("request MoveTo failed: " + status.error_message());
    }

    return DataTypes::MotionState(response);
}

/**
 * @brief Starts a linear motion to the given position
 * @param velocityMms velocity in mm/s
 * @param acceleration acceleration in percent, currently not used
 * @param x X position in mm
 * @param y Y position in mm
 * @param z Z position in mm
 * @param a A orientation in mm, currently not used
 * @param b B orientation in mm, currently not used
 * @param c C orientation in mm, currently not used
 * @param e1 E1 target in degrees, mm or user defined units
 * @param e2 E2 target in degrees, mm or user defined units
 * @param e3 E3 target in degrees, mm or user defined units
 * @param frame user frame or empty for base frame
 */
DataTypes::MotionState AppClient::MoveToLinearRelativeBase(float velocityMms, float acceleration, double x, double y, double z, double a, double b, double c,
                                                           double e1, double e2, double e3, const std::string& frame)
{
    if (!IsConnected()) throw std::runtime_error("not connected");

    robotcontrolapp::MoveToRequest request;
    request.set_app_name(GetAppName());
    robotcontrolapp::MoveToRequest_MoveToCart* cart = request.mutable_cart_relative_base();
    cart->mutable_position()->set_x(x);
    cart->mutable_position()->set_y(y);
    cart->mutable_position()->set_z(z);
    cart->mutable_orientation()->set_x(a);
    cart->mutable_orientation()->set_y(b);
    cart->mutable_orientation()->set_z(c);
    cart->add_external_joints(e1);
    cart->add_external_joints(e2);
    cart->add_external_joints(e3);
    cart->set_velocity(velocityMms);
    cart->set_acceleration(acceleration);
    cart->set_frame(frame);

    robotcontrolapp::MotionState response;
    grpc::ClientContext context;
    auto status = m_grpcStub->MoveTo(&context, request, &response);
    if (!status.ok())
    {
        throw std::runtime_error("request MoveTo failed: " + status.error_message());
    }

    return DataTypes::MotionState(response);
}

/**
 * @brief Starts a linear motion to the given position
 * @param velocityMms velocity in mm/s
 * @param acceleration acceleration in percent, currently not used
 * @param x X position in mm
 * @param y Y position in mm
 * @param z Z position in mm
 * @param a A orientation in mm, currently not used
 * @param b B orientation in mm, currently not used
 * @param c C orientation in mm, currently not used
 * @param e1 E1 target in degrees, mm or user defined units
 * @param e2 E2 target in degrees, mm or user defined units
 * @param e3 E3 target in degrees, mm or user defined units
 */
DataTypes::MotionState AppClient::MoveToLinearRelativeTool(float velocityMms, float acceleration, double x, double y, double z, double a, double b, double c,
                                                           double e1, double e2, double e3)
{
    if (!IsConnected()) throw std::runtime_error("not connected");

    robotcontrolapp::MoveToRequest request;
    request.set_app_name(GetAppName());
    robotcontrolapp::MoveToRequest_MoveToCart* cart = request.mutable_cart_relative_tool();
    cart->mutable_position()->set_x(x);
    cart->mutable_position()->set_y(y);
    cart->mutable_position()->set_z(z);
    cart->mutable_orientation()->set_x(a);
    cart->mutable_orientation()->set_y(b);
    cart->mutable_orientation()->set_z(c);
    cart->add_external_joints(e1);
    cart->add_external_joints(e2);
    cart->add_external_joints(e3);
    cart->set_velocity(velocityMms);
    cart->set_acceleration(acceleration);

    robotcontrolapp::MotionState response;
    grpc::ClientContext context;
    auto status = m_grpcStub->MoveTo(&context, request, &response);
    if (!status.ok())
    {
        throw std::runtime_error("request MoveTo failed: " + status.error_message());
    }

    return DataTypes::MotionState(response);
}

/**
 * @brief Stops a move-to motion
 */
DataTypes::MotionState AppClient::MoveToStop()
{
    if (!IsConnected()) throw std::runtime_error("not connected");

    robotcontrolapp::MoveToRequest request;
    request.set_app_name(GetAppName());
    request.set_allocated_stop(new robotcontrolapp::MoveToRequest_MoveToStop());

    robotcontrolapp::MotionState response;
    grpc::ClientContext context;
    auto status = m_grpcStub->MoveTo(&context, request, &response);
    if (!status.ok())
    {
        throw std::runtime_error("request MoveTo failed: " + status.error_message());
    }

    return DataTypes::MotionState(response);
}

/**
 * @brief Gets the system information
 */
DataTypes::SystemInfo AppClient::GetSystemInfo()
{
    if (!IsConnected()) throw std::runtime_error("not connected");

    robotcontrolapp::SystemInfoRequest request;
    request.set_app_name(GetAppName());

    robotcontrolapp::SystemInfo response;
    grpc::ClientContext context;
    auto status = m_grpcStub->GetSystemInfo(&context, request, &response);
    if (!status.ok())
    {
        throw std::runtime_error("request GetSystemInfo failed: " + status.error_message());
    }

    return DataTypes::SystemInfo(response);
}

/**
 * @brief Gets the current velocity override
 * @return velocity multiplier in percent 0.0..1.0
 */
float AppClient::GetVelocity()
{
    if (!IsConnected()) throw std::runtime_error("not connected");

    robotcontrolapp::RobotStateRequest request;
    request.set_app_name(GetAppName());
    
    robotcontrolapp::RobotState response;
    grpc::ClientContext context;
    auto status = m_grpcStub->GetRobotState(&context, request, &response);
    if (!status.ok())
    {
        throw std::runtime_error("request GetRobotState failed: " + status.error_message());
    }

    return response.velocity_override();
}

/**
 * @brief Sets the velocity override
 * @param velocityPercent requested velocity multiplier in percent 0.0..1.0
 * @return actual velocity multiplier in percent 0.0..1.0
 */
float AppClient::SetVelocity(float velocityPercent)
{
    if (!IsConnected()) throw std::runtime_error("not connected");

    robotcontrolapp::SetVelocityOverrideRequest request;
    request.set_app_name(GetAppName());
    request.set_velocity_override(velocityPercent);
    
    robotcontrolapp::SetVelocityOverrideResponse response;
    grpc::ClientContext context;
    auto status = m_grpcStub->SetVelocityOverride(&context, request, &response);
    if (!status.ok())
    {
        throw std::runtime_error("request SetVelocityOverride failed: " + status.error_message());
    }

    return response.velocity_override();
}

/**
 * @brief Translates a cartesian position to joint positions
 * @param x X coordinate of the TCP in mm
 * @param y Y coordinate of the TCP in mm
 * @param z Z coordinate of the TCP in mm
 * @param a A orientation of the TCP in degrees
 * @param b B orientation of the TCP in degrees
 * @param c C orientation of the TCP in degrees
 * @param initialJoints 6 robot joints and 3 external joints. These are used to derive the initial joint configuration, e.g. whether the elbow points left or
 * right. Set them to 0 if not relevant.
 * @param resultJoints 6 robot joints and 3 external joints. The result is written here
 * @param resultState the result state is written here. 0 on success, other value on error
 * return true on success
 */
bool AppClient::TranslateCartToJoint(double x, double y, double z, double a, double b, double c, const std::array<double, 9>& initialJoints,
                                     std::array<double, 9>& resultJoints, robotcontrolapp::KinematicState& resultState)
{
    if (!IsConnected()) throw std::runtime_error("not connected");

    robotcontrolapp::CartToJointRequest request;
    request.set_app_name(GetAppName());
    for (size_t i = 0; i < initialJoints.size(); i++) request.add_joints(initialJoints[i]);
    request.mutable_position()->set_x(x);
    request.mutable_position()->set_y(y);
    request.mutable_position()->set_z(z);
    request.mutable_orientation()->set_x(a);
    request.mutable_orientation()->set_y(b);
    request.mutable_orientation()->set_z(c);

    robotcontrolapp::CartToJointResponse response;
    grpc::ClientContext context;
    auto status = m_grpcStub->TranslateCartToJoint(&context, request, &response);
    if (!status.ok())
    {
        throw std::runtime_error("request TranslateCartToJoint failed: " + status.error_message());
    }

    for (int i = 0; i < response.joints_size(); i++) resultJoints[i] = response.joints(i);
    resultState = response.kinematicstate();
    return resultState == robotcontrolapp::KINEMATIC_NORMAL;
}

/**
 * @brief Translates joint positions to a cartesian position
 * @param joints joint positions to translate
 * @param x result X coordinate of the TCP in mm
 * @param y result Y coordinate of the TCP in mm
 * @param z result Z coordinate of the TCP in mm
 * @param a result A orientation of the TCP in degrees
 * @param b result B orientation of the TCP in degrees
 * @param c result C orientation of the TCP in degrees
 * @param resultState the result state is written here. 0 on success, other value on error
 * @return true on success
 */
bool AppClient::TranslateJointToCart(const std::array<double, 9>& joints, double& x, double& y, double& z, double& a, double& b, double& c,
    robotcontrolapp::KinematicState& resultState)
{
    DataTypes::Matrix44 resultPosition; 
    bool result = TranslateJointToCart(joints, resultPosition, resultState);
    x = resultPosition.GetX();
    y = resultPosition.GetY();
    z = resultPosition.GetZ();
    resultPosition.GetOrientation(a, b, c);
    return result;
}

/**
 * @brief Translates joint positions to a cartesian position
 * @param joints joint positions to translate
 * @param tcp the matrix defining position and orientation of the TCP is written here
 * @param resultState the result state is written here. 0 on success, other value on error
 * @return true on success
 */
bool AppClient::TranslateJointToCart(const std::array<double, 9>& joints, DataTypes::Matrix44& tcp, robotcontrolapp::KinematicState& resultState)
{
    if (!IsConnected()) throw std::runtime_error("not connected");

    robotcontrolapp::JointToCartRequest request;
    request.set_app_name(GetAppName());
    for (size_t i = 0; i < joints.size(); i++) request.add_joints(joints[i]);

    robotcontrolapp::JointToCartResponse response;
    grpc::ClientContext context;
    auto status = m_grpcStub->TranslateJointToCart(&context, request, &response);
    if (!status.ok())
    {
        throw std::runtime_error("request TranslateJointToCart failed: " + status.error_message());
    }

    tcp = response.position();
    resultState = response.kinematicstate();
    return resultState == robotcontrolapp::KINEMATIC_NORMAL;
}

/**
 * @brief Uploads a file to the robot control
 * @param sourceFile local source file with path relative to the app's directory
 * @param targetFile target file on the robot control, relative to the Data directory
 * @param error if an error occurs the reason is written here
 * @return true on success
 */
bool AppClient::UploadFile(const std::string& sourceFile, const std::string targetFile, std::string& error)
{
    std::ifstream file(sourceFile, std::ios::binary);
    if (!file.good())
    {
        error = "could not open file for reading";
        return false;
    }

    grpc::ClientContext context;
    robotcontrolapp::UploadFileResponse response;
    auto writer = m_grpcStub->UploadFile(&context, &response);

    while (!file.good())
    {
        static const size_t CHUNK_SIZE = 8 * 1024;
        char buffer[CHUNK_SIZE] = {0};
        file.read(buffer, CHUNK_SIZE);
        size_t readCount = file.gcount();
        if (file.bad())
        {
            error = "could not read from file";
            writer->WritesDone();
            writer->Finish();
            return false;
        }
        if (readCount == 0) break;

        robotcontrolapp::UploadFileRequest request;
        request.set_app_name(GetAppName());
        request.set_filename(targetFile);
        request.set_binary_mode(true);
        std::string dataStr(buffer, buffer + readCount);
        request.set_data(dataStr);
        if (!writer->Write(request))
        {
            error = "upload failed";
            writer->WritesDone();
            writer->Finish();
            return false;
        }
    }

    writer->WritesDone();
    grpc::Status status = writer->Finish();
    if (status.ok())
    {
        error = response.error();
        return response.success();
    }
    else
    {
        error = "GRPC request failed";
        return false;
    }
}

/**
 * @brief Uploads a file to the robot control from memory
 * @param data file content
 * @param length length of the file content
 * @param targetFile target file on the robot control, relative to the Data directory
 * @param error if an error occurs the reason is written here
 * @return true on success
 */
bool AppClient::UploadFile(uint8_t* data, size_t length, const std::string targetFile, std::string& error)
{
    grpc::ClientContext context;
    robotcontrolapp::UploadFileResponse response;
    auto writer = m_grpcStub->UploadFile(&context, &response);

    static const size_t CHUNK_SIZE = 8 * 1024;
    for (size_t i = 0; i < length; i += CHUNK_SIZE)
    {
        robotcontrolapp::UploadFileRequest request;
        request.set_app_name(GetAppName());
        request.set_filename(targetFile);
        request.set_binary_mode(true);
        size_t currentChunkSize = std::min(CHUNK_SIZE, (length - i));
        std::string dataStr(data + i, data + i + currentChunkSize);
        request.set_data(dataStr);
        if (!writer->Write(request))
        {
            error = "upload failed";
            return false;
        }
    }

    writer->WritesDone();
    grpc::Status status = writer->Finish();
    if (status.ok())
    {
        error = response.error();
        return response.success();
    }
    else
    {
        error = "GRPC request failed";
        return false;
    }
}

/**
 * @brief Downloads a file from the robot control
 * @param sourceFile source file on the robot control, relative to the Data directory
 * @param targetFile local target, relative to the apps's directory
 * @param error if an error occurs the reason is written here
 * @return true on success
 */
bool AppClient::DownloadFile(const std::string& sourceFile, const std::string targetFile, std::string& error)
{
    if (!IsConnected()) throw std::runtime_error("not connected");

    grpc::ClientContext context;
    robotcontrolapp::DownloadFileRequest request;
    request.set_app_name(GetAppName());
    request.set_filename(sourceFile);

    std::ofstream file(targetFile, std::ios::trunc | std::ios::binary);
    if (!file.good())
    {
        error = "could not open file for writing";
        return false;
    }

    auto reader = m_grpcStub->DownloadFile(&context, request);
    robotcontrolapp::DownloadFileResponse response;

    while (reader->Read(&response))
    {
        if (response.success())
        {
            file.write(response.data().data(), response.data().size());
            if (file.bad())
            {
                reader->Finish();
                error = "could not write data";
                return false;
            }
        }
        else
        {
            reader->Finish();
            error = response.error();
            return false;
        }
    }
    return true;
}

/**
 * @brief Downloads a file from the robot control to memory
 * @param sourceFile source file on the robot control, relative to the Data directory
 * @param data file data is written to this vector. It will be cleared and it's size changed
 * @param error if an error occurs the reason is written here
 * @return true on success
 */
bool AppClient::DownloadFile(const std::string& sourceFile, std::vector<uint8_t>& data, std::string& error)
{
    if (!IsConnected()) throw std::runtime_error("not connected");

    grpc::ClientContext context;
    robotcontrolapp::DownloadFileRequest request;
    request.set_app_name(GetAppName());
    request.set_filename(sourceFile);

    auto reader = m_grpcStub->DownloadFile(&context, request);
    robotcontrolapp::DownloadFileResponse response;

    while (reader->Read(&response))
    {
        if (response.success())
        {
            data.insert(data.end(), response.data().begin(), response.data().end());
        }
        else
        {
            reader->Finish();
            error = response.error();
            return false;
        }
    }
    return true;
}

/**
 * @brief Gets the content of a directory
 * @param directory Directory to list, must be relative to and within the Data directory of the robot control
 * @return Description of the directory's content
 */
AppClient::DirectoryContent AppClient::ListFiles(const std::string& directory)
{
    if (!IsConnected()) throw std::runtime_error("not connected");

    robotcontrolapp::ListFilesRequest request;
    request.set_app_name(GetAppName());
    request.set_path(directory);
    robotcontrolapp::ListFilesResponse response;
    grpc::ClientContext context;
    auto status = m_grpcStub->ListFiles(&context, request, &response);
    if (!status.ok())
    {
        throw std::runtime_error("request ListFiles failed: " + status.error_message());
    }

    AppClient::DirectoryContent result;
    result.success = response.success();
    if (response.has_error()) result.errorMessage = response.error();
    result.entries.reserve(response.entries_size());
    for (const auto& entry : response.entries())
    {
        result.entries.push_back({entry.name(), entry.type()});
    }
    return result;
}

/**
 * @brief Announces to the robot control that the app function call finished. This allows the robot program to continue with the next command.
 * @param callId function call ID from the function call request
 */
void AppClient::SendFunctionDone(int64_t callId)
{
    if (!IsConnected()) throw std::runtime_error("not connected");

    robotcontrolapp::AppAction response;
    response.add_done_functions(callId);
    SendAction(response);
}

/**
 * @brief Announces to the robot control that the app function call failed. This will abort the program with an error message.
 * This is supported from V14-003
 * @param callId function call ID from the function call request
 * @param reason error message
 */
void AppClient::SendFunctionFailed(int64_t callId, const std::string& reason)
{
    if (!IsConnected()) throw std::runtime_error("not connected");

    robotcontrolapp::AppAction response;
    robotcontrolapp::FailedFunction& failedFunction = *response.add_failed_functions();
    failedFunction.set_call_id(callId);
    failedFunction.set_reason(reason);
    SendAction(response);
}

/**
 * @brief Send queued UI updates. Queueing benefits performance by sending all updates in a single message.
 */
void AppClient::SendQueuedUIUpdates() {
    std::unique_lock lock(m_queuedUIUpdatesMutex);
    if (m_queuedUIUpdates.ui_changes_size() > 0)
    {
        SendAction(m_queuedUIUpdates);
    }
    m_queuedUIUpdates.Clear();
}

/**
 * @brief Requests the state of a UI element. The robot control will respond with a call of UiUpdateHandler() if the element exists and if it was changed after
 * start up
 * @param elementName ID of the requested UI element
 */
void AppClient::RequestUIElementState(const std::string& elementName)
{
    if (!IsConnected()) throw std::runtime_error("not connected");

    robotcontrolapp::AppAction request;
    request.add_request_ui_state(elementName);
    SendAction(request);
}

/**
 * @brief Queues a request of the state of a UI element. The robot control will respond with a call of UiUpdateHandler() if the element exists and if it was
 * changed after start up
 * @param elementName ID of the requested UI element
 */
void AppClient::QueueRequestUIElementState(const std::string& elementName)
{
    std::unique_lock lock(m_queuedUIUpdatesMutex);
    m_queuedUIUpdates.add_request_ui_state(elementName);
}

/**
 * @brief Requests the state of several UI elements. The robot control will respond with a call of UiUpdateHandler() if the element exists and if it was changed
 * after start up
 * @param elementNames set of UI element names
 */
void AppClient::RequestUIElementStates(const std::unordered_set<std::string>& elementNames)
{
    if (!IsConnected()) throw std::runtime_error("not connected");

    robotcontrolapp::AppAction request;
    for (const std::string& name : elementNames) request.add_request_ui_state(name);
    SendAction(request);
}

/**
 * @brief Queues a request of the state of several UI elements. The robot control will respond with a call of UiUpdateHandler() if the element exists and if it
 * was changed after start up
 * @param elementNames set of UI element names
 */
void AppClient::QueueRequestUIElementStates(const std::unordered_set<std::string>& elementNames)
{
    std::unique_lock lock(m_queuedUIUpdatesMutex);
    for (const std::string& name : elementNames) m_queuedUIUpdates.add_request_ui_state(name);
}

/**
 * @brief Sets a UI element visible or hidden
 * @param elementName ID of the UI element
 * @param visible true to set the element visible or false to hide it
 */
void AppClient::SetUIVisibility(const std::string& elementName, bool visible)
{
    if (!IsConnected()) throw std::runtime_error("not connected");

    robotcontrolapp::AppAction request;
    robotcontrolapp::AppUIElement& uiElement = *request.add_ui_changes();
    uiElement.set_element_name(elementName);
    uiElement.set_is_visible(visible);
    SendAction(request);
}

/**
 * @brief Queues setting a UI element visible or hidden
 * @param elementName ID of the UI element
 * @param visible true to set the element visible or false to hide it
 */
void AppClient::QueueSetUIVisibility(const std::string& elementName, bool visible)
{
    std::unique_lock lock(m_queuedUIUpdatesMutex);
    robotcontrolapp::AppUIElement& uiElement = *m_queuedUIUpdates.add_ui_changes();
    lock.unlock();

    uiElement.set_element_name(elementName);
    uiElement.set_is_visible(visible);
}

/**
 * @brief Set a list of UI element visible or hidden
 * @param elements list of elements and visibility (key is the element name, value is the visibility state)
 */
void AppClient::SetUIVisibility(const std::unordered_map<std::string, bool>& elements)
{
    if (!IsConnected()) throw std::runtime_error("not connected");

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
 * @brief Queues setting a list of UI element visible or hidden
 * @param elements list of elements and visibility (key is the element name, value is the visibility state)
 */
void AppClient::QueueSetUIVisibility(const std::unordered_map<std::string, bool>& elements)
{
    std::unique_lock lock(m_queuedUIUpdatesMutex);
    for (auto& element : elements)
    {
        robotcontrolapp::AppUIElement& uiElement = *m_queuedUIUpdates.add_ui_changes();
        uiElement.set_element_name(element.first);
        uiElement.set_is_visible(element.second);
    }
}

/**
 * @brief Sets the checked state of a checkbox
 * @param elementName ID of the UI element
 * @param isChecked if true the check box will be checked
 */
void AppClient::SetCheckboxState(const std::string& elementName, bool isChecked)
{
    if (!IsConnected()) throw std::runtime_error("not connected");

    robotcontrolapp::AppAction request;
    robotcontrolapp::AppUIElement& uiElement = *request.add_ui_changes();
    uiElement.set_element_name(elementName);
    uiElement.mutable_state()->set_checkbox_state(isChecked ? robotcontrolapp::CHECKED : robotcontrolapp::UNCHECKED);
    SendAction(request);
}

/**
 * @brief Queues setting the checked state of a checkbox
 * @param elementName ID of the UI element
 * @param isChecked if true the check box will be checked
 */
void AppClient::QueueSetCheckboxState(const std::string& elementName, bool isChecked)
{
    std::unique_lock lock(m_queuedUIUpdatesMutex);
    robotcontrolapp::AppUIElement& uiElement = *m_queuedUIUpdates.add_ui_changes();
    lock.unlock();

    uiElement.set_element_name(elementName);
    uiElement.mutable_state()->set_checkbox_state(isChecked ? robotcontrolapp::CHECKED : robotcontrolapp::UNCHECKED);
}

/**
 * @brief Sets the selected value of a drop down box
 * @param elementName ID of the UI element
 * @param selectedValue selected value
 */
void AppClient::SetDropDownState(const std::string& elementName, const std::string& selectedValue)
{
    if (!IsConnected()) throw std::runtime_error("not connected");

    SetText(elementName, selectedValue);
}

/**
 * @brief Queues setting the selected value of a drop down box
 * @param elementName ID of the UI element
 * @param selectedValue selected value, must be a defined selectable entry
 */
void AppClient::QueueSetDropDownState(const std::string& elementName, const std::string& selectedValue)
{
    QueueSetText(elementName, selectedValue);
}

/**
 * @brief Sets the selected value and the list of selectable values of a drop down box
 * @param elementName ID of the UI element
 * @param selectedValue selected value
 * @param selectableEntries selectable values. If empty the current list will be kept.
 */
void AppClient::SetDropDownState(const std::string& elementName, const std::string& selectedValue, const std::list<std::string>& selectableEntries)
{
    if (!IsConnected()) throw std::runtime_error("not connected");

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
 * @brief Queues setting the selected value and the list of selectable values of a drop down box
 * @param elementName ID of the UI element
 * @param selectedValue selected value, must be a defined selectable entry
 * @param selectableEntries selectable values
 */
void AppClient::QueueSetDropDownState(const std::string& elementName, const std::string& selectedValue, const std::list<std::string>& selectableEntries)
{
    std::unique_lock lock(m_queuedUIUpdatesMutex);
    robotcontrolapp::AppUIElement& uiElement = *m_queuedUIUpdates.add_ui_changes();
    lock.unlock();

    uiElement.set_element_name(elementName);
    uiElement.mutable_state()->mutable_dropdown_state()->set_selected_option(selectedValue);
    for (const std::string& entry : selectableEntries)
    {
        *uiElement.mutable_state()->mutable_dropdown_state()->add_options() = entry;
    }
}

/**
 * @brief Sets the text of a text box, label, etc.
 * @param elementName ID of the UI element
 * @param value text
 */
void AppClient::SetText(const std::string& elementName, const std::string& value)
{
    if (!IsConnected()) throw std::runtime_error("not connected");

    robotcontrolapp::AppAction request;
    robotcontrolapp::AppUIElement& uiElement = *request.add_ui_changes();
    uiElement.set_element_name(elementName);
    uiElement.mutable_state()->mutable_textfield_state()->set_current_text(value);
    SendAction(request);
}

/**
 * @brief Queues setting the text of a text box, label, etc.
 * @param elementName ID of the UI element
 * @param value text
 */
void AppClient::QueueSetText(const std::string& elementName, const std::string& value)
{
    std::unique_lock lock(m_queuedUIUpdatesMutex);
    robotcontrolapp::AppUIElement& uiElement = *m_queuedUIUpdates.add_ui_changes();
    lock.unlock();

    uiElement.set_element_name(elementName);
    uiElement.mutable_state()->mutable_textfield_state()->set_current_text(value);
}

/**
 * @brief Sets the number value of a number box, text box, label, etc.
 * @param elementName ID of the UI element
 * @param value number
 */
void AppClient::SetNumber(const std::string& elementName, double value)
{
    if (!IsConnected()) throw std::runtime_error("not connected");

    robotcontrolapp::AppAction request;
    robotcontrolapp::AppUIElement& uiElement = *request.add_ui_changes();
    uiElement.set_element_name(elementName);
    uiElement.mutable_state()->mutable_numberfield_state()->set_current_number(value);
    SendAction(request);
}

/**
 * @brief Queues setting the number value of a number box, text box, label, etc.
 * @param elementName ID of the UI element
 * @param value number
 */
void AppClient::QueueSetNumber(const std::string& elementName, double value)
{
    std::unique_lock lock(m_queuedUIUpdatesMutex);
    robotcontrolapp::AppUIElement& uiElement = *m_queuedUIUpdates.add_ui_changes();
    lock.unlock();

    uiElement.set_element_name(elementName);
    uiElement.mutable_state()->mutable_numberfield_state()->set_current_number(value);
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
    if (!IsConnected()) throw std::runtime_error("not connected");

    robotcontrolapp::AppAction request;
    robotcontrolapp::AppUIElement& uiElement = *request.add_ui_changes();
    uiElement.set_element_name(elementName);
    uiElement.mutable_state()->mutable_image_state()->mutable_image_data()->set_height(uiHeight);
    uiElement.mutable_state()->mutable_image_state()->mutable_image_data()->set_width(uiWidth);
    uiElement.mutable_state()->mutable_image_state()->mutable_image_data()->set_encoding(encoding);
    uiElement.mutable_state()->mutable_image_state()->mutable_image_data()->set_data(imageData, imageDataLength);
    SendAction(request);
}

/**
 * @brief Queues setting the image of an image element in the UI
 * @param elementName ID of the UI element
 * @param uiWidth width of the image UI element (does not need to be equal to the image width, image will be scaled)
 * @param uiHeight height of the image UI element (does not need to be equal to the image height, image will be scaled)
 * @param imageData binary image data
 * @param imageDataLength length of the image data
 * @param encoding image format
 */
void AppClient::QueueSetImage(const std::string& elementName, unsigned uiWidth, unsigned uiHeight, uint8_t* imageData, size_t imageDataLength,
                         robotcontrolapp::ImageState::ImageData::ImageEncoding encoding)
{
    std::unique_lock lock(m_queuedUIUpdatesMutex);
    robotcontrolapp::AppUIElement& uiElement = *m_queuedUIUpdates.add_ui_changes();
    lock.unlock();

    uiElement.set_element_name(elementName);
    uiElement.mutable_state()->mutable_image_state()->mutable_image_data()->set_height(uiHeight);
    uiElement.mutable_state()->mutable_image_state()->mutable_image_data()->set_width(uiWidth);
    uiElement.mutable_state()->mutable_image_state()->mutable_image_data()->set_encoding(encoding);
    uiElement.mutable_state()->mutable_image_state()->mutable_image_data()->set_data(imageData, imageDataLength);
}

} // namespace App
