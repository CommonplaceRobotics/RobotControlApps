#pragma once

#include <string>
#include <string_view>

#include "AppClient.h"

/**
 * @brief This is an example app implementation
 */
class MinimalApp : public App::AppClient
{
public:
    /// Name of the app, this must be equal to the name in rcapp.xml
    static constexpr std::string_view APP_NAME = "MinimalApp";

    /**
     * @brief Constructor
     * @param target connection target in the following format: "hostname:port" or "ip:port", e.g. "localhost:5000"
     */
    MinimalApp(const std::string& target = std::string(TARGET_LOCALHOST));

    /**
     * @brief Destructor
     */
    virtual ~MinimalApp() = default;

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

private:
    // The following values are used for the examples:
    int m_ExamplePlusMinusValue = 0;

    /**
     * @brief This example prints all app functions contained in an AppFunction request (e.g. coming from the App program command)
     * @param function function parameters
     */
    void ExamplePrintAppFunctionParameters(const robotcontrolapp::AppFunction& function) const;

    /**
     * @brief This example exponentiates the value of a number variable by a given exponent and assigns the result to a different number variable
     * @param function function parameters
     */
    void ExampleExponentiation(const robotcontrolapp::AppFunction& function);

    /**
     * @brief This example prints all UI events contained in a UI update
     * @param updates UI updates
     */
    void ExamplePrintUIEvents(const std::map<std::string, const robotcontrolapp::AppUIElement*>& updates) const;

    /**
     * @brief This example handles the plus/minus buttons to increase a text element in the app UI
     * @param updates UI updates
     */
    void ExampleUIElementClicked(const std::map<std::string, const robotcontrolapp::AppUIElement*>& updates);
};
