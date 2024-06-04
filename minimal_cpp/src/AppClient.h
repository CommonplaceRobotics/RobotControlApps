/**
 * @brief This file defines an abstract app client. It provides a simplified API to the GRPC interface.
 * Derive your app class from AppClient and implement the abstract methods.
 * @author MAB
 */

#pragma once

#include <grpc/grpc.h>

#include <map>
#include <memory>
#include <mutex>
#include <queue>
#include <string>
#include <string_view>
#include <thread>
#include <unordered_map>
#include <unordered_set>

#include "DataTypes/Matrix44.h"
#include "DataTypes/ProgramVariable.h"
#include "robotcontrolapp.grpc.pb.h"

namespace App
{

/**
 * @brief This class is the interface between GRPC and the app logic.
 */
class AppClient
{
public:
    static constexpr std::string_view TARGET_LOCALHOST = "localhost:5000";

    /**
     * @brief Constructor, sets up the connection
     * @param appName app name
     * @param target connection target in the following format: "hostname:port" or "ip:port", e.g. "localhost:5000"
     */
    AppClient(const std::string& appName, const std::string& target = std::string(TARGET_LOCALHOST));
    /**
     * @brief Copy constructor: prohibited
     * @param other app client
     */
    AppClient(const AppClient&) = delete;
    /**
     * @brief Destructor
     */
    virtual ~AppClient();
    /**
     * @brief Copy operator: prohibited
     * @param other app client
     * @return reference to this app client
     */
    AppClient& operator=(const AppClient&) = delete;

    /**
     * @brief Gets the name of the app
     * @return
     */
    const std::string& GetAppName() const { return m_appName; }

    /**
     * @brief Connects the app
     */
    void Connect();

    /**
     * @brief Disconnects the app. Make sure to disconnect in the derived destructor!
     */
    void Disconnect();

    /**
     * @brief Gets the connection state
     * @return true if connected
     */
    bool IsConnected() const { return !m_stopThreads; }

    /**
     * @brief Queues an action to be sent to the robot control
     * @param action app action
     */
    void SendAction(const robotcontrolapp::AppAction& action);

    /**
     * @brief Gets the tool center point position and orientation
     * @return TCP matrix
     */
    DataTypes::Matrix44 GetTcp();

    /**
     * @brief Gets the given program variable, throws exception on error, e.g. if the variable does not exist
     * @param variableName name of the variable
     * @return NumberVariable or PositionVariable
     */
    std::shared_ptr<DataTypes::ProgramVariable> GetProgramVariable(const std::string& variableName);

    /**
     * @brief Gets the given number variable, throws on error, e.g. if the variable does not exist or is of a different type
     * @param variableName name of the variable
     * @return number variable
     */
    std::shared_ptr<DataTypes::NumberVariable> GetNumberVariable(const std::string& variableName);

    /**
     * @brief Gets the given position variable, throws on error, e.g. if the variable does not exist or is of a different type
     * @param variableName name of the variable
     * @return position variable
     */
    std::shared_ptr<DataTypes::PositionVariable> GetPositionVariable(const std::string& variableName);

    /**
     * @brief Gets program variables
     * @param variableNames set of program variables to request
     * @return map of program variables, key is the variable name
     */
    std::map<std::string, std::shared_ptr<DataTypes::ProgramVariable>> GetProgramVariables(const std::unordered_set<std::string>& variableNames);

    /**
     * @brief Sets a number variable
     * @param name name of the variable
     * @param value value to set
     */
    void SetNumberVariable(const std::string& name, double value = 0);

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
    void SetPositionVariable(const std::string& name, double a1 = 0, double a2 = 0, double a3 = 0, double a4 = 0, double a5 = 0, double a6 = 0, double e1 = 0,
                             double e2 = 0, double e3 = 0);
    /**
     * @brief Sets a position variable with a cartesian position. The robot control will try to convert this to joint angles.
     * @param name name of the variable
     * @param cartesianPosition cartesian position and orientation
     * @param e1 position of external axis 1 in degrees, mm or user defined units
     * @param e2 position of external axis 2 in degrees, mm or user defined units
     * @param e3 position of external axis 3 in degrees, mm or user defined units
     */
    void SetPositionVariable(const std::string& name, DataTypes::Matrix44 cartesianPosition, double e1 = 0, double e2 = 0, double e3 = 0);

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
    void SetPositionVariable(const std::string& name, DataTypes::Matrix44 cartesianPosition, double a1, double a2, double a3, double a4, double a5, double a6,
                             double e1 = 0, double e2 = 0, double e3 = 0);

    /**
     * @brief Announces to the robot control that the app function call finished. This allows the robot program to continue with the next command.
     * @param callId function call ID from the function call request
     */
    void SendFunctionDone(int64_t callId);

    /**
     * @brief Announces to the robot control that the app function call failed. This will abort the program with an error message.
     * This is supported from V14-003
     * @param callId function call ID from the function call request
     * @param reason error message
     */
    void SendFunctionFailed(int64_t callId, const std::string& reason);

    /**
     * @brief Requests the state of a UI element. The robot control will respond with a call of UiUpdateHandler() if the element exists and if it was changed
     * after start up
     * @param elementName ID of the requested UI element
     */
    void RequestUIElementState(const std::string& elementName);
    /**
     * @brief Requests the state of several UI elements. The robot control will respond with a call of UiUpdateHandler() if the element exists and if it was
     * changed after start up
     * @param elementNames set of UI element names
     */
    void RequestUIElementStates(const std::unordered_set<std::string>& elementNames);

    /**
     * @brief Sets a UI element visible or hidden
     * @param elementName ID of the UI element
     * @param visible true to set the element visible or false to hide it
     */
    void SetUIVisibility(const std::string& elementName, bool visible);
    /**
     * @brief Set a list of UI element visible or hidden
     * @param elements list of elements and visibility (key is the element name, value is the visibility state)
     */
    void SetUIVisibility(const std::unordered_map<std::string, bool>& elements);

    /**
     * @brief Sets the checked state of a checkbox
     * @param elementName ID of the UI element
     * @param isChecked if true the check box will be checked
     */
    void SetCheckboxState(const std::string& elementName, bool isChecked);
    /**
     * @brief Sets the selected value of a drop down box
     * @param elementName ID of the UI element
     * @param selectedValue selected value, must be a defined selectable entry
     */
    void SetDropDownState(const std::string& elementName, const std::string& selectedValue);
    /**
     * @brief Sets the selected value and the list of selectable values of a drop down box
     * @param elementName ID of the UI element
     * @param selectedValue selected value, must be a defined selectable entry
     * @param selectableEntries selectable values
     */
    void SetDropDownState(const std::string& elementName, const std::string& selectedValue, const std::list<std::string>& selectableEntries);
    /**
     * @brief Sets the text of a text box, label, etc.
     * @param elementName ID of the UI element
     * @param value text
     */
    void SetText(const std::string& elementName, const std::string& value);
    /**
     * @brief Sets the number value of a number box, text box, label, etc.
     * @param elementName ID of the UI element
     * @param value number
     */
    void SetNumber(const std::string& elementName, double value);
    /**
     * @brief Sets the image of an image element in the UI
     * @param elementName ID of the UI element
     * @param uiWidth width of the image UI element (does not need to be equal to the image width, image will be scaled)
     * @param uiHeight height of the image UI element (does not need to be equal to the image height, image will be scaled)
     * @param imageData binary image data
     * @param imageDataLength length of the image data
     * @param encoding image format
     */
    void SetImage(const std::string& elementName, unsigned uiWidth, unsigned uiHeight, uint8_t* imageData, size_t imageDataLength,
                  robotcontrolapp::ImageState::ImageData::ImageEncoding encoding = robotcontrolapp::ImageState_ImageData_ImageEncoding_JPEG);

protected:
    /**
     * @brief Gets called on remote app function calls received from the robot control
     * @param function app function data
     */
    virtual void AppFunctionHandler(const robotcontrolapp::AppFunction& function){};
    /**
     * @brief Gets called on remote UI update requests received from the robot control
     * @param updates updated UI elements. Key is the element name, value contains the changes.
     */
    virtual void UiUpdateHandler(const std::map<std::string, const robotcontrolapp::AppUIElement*>& updates){};

    /**
     * @brief GRPC client stub: This is the generated GRPC client interface.
     * It communicates with the server and provides access to actions, streams etc.
     */
    std::unique_ptr<robotcontrolapp::RobotControlApp::Stub> m_grpcStub;

private:
    /// Name of the app
    const std::string m_appName;

    /// Actions to be sent to the robot control
    std::queue<robotcontrolapp::AppAction> m_actionsQueue;
    /// Mutex for access to the actions queue
    std::mutex m_actionsMutex;

    /// Set this to true to request the threads to Stop
    std::atomic<bool> m_stopThreads = false;
    /// Mutex for starting and stopping the threads
    std::recursive_mutex m_threadMutex;

    /// This thread reads incoming events
    std::thread m_eventReaderThread;
    /// This thread writes outgoing actions
    std::thread m_actionsWriterThread;

    /**
     * @brief Thread method for the event reader. This is used for UI events.
     * @param stream GRPC stream
     */
    void EventReaderThread();
    /**
     * @brief Thread method for the actions writer
     * @param stream GRPC stream
     */
    void ActionsWriterThread();

    /**
     * @brief GRPC stream: This is used for sending/receiving messages.
     */
    std::shared_ptr<grpc::ClientReaderWriter<robotcontrolapp::AppAction, robotcontrolapp::Event>> m_grpcStream;
    /**
     * @brief GRPC context. This context is only for the grpcStream, create temporary contexts for other requests!
     */
    grpc::ClientContext m_grpcStreamContext;
};

} // namespace App
