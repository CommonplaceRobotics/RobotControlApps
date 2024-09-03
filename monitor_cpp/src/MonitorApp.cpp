#include "MonitorApp.h"

#include <algorithm>
#include <sstream>

#include "DataTypes/Matrix44.h"

/**
 * @brief Constructor
 * @param target connection target in the following format: "hostname:port" or "ip:port", e.g. "localhost:5000"
 */
MonitorApp::MonitorApp(const std::string& target) : AppClient(std::string(APP_NAME), target) {}

/**
 * @brief Gets called on remote app function calls received from the robot control
 * @param function app function data
 */
void MonitorApp::AppFunctionHandler(const robotcontrolapp::AppFunction& function)
{}

/**
 * @brief Gets called on remote UI update requests received from the robot control
 * @param updates updated UI elements. Key is the element name, value contains the changes.
 */
void MonitorApp::UiUpdateHandler(const std::map<std::string, const robotcontrolapp::AppUIElement*>& updates)
{
    // Handle faster/slower buttons
    for (auto& update : updates)
    {
        if (update.second->state().state_case() == robotcontrolapp::AppUIElement::AppUIState::kButtonState)
        {
            bool isClicked = update.second->state().button_state() == robotcontrolapp::ButtonState::CLICKED;
            if (isClicked)
            {
                if (update.first == "buttonFaster")
                {
                    SetVelocity(std::min(100.0f, GetVelocity() + 10.0f));
                }
                else if (update.first == "buttonSlower")
                {
                    SetVelocity(std::max(0.0f, GetVelocity() - 10.0f));
                }
            }
        }
    }
}

/**
 * @brief Updates the system info UI
 */
void MonitorApp::UpdateSystemInfo() {
    App::DataTypes::SystemInfo info = GetSystemInfo();

    QueueSetText("textSoftwareVersion", info.version);
    switch (info.systemType)
    {
        default:
        case robotcontrolapp::SystemInfo_SystemType_Other:
            QueueSetText("textSystemType", "unknown");
            break;
        case robotcontrolapp::SystemInfo_SystemType_Linux_x86:
            QueueSetText("textSystemType", "Linux x86");
            break;
        case robotcontrolapp::SystemInfo_SystemType_Raspberry:
            QueueSetText("textSystemType", "Raspberry Pi");
            break;
        case robotcontrolapp::SystemInfo_SystemType_Windows:
            QueueSetText("textSystemType", "Windows");
            break;
    }
    QueueSetText("textProject", info.projectFile);
    QueueSetText("textProjectTitle", info.projectTitle);
    QueueSetText("textProjectAuthor", info.projectAuthor);
    QueueSetText("textRobot", info.robotType);
    QueueSetText("textVoltage", info.voltage == robotcontrolapp::SystemInfo_Voltage_Voltage48V ? "48V" : "24V");
    QueueSetText("textDeviceID", info.deviceID);
    QueueSetText("textRobotAxes", std::to_string(info.robotAxisCount));
    QueueSetText("textExternalAxes", std::to_string(info.externalAxisCount));
    QueueSetText("textToolAxes", std::to_string(info.toolAxisCount));
    QueueSetText("textPlatformAxes", std::to_string(info.platformAxisCount));
    QueueSetText("textDigitalIOModules", std::to_string(info.digitalIOModuleCount));
    QueueSetText("textCycleTarget", std::to_string(info.cycleTimeTarget) + " ms");
    QueueSetText("textCycleAvg", std::to_string(info.cycleTimeAverage) + " ms");
    QueueSetText("textCycleMin", std::to_string(info.cycleTimeMin) + " ms");
    QueueSetText("textCycleMax", std::to_string(info.cycleTimeMax) + " ms");
    QueueSetText("textWorkload", std::to_string(info.workload) + " %");
    SendQueuedUIUpdates();
}

/**
 * @brief Translates a referencing state to a human readable string
 * @param state 
 * @return 
 */
std::string translateReferencingState(App::DataTypes::RobotState::ReferencingState state) {
    switch (state)
    {
        default:
        case App::DataTypes::RobotState::ReferencingState::NOT_REFERENCED:
            return "not referenced";
        case App::DataTypes::RobotState::ReferencingState::IS_REFERENCED:
            return "referenced";
        case App::DataTypes::RobotState::ReferencingState::IS_REFERENCING:
            return "referencing...";
    }
}

std::string translateHardwareState(App::DataTypes::RobotState::HardwareState state) {
    std::stringstream ss;
    ss << std::hex << "0x" << ((int)state);
    return ss.str();
}

/**
 * @brief Updates the robot state UI
 * @param state new robot state
 */
void MonitorApp::UpdateRobotState(const App::DataTypes::RobotState& state)
{
    std::stringstream ssTcp;
    ssTcp << std::fixed << "X=" << state.tcp.GetX() << ", Y=" << state.tcp.GetY() << ", Z=" << state.tcp.GetZ() << ", A=" << state.tcp.GetA() << ", B=" << state.tcp.GetB()
          << ", C=" << state.tcp.GetC();
    QueueSetText("textTCPPosition",  ssTcp.str());
    
    QueueSetText("textA1Name", state.joints[0].name);
    QueueSetText("textA1PosTarget", std::to_string(state.joints[0].targetPosition));
    QueueSetText("textA1PosActual", std::to_string(state.joints[0].actualPosition));
    QueueSetText("textA1State", translateHardwareState(state.joints[0].hardwareState));
    QueueSetText("textA1Referencing", translateReferencingState(state.joints[0].referencingState));
    QueueSetText("textA1TempBoard", std::to_string(state.joints[0].temperatureBoard) + " °C");
    QueueSetText("textA1TempMotor", std::to_string(state.joints[0].temperatureMotor) + " °C");
    QueueSetText("textA1Current", std::to_string(state.joints[0].current) + " mA");
    
    QueueSetText("textE1Name", state.joints[6].name);
    QueueSetText("textE1PosTarget", std::to_string(state.joints[6].targetPosition));
    QueueSetText("textE1PosActual", std::to_string(state.joints[6].actualPosition));
    QueueSetText("textE1State", translateHardwareState(state.joints[6].hardwareState));
    QueueSetText("textE1Referencing", translateReferencingState(state.joints[6].referencingState));
    QueueSetText("textE1TempBoard", std::to_string(state.joints[6].temperatureBoard) + " °C");
    QueueSetText("textE1TempMotor", std::to_string(state.joints[6].temperatureMotor) + " °C");
    QueueSetText("textE1Current", std::to_string(state.joints[6].current) + " mA");
    QueueSetText("textE1Velocity", std::to_string(state.joints[6].targetVelocity));

    std::stringstream ssPlatform;
    ssPlatform << "X=" << state.platformX << ", Y=" << state.platformY << ", heading=" << state.platformHeading;
    QueueSetText("textPlatformPosition", ssPlatform.str());
    QueueSetText("textDIn21", state.digitalInputs[20] ? "High" : "Low");
    QueueSetText("textDOut21", state.digitalOutputs[20] ? "High" : "Low");
    QueueSetText("textGSig1", state.globalSignals[0] ? "High" : "Low");
    QueueSetText("textHWError", state.hardwareState);
    QueueSetText("textVelocityOverride", std::to_string(state.velocityOverride) + " %");
    QueueSetText("textCartVelocity", std::to_string(state.cartesianVelocity) + " mm/s");
    QueueSetText("textTempCPU", std::to_string(state.temperatureCPU) + " °C");
    QueueSetText("textSupplyVoltage", std::to_string(state.supplyVoltage) + " V");
    QueueSetText("textCurrentAll", std::to_string(state.currentAll) + " mA");
    QueueSetText("textReferencingState", translateReferencingState(state.referencingState));
    SendQueuedUIUpdates();
}

/**
 * @brief Updates the robot state UI
 */
void MonitorApp::UpdateRobotState()
{
    // You can also query the robot state like this, use this approach if you don't need frequent updates:
    App::DataTypes::RobotState state = GetRobotState();
    UpdateRobotState(state);
}

/**
 * @brief Is called when the robot state is updated (usually each 10 or 20ms). Override this method, start the stream by calling StartRobotStateStream().
 * @param state new robot state
 */
void MonitorApp::OnRobotStateUpdated(const App::DataTypes::RobotState& state) {
    // For automatic as-fast-as-possible updates override this method (OnRobotStateUpdated) and call StartRobotStateStream()
    UpdateRobotState(state);
}