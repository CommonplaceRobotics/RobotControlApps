/**
 * @brief This file defines an abstract app client. It provides a simplified API to the GRPC interface.
 * Derive your app class from AppClient and implement the abstract methods.
 * @author MAB
 */

#pragma once

#include <grpc/grpc.h>

#include <atomic>
#include <map>
#include <memory>
#include <mutex>
#include <queue>
#include <set>
#include <string>
#include <string_view>
#include <thread>
#include <unordered_map>
#include <unordered_set>
#include <utility>

#include "DataTypes/Matrix44.h"
#include "DataTypes/MotionState.h"
#include "DataTypes/ProgramVariable.h"
#include "DataTypes/RobotState.h"
#include "DataTypes/SystemInfo.h"
#include "robotcontrolapp.grpc.pb.h"

namespace App
{

/**
 * @brief This exception is thrown when trying to call a RPC while the app is not connected
 */
class NotConnectedException : public std::runtime_error
{
public:
    NotConnectedException() : std::runtime_error("not connected") {}
};

/**
 * @brief This class is the interface between GRPC and the app logic.
 */
class AppClient
{
public:
    static constexpr std::string_view TARGET_LOCALHOST = "localhost:5000";

    // Minimum required major version of the RobotControl Core
    static constexpr int VERSION_MAJOR_MIN = 14;
    // Minimum required minor version of the RobotControl Core
    static constexpr int VERSION_MINOR_MIN = 4;
    // Minimum required patch version of the RobotControl Core
    static constexpr int VERSION_PATCH_MIN = 0;

    /**
     * @brief If set true additional output is written to stdout
     */
    bool logDebug = false;

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

    // =========================================================================
    // App function responses
    // =========================================================================
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

    // =========================================================================
    // Variables
    // =========================================================================
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

    // =========================================================================
    // Enabling / disabling motors
    // =========================================================================
    /**
     * @brief Resets hardware errors and disables the motors
     */
    void ResetErrors();
    /**
     * @brief Resets hardware errors and enables the motors
     */
    void EnableMotors();
    /**
     * @brief Disables the motors and IO
     */
    void DisableMotors();

    // =========================================================================
    // Referencing
    // =========================================================================
    /**
     * @brief Starts referencing all joints
     * @param withReferencingProgram if true: call referencing program after referencing, then reference again
     */
    void ReferenceAllJoints(bool withReferencingProgram = false);
    /**
     * @brief Runs the referencing program, then references again. Does not reference before calling the program.
     */
    void ReferencingProgram();
    /**
     * @brief Starts referencing a robot joint
     * @param n joint number 0..5
     */
    void ReferenceRobotJoint(unsigned n);
    /**
     * @brief Starts referencing an external joint
     * @param n joint number 0..3
     */
    void ReferenceExternalJoint(unsigned n);
    /**
     * @brief Starts referencing robot and external joints without delay
     * @param robotJoints set of robot joint numbers 0..6
     * @param externalJoints set of external joint numbers 0..3
     */
    void ReferenceJoints(std::set<int> robotJoints, std::set<int> externalJoints);

    // =========================================================================
    // Robot state
    // =========================================================================
    /**
     * @brief Gets the current state
     * @return robot state
     */
    DataTypes::RobotState GetRobotState();

    /**
     * @brief Starts streaming the robot state
     */
    // void StartRobotStateStream();
    /**
     * @brief Stops streaming the robot state
     */
    // void StopRobotStateStream();
    /**
     * @brief Is called when the robot state is updated (usually each 10 or 20ms). Override this method, start the stream by calling StartRobotStateStream().
     * @param state new robot state
     */
    // virtual void OnRobotStateUpdated(const DataTypes::RobotState& state){};

    /**
     * @brief Sets the state of a digital input (only in simulation)
     * @param number input number (0-63)
     * @param state target state
     */
    void SetDigitalInput(unsigned number, bool state);
    /**
     * @brief Sets the states of the digital inputs (only in simulation). This bundles all changes in one request.
     * @param inputs set of digital inputs to set
     */
    void SetDigitalInputs(const std::map<unsigned, bool>& inputs);

    /**
     * @brief Sets the state of a digital output
     * @param number output number (0-63)
     * @param state target state
     */
    void SetDigitalOutput(unsigned number, bool state);
    /**
     * @brief Sets the states of the digital outputs. This bundles all changes in one request.
     * @param outputs set of digital outputs to set
     */
    void SetDigitalOutputs(const std::map<unsigned, bool>& outputs);

    /**
     * @brief Sets the state of a global signal
     * @param number global signal number (0-99)
     * @param state target state
     */
    void SetGlobalSignal(unsigned number, bool state);
    /**
     * @brief Sets the states of the global signals. This bundles all changes in one request.
     * @param outputs set of global signals to set
     */
    void SetGlobalSignals(const std::map<unsigned, bool>& signals);

    /**
     * @brief Gets the current motion state (program execution etc)
     * @return motion state
     */
    DataTypes::MotionState GetMotionState();

    /**
     * @brief Loads a motion program synchronously
     * @param program program to load, relative to the Data/Programs directory
     * @return motion state, check request_successful and motionProgram.mainProgram for success
     */
    DataTypes::MotionState LoadMotionProgram(const std::string& program);
    /**
     * @brief Unloads the motion program
     * @return motion state
     */
    DataTypes::MotionState UnloadMotionProgram();
    /**
     * @brief Starts or continues the motion program
     * @return motion state
     */
    DataTypes::MotionState StartMotionProgram();
    /**
     * @brief Pauses the motion program at a specific command. Note: if you pass a program that is not loaded as main or sub-program it will be loaded as main
     * program.
     * @param commandIdx command index within the current (sub-)program
     * @param subProgram sub-program or empty for main program
     */
    // DataTypes::MotionState StartMotionProgramAt(unsigned commandIdx = 0, const std::string& subProgram = "");
    /**
     * @brief Pauses the motion program
     * @return motion state
     */
    DataTypes::MotionState PauseMotionProgram();
    /**
     * @brief Stops the motion program
     * @return motion state
     */
    DataTypes::MotionState StopMotionProgram();

    /**
     * @brief Sets the motion program to run once
     * @return motion state
     */
    DataTypes::MotionState SetMotionProgramSingle();
    /**
     * @brief Sets the motion program to repeat
     * @return motion state
     */
    DataTypes::MotionState SetMotionProgramRepeat();
    /**
     * @brief Sets the motion program to pause after each step
     * @return motion state
     */
    DataTypes::MotionState SetMotionProgramStep();

    /**
     * @brief Loads and starts a logic program synchronously
     * @param program program to load, relative to the Data/Programs directory
     * @return motion state, check request_successful and logicProgram.mainProgram for success
     */
    DataTypes::MotionState LoadLogicProgram(const std::string& program);
    /**
     * @brief Unloads the logic program
     * @return motion state
     */
    DataTypes::MotionState UnloadLogicProgram();

    /**
     * @brief Starts a joint motion to the given position
     * @param velocityPercent velocity in percent, 0.0..100.0
     * @param acceleration acceleration in percent, 0.0..100.0, negative values result in default value 40%
     * @param a1 A1 target in degrees or mm
     * @param a2 A2 target in degrees or mm
     * @param a3 A3 target in degrees or mm
     * @param a4 A4 target in degrees or mm
     * @param a5 A5 target in degrees or mm
     * @param a6 A6 target in degrees or mm
     * @param e1 E1 target in degrees, mm or user defined units
     * @param e2 E2 target in degrees, mm or user defined units
     * @param e3 E3 target in degrees, mm or user defined units
     * @return motion state
     */
    DataTypes::MotionState MoveToJoint(float velocityPercent, float acceleration = 40, double a1 = 0, double a2 = 0, double a3 = 0, double a4 = 0,
                                       double a5 = 0, double a6 = 0, double e1 = 0, double e2 = 0, double e3 = 0);
    /**
     * @brief Starts a relative joint motion to the given position
     * @param velocityPercent velocity in percent, 0.0..100.0
     * @param acceleration acceleration in percent, 0.0..100.0, negative values result in default value 40%
     * @param a1 A1 target in degrees or mm
     * @param a2 A2 target in degrees or mm
     * @param a3 A3 target in degrees or mm
     * @param a4 A4 target in degrees or mm
     * @param a5 A5 target in degrees or mm
     * @param a6 A6 target in degrees or mm
     * @param e1 E1 target in degrees, mm or user defined units
     * @param e2 E2 target in degrees, mm or user defined units
     * @param e3 E3 target in degrees, mm or user defined units
     * @return motion state
     */
    DataTypes::MotionState MoveToJointRelative(float velocityPercent, float acceleration = 40, double a1 = 0, double a2 = 0, double a3 = 0, double a4 = 0,
                                               double a5 = 0, double a6 = 0, double e1 = 0, double e2 = 0, double e3 = 0);
    /**
     * @brief Starts a linear motion to the given position
     * @param velocityMms velocity in mm/s
     * @param acceleration acceleration in percent, 0.0..100.0, negative values result in default value 40%
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
     * @return motion state
     */
    DataTypes::MotionState MoveToLinear(float velocityMms, float acceleration = 40, double x = 0, double y = 0, double z = 0, double a = 0, double b = 0,
                                        double c = 0, double e1 = 0, double e2 = 0, double e3 = 0, const std::string& frame = "");
    /**
     * @brief Starts a linear motion to the given position
     * @param velocityMms velocity in mm/s
     * @param acceleration acceleration in percent, 0.0..100.0, negative values result in default value 40%
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
     * @return motion state
     */
    DataTypes::MotionState MoveToLinearRelativeBase(float velocityMms, float acceleration = 40, double x = 0, double y = 0, double z = 0, double a = 0,
                                                    double b = 0, double c = 0, double e1 = 0, double e2 = 0, double e3 = 0, const std::string& frame = "");
    /**
     * @brief Starts a linear motion to the given position
     * @param velocityMms velocity in mm/s
     * @param acceleration acceleration in percent, 0.0..100.0, negative values result in default value 40%
     * @param x X position in mm
     * @param y Y position in mm
     * @param z Z position in mm
     * @param a A orientation in mm, currently not used
     * @param b B orientation in mm, currently not used
     * @param c C orientation in mm, currently not used
     * @param e1 E1 target in degrees, mm or user defined units
     * @param e2 E2 target in degrees, mm or user defined units
     * @param e3 E3 target in degrees, mm or user defined units
     * @return motion state
     */
    DataTypes::MotionState MoveToLinearRelativeTool(float velocityMms, float acceleration = 40, double x = 0, double y = 0, double z = 0, double a = 0,
                                                    double b = 0, double c = 0, double e1 = 0, double e2 = 0, double e3 = 0);
    /**
     * @brief Stops a move-to motion
     * @return motion state
     */
    DataTypes::MotionState MoveToStop();

    /**
     * @brief Returns true if the robot moves automatically. This does not indicate other motion types, like jog motion!
     * @return true if a Move To command is being executed, if a motion program is running or if the position interface is used.
     */
    bool IsAutomaticMotion();

    /**
     * @brief Waits until the Move-To command or motion program is done. See the criteria given for IsAutomaticMotion().
     * @param timeout The function returns when the motion is done or when this timeout is exceeded. Default: Effectively infinitely.
     * @param precision Sleep duration between checks. 20 ms is one cycle for most robots and two for fast ones. There is no benefit in going faster than once
     * per cycle.
     * @return true if motion is done, false on timeout
     */
    bool WaitMotionDone(std::chrono::steady_clock::duration timeout = std::chrono::hours(9999999),
                        std::chrono::steady_clock::duration precision = std::chrono::milliseconds(20));

    /**
     * @brief Gets the system information
     */
    DataTypes::SystemInfo GetSystemInfo();

    /**
     * @brief Gets the tool center point position and orientation
     * @return TCP matrix
     */
    DataTypes::Matrix44 GetTCP();

    /**
     * @brief Gets the current velocity override
     * @return velocity multiplier in percent 0.0..100.0
     */
    float GetVelocityOverride();
    /**
     * @brief Sets the velocity override
     * @param velocityPercent requested velocity multiplier in percent 0.0..100.0
     * @return actual velocity multiplier in percent 0.0..100.0
     */
    float SetVelocityOverride(float velocityPercent);

    // =========================================================================
    // Kinematics
    // =========================================================================
    /**
     * @brief Translates a cartesian position to joint positions
     * @param x X coordinate of the TCP in mm
     * @param y Y coordinate of the TCP in mm
     * @param z Z coordinate of the TCP in mm
     * @param a A orientation of the TCP in degrees
     * @param b B orientation of the TCP in degrees
     * @param c C orientation of the TCP in degrees
     * @param initialJoints 6 robot joints and 3 external joints. These are used to derive the initial joint configuration, e.g. whether the elbow points left
     * or right. Set them to 0 if not relevant.
     * @param resultJoints 6 robot joints and 3 external joints. The result is written here
     * @param resultState the result state is written here. 0 on success, other value on error
     * return true on success
     */
    bool TranslateCartToJoint(double x, double y, double z, double a, double b, double c, const std::array<double, 9>& initialJoints,
                              std::array<double, 9>& resultJoints, robotcontrolapp::KinematicState& resultState);

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
    bool TranslateJointToCart(const std::array<double, 9>& joints, double& x, double& y, double& z, double& a, double& b, double& c,
                              robotcontrolapp::KinematicState& resultState);

    /**
     * @brief Translates joint positions to a cartesian position
     * @param joints joint positions to translate
     * @param tcp the matrix defining position and orientation of the TCP is written here
     * @param resultState the result state is written here. 0 on success, other value on error
     * @return true on success
     */
    bool TranslateJointToCart(const std::array<double, 9>& joints, DataTypes::Matrix44& tcp, robotcontrolapp::KinematicState& resultState);

    // =========================================================================
    // File access
    // =========================================================================
    /**
     * @brief Uploads a file to the robot control
     * @param sourceFile local source file with path relative to the app's directory
     * @param targetFile target file on the robot control, relative to the Data directory
     * @param error if an error occurs the reason is written here
     * @return true on success
     */
    bool UploadFile(const std::string& sourceFile, const std::string targetFile, std::string& error);
    /**
     * @brief Uploads a file to the robot control from memory
     * @param data file content
     * @param length length of the file content
     * @param targetFile target file on the robot control, relative to the Data directory
     * @param error if an error occurs the reason is written here
     * @return true on success
     */
    bool UploadFile(uint8_t* data, size_t length, const std::string targetFile, std::string& error);
    /**
     * @brief Downloads a file from the robot control
     * @param sourceFile source file on the robot control, relative to the Data directory
     * @param targetFile local target, relative to the apps's directory
     * @param error if an error occurs the reason is written here
     * @return true on success
     */
    bool DownloadFile(const std::string& sourceFile, const std::string targetFile, std::string& error);
    /**
     * @brief Downloads a file from the robot control to memory
     * @param sourceFile source file on the robot control, relative to the Data directory
     * @param data file data is written to this vector. It will be cleared and it's size changed
     * @param error if an error occurs the reason is written here
     * @return true on success
     */
    bool DownloadFile(const std::string& sourceFile, std::vector<uint8_t>& data, std::string& error);

    /**
     * @brief Removes a file from the robot control
     * @param file file on the robot control, relative to the Data directory
     * @param error if an error occurs the reason is written here
     * @return true on success
     */
    bool RemoveFile(const std::string& file, std::string& error);

    /**
     * @brief Description of a directory's content
     */
    struct DirectoryContent
    {
        // false if any error occured
        bool success;
        // error message
        std::string errorMessage;

        struct DirectoryEntry
        {
            // name of the directory entry (file / sub-directory)
            std::string name;
            // type of the directory entry
            robotcontrolapp::ListFilesResponse_DirectoryEntry_Type type;
        };
        // List of directory entries
        std::vector<DirectoryEntry> entries;
    };

    /**
     * @brief Gets the content of a directory
     * @param directory Directory to list, must be relative to and within the Data directory of the robot control
     * @return Description of the directory's content
     */
    DirectoryContent ListFiles(const std::string& directory);

    // =========================================================================
    // App UI
    // =========================================================================

    /**
     * @brief Send queued UI updates. Queueing benefits performance by sending all updates in a single message.
     */
    void SendQueuedUIUpdates();

    /**
     * @brief Requests the state of a UI element. The robot control will respond with a call of UiUpdateHandler() if the element exists and if it was changed
     * after start up
     * @param elementName ID of the requested UI element
     */
    void RequestUIElementState(const std::string& elementName);
    /**
     * @brief Queues a request of the state of a UI element. The robot control will respond with a call of UiUpdateHandler() if the element exists and if it was
     * changed after start up
     * @param elementName ID of the requested UI element
     */
    void QueueRequestUIElementState(const std::string& elementName);

    /**
     * @brief Requests the state of several UI elements. The robot control will respond with a call of UiUpdateHandler() if the element exists and if it was
     * changed after start up
     * @param elementNames set of UI element names
     */
    void RequestUIElementStates(const std::unordered_set<std::string>& elementNames);
    /**
     * @brief Queues a request of the state of several UI elements. The robot control will respond with a call of UiUpdateHandler() if the element exists and if
     * it was changed after start up
     * @param elementNames set of UI element names
     */
    void QueueRequestUIElementStates(const std::unordered_set<std::string>& elementNames);

    /**
     * @brief Sets a UI element visible or hidden
     * @param elementName ID of the UI element
     * @param visible true to set the element visible or false to hide it
     */
    void SetUIVisibility(const std::string& elementName, bool visible);
    /**
     * @brief Queues setting a UI element visible or hidden
     * @param elementName ID of the UI element
     * @param visible true to set the element visible or false to hide it
     */
    void QueueSetUIVisibility(const std::string& elementName, bool visible);

    /**
     * @brief Set a list of UI element visible or hidden
     * @param elements list of elements and visibility (key is the element name, value is the visibility state)
     */
    void SetUIVisibility(const std::unordered_map<std::string, bool>& elements);
    /**
     * @brief Queues setting a list of UI element visible or hidden
     * @param elements list of elements and visibility (key is the element name, value is the visibility state)
     */
    void QueueSetUIVisibility(const std::unordered_map<std::string, bool>& elements);

    /**
     * @brief Sets the checked state of a checkbox
     * @param elementName ID of the UI element
     * @param isChecked if true the check box will be checked
     */
    void SetCheckboxState(const std::string& elementName, bool isChecked);
    /**
     * @brief Queues setting the checked state of a checkbox
     * @param elementName ID of the UI element
     * @param isChecked if true the check box will be checked
     */
    void QueueSetCheckboxState(const std::string& elementName, bool isChecked);

    /**
     * @brief Sets the selected value of a drop down box
     * @param elementName ID of the UI element
     * @param selectedValue selected value, must be a defined selectable entry
     */
    void SetDropDownState(const std::string& elementName, const std::string& selectedValue);
    /**
     * @brief Queues setting the selected value of a drop down box
     * @param elementName ID of the UI element
     * @param selectedValue selected value, must be a defined selectable entry
     */
    void QueueSetDropDownState(const std::string& elementName, const std::string& selectedValue);

    /**
     * @brief Sets the selected value and the list of selectable values of a drop down box
     * @param elementName ID of the UI element
     * @param selectedValue selected value, must be a defined selectable entry
     * @param selectableEntries selectable values
     */
    void SetDropDownState(const std::string& elementName, const std::string& selectedValue, const std::list<std::string>& selectableEntries);
    /**
     * @brief Queues setting the selected value and the list of selectable values of a drop down box
     * @param elementName ID of the UI element
     * @param selectedValue selected value, must be a defined selectable entry
     * @param selectableEntries selectable values
     */
    void QueueSetDropDownState(const std::string& elementName, const std::string& selectedValue, const std::list<std::string>& selectableEntries);

    /**
     * @brief Sets the text of a text box, label, etc.
     * @param elementName ID of the UI element
     * @param value text
     */
    void SetText(const std::string& elementName, const std::string& value);
    /**
     * @brief Queues setting the text of a text box, label, etc.
     * @param elementName ID of the UI element
     * @param value text
     */
    void QueueSetText(const std::string& elementName, const std::string& value);

    /**
     * @brief Sets the number value of a number box, text box, label, etc.
     * @param elementName ID of the UI element
     * @param value number
     */
    void SetNumber(const std::string& elementName, double value);
    /**
     * @brief Queues seting the number value of a number box, text box, label, etc.
     * @param elementName ID of the UI element
     * @param value number
     */
    void QueueSetNumber(const std::string& elementName, double value);

    /**
     * @brief Sets the image of an image element in the UI
     * @param elementName ID of the UI element
     * @param uiWidth width of the image UI element (does not need to be equal to the image width, image will be scaled) - currently not used yet
     * @param uiHeight height of the image UI element (does not need to be equal to the image height, image will be scaled) - currently not used yet
     * @param imageData binary image data
     * @param imageDataLength length of the image data. All shown images combined must be less than 290kB, otherwise the UI may fail to load after reconnect!
     * @param encoding image format
     */
    void SetImage(const std::string& elementName, unsigned uiWidth, unsigned uiHeight, const uint8_t* imageData, size_t imageDataLength,
                  robotcontrolapp::ImageState::ImageData::ImageEncoding encoding = robotcontrolapp::ImageState_ImageData_ImageEncoding_JPEG);

    /**
     * @brief Sets the image of an image element in the UI
     * @param elementName ID of the UI element
     * @param uiWidth width of the image UI element (does not need to be equal to the image width, image will be scaled)
     * @param uiHeight height of the image UI element (does not need to be equal to the image height, image will be scaled)
     * @param imageFile file name and path of the image file to load. All shown images combined must be less than 290kB, otherwise the UI may fail to load after
     * reconnect!
     */
    void SetImage(const std::string& elementName, unsigned uiWidth, unsigned uiHeight, const std::string& imageFile);

    /**
     * @brief Queues setting the image of an image element in the UI
     * @param elementName ID of the UI element
     * @param uiWidth width of the image UI element (does not need to be equal to the image width, image will be scaled) - currently not used yet
     * @param uiHeight height of the image UI element (does not need to be equal to the image height, image will be scaled) - currently not used yet
     * @param imageData binary image data
     * @param imageDataLength length of the image data
     * @param encoding image format
     */
    void QueueSetImage(const std::string& elementName, unsigned uiWidth, unsigned uiHeight, uint8_t* imageData, size_t imageDataLength,
                       robotcontrolapp::ImageState::ImageData::ImageEncoding encoding = robotcontrolapp::ImageState_ImageData_ImageEncoding_JPEG);

    /**
     * @brief Shows an info dialog window to the user.
     * Note: If iRC is not connected or older than V14-004 the dialog will never be shown. Currently there is no way for the app to find out whether this is the
     * case. than V14-004 only error messages are shown.
     * @param message The message to be displayed
     * @param title The dialog title
     */
    void ShowInfoDialog(const std::string& message, const std::string& title);

    /**
     * @brief Shows a warning dialog window to the user.
     * Note: If iRC is not connected or older than V14-004 the dialog will never be shown. Currently there is no way for the app to find out whether this is the
     * case. than V14-004 only error messages are shown.
     * @param message The message to be displayed
     * @param title The dialog title
     */
    void ShowWarningDialog(const std::string& message, const std::string& title);

    /**
     * @brief Shows an error dialog window to the user.
     * Note: If iRC is not connected the dialog will never be shown. Currently there is no way for the app to find out whether this is the case.
     * than V14-004 only error messages are shown.
     * @param message The message to be displayed
     * @param title The dialog title
     */
    void ShowErrorDialog(const std::string& message, const std::string& title);

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
    std::atomic<bool> m_stopThreads = true;
    /// Mutex for starting and stopping the threads
    std::recursive_mutex m_threadMutex;

    /// This thread reads incoming events
    std::thread m_eventReaderThread;
    /// This thread writes outgoing actions
    std::thread m_actionsWriterThread;

    /// This thread streams robot state updates
    std::thread m_robotStateThread;
    /// Set to false to stop streaming the robot state
    std::atomic<bool> m_robotStateStreamActive = false;

    /// UI updates are queued here
    robotcontrolapp::AppAction m_queuedUIUpdates;
    /// Mutex for adding UI updates to the queue
    std::mutex m_queuedUIUpdatesMutex;

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
     * @brief Thread method for the RobotState reader
     */
    // void RobotStateThread();

    /**
     * @brief GRPC stream: This is used for sending/receiving messages.
     */
    std::shared_ptr<grpc::ClientReaderWriter<robotcontrolapp::AppAction, robotcontrolapp::Event>> m_grpcStream;
    /**
     * @brief GRPC context. This context is only for the grpcStream, create temporary contexts for other requests!
     */
    grpc::ClientContext m_grpcStreamContext;

    /**
     * @brief Sets the replay mode (single / repeat / step) of the motion program
     * @param replayMode replay mode to set
     * @return motion state after executing the command
     */
    DataTypes::MotionState SetMotionProgramReplayMode(robotcontrolapp::ReplayMode replayMode);
    /**
     * @brief Sets the run state (start / stop / pause) of the motion program
     * @param replayMode replay mode to set
     * @return motion state after executing the command
     */
    DataTypes::MotionState SetMotionProgramRunState(robotcontrolapp::RunState runState);

    /**
     * @brief Shows a dialog window to the user.
     * Note: If iRC is not connected the dialog will never be shown. Currently there is no way for the app to find out whether this is the case. If iRC is older
     * than V14-004 only error messages are shown.
     * @param message The message to be displayed
     * @param title The dialog title
     * @param type the dialog type (Info, Error, Warning)
     */
    void ShowDialog(const std::string& message, const std::string& title, robotcontrolapp::ShowDialogRequest_DialogType type);

    /**
     * @brief Checks whether the connected robot supports all features of this AppClient
     * @param sysInfo system info
     * @return true if all features are supported
     */
    static bool CheckCoreVersion(const DataTypes::SystemInfo& sysInfo);

    /**
     * @brief Sends the apps capabilities / API version to the server
     */
    void SendCapabilities();
};

} // namespace App
