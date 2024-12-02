#include "ControlApp.h"

#include <math.h>

#include <sstream>

#include "DataTypes/Matrix44.h"

/**
 * @brief Constructor
 * @param target connection target in the following format: "hostname:port" or "ip:port", e.g. "localhost:5000"
 */
ControlApp::ControlApp(const std::string& target) : AppClient(std::string(APP_NAME), target) {}

/**
 * @brief Gets called on remote app function calls received from the robot control
 * @param function app function data
 */
void ControlApp::AppFunctionHandler(const robotcontrolapp::AppFunction& function) {}

/**
 * @brief Gets called on remote UI update requests received from the robot control
 * @param updates updated UI elements. Key is the element name, value contains the changes.
 */
void ControlApp::UiUpdateHandler(const std::map<std::string, const robotcontrolapp::AppUIElement*>& updates)
{
    for (auto& update : updates)
    {
        // Handle buttons
        if (update.second->state().state_case() == robotcontrolapp::AppUIElement::AppUIState::kButtonState)
        {
            bool isClicked = update.second->state().button_state() == robotcontrolapp::ButtonState::CLICKED;
            if (isClicked)
            {
                // Init
                if (update.first == "buttonReset")
                    ResetErrors();
                else if (update.first == "buttonEnable")
                    EnableMotors();
                else if (update.first == "buttonDisable")
                    DisableMotors();
                else if (update.first == "buttonReferenceAll")
                    ReferenceAllJoints();
                else if (update.first == "buttonReferenceA1")
                    ReferenceRobotJoint(0);
                else if (update.first == "buttonReferenceProgram")
                    ReferenceAllJoints(true);

                // Velocity override
                else if (update.first == "buttonFaster")
                    ExampleFaster();
                else if (update.first == "buttonSlower")
                    ExampleSlower();

                // Programs
                else if (update.first == "buttonProgramStart")
                    StartMotionProgram();
                else if (update.first == "buttonProgramStop")
                    StopMotionProgram();
                else if (update.first == "buttonProgramPause")
                    PauseMotionProgram();
                else if (update.first == "buttonProgramSingle")
                    SetMotionProgramSingle();
                else if (update.first == "buttonProgramRepeat")
                    SetMotionProgramRepeat();
                else if (update.first == "buttonProgramStep")
                    SetMotionProgramStep();
                else if (update.first == "buttonMotionProgramLoad")
                    LoadMotionProgram(m_motionProgramFile);
                else if (update.first == "buttonMotionProgramUnload")
                    UnloadMotionProgram();
                else if (update.first == "buttonLogicProgramLoad")
                    LoadLogicProgram(m_logicProgramFile);
                else if (update.first == "buttonLogicProgramUnload")
                    UnloadLogicProgram();

                // Move To
                else if (update.first == "buttonMoveToStop")
                    MoveToStop();
                else if (update.first == "buttonMoveToJoint")
                    ExampleMoveToJoint();
                else if (update.first == "buttonMoveToJointRelative")
                    ExampleMoveToJointRelative();
                else if (update.first == "buttonMoveToCart")
                    ExampleMoveToCart();
                else if (update.first == "buttonMoveToCartBaseRelative")
                    ExampleMoveToCartRelativeBase();
                else if (update.first == "buttonMoveToCartToolRelative")
                    ExampleMoveToCartRelativeTool();
                else if (update.first == "buttonProgramUploadSampleFile")
                    ExampleUploadSampleProgramFromFile();
                else if (update.first == "buttonProgramUploadSampleMemory")
                    ExampleUploadSampleProgramFromMemory();
                else if (update.first == "buttonProgramDownloadSampleFile")
                    ExampleDownloadSampleProgramToFile();
                else if (update.first == "buttonProgramDownloadSampleMemory")
                    ExampleDownloadSampleProgramToMemory();
                else if (update.first == "buttonProgramList")
                    ExampleListPrograms();

                // Digital IO
                else if (update.first == "buttonDIn22True")
                    SetDigitalInput(21, true);
                else if (update.first == "buttonDIn22False")
                    SetDigitalInput(21, false);
                else if (update.first == "buttonDOut22True")
                    SetDigitalOutput(21, true);
                else if (update.first == "buttonDOut22False")
                    SetDigitalOutput(21, false);
                else if (update.first == "buttonGSig2True")
                    SetGlobalSignal(1, true);
                else if (update.first == "buttonGSig2False")
                    SetGlobalSignal(1, false);
            }
        }
        // Handle text boxes
        else if (update.second->state().state_case() == robotcontrolapp::AppUIElement::AppUIState::kTextfieldState)
        {
            if (update.first == "textboxMotionProgramFile")
            {
                m_motionProgramFile = update.second->state().textfield_state().current_text();
            }
            else if (update.first == "textboxLogicProgramFile")
            {
                m_logicProgramFile = update.second->state().textfield_state().current_text();
            }
        }
        // Handle number boxes
        else if (update.second->state().state_case() == robotcontrolapp::AppUIElement::AppUIState::kNumberfieldState)
        {
            if (update.first == "numberboxMoveToJointA1")
            {
                m_moveToJointsA1Target = update.second->state().numberfield_state().current_number();
            }
            else if (update.first == "numberboxMoveToJointE1")
            {
                m_moveToJointsE1Target = update.second->state().numberfield_state().current_number();
            }
            else if (update.first == "numberboxMoveToJointSpeed")
            {
                m_moveToJointSpeed = update.second->state().numberfield_state().current_number();
                if (m_moveToJointSpeed < 0)
                {
                    m_moveToJointSpeed = 0;
                    SetNumber("numberboxMoveToJointSpeed", m_moveToJointSpeed);
                }
                else if (m_moveToJointSpeed > 100.0)
                {
                    m_moveToJointSpeed = 100.0;
                    SetNumber("numberboxMoveToJointSpeed", m_moveToJointSpeed);
                }
            }
            else if (update.first == "numberboxMoveToLinearX")
            {
                m_moveToCartXTarget = update.second->state().numberfield_state().current_number();
            }
            else if (update.first == "numberboxMoveToLinearE1")
            {
                m_moveToCartE1Target = update.second->state().numberfield_state().current_number();
            }
            else if (update.first == "numberboxMoveToLinearSpeed")
            {
                m_moveToCartSpeed = update.second->state().numberfield_state().current_number();
                if (m_moveToCartSpeed < 0)
                {
                    m_moveToCartSpeed = 0; 
                    SetNumber("numberboxMoveToLinearSpeed", m_moveToCartSpeed);
                }
            }
        }
    }
}

/**
 * @brief Translates a referencing state to a human readable string
 * @param state
 * @return
 */
std::string translateReferencingState(App::DataTypes::RobotState::ReferencingState state)
{
    switch (state)
    {
        default:
            return "n/a";
        case App::DataTypes::RobotState::ReferencingState::NOT_REFERENCED:
            return "not referenced";
        case App::DataTypes::RobotState::ReferencingState::IS_REFERENCED:
            return "referenced";
        case App::DataTypes::RobotState::ReferencingState::IS_REFERENCING:
            return "referencing...";
    }
}

/**
 * @brief Translates a program run state to a human readable string
 * @param runState
 * @return
 */
std::string translateProgramState(App::DataTypes::MotionState::RunState runState)
{
    switch (runState)
    {
        default:
            return "n/a";
        case App::DataTypes::MotionState::RunState::NOT_RUNNING:
            return "not running";
        case App::DataTypes::MotionState::RunState::RUNNING:
            return "running";
        case App::DataTypes::MotionState::RunState::PAUSED:
            return "paused";
    }
}

/**
 * @brief Updates the status UI
 */
void ControlApp::UpdateUI()
{
    // Section Initializing
    auto robotState = GetRobotState();
    QueueSetText("textHardwareState", robotState.hardwareState);
    QueueSetText("textReferencingStateAll", translateReferencingState(robotState.referencingState));
    QueueSetText("textReferencingStateA1", translateReferencingState(robotState.joints[0].referencingState));
    QueueSetText("textVelocityOverride", std::to_string((int)robotState.velocityOverride) + " %");

    // Section digital IO
    QueueSetText("textDIn22", robotState.digitalInputs.at(21) ? "ON" : "OFF"); // DIn22
    QueueSetText("textDOut22", robotState.digitalOutputs.at(21) ? "ON" : "OFF"); // DOut22
    QueueSetText("textGSig2", robotState.globalSignals.at(1) ? "ON" : "OFF"); // GSig2

    // Section Motion Program
    auto programState = GetMotionState();
    std::stringstream ssMotion;
    ssMotion << translateProgramState(programState.motionProgram.runState);
    if (programState.motionProgram.runState != App::DataTypes::MotionState::RunState::NOT_RUNNING)
    {
        ssMotion << ", in '" << programState.motionProgram.currentProgram << "' (" << (programState.motionProgram.currentProgramIndex + 1) << "/"
                 << programState.motionProgram.programCount << "), cmd " << (programState.motionProgram.currentCommandIndex + 1) << "/"
                 << programState.motionProgram.commandCount;
    }
    else {
        ssMotion << ", in '" << programState.motionProgram.currentProgram << "(not running)";
    }
    QueueSetText("textMotionProgramStatus", ssMotion.str());
    QueueSetText("textboxMotionProgramFile", programState.motionProgram.mainProgram);

    // Section Logic Program
    std::stringstream ssLogic;
    ssLogic << translateProgramState(programState.logicProgram.runState);
    if (programState.logicProgram.runState != App::DataTypes::MotionState::RunState::NOT_RUNNING)
    {
        ssLogic << ", in '" << programState.logicProgram.currentProgram << "' ("
                << (programState.logicProgram.currentProgramIndex + 1) << "/" << programState.logicProgram.programCount << "), cmd "
                << (programState.logicProgram.currentCommandIndex + 1) << "/" << programState.logicProgram.commandCount;
    }
    else
    {
        ssLogic << ", in '" << programState.logicProgram.currentProgram << "(not running)";
    }
    QueueSetText("textLogicProgramStatus", ssLogic.str());
    QueueSetText("textboxLogicProgramFile", programState.logicProgram.mainProgram);

    SendQueuedUIUpdates();
}

/**
 * @brief Increases the velocity override
 */
void ControlApp::ExampleFaster()
{
    SetVelocity(std::min(100.0f, GetVelocity() + 10.0f));
    SetText("textVelocityOverride", std::to_string((int)GetVelocity()) + " %");
}

/**
 * @brief Decreases the velocity override
 */
void ControlApp::ExampleSlower() {
    SetVelocity(std::max(0.0f, GetVelocity() - 10.0f));
    SetText("textVelocityOverride", std::to_string((int)GetVelocity()) + " %");
}

/**
 * @brief Example: Move to position by joint motion
 */
void ControlApp::ExampleMoveToJoint()
{
    // Only move A1 and E1 as given by the user, keep all other joints at their current position
    auto robotState = GetRobotState();
    MoveToJoint(m_moveToJointSpeed, 40, m_moveToJointsA1Target, robotState.joints[1].targetPosition, robotState.joints[2].targetPosition,
                robotState.joints[3].targetPosition, robotState.joints[4].targetPosition, robotState.joints[5].targetPosition, m_moveToJointsE1Target,
                robotState.joints[7].targetPosition, robotState.joints[8].targetPosition);
}

/**
 * @brief Example: Move to relative position by joint motion
 */
void ControlApp::ExampleMoveToJointRelative()
{
    MoveToJointRelative(m_moveToJointSpeed, 40, m_moveToJointsA1Target, 0, 0, 0, 0, 0, m_moveToJointsE1Target, 0, 0);
}

/**
 * @brief Example: Move to position by linear motion
 */
void ControlApp::ExampleMoveToCart()
{
    // Only move X and E1 as given by the user, keep all other axes at their current position
    auto robotState = GetRobotState();
    MoveToLinear(m_moveToCartSpeed, 40, m_moveToCartXTarget, robotState.tcp.GetY(), robotState.tcp.GetZ(), robotState.tcp.GetA(), robotState.tcp.GetB(),
                 robotState.tcp.GetC(), m_moveToCartE1Target, robotState.joints[7].targetPosition, robotState.joints[8].targetPosition);
}

/**
 * @brief Example: Move to relative position by linear motion
 */
void ControlApp::ExampleMoveToCartRelativeBase()
{
    MoveToLinearRelativeBase(m_moveToCartSpeed, 40, m_moveToCartXTarget, 0, 0, 0, 0, 0, m_moveToCartE1Target, 0, 0);
}

/**
 * @brief Example: Move to relative position by linear motion
 */
void ControlApp::ExampleMoveToCartRelativeTool()
{
    MoveToLinearRelativeTool(m_moveToCartSpeed, 40, m_moveToCartXTarget, 0, 0, 0, 0, 0, m_moveToCartE1Target, 0, 0);
}

/**
 * @brief Example: Upload sample program file from file
 */
void ControlApp::ExampleUploadSampleProgramFromFile() {
    std::cout << "Uploading sample file '" << m_sampleRemoteFileName << "' from file '" << m_sampleUploadFileName <<"'..." << std::endl;

    std::string errorMsg;
    if (UploadFile(m_sampleUploadFileName, m_sampleRemoteFileName, errorMsg))
    {
        std::cout << "Sample file '" << m_sampleUploadFileName << "' uploaded from file" << std::endl;
    }
    else
    {
        std::cout << "Could not upload sample file '" << m_sampleUploadFileName << "': " << errorMsg << std::endl;
    }
}

/**
 * @brief Example: Upload sample program file from memory
 */
void ControlApp::ExampleUploadSampleProgramFromMemory() {
    std::cout << "Uploading sample file '" << m_sampleRemoteFileName << "' from memory..." << std::endl;

    // Flash DOut21 in a 1s interval
    std::string content =
        "<?xml version=\"1.0\" encoding=\"utf-8\"?>"
        "<Program>"
        "    <Output Nr=\"1\" Channel=\"DOut21\" State=\"True\" Descr=\"\" />"
        "    <Wait Nr=\"2\" Type=\"Time\" Seconds=\"1\" Descr=\"\" />"
        "    <Output Nr=\"3\" Channel=\"DOut21\" State=\"False\" Descr=\"\" />"
        "    <Wait Nr=\"4\" Type=\"Time\" Seconds=\"1\" Descr=\"\" />"
        "</Program>";

    std::string errorMsg;
    if (UploadFile((uint8_t*)content.data(), content.size(), m_sampleRemoteFileName, errorMsg))
    {
        std::cout << "Sample file '" << m_sampleRemoteFileName << "' uploaded from memory" << std::endl;
    }
    else
    {
        std::cout << "Could not upload sample file '" << m_sampleRemoteFileName <<"' from memory: " << errorMsg << std::endl;
    }
}

/**
 * @brief Example: Download sample program file to file
 */
void ControlApp::ExampleDownloadSampleProgramToFile()
{
    std::cout << "Downloading sample file '" << m_sampleRemoteFileName << "' to file '" << m_sampleDownloadFileName << "'..." << std::endl;

    std::string errorMsg;
    if (DownloadFile(m_sampleRemoteFileName, m_sampleDownloadFileName, errorMsg))
    {
        std::cout << "Sample file '" << m_sampleRemoteFileName << "' downloaded to file '" << m_sampleDownloadFileName << std::endl;
    }
    else
    {
        std::cerr << "Could not download sample file '" << m_sampleRemoteFileName << "' to file '" << m_sampleDownloadFileName << "': " << errorMsg
                  << std::endl;
    }
}

/**
 * @brief Example: Download sample program file to memory
 */
void ControlApp::ExampleDownloadSampleProgramToMemory()
{
    std::cout << "Downloading sample file '" << m_sampleRemoteFileName << "' to memory..." << std::endl;

    std::vector<uint8_t> data;
    std::string errorMsg;
    if (DownloadFile(m_sampleRemoteFileName, data, errorMsg))
    {
        std::cout << "Sample file '" << m_sampleRemoteFileName << "' downloaded to memory (" << data.size() << " bytes):" << std::endl;

        // convert binary data to string
        std::string dataStr(reinterpret_cast<char*>(data.data()), data.size());
        // print only the first bytes of the file
        if (dataStr.size() > 1024)
        {
            std::cout << dataStr.substr(0, 1024) << std::endl;
            std::cout << "..." << std::endl;
        }
        else
        {
            std::cout << dataStr << std::endl;
        }
    }
    else
    {
        std::cerr << "Could not download sample file '" << m_sampleRemoteFileName << "' to memory: " << errorMsg << std::endl;
    }
}

/**
 * @brief Example: List the files in the Programs directory
 */
void ControlApp::ExampleListPrograms()
{
    std::string directoryName = "Programs";
    AppClient::DirectoryContent files = ListFiles(directoryName);

    if (files.success)
    {
        std::cout << "Content of directory '" << directoryName << "' (" << files.entries.size() << " entries):" << std::endl;
        for (const auto& entry : files.entries)
        {
            switch (entry.type)
            {
                case robotcontrolapp::ListFilesResponse_DirectoryEntry_Type_File:
                    std::cout << "File:  ";
                    break;
                case robotcontrolapp::ListFilesResponse_DirectoryEntry_Type_Directory:
                    std::cout << "Dir:   ";
                    break;
                case robotcontrolapp::ListFilesResponse_DirectoryEntry_Type_Other:
                    std::cout << "Other: ";
                    break;
                default:
                    std::cout << "???:   ";
                    break;
            }
            std::cout << entry.name << std::endl;
        }
    }
    else
    {
        std::cerr << "Could not read directory '" << directoryName << "': " << files.errorMessage << std::endl;
    }
}