#pragma once

#include <string>
#include <string_view>

#include "AppClient.h"

/**
 * @brief This is an example app implementation
 */
class MonitorApp : public App::AppClient
{
public:
    /// Name of the app, this must be equal to the name in rcapp.xml
    static constexpr std::string_view APP_NAME = "MonitorApp";

    /**
     * @brief Constructor
     * @param target connection target in the following format: "hostname:port" or "ip:port", e.g. "localhost:5000"
     */
    MonitorApp(const std::string& target = std::string(TARGET_LOCALHOST));

    /**
     * @brief Destructor
     */
    virtual ~MonitorApp() = default;

    /**
     * @brief Gets called on remote app function calls received from the robot control
     * @param function app function data
     */
    virtual void AppFunctionHandler(const robotcontrolapp::AppFunction& function) override;
    /**
     * @brief Gets called on remote UI update requests received from the robot control
     * @param updates updated UI elements. Key is the element name, value contains the changes.
     */
    virtual void UiUpdateHandler(const std::map<std::string, const robotcontrolapp::AppUIElement*>& updates) override;

    /**
     * @brief Updates the system info UI
     */
    void UpdateSystemInfo();
    /**
     * @brief Updates the robot state UI
     * @param state new robot state
     */
    void UpdateRobotState(const App::DataTypes::RobotState& state);
    /**
     * @brief Updates the robot state UI
     * @param state new robot state
     */
    void UpdateRobotState();

    /**
     * @brief Is called when the robot state is updated (usually each 10 or 20ms). Override this method, start the stream by calling StartRobotStateStream().
     * @param state new robot state
     */
    virtual void OnRobotStateUpdated(const App::DataTypes::RobotState& state) override;
};
