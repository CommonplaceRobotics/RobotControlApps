import sys
from AppClient import AppClient
from DataTypes import RobotState
from DataTypes.Matrix44 import Matrix44
from robotcontrolapp_pb2 import AppFunction, AppUIElement, ButtonState, CheckboxState, HardwareState, ReferencingState, SystemInfo
from google.protobuf.internal import containers as protobufContainers


class MonitorApp(AppClient):
    """This is an example app implementation"""
    
    def __init__(self, appName: str, target: str):
        """Initializes the app. Pass the app name (as defined in rcapp.xml) and socket to connect to (default: "localhost:5000")"""
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
                    if update.element_name == "buttonFaster":
                        self.SetVelocity(min(100, self.GetVelocity() + 10))
                    if update.element_name == "buttonSlower":
                        self.ResetErrors(max(0, self.GetVelocity() - 10))

    def UpdateSystemInfo(self):
        """Updates the system info UI"""
        info = self.GetSystemInfo()

        self.QueueSetText("textSoftwareVersion", info.version)
        if info.systemType == SystemInfo.SystemType.Other:
            self.QueueSetText("textSystemType", "unknown")
        elif info.systemType == SystemInfo.SystemType.Linux_x86:
            self.QueueSetText("textSystemType", "Linux x86")
        elif info.systemType == SystemInfo.SystemType.Raspberry:
            self.QueueSetText("textSystemType", "Raspberry Pi")
        elif info.systemType == SystemInfo.SystemType.Windows:
            self.QueueSetText("textSystemType", "Windows")
        else:
            self.QueueSetText("textSystemType", "unknown")

        self.QueueSetText("textProject", info.projectFile)
        self.QueueSetText("textProjectTitle", info.projectFile)
        self.QueueSetText("textProjectAuthor", info.projectAuthor)
        self.QueueSetText("textRobot", info.robotType)
        self.QueueSetText("textVoltage", info.voltage)
        self.QueueSetText("textDeviceID", info.deviceID)
        self.QueueSetText("textIsSimulation", info.isSimulation)
        self.QueueSetText("textRobotAxes", info.robotAxisCount)
        self.QueueSetText("textExternalAxes", info.externalAxisCount)
        self.QueueSetText("textToolAxes", info.toolAxisCount)
        self.QueueSetText("textPlatformAxes", info.platformAxisCount)
        self.QueueSetText("textDigitalIOModules", info.digitalIOModuleCount)
        self.QueueSetText("textCycleTarget", info.cycleTimeTarget + " ms")
        self.QueueSetText("textCycleAvg", info.cycleTimeAverage + " ms")
        self.QueueSetText("textCycleMin", info.cycleTimeMin + " ms")
        self.QueueSetText("textCycleMax", info.cycleTimeMax + " ms")
        self.QueueSetText("textWorkload", info.workload + " %")
    
    def translateReferencingState(self, state: ReferencingState) -> str:
        """Translates a referencing state to a human readable string"""
        if state == ReferencingState.NOT_REFERENCED:
            return "not referenced"
        elif state == ReferencingState.IS_REFERENCED:
            return "referenced"
        elif state == ReferencingState.IS_REFERENCING:
            return "referencing..."
        else:
            return "n/a"
        
    def translateHardwareState(self, state: HardwareState) -> str:
        """Translates a hardware state to a human readable string"""
        return f"{state:#x}"
    
    def UpdateRobotState(self, state: RobotState):
        """Updates the robot state UI"""
        tcpStr = "X=" + state.tcp.GetX() + ", Y=" + state.tcp.GetY() + ", Z=" + state.tcp.GetZ()+ ", A=" + state.tcp.GetA() + ", B=" + state.tcp.GetB() + ", C=" + state.tcp.GetC()
        self.QueueSetText("textTCPPosition", tcpStr)

        self.QueueSetText("textA1Name", state.joints[0].name)
        self.QueueSetText("textA1PosTarget", state.joints[0].targetPosition)
        self.QueueSetText("textA1PosActual", state.joints[0].actualPosition)
        self.QueueSetText("textA1State", state.joints[0].hardwareState)
        self.QueueSetText("textA1Referencing", state.joints[0].referencingState)
        self.QueueSetText("textA1TempBoard", state.joints[0].temperatureBoard + " °C")
        self.QueueSetText("textA1TempMotor", state.joints[0].temperatureMotor + " °C")
        self.QueueSetText("textA1Current", state.joints[0].current + " mA")

        self.QueueSetText("textE1Name", state.joints[6].name)
        self.QueueSetText("textE1PosTarget", state.joints[6].targetPosition)
        self.QueueSetText("textE1PosActual", state.joints[6].actualPosition)
        self.QueueSetText("textE1State", state.joints[6].hardwareState)
        self.QueueSetText("textE1Referencing", state.joints[6].referencingState)
        self.QueueSetText("textE1TempBoard", state.joints[6].temperatureBoard + " °C")
        self.QueueSetText("textE1TempMotor", state.joints[6].temperatureMotor + " °C")
        self.QueueSetText("textE1Current", state.joints[6].current + " mA")
        self.QueueSetText("textE1Velocity", state.joints[6].targetVelocity)

        platformStr = "X=" + state.platformX + ", Y=" + state.platformY + ", Z=" + state.platformHeading
        self.QueueSetText("textPlatformPosition", platformStr)
        if state.digitalInputs[20]:
            self.QueueSetText("textDIn21", "High")    
        else:
            self.QueueSetText("textDIn21", "Low")    
        if state.digitalOutputs[20]:            
            self.QueueSetText("textDOut21", "High")
        else:
            self.QueueSetText("textDOut21", "Low")
        if state.globalSignals[0]:
            self.QueueSetText("textGSig1", "High")
        else:
            self.QueueSetText("textGSig1", "Low")
        self.QueueSetText("textHWError", state.hardwareState)
        self.QueueSetText("textVelocityOverride", state.velocityOverride + " %")
        self.QueueSetText("textCartVelocity", state.cartesianVelocity + " mm/s")
        self.QueueSetText("textTempCPU", state.temperatureCPU + " °C")
        self.QueueSetText("textSupplyVoltage", state.supplyVoltage + " V")
        self.QueueSetText("textCurrentAll", state.currentAll + " mA")
        self.QueueSetText("textReferencingState", state.referencingState)
        self.SendQueuedUIUpdates()
    
    def ReadAndUpdateRobotState(self):
        """Updates the robot state UI"""
        state = self.GetRobotState()
        self.UpdateRobotState(state)
    
    def OnRobotStateUpdated(self, state: RobotState):
        """Is called when the robot state is updated (usually each 10 or 20ms). Override this method, start the stream by calling StartRobotStateStream()."""
        self.UpdateRobotState(state)


