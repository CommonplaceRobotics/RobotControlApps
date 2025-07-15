from io import BufferedReader
from queue import Queue
import sys
from threading import Thread, Lock
import threading
from typing import List
import grpc
from google.protobuf.internal import containers as protobufContainers
from DataTypes.Matrix44 import Matrix44
from DataTypes.ProgramVariable import NumberVariable, PositionVariable, ProgramVariable
from DataTypes.SystemInfo import SystemInfo
from DataTypes.RobotState import RobotState
from DataTypes.MotionState import MotionState
import robotcontrolapp_pb2
from robotcontrolapp_pb2_grpc import RobotControlAppStub
import time


class NotConnectedException(RuntimeError):
    """not connected"""


class AppClient:
    """This class is the interface between GRPC and the app logic."""

    # Constructor, arguments are the name of the app and the target socket
    def __init__(self, appName: str, target: str):
        self.VERSION_MAJOR_MIN = 14
        """Minimum required major version of the RobotControl Core"""
        self.VERSION_MINOR_MIN = 4
        """Minimum required minor version of the RobotControl Core"""
        self.VERSION_PATCH_MIN = 0
        """Minimum required patch version of the RobotControl Core"""

        self.logDebug = False
        """If set true additional output is written to stdout"""

        self.__appName = appName
        """Name of the app"""
        self.__targetSocket = target
        self.__grpcChannel = grpc.insecure_channel(self.__targetSocket)
        self.__grpcStub = RobotControlAppStub(self.__grpcChannel)
        """GRPC client stub: This is the generated GRPC client interface."""
        self.__stopThreads = True
        """Set this to true to request the threads to Stop"""
        self.__queuedUIUpdates = robotcontrolapp_pb2.AppAction()
        """UI updates are queued here"""
        self.__queuedUIUpdatesMutex = Lock()
        """Mutex for adding UI updates to the queue"""

    def __enter__(self):
        pass  # do nothint

    def __exit__(self, type, value, traceback):
        self.Disconnect()

    def __del__(self):
        self.Disconnect()

    def GetAppName(self) -> str:
        """Gets the name of the app"""
        return self.__appName

    def Connect(self):
        """Connects the app"""
        if not self.IsConnected():
            if self.logDebug:
                print("Connecting app '" + self.__appName + "'")
            self.__stopThreads = False

            # clear queue
            self.__actionsQueue = Queue()

            try:
                # Send an empty action at startup (this is queued and sent later by the thread)
                self.SendAction(robotcontrolapp_pb2.AppAction())

                # Start threads
                self.__receivedActions = self.__grpcStub.RecieveActions(
                    iter(self.__actionsQueue.get, None)
                )
                self.__eventReaderThread = Thread(target=self.EventReaderThread)
                self.__eventReaderThread.start()

                self.SendCapabilities()
                systemInfo = self.GetSystemInfo()
                if not self.CheckCoreVersion(systemInfo):
                    print(
                        f"WARNING: The connected robot does not support all features of this app API (V{systemInfo.versionMajor}.{systemInfo.versionMinor}.{systemInfo.versionPatch} < V{self.VERSION_MAJOR_MIN}.{self.VERSION_MINOR_MIN}.{self.VERSION_PATCH_MIN}). This app may not work correctly."
                    )
            except Exception:
                self.Disconnect()
                raise
        else:
            print(
                f"Connect requested for app '{self.GetAppName()}' but it is still connected. Please call disconnect first!",
                file=sys.stderr,
            )

    def Disconnect(self):
        """Disconnects the app"""
        if self.IsConnected():
            if self.logDebug:
                print(f"Disconnecting app '{self.GetAppName()}'")

            self.__stopThreads = True
            self.__grpcChannel.close()
            if threading.current_thread != self.__eventReaderThread:
                self.__eventReaderThread.join()

            if self.logDebug:
                print(f"App '{self.GetAppName()}' disconnected")

    def IsConnected(self) -> bool:
        """Gets the connection state"""
        return not self.__stopThreads

    def SendAction(self, action: robotcontrolapp_pb2.AppAction):
        """Queues an action to be sent to the robot control"""
        action.app_name = self.GetAppName()
        self.__actionsQueue.put(action)

    def EventReaderThread(self):
        """This thread handles reading the received actions"""
        try:
            while not self.__stopThreads:
                receivedAction = self.__receivedActions.next()

                if len(receivedAction.ui_updates) > 0:
                    self._UiUpdateHandler(receivedAction.ui_updates)

                if len(receivedAction.function.name) > 0:
                    self._AppFunctionHandler(receivedAction.function)

                if receivedAction.HasField("disconnect_request"):
                    print(
                        f"Server requested disconnect, reason: {receivedAction.disconnect_request.reason}",
                        file=sys.stderr,
                    )
                    self.__stopThreads = True
                    return
        except grpc._channel._MultiThreadedRendezvous as ex:
            # Print error only if we did not disconnect first
            if not self.__stopThreads:
                print(f"App '{self.GetAppName()}' lost connection: {ex.details()}")
                self.__stopThreads = True

    def GetTCP(self) -> Matrix44:
        """Gets the tool center point position and orientation"""
        if not self.IsConnected():
            raise NotConnectedException()

        request = robotcontrolapp_pb2.GetTCPRequest()
        request.app_name = self.GetAppName()
        response = self.__grpcStub.GetTCP(request)
        return Matrix44.FromGrpc(response)

    def GetProgramVariable(self, variableName: str) -> ProgramVariable:
        """
        Gets the program variable, throws exception on error, e.g. if the variable does not exist
        Parameters:
            variableName: name of the variable
        Returns:
            NumberVariable or PositionVariable
        """
        if len(variableName) == 0:
            raise RuntimeError("requested variable with empty name")

        names = {variableName}
        result = self.GetProgramVariables(names)
        if variableName in result:
            return result[variableName]
        else:
            raise RuntimeError(
                f"failed to get variable '{variableName}': variable does not exist"
            )

    def GetNumberVariable(self, variableName: str) -> NumberVariable:
        """
        Gets the given number variable, throws on error, e.g. if the variable does not exist or is of a different type
        Parameters:
            variableName: name of the variable
        Returns:
            number variable
        """
        variable = self.GetProgramVariable(variableName)
        if not isinstance(variable, NumberVariable):
            raise RuntimeError(
                f"requested variable '{variableName}' is no number variable"
            )
        return variable

    def GetPositionVariable(self, variableName: str) -> PositionVariable:
        """
        Gets the given position variable, throws on error, e.g. if the variable does not exist or is of a different type
        Parameters:
            variableName: name of the variable
        Returns:
            position variable
        """
        variable = self.GetProgramVariable(variableName)
        if not isinstance(variable, PositionVariable):
            raise RuntimeError(
                f"requested variable '{variableName}' is no position variable"
            )
        return variable

    def GetProgramVariables(
        self, variableNames: set[str]
    ) -> dict[str, ProgramVariable]:
        """
        Gets program variables
        Parameters:
            variableNames: set of program variables to request
        Returns:
            map of program variables, key is the variable name
        """
        if not self.IsConnected():
            raise NotConnectedException()

        request = robotcontrolapp_pb2.ProgramVariablesRequest()
        request.app_name = self.GetAppName()
        for variableName in variableNames:
            if len(variableName) > 0:
                request.variable_names.append(variableName)

        resultVariables = dict()
        for grpcVariable in self.__grpcStub.GetProgramVariables(request):
            if grpcVariable.HasField("number"):
                resultVariables[grpcVariable.name] = NumberVariable(
                    grpcVariable.name, grpcVariable.number
                )
            elif grpcVariable.HasField("position"):
                if grpcVariable.position.HasField("robot_joints"):
                    resultVariables[grpcVariable.name] = PositionVariable.MakeJoint(
                        grpcVariable.name,
                        grpcVariable.position.robot_joints.joints,
                        grpcVariable.position.external_joints,
                    )
                elif grpcVariable.position.HasField("both"):
                    cartesian = Matrix44.FromGrpc(grpcVariable.position.both.cartesian)
                    resultVariables[grpcVariable.name] = PositionVariable.MakeBoth(
                        grpcVariable.name,
                        cartesian,
                        grpcVariable.position.both.robot_joints.joints,
                        grpcVariable.position.external_joints,
                    )
                elif grpcVariable.position.HasField("cartesian"):
                    cartesian = Matrix44.FromGrpc(grpcVariable.position.cartesian)
                    resultVariables[grpcVariable.name] = PositionVariable.MakeCartesian(
                        grpcVariable.name,
                        cartesian,
                        grpcVariable.position.external_joints,
                    )
        return resultVariables

    def SetNumberVariable(self, name: str, value: float):
        """
        Sets a number variable
        Parameters:
            name: name of the variable
            value: value to set
        """
        if not self.IsConnected():
            raise NotConnectedException()
        if not name:
            raise RuntimeError("empty variable name")
        if " " in name:
            raise RuntimeError("space in variable name")

        request = robotcontrolapp_pb2.SetProgramVariablesRequest()
        request.app_name = self.GetAppName()
        variable = request.variables.add()
        variable.name = name
        variable.number = value
        self.__grpcStub.SetProgramVariables(request)

    def SetPositionVariableJoints(
        self,
        name: str,
        a1: float,
        a2: float,
        a3: float,
        a4: float,
        a5: float,
        a6: float,
        e1: float,
        e2: float,
        e3: float,
    ):
        """
        Sets a position variable with joint angles. The robot control will try to convert these to cartesian.
        Parameters:
            name: name of the variable
            a1: position of robot axis 1 in degrees or mm
            a2: position of robot axis 2 in degrees or mm
            a3: position of robot axis 3 in degrees or mm
            a4: position of robot axis 4 in degrees or mm
            a5: position of robot axis 5 in degrees or mm
            a6: position of robot axis 6 in degrees or mm
            e1: position of external axis 1 in degrees, mm or user defined units
            e2: position of external axis 2 in degrees, mm or user defined units
            e3: position of external axis 3 in degrees, mm or user defined units
        """
        if not self.IsConnected():
            raise NotConnectedException()
        if not name:
            raise RuntimeError("empty variable name")
        if " " in name:
            raise RuntimeError("space in variable name")

        request = robotcontrolapp_pb2.SetProgramVariablesRequest()
        request.app_name = self.GetAppName()
        variable = request.variables.add()
        variable.name = name
        variable.position.robot_joints.joints.append(a1)
        variable.position.robot_joints.joints.append(a2)
        variable.position.robot_joints.joints.append(a3)
        variable.position.robot_joints.joints.append(a4)
        variable.position.robot_joints.joints.append(a5)
        variable.position.robot_joints.joints.append(a6)
        variable.position.external_joints.append(e1)
        variable.position.external_joints.append(e2)
        variable.position.external_joints.append(e3)
        self.__grpcStub.SetProgramVariables(request)

    def SetPositionVariableCart(
        self, name: str, cartesianPosition: Matrix44, e1: float, e2: float, e3: float
    ):
        """
        Sets a position variable with a cartesian position. The robot control will try to convert this to joint angles
        Parameters:
            name: name of the variable
            cartesianPosition: cartesian position and orientation
            e1: position of external axis 1 in degrees, mm or user defined units
            e2: position of external axis 2 in degrees, mm or user defined units
            e3: position of external axis 3 in degrees, mm or user defined units
        """
        if not self.IsConnected():
            raise NotConnectedException()
        if not name:
            raise RuntimeError("empty variable name")
        if " " in name:
            raise RuntimeError("space in variable name")

        request = robotcontrolapp_pb2.SetProgramVariablesRequest()
        request.app_name = self.GetAppName()
        variable = request.variables.add()
        variable.name = name
        variable.position.cartesian.CopyFrom(cartesianPosition.ToGrpc())
        variable.position.external_joints.append(e1)
        variable.position.external_joints.append(e2)
        variable.position.external_joints.append(e3)
        self.__grpcStub.SetProgramVariables(request)

    def SetPositionVariableBoth(
        self,
        name: str,
        cartesianPosition: Matrix44,
        a1: float,
        a2: float,
        a3: float,
        a4: float,
        a5: float,
        a6: float,
        e1: float,
        e2: float,
        e3: float,
    ):
        """
        Sets a position variable with joint angles and cartesian position. Warning: joint angles and cartesian may refer to different positions!
        Parameters:
            name: name of the variable
            cartesianPosition: cartesian position and orientation
            a1: position of robot axis 1 in degrees or mm
            a2: position of robot axis 2 in degrees or mm
            a3: position of robot axis 3 in degrees or mm
            a4: position of robot axis 4 in degrees or mm
            a5: position of robot axis 5 in degrees or mm
            a6: position of robot axis 6 in degrees or mm
            e1: position of external axis 1 in degrees, mm or user defined units
            e2: position of external axis 2 in degrees, mm or user defined units
            e3: position of external axis 3 in degrees, mm or user defined units
        """
        if not self.IsConnected():
            raise NotConnectedException()
        if not name:
            raise RuntimeError("empty variable name")
        if " " in name:
            raise RuntimeError("space in variable name")

        request = robotcontrolapp_pb2.SetProgramVariablesRequest()
        request.app_name = self.GetAppName()
        variable = request.variables.add()
        variable.name = name
        variable.position.both.cartesian.CopyFrom(cartesianPosition.ToGrpc())
        variable.position.both.robot_joints.joints.append(a1)
        variable.position.both.robot_joints.joints.append(a2)
        variable.position.both.robot_joints.joints.append(a3)
        variable.position.both.robot_joints.joints.append(a4)
        variable.position.both.robot_joints.joints.append(a5)
        variable.position.both.robot_joints.joints.append(a6)
        variable.position.external_joints.append(e1)
        variable.position.external_joints.append(e2)
        variable.position.external_joints.append(e3)
        self.__grpcStub.SetProgramVariables(request)

    def SendFunctionDone(self, callId: int):
        """
        Announces to the robot control that the app function call finished. This allows the robot program to continue with the next command.
        Parameters:
            callId: function call ID from the function call request
        """
        if not self.IsConnected():
            raise NotConnectedException()

        response = robotcontrolapp_pb2.AppAction()
        response.done_functions.append(callId)
        self.SendAction(response)

    def SendFunctionFailed(self, callId: int, reason: str):
        """
        Announces to the robot control that the app function call failed. This will abort the program with an error message.
        This is supported from V14-003
        Parameters:
            callId: function call ID from the function call request
            reason: error message
        """
        if not self.IsConnected():
            raise NotConnectedException()

        response = robotcontrolapp_pb2.AppAction()
        failedFunction = robotcontrolapp_pb2.FailedFunction()
        failedFunction.call_id = callId
        failedFunction.reason = reason
        response.failed_functions.append(failedFunction)
        self.SendAction(response)

    # =========================================================================
    # Enabling / disabling motors
    # =========================================================================
    def ResetErrors(self):
        """Resets hardware errors and disables the motors"""
        if not self.IsConnected():
            raise NotConnectedException()

        request = robotcontrolapp_pb2.ResetErrorsRequest()
        request.app_name = self.GetAppName()
        self.__grpcStub.ResetErrors(request)

    def EnableMotors(self):
        """Resets hardware errors and enables the motors"""
        if not self.IsConnected():
            raise NotConnectedException()

        request = robotcontrolapp_pb2.EnableMotorsRequest()
        request.app_name = self.GetAppName()
        request.enable = True
        self.__grpcStub.EnableMotors(request)

    def DisableMotors(self):
        """Disables the motors and IO"""
        if not self.IsConnected():
            raise NotConnectedException()

        request = robotcontrolapp_pb2.EnableMotorsRequest()
        request.app_name = self.GetAppName()
        request.enable = False
        self.__grpcStub.EnableMotors(request)

    # =========================================================================
    # Referencing
    # =========================================================================
    def ReferenceAllJoints(self, withReferencingProgram: bool):
        """
        Starts referencing all joints
        Parameters:
            withReferencingProgram: if true: call referencing program after referencing, then reference again
        """
        if not self.IsConnected():
            raise NotConnectedException()

        request = robotcontrolapp_pb2.ReferenceJointsRequest()
        request.app_name = self.GetAppName()
        request.reference_all = True
        request.referencing_program = withReferencingProgram == True
        self.__grpcStub.ReferenceJoints(request)

    def ReferencingProgram(self):
        """Runs the referencing program, then references again. Does not reference before calling the program."""
        if not self.IsConnected():
            raise NotConnectedException()

        request = robotcontrolapp_pb2.ReferenceJointsRequest()
        request.app_name = self.GetAppName()
        request.reference_all = False
        request.referencing_program = True
        self.__grpcStub.ReferenceJoints(request)

    def ReferenceRobotJoint(self, n: int):
        """
        Starts referencing a robot joint
        Parameters:
            n: joint number 0..5
        """
        if not self.IsConnected():
            raise NotConnectedException()

        request = robotcontrolapp_pb2.ReferenceJointsRequest()
        request.app_name = self.GetAppName()
        request.reference_all = False
        request.referencing_program = False
        request.reference_robot_joints.append(n)
        self.__grpcStub.ReferenceJoints(request)

    def ReferenceExternalJoint(self, n: int):
        """
        Starts referencing an external joint
        Parameters:
            n: joint number 0..3
        """
        if not self.IsConnected():
            raise NotConnectedException()

        request = robotcontrolapp_pb2.ReferenceJointsRequest()
        request.app_name = self.GetAppName()
        request.reference_all = False
        request.referencing_program = False
        request.reference_external_joints.append(n)
        self.__grpcStub.ReferenceJoints(request)

    def ReferenceJoints(self, robotJoints: set[int], externalJoints: set[int]):
        """
        Starts referencing robot and external joints without delay
        Paramters:
            robotJoints: set of robot joint numbers 0..6
            externalJoints: set of external joint numbers 0..3

        """
        if not self.IsConnected():
            raise NotConnectedException()

        request = robotcontrolapp_pb2.ReferenceJointsRequest()
        request.app_name = self.GetAppName()
        request.reference_all = False
        request.referencing_program = False
        request.reference_robot_joints.extend(robotJoints)
        request.reference_external_joints.extend(externalJoints)
        self.__grpcStub.ReferenceJoints(request)

    # =========================================================================
    # Robot state
    # =========================================================================
    def GetRobotState(self) -> RobotState:
        """
        Gets the current state
        Returns:
            robot state
        """
        if not self.IsConnected():
            raise NotConnectedException()

        request = robotcontrolapp_pb2.RobotStateRequest()
        request.app_name = self.GetAppName()
        return RobotState.FromGrpc(self.__grpcStub.GetRobotState(request))

    def SetDigitalInput(self, number: int, state: bool):
        """
        Sets the state of a digital input (only in simulation)
        Parameters:
            number: input number (0-63)
            state: target state
        """
        if not self.IsConnected():
            raise NotConnectedException()

        request = robotcontrolapp_pb2.IOStateRequest()
        din = request.DIns.add()
        din.id = number
        if state:
            din.state = robotcontrolapp_pb2.DIOState.HIGH
        else:
            din.state = robotcontrolapp_pb2.DIOState.LOW

        request.app_name = self.GetAppName()
        self.__grpcStub.SetIOState(request)

    def SetDigitalInputs(self, inputs: dict):
        """
        Sets the states of the digital inputs (only in simulation). This bundles all changes in one request.
        Parameters:
            inputs: map of digital inputs to set. First element of each tuple is the signal number (0..99), the second element is the requested state (boolean).
        """
        if not self.IsConnected():
            raise NotConnectedException()

        request = robotcontrolapp_pb2.IOStateRequest()
        for key, state in inputs.items():
            din = request.DIns.add()
            din.id = key
            if state:
                din.state = robotcontrolapp_pb2.DIOState.HIGH
            else:
                din.state = robotcontrolapp_pb2.DIOState.LOW

        request.app_name = self.GetAppName()
        self.__grpcStub.SetIOState(request)

    def SetDigitalOutput(self, number: int, state: bool):
        """
        Sets the state of a digital output (only in simulation)
        Parameters:
            number: input number (0-63)
            state: target state
        """
        if not self.IsConnected():
            raise NotConnectedException()

        request = robotcontrolapp_pb2.IOStateRequest()
        dout = request.DOuts.add()
        dout.id = number
        if state:
            dout.target_state = robotcontrolapp_pb2.DIOState.HIGH
        else:
            dout.target_state = robotcontrolapp_pb2.DIOState.LOW

        request.app_name = self.GetAppName()
        self.__grpcStub.SetIOState(request)

    def SetDigitalOutputs(self, outputs: dict):
        """
        Sets the states of the digital outputs. This bundles all changes in one request.
        Parameters:
            outputs: map of digital outputs to set. First element of each tuple is the signal number (0..99), the second element is the requested state (boolean).
        """
        if not self.IsConnected():
            raise NotConnectedException()

        request = robotcontrolapp_pb2.IOStateRequest()
        for key, state in outputs.items():
            dout = request.DOuts.add()
            dout.id = key
            if state:
                dout.target_state = robotcontrolapp_pb2.DIOState.HIGH
            else:
                dout.target_state = robotcontrolapp_pb2.DIOState.LOW

        request.app_name = self.GetAppName()
        self.__grpcStub.SetIOState(request)

    def SetGlobalSignal(self, number: int, state: bool):
        """
        Sets the state of a global signal (only in simulation)
        Parameters:
            number: input number (0-63)
            state: target state
        """
        if not self.IsConnected():
            raise NotConnectedException()

        request = robotcontrolapp_pb2.IOStateRequest()
        gsig = request.GSigs.add()
        gsig.id = number
        if state:
            gsig.target_state = robotcontrolapp_pb2.DIOState.HIGH
        else:
            gsig.target_state = robotcontrolapp_pb2.DIOState.LOW

        request.app_name = self.GetAppName()
        self.__grpcStub.SetIOState(request)

    def SetGlobalSignals(self, signals: dict):
        """
        Sets the states of the global signals. This bundles all changes in one request.
        Parameters:
            signals: Set of tuples: first element of each tuple is the signal number (0..99), the second element is the requested state (boolean)
            signals: map of global signals to set. First element of each tuple is the signal number (0..99), the second element is the requested state (boolean).
        """
        if not self.IsConnected():
            raise NotConnectedException()

        request = robotcontrolapp_pb2.IOStateRequest()
        for key, state in signals.items():
            gsig = request.GSigs.add()
            gsig.id = key
            if state:
                gsig.target_state = robotcontrolapp_pb2.DIOState.HIGH
            else:
                gsig.target_state = robotcontrolapp_pb2.DIOState.LOW

        request.app_name = self.GetAppName()
        self.__grpcStub.SetIOState(request)

    def GetMotionState(self) -> MotionState:
        """Gets the current motion state (program execution etc)"""
        if not self.IsConnected():
            raise NotConnectedException()

        request = robotcontrolapp_pb2.GetMotionStateRequest()
        request.app_name = self.GetAppName()
        return MotionState.FromGrpc(self.__grpcStub.GetMotionState(request))

    def LoadMotionProgram(self, program: str) -> MotionState:
        """
        Loads a motion program synchronously
        Parameters:
            program: program to load, relative to the Data/Programs directory
        Returns:
            motion state, check request_successful and motionProgram.mainProgram for success
        """
        if not self.IsConnected():
            raise NotConnectedException()

        request = robotcontrolapp_pb2.MotionInterpolatorRequest()
        request.app_name = self.GetAppName()
        request.main_program = program
        return MotionState.FromGrpc(self.__grpcStub.SetMotionInterpolator(request))

    def UnloadMotionProgram(self) -> MotionState:
        """
        Unloads the motion program
        Returns:
            motion state after executing the command
        """
        return self.LoadMotionProgram("")

    def SetMotionProgramRunState(
        self, replayMode: robotcontrolapp_pb2.RunState
    ) -> MotionState:
        """
        Sets the run state (start / stop / pause) of the motion program
        Parameters:
            replayMode: replay mode to set
        Returns:
            motion state after executing the command
        """
        if not self.IsConnected():
            raise NotConnectedException()

        request = robotcontrolapp_pb2.MotionInterpolatorRequest()
        request.app_name = self.GetAppName()
        request.runstate = replayMode
        return MotionState.FromGrpc(self.__grpcStub.SetMotionInterpolator(request))

    def StartMotionProgram(self) -> MotionState:
        """
        Starts or continues the motion program
        Returns:
            motion state after executing the command
        """
        return self.SetMotionProgramRunState(robotcontrolapp_pb2.RunState.RUNNING)

    # def StartMotionProgramAt(self, commandIdx: int, subProgram: str) -> MotionState:
    #     """Pauses the motion program at a specific command. Note: if you pass a program that is not loaded as main or sub-program it will be loaded as main"""
    #     if not self.IsConnected():
    #         raise NotConnectedException()

    #     request = robotcontrolapp_pb2.MotionInterpolatorRequest()
    #     request.app_name = self.GetAppName()
    #     request.runstate = robotcontrolapp_pb2.RunState.RUNNING
    #     request.start_at.program = subProgram
    #     request.start_at.command = commandIdx
    #     return MotionState.FromGrpc(self.__grpcStub.SetMotionInterpolator(request))

    def PauseMotionProgram(self) -> MotionState:
        """
        Pauses the motion program
        Returns:
            motion state after executing the command
        """
        return self.SetMotionProgramRunState(robotcontrolapp_pb2.RunState.PAUSED)

    def StopMotionProgram(self) -> MotionState:
        """
        Stops the motion program
        Returns:
            motion state after executing the command
        """
        return self.SetMotionProgramRunState(robotcontrolapp_pb2.RunState.NOT_RUNNING)

    def SetMotionProgramReplayMode(
        self, replayMode: robotcontrolapp_pb2.ReplayMode
    ) -> MotionState:
        """
        Sets the replay mode (single / repeat / step) of the motion program
        Parameters:
            replayMode: replay mode to set
        Returns:
            motion state after executing the command
        """
        if not self.IsConnected():
            raise NotConnectedException()

        request = robotcontrolapp_pb2.MotionInterpolatorRequest()
        request.app_name = self.GetAppName()
        request.replay_mode = replayMode
        return MotionState.FromGrpc(self.__grpcStub.SetMotionInterpolator(request))

    def SetMotionProgramSingle(self) -> MotionState:
        """
        Sets the motion program to run once
        Returns:
            motion state after executing the command
        """
        return self.SetMotionProgramReplayMode(robotcontrolapp_pb2.ReplayMode.SINGLE)

    def SetMotionProgramRepeat(self) -> MotionState:
        """
        Sets the motion program to repeat
        Returns:
            motion state after executing the command
        """
        return self.SetMotionProgramReplayMode(robotcontrolapp_pb2.ReplayMode.REPEAT)

    def SetMotionProgramStep(self) -> MotionState:
        """
        Sets the motion program to pause after each step
        Returns:
            motion state after executing the command
        """
        return self.SetMotionProgramReplayMode(robotcontrolapp_pb2.ReplayMode.STEP)

    def LoadLogicProgram(self, program: str) -> MotionState:
        """
        Loads and starts a logic program synchronously
        Parameters:
            program: program to load, relative to the Data/Programs directory
        Returns:
            motion state, check request_successful and logicProgram.mainProgram for success
        """
        if not self.IsConnected():
            raise NotConnectedException()

        request = robotcontrolapp_pb2.LogicInterpolatorRequest()
        request.app_name = self.GetAppName()
        request.main_program = program
        return MotionState.FromGrpc(self.__grpcStub.SetLogicInterpolator(request))

    def UnloadLogicProgram(self) -> MotionState:
        """
        Unloads the logic program
        Returns:
            motion state after executing the command
        """
        return self.LoadLogicProgram("")

    def MoveToJoint(
        self,
        velocityPercent: float,
        acceleration: float,
        a1: float,
        a2: float,
        a3: float,
        a4: float,
        a5: float,
        a6: float,
        e1: float,
        e2: float,
        e3: float,
    ) -> MotionState:
        """
        Starts a joint motion to the given position
        Parameters:
            velocityPercent: velocity in percent, 0.0..100.0
            acceleration: acceleration in percent, 0.0..100.0, negative values result in default value 40%
            a1: A1 target in degrees or mm
            a2: A2 target in degrees or mm
            a3: A3 target in degrees or mm
            a4: A4 target in degrees or mm
            a5: A5 target in degrees or mm
            a6: A6 target in degrees or mm
            e1: E1 target in degrees, mm or user defined units
            e2: E2 target in degrees, mm or user defined units
            e3: E3 target in degrees, mm or user defined units
        Returns:
            motion state after executing the command
        """
        if not self.IsConnected():
            raise NotConnectedException()

        request = robotcontrolapp_pb2.MoveToRequest()
        request.app_name = self.GetAppName()
        request.joint.velocity = velocityPercent
        request.joint.acceleration = acceleration
        request.joint.robot_joints.append(a1)
        request.joint.robot_joints.append(a2)
        request.joint.robot_joints.append(a3)
        request.joint.robot_joints.append(a4)
        request.joint.robot_joints.append(a5)
        request.joint.robot_joints.append(a6)
        request.joint.external_joints.append(e1)
        request.joint.external_joints.append(e2)
        request.joint.external_joints.append(e3)
        return MotionState.FromGrpc(self.__grpcStub.MoveTo(request))

    def MoveToJointRelative(
        self,
        velocityPercent: float,
        acceleration: float,
        a1: float,
        a2: float,
        a3: float,
        a4: float,
        a5: float,
        a6: float,
        e1: float,
        e2: float,
        e3: float,
    ) -> MotionState:
        """
        Starts a relative joint motion to the given position
        Parameters:
            velocityPercent: velocity in percent, 0.0..100.0
            acceleration: acceleration in percent, 0.0..100.0, negative values result in default value 40%
            a1: A1 target in degrees or mm
            a2: A2 target in degrees or mm
            a3: A3 target in degrees or mm
            a4: A4 target in degrees or mm
            a5: A5 target in degrees or mm
            a6: A6 target in degrees or mm
            e1: E1 target in degrees, mm or user defined units
            e2: E2 target in degrees, mm or user defined units
            e3: E3 target in degrees, mm or user defined units
        Returns:
            motion state after executing the command
        """
        if not self.IsConnected():
            raise NotConnectedException()

        request = robotcontrolapp_pb2.MoveToRequest()
        request.app_name = self.GetAppName()
        request.joint_relative.velocity = velocityPercent
        request.joint_relative.acceleration = acceleration
        request.joint_relative.robot_joints.append(a1)
        request.joint_relative.robot_joints.append(a2)
        request.joint_relative.robot_joints.append(a3)
        request.joint_relative.robot_joints.append(a4)
        request.joint_relative.robot_joints.append(a5)
        request.joint_relative.robot_joints.append(a6)
        request.joint_relative.external_joints.append(e1)
        request.joint_relative.external_joints.append(e2)
        request.joint_relative.external_joints.append(e3)
        return MotionState.FromGrpc(self.__grpcStub.MoveTo(request))

    def MoveToLinear(
        self,
        velocityMms: float,
        acceleration: float,
        x: float,
        y: float,
        z: float,
        a: float,
        b: float,
        c: float,
        e1: float,
        e2: float,
        e3: float,
        frame: str,
    ) -> MotionState:
        """
        Starts a linear motion to the given position
        Parameters:
            velocityMms: velocity in mm/s
            acceleration: acceleration in percent, 0.0..100.0, negative values result in default value 40%
            x: X position in mm
            y: Y position in mm
            z: Z position in mm
            a: A orientation in mm
            b: B orientation in mm
            c: C orientation in mm
            e1: E1 target in degrees, mm or user defined units
            e2: E2 target in degrees, mm or user defined units
            e3: E3 target in degrees, mm or user defined units
            frame: user frame or empty for base frame
        Returns:
            motion state after executing the command
        """
        if not self.IsConnected():
            raise NotConnectedException()

        request = robotcontrolapp_pb2.MoveToRequest()
        request.app_name = self.GetAppName()
        request.cart.velocity = velocityMms
        request.cart.acceleration = acceleration
        request.cart.position.x = x
        request.cart.position.y = y
        request.cart.position.z = z
        request.cart.orientation.x = a
        request.cart.orientation.y = b
        request.cart.orientation.z = c
        request.cart.external_joints.append(e1)
        request.cart.external_joints.append(e2)
        request.cart.external_joints.append(e3)
        request.cart.frame = frame
        return MotionState.FromGrpc(self.__grpcStub.MoveTo(request))

    def MoveToLinearRelativeBase(
        self,
        velocityMms: float,
        acceleration: float,
        x: float,
        y: float,
        z: float,
        a: float,
        b: float,
        c: float,
        e1: float,
        e2: float,
        e3: float,
        frame: str,
    ) -> MotionState:
        """
        Starts a linear motion to the given position
        Parameters:
            velocityMms: velocity in mm/s
            acceleration: acceleration in percent, 0.0..100.0, negative values result in default value 40%
            x: X position in mm
            y: Y position in mm
            z: Z position in mm
            a: A orientation in mm, currently not used
            b: B orientation in mm, currently not used
            c: C orientation in mm, currently not used
            e1: E1 target in degrees, mm or user defined units
            e2: E2 target in degrees, mm or user defined units
            e3: E3 target in degrees, mm or user defined units
            frame: user frame or empty for base frame
        Returns:
            motion state after executing the command
        """
        if not self.IsConnected():
            raise NotConnectedException()

        request = robotcontrolapp_pb2.MoveToRequest()
        request.app_name = self.GetAppName()
        request.cart_relative_base.velocity = velocityMms
        request.cart_relative_base.acceleration = acceleration
        request.cart_relative_base.position.x = x
        request.cart_relative_base.position.y = y
        request.cart_relative_base.position.z = z
        request.cart_relative_base.orientation.x = a
        request.cart_relative_base.orientation.y = b
        request.cart_relative_base.orientation.z = c
        request.cart_relative_base.external_joints.append(e1)
        request.cart_relative_base.external_joints.append(e2)
        request.cart_relative_base.external_joints.append(e3)
        request.cart_relative_base.frame = frame
        return MotionState.FromGrpc(self.__grpcStub.MoveTo(request))

    def MoveToLinearRelativeTool(
        self,
        velocityMms: float,
        acceleration: float,
        x: float,
        y: float,
        z: float,
        a: float,
        b: float,
        c: float,
        e1: float,
        e2: float,
        e3: float,
    ) -> MotionState:
        """
        Starts a linear motion to the given position
        Parameters:
        velocityMms: velocity in mm/s
            acceleration: acceleration in percent, 0.0..100.0, negative values result in default value 40%
            x: X position in mm
            y: Y position in mm
            z: Z position in mm
            a: A orientation in mm, currently not used
            b: B orientation in mm, currently not used
            c: C orientation in mm, currently not used
            e1: E1 target in degrees, mm or user defined units
            e2: E2 target in degrees, mm or user defined units
            e3: E3 target in degrees, mm or user defined units
        Returns:
            motion state after executing the command
        """
        if not self.IsConnected():
            raise NotConnectedException()

        request = robotcontrolapp_pb2.MoveToRequest()
        request.app_name = self.GetAppName()
        request.cart_relative_tool.velocity = velocityMms
        request.cart_relative_tool.acceleration = acceleration
        request.cart_relative_tool.position.x = x
        request.cart_relative_tool.position.y = y
        request.cart_relative_tool.position.z = z
        request.cart_relative_tool.orientation.x = a
        request.cart_relative_tool.orientation.y = b
        request.cart_relative_tool.orientation.z = c
        request.cart_relative_tool.external_joints.append(e1)
        request.cart_relative_tool.external_joints.append(e2)
        request.cart_relative_tool.external_joints.append(e3)
        return MotionState.FromGrpc(self.__grpcStub.MoveTo(request))

    def MoveToStop(self) -> MotionState:
        """
        Stops a move-to motion
        Returns:
            motion state after executing the command
        """
        if not self.IsConnected():
            raise NotConnectedException()

        request = robotcontrolapp_pb2.MoveToRequest()
        request.app_name = self.GetAppName()
        request.stop.SetInParent()
        return MotionState.FromGrpc(self.__grpcStub.MoveTo(request))

    def IsAutomaticMotion(self) -> bool:
        """
        Returns true if the robot moves automatically. This does not indicate other motion types, like jog motion!
        Returns:
            true if a Move To command is being executed, if a motion program is running or if the position interface is used.
        """
        motionState = self.GetMotionState()
        return (
            motionState.motionProgram.runState == robotcontrolapp_pb2.RunState.RUNNING
            or motionState.moveTo.runState == robotcontrolapp_pb2.RunState.RUNNING
            or (
                motionState.positionInterface.isEnabled
                and motionState.positionInterface.isInUse
            )
        )

    def WaitMotionDone(self, timeout: float) -> bool:
        """
        Waits until the Move-To command or motion program is done. See the criteria given for IsAutomaticMotion.
        Parameters:
            timeout: The function returns when the motion is done or when this timeout in s is exceeded
        Returns:
            true if motion is done, false on timeout
        """
        startTime = time.time()
        while True:
            if not self.IsAutomaticMotion():
                return True
            now = time.time()
            if now - startTime > timeout:
                break
            time.sleep(0.02)
        return False

    def GetSystemInfo(self) -> SystemInfo:
        """Gets the system information"""
        if not self.IsConnected():
            raise NotConnectedException()

        request = robotcontrolapp_pb2.SystemInfoRequest()
        request.app_name = self.GetAppName()
        return SystemInfo.FromGrpc(self.__grpcStub.GetSystemInfo(request))

    def GetTCP(self) -> Matrix44:
        """Gets the tool center point position and orientation"""
        if not self.IsConnected():
            raise NotConnectedException()

        request = robotcontrolapp_pb2.RobotStateRequest()
        request.app_name = self.GetAppName()
        response = self.__grpcStub.GetRobotState(request)
        return Matrix44.FromGrpc(response.tcp)

    def GetVelocityOverride(self) -> float:
        """
        Gets the current velocity override
        Returns:
            velocity multiplier in percent 0.0..100.0
        """
        if not self.IsConnected():
            raise NotConnectedException()

        request = robotcontrolapp_pb2.RobotStateRequest()
        request.app_name = self.GetAppName()
        response = self.__grpcStub.GetRobotState(request)
        return response.velocity_override

    def SetVelocityOverride(self, velocityPercent: float) -> float:
        """
        Sets the velocity override
        Parameters:
            velocityPercent: requested velocity multiplier in percent 0.0..100.0
        Returns:
            actual velocity multiplier in percent 0.0..100.0
        """
        if not self.IsConnected():
            raise NotConnectedException()

        request = robotcontrolapp_pb2.SetVelocityOverrideRequest()
        request.app_name = self.GetAppName()
        request.velocity_override = velocityPercent
        result = self.__grpcStub.SetVelocityOverride(request)
        return result.velocity_override

    # =========================================================================
    # Kinematics
    # =========================================================================
    def TranslateCartToJoint(
        self,
        x: float,
        y: float,
        z: float,
        a: float,
        b: float,
        c: float,
        initialJoints: list[float],
    ) -> tuple[list[float], robotcontrolapp_pb2.KinematicState]:
        """
        Translates a cartesian position to joint positions
        Parameters:
            x: X coordinate of the TCP in mm
            y: Y coordinate of the TCP in mm
            z: Z coordinate of the TCP in mm
            a: A orientation of the TCP in degrees
            b: B orientation of the TCP in degrees
            c: C orientation of the TCP in degrees
            initialJoints: 6 robot joints and 3 external joints. These are used to derive the initial joint configuration, e.g. whether the elbow points left or right. Set them to 0 if not relevant.
        Returns:
            tuple consisting of a list of joints (6 robot joints, 3 external joints) and the kinematic state. This is 0 if the conversion was successful or a different value on error.
        """
        if not self.IsConnected():
            raise NotConnectedException()

        request = robotcontrolapp_pb2.CartToJointRequest()
        request.app_name = self.GetAppName()
        request.joints.extend(initialJoints)
        request.position.x = x
        request.position.y = y
        request.position.z = z
        request.orientation.x = a
        request.orientation.y = b
        request.orientation.z = c

        response = self.__grpcStub.TranslateCartToJoint(request)
        return (response.joints, response.kinematicState)

    def TranslateJointToCartXYZ(
        self, joints: list[float]
    ) -> tuple[
        float, float, float, float, float, float, robotcontrolapp_pb2.KinematicState
    ]:
        """
        Translates joint positions to a cartesian position
        Parameters:
            joints: joint positions to translate
        Returns:
            A tuple containing the following values in order:
            result X coordinate of the TCP in mm,
            result Y coordinate of the TCP in mm,
            result Z coordinate of the TCP in mm,
            result A orientation of the TCP in degrees,
            result B orientation of the TCP in degrees,
            result C orientation of the TCP in degrees,
            the result state is written here. 0 on success, other value on error
        """
        (mat, state) = self.TranslateJointToCart(joints)
        (a, b, c) = mat.GetOrientation()
        return (mat.GetX(), mat.GetY(), mat.GetZ(), a, b, c, state)

    def TranslateJointToCart(
        self, joints: list[float]
    ) -> tuple[Matrix44, robotcontrolapp_pb2.KinematicState]:
        """
        Translates joint positions to a cartesian position. Note that out-of-range joint values may give you a successful result that may not be reachable or could cause collisions.
        Parameters:
            joints: joint positions to translate
        Returns:
            the matrix defining position and orientation of the TCP is written here,
            the result state is written here. 0 on success, other value on error

        """
        if not self.IsConnected():
            raise NotConnectedException()

        request = robotcontrolapp_pb2.JointToCartRequest()
        request.app_name = self.GetAppName()
        request.joints.extend(joints)

        response = self.__grpcStub.TranslateJointToCart(request)
        return (Matrix44.FromGrpc(response.position), response.kinematicState)

    # =========================================================================
    # File access
    # =========================================================================
    class FileReadIterator:
        """Iterator for reading a file into UploadFileRequests"""

        def __init__(
            self,
            appName: str,
            sourceFile: BufferedReader,
            targetFile: str,
            chunkSize: int,
        ):
            self.__file = sourceFile
            self.__chunkSize = chunkSize
            self.__request = robotcontrolapp_pb2.UploadFileRequest()
            self.__request.app_name = appName
            self.__request.binary_mode = True
            self.__request.filename = targetFile
            # Make sure at least one request is sent, even if empty. Otherwise we can not transmit empty files
            self.__anyRequestSent = False

        def __iter__(self):
            return self

        def __next__(self):
            data = self.__file.read(self.__chunkSize)
            dataStr = data.decode("utf-8")
            if len(data) > 0:
                self.__anyRequestSent = True
                self.__request.data = data
                return self.__request
            elif not self.__anyRequestSent:
                self.__anyRequestSent = True
                self.__request.data = bytes()
                return self.__request
            else:
                raise StopIteration

    class MemoryReadIterator:
        """Iterator for reading data from memory into UploadFileRequests"""

        def __init__(self, appName: str, data: bytes, targetFile: str, chunkSize: int):
            self.__data = memoryview(data)
            self.__chunkSize = chunkSize
            self.__dataIndex = 0
            self.__request = robotcontrolapp_pb2.UploadFileRequest()
            self.__request.app_name = appName
            self.__request.binary_mode = True
            self.__request.filename = targetFile
            # Make sure at least one request is sent, even if empty. Otherwise we can not transmit empty files
            self.__anyRequestSent = False

        def __iter__(self):
            return self

        def __next__(self):
            start = self.__dataIndex
            end = min(start + self.__chunkSize, len(self.__data))
            self.__dataIndex = end
            if start < end:
                self.__anyRequestSent = True
                # why can I not pass memoryview here?
                # self.__request.data = self.__data[start:end]
                self.__request.data = bytes(self.__data[start:end])
                return self.__request
            elif not self.__anyRequestSent:
                self.__anyRequestSent = True
                self.__request.data = bytes()
                return self.__request
            else:
                raise StopIteration

    def UploadFileFromFile(self, sourceFile: str, targetFile: str) -> tuple[bool, str]:
        """
        Uploads a file to the robot control from a file

        Parameters:
            sourceFile: local source file with path relative to the app's directory
            targetFile: target file on the robot control, relative to the Data directory
        Returns:
            Tuple consisting of a boolean (true on success) and error string
        """
        if not self.IsConnected():
            raise NotConnectedException()

        with open(sourceFile, "rb") as file:
            try:
                CHUNK_SIZE = 8 * 1024
                iterator = AppClient.FileReadIterator(
                    self.GetAppName(), file, targetFile, CHUNK_SIZE
                )
                result = self.__grpcStub.UploadFile(iterator)
                return (result.success, result.error)
            except FileNotFoundError:
                raise
            except Exception as ex:
                return (False, ex)

    def UploadFileFromMemory(self, data: bytes, targetFile: str) -> tuple[bool, str]:
        """
        Uploads a file to the robot control from memory

        Parameters:
            data: file content
            targetFile: target file on the robot control, relative to the Data directory
        Returns:
            Tuple consisting of a boolean (true on success) and error string
        """
        if not self.IsConnected():
            raise NotConnectedException()

        try:
            CHUNK_SIZE = 8 * 1024
            iterator = AppClient.MemoryReadIterator(
                self.GetAppName(), data, targetFile, CHUNK_SIZE
            )
            result = self.__grpcStub.UploadFile(iterator)
            return (result.success, result.error)
        except Exception as ex:
            return (False, ex)

    def DownloadFileToFile(self, sourceFile: str, targetFile: str) -> tuple[bool, str]:
        """
        Downloads a file from the robot control to a file

        Parameters:
            sourceFile: source file on the robot control, relative to the Data directory
            targetFile: local target, relative to the apps's directory
        Returns:
            Tuple consisting of a boolean (true on success) and error string
        """
        if not self.IsConnected():
            raise NotConnectedException()

        with open(targetFile, "wb") as file:
            request = robotcontrolapp_pb2.DownloadFileRequest()
            request.app_name = self.GetAppName()
            request.filename = sourceFile
            try:
                for chunk in self.__grpcStub.DownloadFile(request):
                    if chunk.success:
                        file.write(chunk.data)
                    else:
                        file.close()
                        return (False, chunk.error)
            except Exception as ex:
                return (False, ex)
        return (True, "")

    def DownloadFileToMemory(self, sourceFile: str) -> tuple[bool, str, bytearray]:
        """
        Downloads a file from the robot control to memory

        Parameters:
            sourceFile: source file on the robot control, relative to the Data directory
        Returns:
            Tuple consisting of a boolean (true on success), error string and result data
        """
        if not self.IsConnected():
            raise NotConnectedException()

        request = robotcontrolapp_pb2.DownloadFileRequest()
        request.app_name = self.GetAppName()
        request.filename = sourceFile
        resultData = bytearray()
        try:
            for chunk in self.__grpcStub.DownloadFile(request):
                if chunk.success:
                    resultData.extend(chunk.data)
                else:
                    return (False, chunk.error, resultData)
            return (True, "", resultData)
        except Exception as ex:
            return (False, ex, bytearray())

    def RemoveFile(self, file: str) -> tuple[bool, str]:
        """
        Removes a file from the robot control
        Parameters:
            file file on the robot control, relative to the Data directory
        Returns:
            true on success
        """
        if not self.IsConnected():
            raise NotConnectedException()

        request = robotcontrolapp_pb2.RemoveFilesRequest()
        request.app_name = self.GetAppName()
        request.files.append(file)
        response = self.__grpcStub.RemoveFiles(request)

        if len(response.results) > 0 and not response.results[0].success:
            return (False, response.results[0].error)
        elif response.success:
            return (True, "")
        else:
            return (False, "unknown error")

    class DirectoryContent:
        """Description of a directory's content"""

        def __init__(self):
            self.success = False
            self.errorMessage = ""
            self.entries = []

        def FromGrcp(grpc: robotcontrolapp_pb2.ListFilesResponse):
            """
            Creates an object from a GRPC ListFilesResponse
            Returns:
                A new DirectoryContent object
            """
            self = AppClient.DirectoryContent()
            self.success = grpc.success
            self.errorMessage = grpc.error
            self.entries.extend(grpc.entries)
            return self

    def ListFiles(self, directory: str) -> DirectoryContent:
        """Gets the content of a directory"""
        if not self.IsConnected():
            raise NotConnectedException()

        request = robotcontrolapp_pb2.ListFilesRequest()
        request.app_name = self.GetAppName()
        request.path = directory
        return AppClient.DirectoryContent.FromGrcp(self.__grpcStub.ListFiles(request))

    # =========================================================================
    # App UI
    # =========================================================================
    def SendQueuedUIUpdates(self):
        """Send queued UI updates. Queueing benefits performance by sending all updates in a single message."""
        with self.__queuedUIUpdatesMutex:
            if len(self.__queuedUIUpdates.ui_changes) > 0:
                self.SendAction(self.__queuedUIUpdates)
                self.__queuedUIUpdates = robotcontrolapp_pb2.AppAction()

    def RequestUIElementState(self, elementName: str):
        """Requests the state of a UI element. The robot control will respond with a call of UiUpdateHandler() if the element exists and if it was changed after"""
        request = robotcontrolapp_pb2.AppAction()
        request.request_ui_state.append(elementName)
        self.SendAction(request)

    def RequestUIElementStates(self, elementNames: set[str]):
        """Requests the state of several UI elements. The robot control will respond with a call of UiUpdateHandler() if the element exists and if it was changed"""
        request = robotcontrolapp_pb2.AppAction()
        request.request_ui_state.extend(elementNames)
        self.SendAction(request)

    def SetUIVisibility(self, elementName: str, visible: bool):
        """Sets a UI element visible or hidden"""
        request = robotcontrolapp_pb2.AppAction()
        uiElement = request.ui_changes.add()
        uiElement.element_name = elementName
        uiElement.is_visible = visible
        self.SendAction(request)

    def QueueSetUIVisibility(self, elementName: str, visible: bool):
        """Queues setting a UI element visible or hidden"""
        with self.__queuedUIUpdatesMutex:
            uiElement = self.__queuedUIUpdates.ui_changes.add()
            uiElement.element_name = elementName
            uiElement.is_visible = visible

    def SetUIVisibilitySet(self, elements: set[tuple[str, bool]]):
        """Set a list of UI element visible or hidden"""
        request = robotcontrolapp_pb2.AppAction()
        for element in elements:
            uiElement = request.ui_changes.add()
            uiElement.element_name = element[0]
            uiElement.is_visible = element[1]
        self.SendAction(request)

    def QueueSetUIVisibilitySet(self, elements: set[tuple[str, bool]]):
        """Queues setting a list of UI element visible or hidden"""
        with self.__queuedUIUpdatesMutex:
            for element in elements:
                uiElement = self.__queuedUIUpdates.ui_changes.add()
                uiElement.element_name = element[0]
                uiElement.is_visible = element[1]

    def SetCheckboxState(self, elementName: str, isChecked: bool):
        """Sets the checked state of a checkbox"""
        request = robotcontrolapp_pb2.AppAction()
        uiElement = request.ui_changes.add()
        uiElement.element_name = elementName
        if isChecked:
            uiElement.state.checkbox_state = robotcontrolapp_pb2.CHECKED
        else:
            uiElement.state.checkbox_state = robotcontrolapp_pb2.UNCHECKED
        self.SendAction(request)

    def QueueSetCheckboxState(self, elementName: str, isChecked: bool):
        """Queues setting the checked state of a checkbox"""
        with self.__queuedUIUpdatesMutex:
            uiElement = self.__queuedUIUpdates.ui_changes.add()
            uiElement.element_name = elementName
            if isChecked:
                uiElement.state.checkbox_state = robotcontrolapp_pb2.CHECKED
            else:
                uiElement.state.checkbox_state = robotcontrolapp_pb2.UNCHECKED

    def SetDropDownState(self, elementName: str, selectedValue: str):
        """Sets the selected value of a drop down box"""
        request = robotcontrolapp_pb2.AppAction()
        uiElement = request.ui_changes.add()
        uiElement.element_name = elementName
        uiElement.state.dropdown_state.selected_option = selectedValue
        self.SendAction(request)

    def QueueSetDropDownState(self, elementName: str, selectedValue: str):
        """Queues setting the selected value of a drop down box"""
        with self.__queuedUIUpdatesMutex:
            uiElement = self.__queuedUIUpdates.ui_changes.add()
            uiElement.element_name = elementName
            uiElement.element_name = elementName
        uiElement.state.dropdown_state.selected_option = selectedValue

    def SetDropDownState(
        self, elementName: str, selectedValue: str, selectableEntries: List[str]
    ):
        """Sets the selected value and the list of selectable values of a drop down box"""
        request = robotcontrolapp_pb2.AppAction()
        uiElement = request.ui_changes.add()
        uiElement.element_name = elementName
        uiElement.state.dropdown_state.selected_option = selectedValue
        uiElement.state.dropdown_state.options.extend(selectableEntries)
        self.SendAction(request)

    def QueueSetDropDownState(
        self, elementName: str, selectedValue: str, selectableEntries: List[str]
    ):
        """Queues setting the selected value and the list of selectable values of a drop down box"""
        with self.__queuedUIUpdatesMutex:
            uiElement = self.__queuedUIUpdates.ui_changes.add()
            uiElement.element_name = elementName
            uiElement.element_name = elementName
            uiElement.state.dropdown_state.selected_option = selectedValue
            uiElement.state.dropdown_state.options.extend(selectableEntries)

    def SetText(self, elementName: str, value: str):
        """Sets the text of a text box, label, etc."""
        request = robotcontrolapp_pb2.AppAction()
        uiElement = request.ui_changes.add()
        uiElement.element_name = elementName
        uiElement.state.textfield_state.current_text = value
        self.SendAction(request)

    def QueueSetText(self, elementName: str, value: str):
        """Queues setting the text of a text box, label, etc."""
        with self.__queuedUIUpdatesMutex:
            uiElement = self.__queuedUIUpdates.ui_changes.add()
            uiElement.element_name = elementName
            uiElement.state.textfield_state.current_text = value

    def SetNumber(self, elementName: str, value: float):
        """Sets the number value of a number box, text box, label, etc."""
        request = robotcontrolapp_pb2.AppAction()
        uiElement = request.ui_changes.add()
        uiElement.element_name = elementName
        uiElement.state.numberfield_state.current_number = value
        self.SendAction(request)

    def QueueSetNumber(self, elementName: str, value: float):
        """Queues setting the number value of a number box, text box, label, etc."""
        with self.__queuedUIUpdatesMutex:
            uiElement = self.__queuedUIUpdates.ui_changes.add()
            uiElement.element_name = elementName
            uiElement.state.numberfield_state.current_number = value

    def SetImage(
        self,
        elementName: str,
        uiWidth: int,
        uiHeight: int,
        imageData: bytearray,
        encoding: robotcontrolapp_pb2.ImageState.ImageData.ImageEncoding,
    ):
        """
        Sets the image of an image element in the UI
        Parameters:
            elementName: UI element name
            uiWidth: Width of the image in the UI in pixels - currently not used yet
            uiHeight: Height of the image in the UI in pixels - currently not used yet
            imageData: Image bytes. All shown images combined must be less than 290kB, otherwise the UI may fail to load after reconnect!
            encoding: Image encoding
        """
        # Check the image size. The CRI input buffer currently is 400kB and image data is transmitted base64 encoded. This means an upper limit of less than 300kB.
        # Note that this limit effectively decreases when using more images or UI elements! The entire UI XML including all images must fit, otherwise it will not be shown after reconnect.
        if len(imageData) > (290 * 1024):
            raise RuntimeError("Image too big! Images must be smaller than 290kB!")

        request = robotcontrolapp_pb2.AppAction()
        uiElement = request.ui_changes.add()
        uiElement.element_name = elementName
        uiElement.state.image_state.image_data.height = uiHeight
        uiElement.state.image_state.image_data.width = uiWidth
        uiElement.state.image_state.image_data.encoding = encoding
        uiElement.state.image_state.image_data.data = imageData
        self.SendAction(request)

    def SetImageFromFile(
        self, elementName: str, uiWidth: int, uiHeight: int, imageFile: str
    ):
        """
        Sets the image of an image element in the UI
        Parameters:
            elementName: UI element name
            uiWidth: Width of the image in the UI in pixels - currently not used yet
            uiHeight: Height of the image in the UI in pixels - currently not used yet
            imageFile: File name and path of the image file to load
        """
        with open(imageFile, "rb") as file:
            imageBytes = file.read()
            self.SetImage(
                elementName,
                uiWidth,
                uiHeight,
                imageBytes,
                robotcontrolapp_pb2.ImageState.ImageData.ImageEncoding.JPEG,
            )

    def QueueSetImage(
        self,
        elementName: str,
        uiWidth: int,
        uiHeight: int,
        imageData: bytearray,
        encoding: robotcontrolapp_pb2.ImageState.ImageData.ImageEncoding,
    ):
        """Queues setting the image of an image element in the UI"""

        # Check the image size. The CRI input buffer currently is 400kB and image data is transmitted base64 encoded. This means an upper limit of less than 300kB.
        if len(imageData) > (290 * 1024):
            raise RuntimeError("Image too big! Images must be smaller than 290kB!")

        with self.__queuedUIUpdatesMutex:
            uiElement = self.__queuedUIUpdates.ui_changes.add()
            uiElement.element_name = elementName
            uiElement.state.image_state.image_data.height = uiHeight
            uiElement.state.image_state.image_data.width = uiWidth
            uiElement.state.image_state.image_data.encoding = encoding
            uiElement.state.image_state.image_data.data = imageData

    def _ShowDialog(
        self,
        message: str,
        title: str,
        dlgType: robotcontrolapp_pb2.ShowDialogRequest.DialogType,
    ):
        """
        Shows a dialog window to the user.
        Note: If iRC is not connected the dialog will never be shown. Currently there is no way for the app to find out whether this is the case. If iRC is older than V14-004 only error messages are shown.
        Parameters:
            message: The message to be displayed
            title: The dialog title
            dlgType: the dialog type (Info, Error, Warning)
        """
        if not self.IsConnected():
            raise NotConnectedException()

        request = robotcontrolapp_pb2.ShowDialogRequest()
        request.app_name = self.GetAppName()
        request.message_dialog.type = dlgType
        request.message_dialog.title = title
        request.message_dialog.message = message
        self.__grpcStub.ShowDialog(request)

    def ShowInfoDialog(self, message: str, title: str):
        """
        Shows an info dialog window to the user.
        Note: If iRC is not connected or older than V14-004 the dialog will never be shown. Currently there is no way for the app to find out whether this is the case.
        Parameters:
            message: The message to be displayed
            title: The dialog title
        """
        self._ShowDialog(
            message, title, robotcontrolapp_pb2.ShowDialogRequest.DialogType.INFO
        )

    def ShowWarningDialog(self, message: str, title: str):
        """
        Shows an info dialog window to the user.
        Note: If iRC is not connected or older than V14-004 the dialog will never be shown. Currently there is no way for the app to find out whether this is the case.
        Parameters:
            message: The message to be displayed
            title: The dialog title
        """
        self._ShowDialog(
            message, title, robotcontrolapp_pb2.ShowDialogRequest.DialogType.WARNING
        )

    def ShowErrorDialog(self, message: str, title: str):
        """
        Shows an info dialog window to the user.
        Note: If iRC is not connected the dialog will never be shown. Currently there is no way for the app to find out whether this is the case.
        Parameters:
            message: The message to be displayed
            title: The dialog title
        """
        self._ShowDialog(
            message, title, robotcontrolapp_pb2.ShowDialogRequest.DialogType.ERROR
        )

    # =========================================================================
    # Internal helpers
    # =========================================================================

    def CheckCoreVersion(self, sysInfo: SystemInfo):
        """Checks whether the connected robot supports all features of this AppClient"""
        if sysInfo.versionMajor > self.VERSION_MAJOR_MIN:
            return True
        elif sysInfo.versionMajor == self.VERSION_MAJOR_MIN:
            if sysInfo.versionMinor > self.VERSION_MINOR_MIN:
                return True
            elif sysInfo.versionMinor == self.VERSION_MINOR_MIN:
                if sysInfo.versionPatch >= self.VERSION_PATCH_MIN:
                    return True
        return False

    def SendCapabilities(self):
        """Sends the apps capabilities / API version to the server"""
        if not self.IsConnected():
            raise NotConnectedException()

        request = robotcontrolapp_pb2.CapabilitiesRequest()
        request.app_name = self.GetAppName()
        request.api_version_major = self.VERSION_MAJOR_MIN
        request.api_version_minor = self.VERSION_MINOR_MIN
        request.api_version_patch = self.VERSION_PATCH_MIN
        self.__grpcStub.SetCapabilities(request)

    # =========================================================================
    # Virtual methods to override
    # =========================================================================

    def _AppFunctionHandler(self, function: robotcontrolapp_pb2.AppFunction):
        """
        Gets called on remote app function calls received from the robot control.
        Override this in your app!
        """
        raise NotImplementedError()

    def _UiUpdateHandler(
        self,
        updates: protobufContainers.RepeatedCompositeFieldContainer[
            robotcontrolapp_pb2.AppUIElement
        ],
    ):
        """
        Gets called on remote UI update requests received from the robot control.
        Override this in your app!
        """
        raise NotImplementedError()
