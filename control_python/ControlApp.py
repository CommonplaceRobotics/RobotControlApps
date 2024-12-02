import sys
from AppClient import AppClient
from DataTypes.Matrix44 import Matrix44
from robotcontrolapp_pb2 import AppFunction, AppUIElement, ButtonState, CheckboxState, ListFilesResponse, ReferencingState, RunState
from google.protobuf.internal import containers as protobufContainers


class ControlApp(AppClient):
    """This is an example app implementation"""
    
    def __init__(self, appName: str, target: str):
        """Initializes the app. Pass the app name (as defined in rcapp.xml) and socket to connect to (default: "localhost:5000")"""
        self.__motionProgramFile = ""
        self.__logicProgramFile = ""
        self.__moveToJointsA1Target = 0
        self.__moveToJointsE1Target = 0
        self.__moveToCartXTarget = 0
        self.__moveToCartE1Target = 0
        self.__moveToJointSpeed = 0
        self.__moveToCartSpeed = 0
        self.__sampleRemoteFileName = ""
        self.__sampleUploadFileName = ""
        self.__sampleDownloadFileName = ""
        AppClient.__init__(self, appName, target)

    def _AppFunctionHandler(self, function: AppFunction):
        """Gets called on remote app function calls received from the robot control"""
        return

    def _UiUpdateHandler(self, updates: protobufContainers.RepeatedCompositeFieldContainer[AppUIElement]):
        """Gets called on remote UI update requests received from the robot control"""
        for update in updates:
            if update.state.HasField("button_state"):
                # Handle buttons
                isClicked = update.state.button_state == ButtonState.CLICKED
                if isClicked:
                    # Init
                    if update.element_name == "buttonReset":
                        self.ResetErrors()
                    elif update.element_name == "buttonEnable":
                        self.EnableMotors()
                    elif update.element_name == "buttonDisable":
                        self.DisableMotors()
                    elif update.element_name == "buttonReferenceAll":
                        self.ReferenceAllJoints()
                    elif update.element_name == "buttonReferenceA1":
                        self.ReferenceJoints(0)
                    elif update.element_name == "buttonReferenceProgram":
                        self.ReferenceAllJoints(True)

                    # Velocity override
                    elif update.element_name == "buttonFaster":
                        self.ExampleFaster()
                    elif update.element_name == "buttonSlower":
                        self.ExampleSlower()

                    # Programs
                    elif update.element_name == "buttonProgramStart":
                        self.StartMotionProgram()
                    elif update.element_name == "buttonProgramStop":
                        self.StopMotionProgram()
                    elif update.element_name == "buttonProgramPause":
                        self.PauseMotionProgram()
                    elif update.element_name == "buttonProgramSingle":
                        self.SetMotionProgramSingle()
                    elif update.element_name == "buttonProgramRepeat":
                        self.SetMotionProgramRepeat()
                    elif update.element_name == "buttonProgramStep":
                        self.SetMotionProgramStep()
                    elif update.element_name == "buttonMotionProgramLoad":
                        self.LoadMotionProgram(self.__motionProgramFile)
                    elif update.element_name == "buttonMotionProgramUnload":
                        self.UnloadMotionProgram()
                    elif update.element_name == "buttonLogicProgramLoad":
                        self.LoadLogicProgram(self.__logicProgramFile)
                    elif update.element_name == "buttonLogicProgramUnload":
                        self.UnloadLogicProgram()
                    
                    # Move To
                    elif update.element_name == "buttonMoveToStop":
                        self.MoveToStop()
                    elif update.element_name == "buttonMoveToJoint":
                        self.ExampleMoveToJoint()
                    elif update.element_name == "buttonMoveToJointRelative":
                        self.ExampleMoveToJointRelative()
                    elif update.element_name == "buttonMoveToCart":
                        self.ExampleMoveToCart()
                    elif update.element_name == "buttonMoveToCartBaseRelative":
                        self.ExampleMoveToCartRelativeBase()
                    elif update.element_name == "buttonMoveToCartToolRelative":
                        self.ExampleMoveToCartRelativeTool()
                    elif update.element_name == "buttonProgramUploadSampleFile":
                        self.ExampleUploadSampleProgramFromFile()
                    elif update.element_name == "buttonProgramUploadSampleMemory":
                        self.ExampleUploadSampleProgramFromMemory()
                    elif update.element_name == "buttonProgramDownloadSampleFile":
                        self.ExampleDownloadSampleProgramToFile()
                    elif update.element_name == "buttonProgramDownloadSampleMemory":
                        self.ExampleUploadSampleProgramFromMemory()
                    elif update.element_name == "buttonProgramList":
                        self.ExampleListPrograms()

                    # Digital IO
                    elif update.element_name == "buttonDIn22True":
                        self.SetDigitalInput(21, True)
                    elif update.element_name == "buttonDIn22False":
                        self.SetDigitalInput(21, False)
                    elif update.element_name == "buttonDOut22True":
                        self.SetDigitalOutput(21, True)
                    elif update.element_name == "buttonDOut22False":
                        self.SetDigitalOutput(21, False)
                    elif update.element_name == "buttonGSig2True":
                        self.SetGlobalSignal(1, True)
                    elif update.element_name == "buttonGSig2False":
                        self.SetGlobalSignal(1, False)
                        
            elif update.HasField("textfield_state"):
                # Handle text boxes
                if update.element_name == "textboxMotionProgramFile":
                    self.__motionProgramFile = update.state.textfield_state.current_text()
                elif update.element_name == "textboxLogicProgramFile":
                    self.__logicProgramFile = update.state.textfield_state.current_text()

            elif update.HasField("numberfield_state"):
                # Handle number boxes
                if update.element_name == "numberboxMoveToJointA1":
                    self.__moveToJointsA1Target = update.state.numberfield_state.current_number()
                elif update.element_name == "numberboxMoveToJointE1":
                    self.__moveToJointsE1Target = update.state.numberfield_state.current_number()
                elif update.element_name == "numberboxMoveToJointSpeed":
                    self.__moveToJointSpeed = update.state.numberfield_state.current_number()
                    if self.__moveToJointSpeed < 0:
                        self.__moveToJointSpeed = 0
                        self.SetNumber("numberboxMoveToJointSpeed", self.__moveToJointSpeed)
                    elif self.__moveToJointSpeed > 100:
                        self.__moveToJointSpeed = 100
                        self.SetNumber("numberboxMoveToJointSpeed", self.__moveToJointSpeed)
                elif update.element_name == "numberboxMoveToLinearX":
                    self.__moveToCartXTarget = update.state.numberfield_state.current_number()
                elif update.element_name == "numberboxMoveToLinearE1":
                    self.__moveToCartE1Target = update.state.numberfield_state.current_number()
                elif update.element_name == "numberboxMoveToLinearSpeed":
                    self.__moveToCartSpeed = update.state.numberfield_state.current_number()
                    if self.__moveToCartSpeed < 0:
                        self.__moveToCartSpeed = 0
                        self.SetNumber("numberboxMoveToLinearSpeed", self.__moveToCartSpeed)

    def translateReferencingState(state: ReferencingState) -> str:
        """Translates a referencing state to a human readable string"""
        if state == ReferencingState.NOT_REFERENCED:
            return "not referenced"
        elif state == ReferencingState.IS_REFERENCED:
            return "referenced"
        elif state == ReferencingState.IS_REFERENCING:
            return "referencing..."
        else:
            return "n/a"
      
    def translateProgramState(runState: RunState) -> str:
        """Translates a program run state to a human readable string"""
        if runState == RunState.NOT_RUNNING:
            return "not running"
        elif runState == RunState.RUNNING:
            return "running"
        elif runState == RunState.PAUSED:
            return "paused"
        else:
            return "n/a"

    def UpdateUI(self):
        """Updates the status UI"""
        
        # Section Initializing
        robotState = self.GetRobotState()
        self.QueueSetText("textHardwareState", robotState.hardwareState)
        self.QueueSetText("textReferencingStateAll", self.translateReferencingState(robotState.referencingState))
        self.QueueSetText("textReferencingStateA1", self.translateReferencingState(robotState.joints[0].referencingState))
        self.QueueSetText("textVelocityOverride", robotState.velocityOverride + " %")

        # Section digital IO
        if robotState.digitalInputs[21]: # DIn22
            self.QueueSetText("textDIn22", "ON")
        else:
            self.QueueSetText("textDIn22", "OFF")
        if robotState.digitalOutputs[21]: # DOut22
            self.QueueSetText("textDOut22", "ON" )
        else:
            self.QueueSetText("textDOut22", "OFF")
        if robotState.globalSignals[1]: # GSig2
            self.QueueSetText("textGSig2", "ON")
        else:
            self.QueueSetText("textGSig2", "OFF")

        # Section Motion Program
        programState = self.GetMotionState()
        motionStr = self.translateProgramState(programState.motionProgram.runState)
        if programState.motionProgram.runState != RunState.NOT_RUNNING:
            motionStr = motionStr + ", in '" + programState.motionProgram.currentProgram + "' (" +(programState.motionProgram.currentProgramIndex +1) + "/" + programState.motionProgram.programCount
            motionStr = motionStr + "), cmd " + (programState.motionProgram.currentCommandIndex + 1) + "/" + programState.motionProgram.commandCount
        else:
            motionStr = motionStr + ", in '" + programState.motionProgram.currentProgram + " (not running)"
        
        self.QueueSetText("textMotionProgramStatus", motionStr)
        self.QueueSetText("textboxMotionProgramFile", programState.motionProgram.mainProgram)

        # Section Logic Program
        logicStr = self.translateProgramState(programState.logicProgram.runState)
        if programState.logicProgram.runState != RunState.NOT_RUNNING:
            logicStr = logicStr + ", in '" + programState.logicProgram.currentProgram + "' (" +(programState.logicProgram.currentProgramIndex +1) + "/" + programState.motionProgram.programCount
            logicStr = logicStr + "), cmd " + (programState.logicProgram.currentCommandIndex + 1) + "/" + programState.logicProgram.commandCount
        else:
            logicStr = logicStr + ", in '" + programState.logicProgram.currentProgram + " (not running)"
        
        self.QueueSetText("textLogicProgramStatus", logicStr)
        self.QueueSetText("textboxLogicProgramFile", programState.logicProgram.mainProgram)

        # Send UI updates
        self.SendQueuedUIUpdates()

    def ExampleFaster(self):
        """Increases the velocity override"""
        self.SetVelocity(min(100, self.GetVelocity() + 10))
        self.SetText("textVelocityOverride", self.GetVelocity() + " %")
    
    def ExampleSlower(self):
        """Decreases the velocity override"""
        self.SetVelocity(max(0, self.GetVelocity() - 10))
        self.SetText("textVelocityOverride", self.GetVelocity() + " %")
    
    def ExampleMoveToJoint(self):
        """Example: Move to position by joint motion"""
        robotState = self.GetRobotState()
        self.MoveToJoint(self.__moveToJointSpeed, 40, self.__moveToJointsA1Target, robotState.joints[1].targetPosition, robotState.joints[2].targetPosition, robotState.joints[3].targetPosition, robotState.joints[4].targetPosition, robotState.joints[5].targetPosition, self.__moveToJointsE1Target, robotState.joints[7].targetPosition, robotState.joints[8].targetPosition)
    
    def ExampleMoveToJointRelative(self):
        """Example: Move to relative position by joint motion"""
        self.MoveToJointRelative(self.__moveToJointSpeed, 40, self.__moveToJointsA1Target, 0, 0, 0, 0, 0, self.__moveToJointsE1Target, 0 ,0)
    
    def ExampleMoveToCart(self):
        """Example: Move to position by linear motion"""
        robotState = self.GetRobotState()
        self.MoveToJoint(self.__moveToCartSpeed, 40, self.__moveToCartXTarget, robotState.tcp.GetY(), robotState.tcp.GetZ(),robotState.tcp.GetA(), robotState.tcp.GetB(), robotState.tcp.GetC(), self.__moveToCartE1Target, robotState.joints[7].targetPosition, robotState.joints[8].targetPosition)
    
    def ExampleMoveToCartRelativeBase(self):
        """Example: Move to relative position by linear motion"""
        self.MoveToLinearRelativeBase(self.__moveToCartSpeed, 40, self.__moveToCartXTarget, 0, 0, 0, 0, 0, self.__moveToCartE1Target, 0, 0)
    
    def ExampleMoveToCartRelativeTool(self):
        """Example: Move to relative position by linear motion"""
        self.MoveToLinearRelativeTool(self.__moveToCartSpeed, 40, self.__moveToCartXTarget, 0, 0, 0, 0, 0, self.__moveToCartE1Target, 0, 0)

    def ExampleUploadSampleProgramFromFile(self):
        """Example: Upload sample program file from file"""
        (success, errorMsg) = self.UploadFileFromFile(self.__sampleUploadFileName, self.__sampleRemoteFileName)
        if success:
            print("Sample file '" + self.__sampleRemoteFileName + "' uploaded from file '" + self.__sampleUploadFileName + "'...")
        else:
            print("Could not upload sample file '" + self.__sampleRemoteFileName + "': " << errorMsg)
    
    def ExampleUploadSampleProgramFromMemory(self):
        """Example: Upload sample program file from memory"""
        print("Uploading sample file '" + self.__sampleRemoteFileName + "' from memory...")
        
        # Flash DOut21 in a 1s interval
        content = "<?xml version=\"1.0\" encoding=\"utf-8\"?>"
        "<Program>"
        "    <Output Nr=\"1\" Channel=\"DOut21\" State=\"True\" Descr=\"\" />"
        "    <Wait Nr=\"2\" Type=\"Time\" Seconds=\"1\" Descr=\"\" />"
        "    <Output Nr=\"3\" Channel=\"DOut21\" State=\"False\" Descr=\"\" />"
        "    <Wait Nr=\"4\" Type=\"Time\" Seconds=\"1\" Descr=\"\" />"
        "</Program>"

        (success, errorMsg) = self.UploadFileFromMemory(content, self.__sampleRemoteFileName)
        if success:
            print("Sample file '" + self.__sampleRemoteFileName + "' uploaded from memory")
        else:
            print("Could not upload sample file '" + self.__sampleRemoteFileName + "': " << errorMsg)
    
    def ExampleDownloadSampleProgramToFile(self):
        """Example: Download sample program file to file"""
        print("Downloading sample file '" + self.__sampleRemoteFileName + "' to file '" + self.__sampleDownloadFileName + "'..." )

        (success, errorMsg) = self.DownloadFileToFile(self.__sampleRemoteFileName, self.__sampleDownloadFileName)
        if success:
            print("Sample file '" + self.__sampleRemoteFileName + "' downloaded to file '" + self.__sampleDownloadFileName)
        else:
            print("Could not download sample file '" + self.__sampleRemoteFileName + "' to file '" + self.__sampleDownloadFileName + "': " + errorMsg)
    
    def ExampleDownloadSampleProgramToMemory(self):
        """Example: Download sample program file to memory"""
        print("Downloading sample file '" + self.__sampleRemoteFileName + "' to memory...")

        (success, errorMsg, data) = self.DownloadFileToMemory(self.__sampleRemoteFileName)
        if success:
            print("Sample file '" + self.__sampleRemoteFileName + "' downloaded to memory (" + data.count() + " bytes):")
            if(data.count > 1024):
                # Print only the first bytes of the file
                dataStr = str(data[:1024])
                print(dataStr)
            else:
                print(str(data))
        else:
            print("Could not download sample file '" + self.__sampleRemoteFileName + "' to memory: " + errorMsg)
    
    def ExampleListPrograms(self):
        """Example: List the files in the Programs directory"""
        directoryName = "Programs"
        files = self.ListFiles(directoryName)

        if(files.success):
            print("Content of directory '" + directoryName + "' (" + files.entries.count() + " entries):")

            for entry in files.entries:
                if entry.type == ListFilesResponse.DirectoryEntry.Type.File:
                    print("File: " + entry.name)
                elif entry.type == ListFilesResponse.DirectoryEntry.Type.Directory:
                    print("Directory: " + entry.name)
                elif entry.type == ListFilesResponse.DirectoryEntry.Type.Other:
                    print("Other: " + entry.name)
                else:
                    print("???: " + entry.name)
        else:
            print("Could not read directory '" + directoryName + "': " + files.errorMessage)