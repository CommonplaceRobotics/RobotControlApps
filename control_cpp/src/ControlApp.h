#pragma once

#include <string>
#include <string_view>

#include "AppClient.h"

/**
 * @brief This is an example app implementation
 */
class ControlApp : public App::AppClient
{
public:
    /// Name of the app, this must be equal to the name in rcapp.xml
    static constexpr std::string_view APP_NAME = "ControlApp";

    /**
     * @brief Constructor
     * @param target connection target in the following format: "hostname:port" or "ip:port", e.g. "localhost:5000"
     */
    ControlApp(const std::string& target = std::string(TARGET_LOCALHOST));

    /**
     * @brief Destructor
     */
    virtual ~ControlApp() = default;

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
     * @brief Updates the status UI
     */
    void UpdateUI();

private:
    /// The motion program file name entered by the user
    std::string m_motionProgramFile;
    /// The logic program file name entered by the user
    std::string m_logicProgramFile;

    /// The A1 target for move-to entered by the user
    double m_moveToJointsA1Target = 0;
    /// The E1 target for move-to entered by the user
    double m_moveToJointsE1Target = 0;
    /// The X target for move-to entered by the user
    double m_moveToCartXTarget = 0;
    /// The E1 target for move-to entered by the user
    double m_moveToCartE1Target = 0;
    /// The joint speed (in percent) for move-to entered by the user
    double m_moveToJointSpeed = 100;
    /// The cartesian speed (in mm/s) for move-to entered by the user
    double m_moveToCartSpeed = 100;

    std::string m_sampleRemoteFileName = "Programs/SampleProgram.xml";
    std::string m_sampleUploadFileName = "SampleProgram.xml";
    std::string m_sampleDownloadFileName = "SampleProgramDownloaded.xml";

    /**
     * @brief Increases the velocity override
     */
    void ExampleFaster();
    /**
     * @brief Decreases the velocity override
     */
    void ExampleSlower();

    /**
     * @brief Example: Move to position by joint motion
     */
    void ExampleMoveToJoint();
    /**
     * @brief Example: Move to relative position by joint motion
     */
    void ExampleMoveToJointRelative();
    /**
     * @brief Example: Move to position by linear motion
     */
    void ExampleMoveToCart();
    /**
     * @brief Example: Move to relative position by linear motion
     */
    void ExampleMoveToCartRelativeBase();
    /**
     * @brief Example: Move to relative position by linear motion
     */
    void ExampleMoveToCartRelativeTool();

    /**
     * @brief Example: Upload sample program file from file
     */
    void ExampleUploadSampleProgramFromFile();
    /**
     * @brief Example: Upload sample program file from memory
     */
    void ExampleUploadSampleProgramFromMemory();
    /**
     * @brief Example: Download sample program file to file
     */
    void ExampleDownloadSampleProgramToFile();
    /**
     * @brief Example: Download sample program file to memory
     */
    void ExampleDownloadSampleProgramToMemory();

    /**
     * @brief Example: List the files in the Programs directory
     */
    void ExampleListPrograms();
};
