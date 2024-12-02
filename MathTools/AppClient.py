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


class AppClient:
    """This class is the interface between GRPC and the app logic."""

    # Constructor, arguments are the name of the app and the target socket
    def __init__(self, appName: str, target: str):
        self.__appName = appName
        self.__targetSocket = target
        self.__grpcChannel = grpc.insecure_channel(self.__targetSocket)
        self.__grpcStub = RobotControlAppStub(self.__grpcChannel)
        self.__stopThreads = True
        self.__queuedUIUpdates = robotcontrolapp_pb2.AppAction()
        self.__queuedUIUpdatesMutex = Lock()

    def __enter__(self):
        self.Connect()

    def __exit__(self):
        self.Disconnect()

    def GetAppName(self) -> str:
        """Gets the name of the app"""
        return self.__appName

    def Connect(self):
        """Connects the app"""
        if not self.IsConnected():
            print("Connecting app '" + self.__appName + "'")
            self.__stopThreads = False

            # clear queue
            self.__actionsQueue = Queue()

            # Send an empty action at startup (this is queued and sent later by the thread)
            self.SendAction(robotcontrolapp_pb2.AppAction())

            # Start threads
            self.__receivedActions = self.__grpcStub.RecieveActions(
                iter(self.__actionsQueue.get, None)
            )
            self.__eventReaderThread = Thread(target=self.EventReaderThread)
            self.__eventReaderThread.start()
        else:
            print(
                f"Connect requested for app '{self.GetAppName()}' but it is still connected. Please call disconnect first!",
                file=sys.stderr,
            )

    def Disconnect(self):
        """Disconnects the app"""
        if self.IsConnected():
            print(f"Disconnecting app '{self.GetAppName()}'")
            self.__stopThreads = True
            self.__grpcChannel.close()
            if threading.current_thread != self.__eventReaderThread:
                self.__eventReaderThread.join()

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

    def GetTcp(self) -> Matrix44:
        """Gets the tool center point position and orientation"""
        if not self.IsConnected():
            raise RuntimeError("not connected")

        request = robotcontrolapp_pb2.GetTCPRequest()
        request.app_name = self.GetAppName()
        response = self.__grpcStub.GetTCP(request)
        return Matrix44.FromGrpc(response)

    def GetProgramVariable(self, variableName: str) -> ProgramVariable:
        """Gets the program variable, throws exception on error, e.g. if the variable does not exist"""
        if len(variableName) == 0:
            raise RuntimeError("requested variable with empty name")

        names = {variableName}
        result = self.GetProgramVariables(names)
        if len(result) == 0:
            raise RuntimeError(
                f"failed to get variable '{variableName}': variable does not exist"
            )
        return result.pop()

    def GetNumberVariable(self, variableName: str) -> NumberVariable:
        """Gets the given number variable, throws on error, e.g. if the variable does not exist or is of a different type"""
        variable = self.GetProgramVariable(variableName)
        if not isinstance(variable, NumberVariable):
            raise RuntimeError(
                "requested variable '" + variableName + "' is no number variable"
            )
        return variable

    def GetPositionVariable(self, variableName: str) -> PositionVariable:
        """Gets the given position variable, throws on error, e.g. if the variable does not exist or is of a different type"""
        variable = self.GetProgramVariable(variableName)
        if not isinstance(variable, PositionVariable):
            raise RuntimeError(
                "requested variable '" + variableName + "' is no position variable"
            )
        return variable

    def GetProgramVariables(self, variableNames: set[str]) -> set[ProgramVariable]:
        """Gets program variables"""
        if not self.IsConnected():
            raise RuntimeError("not connected")

        request = robotcontrolapp_pb2.ProgramVariablesRequest()
        request.app_name = self.GetAppName()
        for variableName in variableNames:
            if len(variableName) > 0:
                request.variable_names.append(variableName)

        resultVariables = set()
        for grpcVariable in self.__grpcStub.GetProgramVariables(request):
            if grpcVariable.HasField("number"):
                resultVariables.add(
                    NumberVariable(grpcVariable.name, grpcVariable.number)
                )
            elif grpcVariable.HasField("position"):
                if grpcVariable.position.HasField("robot_joints"):
                    resultVariables.add(
                        PositionVariable.MakeJoint(
                            grpcVariable.name,
                            grpcVariable.position.robot_joints.joints,
                            grpcVariable.position.external_joints,
                        )
                    )
                elif grpcVariable.position.HasField("both"):
                    cartesian = Matrix44.FromGrpc(grpcVariable.position.both.cartesian)
                    resultVariables.add(
                        PositionVariable.MakeBoth(
                            grpcVariable.name,
                            cartesian,
                            grpcVariable.position.both.robot_joints.joints,
                            grpcVariable.position.external_joints,
                        )
                    )
                elif grpcVariable.position.HasField("cartesian"):
                    cartesian = Matrix44.FromGrpc(grpcVariable.position.cartesian)
                    resultVariables.add(
                        PositionVariable.MakeCartesian(
                            grpcVariable.name,
                            cartesian,
                            grpcVariable.position.external_joints,
                        )
                    )

        return resultVariables

    def SetNumberVariable(self, name: str, value: float):
        """Sets a number variable"""
        if not self.IsConnected():
            raise RuntimeError("not connected")

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
        """Sets a position variable with joint angles. The robot control will try to convert these to cartesian."""
        if not self.IsConnected():
            raise RuntimeError("not connected")

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
        """Sets a position variable with a cartesian position. The robot control will try to convert this to joint angles"""
        if not self.IsConnected():
            raise RuntimeError("not connected")

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
        """Sets a position variable with joint angles and cartesian position. Warning: joint angles and cartesian may refer to different positions!"""
        if not self.IsConnected():
            raise RuntimeError("not connected")

        request = robotcontrolapp_pb2.SetProgramVariablesRequest()
        request.app_name = self.GetAppName()
        variable = request.variables.add()
        variable.name = name
        variable.position.cartesian.CopyFrom(cartesianPosition.ToGrpc())
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

    def SendFunctionDone(self, callId: int):
        """Announces to the robot control that the app function call finished. This allows the robot program to continue with the next command."""
        response = robotcontrolapp_pb2.AppAction()
        response.done_functions.append(callId)
        self.SendAction(response)

    def SendFunctionFailed(self, callId: int, reason: str):
        """
        Announces to the robot control that the app function call failed. This will abort the program with an error message.
        This is supported from V14-003
        """
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
            raise RuntimeError("not connected")
        
        request = robotcontrolapp_pb2.ResetErrorsRequest()
        request.app_name = self.GetAppName()
        self.__grpcStub.ResetErrors(request)

    def EnableMotors(self):
        """Resets hardware errors and enables the motors"""
        if not self.IsConnected():
            raise RuntimeError("not connected")
        
        request = robotcontrolapp_pb2.EnableMotorsRequest()
        request.app_name = self.GetAppName()
        request.enable = True
        self.__grpcStub.EnableMotors(request)

    def DisableMotors(self):
        """Disables the motors and IO"""
        if not self.IsConnected():
            raise RuntimeError("not connected")
        
        request = robotcontrolapp_pb2.EnableMotorsRequest()
        request.app_name = self.GetAppName()
        request.enable = False
        self.__grpcStub.EnableMotors(request)

    # =========================================================================
    # Referencing
    # =========================================================================
    def ReferenceAllJoints(self, withReferencingProgram: bool | None):
        """Starts referencing all joints"""
        if not self.IsConnected():
            raise RuntimeError("not connected")
        
        request = robotcontrolapp_pb2.ReferenceJointsRequest()
        request.app_name = self.GetAppName()
        request.reference_all = True
        request.referencing_program = withReferencingProgram == True
        self.__grpcStub.ReferenceJoints(request)

    def ReferencingProgram(self):
        """Runs the referencing program, then references again. Does not reference before calling the program."""
        if not self.IsConnected():
            raise RuntimeError("not connected")
        
        request = robotcontrolapp_pb2.ReferenceJointsRequest()
        request.app_name = self.GetAppName()
        request.reference_all = False
        request.referencing_program = True
        self.__grpcStub.ReferenceJoints(request)

    def ReferenceRobotJoint(self, n: int):
        """Starts referencing a robot joint"""
        if not self.IsConnected():
            raise RuntimeError("not connected")
        
        request = robotcontrolapp_pb2.ReferenceJointsRequest()
        request.app_name = self.GetAppName()
        request.reference_all = False
        request.referencing_program = False
        request.reference_robot_joints.append(n)
        self.__grpcStub.ReferenceJoints(request)

    def ReferenceExternalJoint(self, n: int):
        """Starts referencing an external joint"""
        if not self.IsConnected():
            raise RuntimeError("not connected")
        
        request = robotcontrolapp_pb2.ReferenceJointsRequest()
        request.app_name = self.GetAppName()
        request.reference_all = False
        request.referencing_program = False
        request.reference_external_joints.append(n)
        self.__grpcStub.ReferenceJoints(request)

    def ReferenceJoints(self, robotJoints: set[int], externalJoints: set[int]):
        """Starts referencing robot and external joints without delay"""
        if not self.IsConnected():
            raise RuntimeError("not connected")
        
        request = robotcontrolapp_pb2.ReferenceJointsRequest()
        request.app_name = self.GetAppName()
        request.reference_all = False
        request.referencing_program = False
        for j in robotJoints:
            request.reference_robot_joints.append(j)
        for j in externalJoints:
            request.reference_external_joints.append(j)
        self.__grpcStub.ReferenceJoints(request)

    # =========================================================================
    # Robot state
    # =========================================================================
    def GetRobotState(self) -> RobotState:
        """Gets the current state"""
        if not self.IsConnected():
            raise RuntimeError("not connected")
        
        request = robotcontrolapp_pb2.RobotStateRequest()
        request.app_name = self.GetAppName()
        return MotionState.FromGrpc(self.__grpcStub.GetRobotState(request))

    class RobotStateIterator:
        """An iterator for streaming the RobotState. Set stopIteration to True to stop the stream"""
        def __init__(self, appName: str):
            """
            Constructor
            Parameters:
                appName app name for the request
            """
            self.__request = robotcontrolapp_pb2.RobotStateRequest()
            self.__request.app_name = self.GetAppName()
            self.stopIteration = False
        
        def __iter__(self):
            return self
        
        def __next__(self):
            if self.stopIteration:
                raise StopIteration
            return self.__request

    def __RobotStateThread(self):
        """Thread method for the RobotState reader"""
        iterator = AppClient.RobotStateIterator(self.GetAppName())
        while not iterator.stopIteration:
            if not self.__robotStateStreamActive or not self.IsConnected():
                response.stopIteration = True
            response = self.__grpcStub.GetRobotStateStream(iterator)
            if response.stopIteration:
                break
            else:
                self._OnRobotStateUpdated(response)
        self.__robotStateStreamActive = False

    def StartRobotStateStream(self):
        """Starts streaming the robot state"""
        if not self.IsConnected():
            raise RuntimeError("not connected")
        
        self.StopRobotStateStream()
        self.__robotStateStreamActive = True
        self.__robotStateThread = Thread(target=self.__RobotStateThread)
        self.__robotStateThread.start()
    
    def StopRobotStateStream(self):
        """Stops streaming the robot state"""
        if hasattr(self.__robotStateThread) and self.__robotStateThread.is_alive():
            self.__robotStateStreamActive = False
            self.__robotStateThread.join()

    def _OnRobotStateUpdated(self, state: RobotState):
        """Is called when the robot state is updated (usually each 10 or 20ms). Override this method, start the stream by calling StartRobotStateStream()."""
        raise NotImplementedError("Derive _OnRobotStateUpdated() before using StartRobotStateStream()!")

    def SetDigitalInput(self, number: int, state: bool):
        """Sets the state of a digital input (only in simulation)"""
        if not self.IsConnected():
            raise RuntimeError("not connected")
        
        request = robotcontrolapp_pb2.IOStateRequest()
        din = request.DIns.add()
        din.id = number
        if state:
            din.state = robotcontrolapp_pb2.DIOState.HIGH 
        else:
            din.state = robotcontrolapp_pb2.DIOState.LOW

        request.app_name = self.GetAppName()
        self.__grpcStub.SetIOState(request)

    def SetDigitalOutput(self, number: int, state: bool):
        """Sets the state of a digital output (only in simulation)"""
        if not self.IsConnected():
            raise RuntimeError("not connected")
        
        request = robotcontrolapp_pb2.IOStateRequest()
        dout = request.DOuts.add()
        dout.id = number
        if state:
            dout.target_state = robotcontrolapp_pb2.DIOState.HIGH 
        else:
            dout.target_state = robotcontrolapp_pb2.DIOState.LOW

        request.app_name = self.GetAppName()
        self.__grpcStub.SetIOState(request)

    def SetGlobalSignal(self, number: int, state: bool):
        """Sets the state of a global signal (only in simulation)"""
        if not self.IsConnected():
            raise RuntimeError("not connected")
        
        request = robotcontrolapp_pb2.IOStateRequest()
        gsig = request.GSigs.add()
        gsig.id = number
        if state:
            gsig.target_state = robotcontrolapp_pb2.DIOState.HIGH 
        else:
            gsig.target_state = robotcontrolapp_pb2.DIOState.LOW

        request.app_name = self.GetAppName()
        self.__grpcStub.SetIOState(request)

    def GetMotionState(self) -> MotionState:
        """Gets the current motion state (program execution etc)"""
        if not self.IsConnected():
            raise RuntimeError("not connected")
        
        request = robotcontrolapp_pb2.GetMotionStateRequest()
        request.app_name = self.GetAppName()
        return MotionState.FromGrpc(self.__grpcStub.GetMotionState(request))

    def LoadMotionProgram(self, program: str) -> MotionState:
        """Loads a motion program"""
        if not self.IsConnected():
            raise RuntimeError("not connected")
        
        request = robotcontrolapp_pb2.MotionInterpolatorRequest()
        request.app_name = self.GetAppName()
        request.main_program = program
        return MotionState.FromGrpc(self.__grpcStub.SetMotionInterpolator(request))
    
    def UnloadMotionProgram(self) -> MotionState:
        """Unloads the motion program"""
        return self.LoadMotionProgram("")

    def StartMotionProgram(self) -> MotionState:
        """Starts or continues the motion program"""
        if not self.IsConnected():
            raise RuntimeError("not connected")
        
        request = robotcontrolapp_pb2.MotionInterpolatorRequest()
        request.app_name = self.GetAppName()
        request.runstate = robotcontrolapp_pb2.RunState.RUNNING
        return MotionState.FromGrpc(self.__grpcStub.SetMotionInterpolator(request))

    def StartMotionProgramAt(self, commandIdx: int, subProgram: str) -> MotionState:
        """Starts or continues the motion program at a specific command"""
        if not self.IsConnected():
            raise RuntimeError("not connected")
        
        request = robotcontrolapp_pb2.MotionInterpolatorRequest()
        request.app_name = self.GetAppName()
        request.runstate = robotcontrolapp_pb2.RunState.RUNNING
        request.start_at.program = subProgram
        request.start_at.command = commandIdx
        return MotionState.FromGrpc(self.__grpcStub.SetMotionInterpolator(request))

    def PauseMotionProgram(self) -> MotionState:
        """Pauses the motion program"""
        if not self.IsConnected():
            raise RuntimeError("not connected")
        
        request = robotcontrolapp_pb2.MotionInterpolatorRequest()
        request.app_name = self.GetAppName()
        request.runstate = robotcontrolapp_pb2.RunState.PAUSED
        return MotionState.FromGrpc(self.__grpcStub.SetMotionInterpolator(request))
    
    def StopMotionProgram(self) -> MotionState:
        """Stops the motion program"""
        if not self.IsConnected():
            raise RuntimeError("not connected")
        
        request = robotcontrolapp_pb2.MotionInterpolatorRequest()
        request.app_name = self.GetAppName()
        request.runstate = robotcontrolapp_pb2.RunState.NOT_RUNNING
        return MotionState.FromGrpc(self.__grpcStub.SetMotionInterpolator(request))

    def SetMotionProgramSingle(self) -> MotionState:
        """Sets the motion program to run once"""
        if not self.IsConnected():
            raise RuntimeError("not connected")
        
        request = robotcontrolapp_pb2.MotionInterpolatorRequest()
        request.app_name = self.GetAppName()
        request.replay_mode = robotcontrolapp_pb2.ReplayMode.SINGLE
        return MotionState.FromGrpc(self.__grpcStub.SetMotionInterpolator(request))
    
    def SetMotionProgramRepeat(self) -> MotionState:
        """Sets the motion program to repeat"""
        if not self.IsConnected():
            raise RuntimeError("not connected")
        
        request = robotcontrolapp_pb2.MotionInterpolatorRequest()
        request.app_name = self.GetAppName()
        request.replay_mode = robotcontrolapp_pb2.ReplayMode.REPEAT
        return MotionState.FromGrpc(self.__grpcStub.SetMotionInterpolator(request))
    
    def SetMotionProgramStep(self) -> MotionState:
        """Sets the motion program to pause after each step"""
        if not self.IsConnected():
            raise RuntimeError("not connected")
        
        request = robotcontrolapp_pb2.MotionInterpolatorRequest()
        request.app_name = self.GetAppName()
        request.replay_mode = robotcontrolapp_pb2.ReplayMode.STEP
        return MotionState.FromGrpc(self.__grpcStub.SetMotionInterpolator(request))

    def LoadLogicProgram(self, program: str) -> MotionState:
        """Loads and starts a logic program"""
        if not self.IsConnected():
            raise RuntimeError("not connected")
        
        request = robotcontrolapp_pb2.LogicInterpolatorRequest()
        request.app_name = self.GetAppName()
        request.main_program = program
        return MotionState.FromGrpc(self.__grpcStub.SetLogicInterpolator(request))

    def UnloadLogicProgram(self) -> MotionState:
        """Unloads the logic program"""
        return self.LoadLogicProgram("")

    def MoveToJoint(self, velocityPercent: float, acceleration: float, a1: float, a2: float, a3: float, a4: float, a5: float, a6: float, e1: float, e2: float, e3: float) -> MotionState:
        """Starts a joint motion to the given position"""
        if not self.IsConnected():
            raise RuntimeError("not connected")
        
        request = robotcontrolapp_pb2.MoveToRequest()
        request.app_name = self.GetAppName()
        request.joint = robotcontrolapp_pb2.MoveToRequest.MoveToJoint()
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
    
    def MoveToJointRelative(self, velocityPercent: float, acceleration: float, float, a1: float, a2: float, a3: float, a4: float, a5: float, a6: float, e1: float, e2: float, e3: float) -> MotionState:
        """Starts a relative joint motion to the given position"""
        if not self.IsConnected():
            raise RuntimeError("not connected")
        
        request = robotcontrolapp_pb2.MoveToRequest()
        request.app_name = self.GetAppName()
        request.joint_relative = robotcontrolapp_pb2.MoveToRequest.MoveToJoint()
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

    def MoveToLinear(self, velocityMms: float, acceleration: float, x: float, y: float, z: float, a: float, b: float, c: float, e1: float, e2: float, e3: float, frame: str) -> MotionState:
        """Starts a linear motion to the given position"""
        if not self.IsConnected():
            raise RuntimeError("not connected")
        
        request = robotcontrolapp_pb2.MoveToRequest()
        request.app_name = self.GetAppName()
        request.cart = robotcontrolapp_pb2.MoveToRequest.MoveToCart()
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
    
    def MoveToLinearRelativeBase(self, velocityMms: float, acceleration: float, x: float, y: float, z: float, a: float, b: float, c: float, e1: float, e2: float, e3: float, frame: str) -> MotionState:
        """Starts a linear motion to the given position"""
        if not self.IsConnected():
            raise RuntimeError("not connected")
        
        request = robotcontrolapp_pb2.MoveToRequest()
        request.app_name = self.GetAppName()
        request.cart_relative_base = robotcontrolapp_pb2.MoveToRequest.MoveToCart()
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
    
    def MoveToLinearRelativeTool(self, velocityMms: float, acceleration: float, x: float, y: float, z: float, a: float, b: float, c: float, e1: float, e2: float, e3: float) -> MotionState:
        """Starts a linear motion to the given position"""
        if not self.IsConnected():
            raise RuntimeError("not connected")
        
        request = robotcontrolapp_pb2.MoveToRequest()
        request.app_name = self.GetAppName()
        request.cart_relative_tool = robotcontrolapp_pb2.MoveToRequest.MoveToCart()
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
        """Stops a move-to motion"""
        if not self.IsConnected():
            raise RuntimeError("not connected")
        
        request = robotcontrolapp_pb2.MoveToRequest()
        request.app_name = self.GetAppName()
        request.stop = robotcontrolapp_pb2.MoveToRequest.MoveToStop()
        return MotionState.FromGrpc(self.__grpcStub.MoveTo(request))

    def GetSystemInfo(self) -> SystemInfo:
        """Gets the system information"""
        if not self.IsConnected():
            raise RuntimeError("not connected")
        
        request = robotcontrolapp_pb2.SystemInfoRequest()
        request.app_name = self.GetAppName()
        return MotionState.FromGrpc(self.__grpcStub.GetSystemInfo(request))

    def GetTcp(self) -> Matrix44:
        """Gets the tool center point position and orientation"""
        if not self.IsConnected():
            raise RuntimeError("not connected")
        
        request = robotcontrolapp_pb2.RobotStateRequest()
        request.app_name = self.GetAppName()
        response = self.__grpcStub.GetRobotState(request)
        return Matrix44.FromGrpc(response.tcp)
    
    def GetVelocity(self) -> float:
        """Gets the current velocity override"""
        if not self.IsConnected():
            raise RuntimeError("not connected")
        
        request = robotcontrolapp_pb2.RobotStateRequest()
        request.app_name = self.GetAppName()
        response = self.__grpcStub.GetRobotState(request)
        return response.velocity_override

    def SetVelocity(self, velocityPercent: float):
        """Sets the velocity override"""
        if not self.IsConnected():
            raise RuntimeError("not connected")
        
        request = robotcontrolapp_pb2.SetVelocityOverrideRequest()
        request.app_name = self.GetAppName()
        request.velocity_override = velocityPercent
        self.__grpcStub.SetVelocityOverride(request)

    # =========================================================================
    # Kinematics
    # =========================================================================
    def TranslateCartToJoint(self, x: float, y:float, z:float, a:float, b:float, c:float, initialJoints : list[float]) -> tuple[list[float], robotcontrolapp_pb2.KinematicState]:
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
            raise RuntimeError("not connected")
        
        request = robotcontrolapp_pb2.CartToJointRequest()
        request.app_name = self.GetAppName()
        request.joints = initialJoints
        request.position.x = x
        request.position.y = y
        request.position.z = z
        request.orientation.x = a
        request.orientation.y = b
        request.orientation.z = c
        
        response = self.__grpcStub.TranslateCartToJoint(request)
        return (response.joints, response.kinematicstate)
    
    def TranslateJointToCartXYZ(self, joints: list[float]) -> tuple[float,float,float,float,float,float, robotcontrolapp_pb2.KinematicState]:
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

    def TranslateJointToCart(self, joints: list[float]) -> tuple[Matrix44, robotcontrolapp_pb2.KinematicState]:
        """
        Translates joint positions to a cartesian position
        Parameters:
            joints: joint positions to translate
        Returns:
            the matrix defining position and orientation of the TCP is written here,
            the result state is written here. 0 on success, other value on error

        """
        if not self.IsConnected():
            raise RuntimeError("not connected")

        request = robotcontrolapp_pb2.JointToCartRequest()
        request.app_name = self.GetAppName()
        request.joints = joints

        response = self.__grpcStub.TranslateJointToCart(request)
        return (Matrix44.FromGrpc(response.position), response.kinematicstate)

    # =========================================================================
    # File access
    # =========================================================================
    class FileReadIterator:
        """Iterator for reading a file into UploadFileRequests"""
        def __init__(self, appName: str, sourceFile: str, targetFile: str, chunkSize: int):
            self.__file = open(sourceFile, "rb")
            self.__chunkSize = chunkSize
            self.__request = robotcontrolapp_pb2.UploadFileRequest()
            self.__request.app_name = appName
            self.__request.binary_mode = True
            self.__request.filename = targetFile

        def __enter__(self):
            return
        
        def __exit__(self):
            self.__file.close()

        def __iter__(self):
            return self

        def __next__(self):
            self.__request.data = self.__file.read(self.__chunkSize)
            if self.__request.data.count > 0:
                return self.__request
            else:
                self.__file.close()
                raise StopIteration
        
    class MemoryReadIterator:
        """Iterator for reading data from memory into UploadFileRequests"""
        def __init__(self, appName: str, data : bytes | bytearray, targetFile: str, chunkSize: int):
            self.__data = memoryview(data)
            self.__chunkSize = chunkSize
            self.__dataIndex = 0
            self.__request = robotcontrolapp_pb2.UploadFileRequest()
            self.__request.app_name = appName
            self.__request.binary_mode = True
            self.__request.filename = targetFile

        def __iter__(self):
            return self

        def __next__(self):
            start = self.__dataIndex
            end = min(start + self.__chunkSize, self.__data.count-1)
            if start < end:
                self.__request.data = self.__request.data[start:end+1]
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
            raise RuntimeError("not connected")

        try:
            CHUNK_SIZE = 8 * 1024
            with AppClient.FileReadIterator(self.GetAppName(), sourceFile, targetFile, CHUNK_SIZE) as iterator:
                result = self.__grpcStub.UploadFile(iterator)
                return (result.success, result.error)
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
            raise RuntimeError("not connected")

        try:
            CHUNK_SIZE = 8 * 1024
            iterator = AppClient.MemoryReadIterator(self.GetAppName(), data, targetFile, CHUNK_SIZE)
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
            raise RuntimeError("not connected")
        
        with open(targetFile, "w") as file:
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
            raise RuntimeError("not connected")
        
        request = robotcontrolapp_pb2.DownloadFileRequest()
        request.app_name = self.GetAppName()
        request.filename = sourceFile
        resultData = bytearray()
        try:
            for chunk in self.__grpcStub.DownloadFile(request):
                if chunk.success:
                    resultData.append(chunk.data)
                else:
                    return (False, chunk.error, resultData)
            return (True, "", resultData)
        except Exception as ex:
            return (False, ex)

    class DirectoryContent:
        """Description of a directory's content"""
        def __init__(self):
            self.success = False
            self.errorMessage = ""
            self.entries = list[robotcontrolapp_pb2.ListFilesResponse.DirectoryEntry]

        def FromGrcp(grpc: robotcontrolapp_pb2.ListFilesResponse):
            """
            Creates an object from a GRPC ListFilesResponse
            Returns:
                A new DirectoryContent object
            """
            self = AppClient.DirectoryContent()
            self.success = grpc.success
            self.errorMessage = grpc.error
            for entry in grpc.entries:
                self.entries.append(entry)
            return self

    def ListFiles(self, directory: str) -> DirectoryContent:
        """Gets the content of a directory"""
        if not self.IsConnected():
            raise RuntimeError("not connected")
        
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
            if(self.__queuedUIUpdates.ui_changes.count() > 0):
                self.SendAction(self.__queuedUIUpdates)
                self.__queuedUIUpdates.Clear()

    def RequestUIElementState(self, elementName: str):
        """Requests the state of a UI element. The robot control will respond with a call of UiUpdateHandler() if the element exists and if it was changed after"""
        request = robotcontrolapp_pb2.AppAction()
        request.request_ui_state.append(elementName)
        self.SendAction(request)

    def RequestUIElementStates(self, elementNames: set[str]):
        """Requests the state of several UI elements. The robot control will respond with a call of UiUpdateHandler() if the element exists and if it was changed"""
        request = robotcontrolapp_pb2.AppAction()
        for elementName in elementNames:
            request.request_ui_state.append(elementName)
        self.SendAction(request)

    # Sets a UI element visible or hidden
    def SetUIVisibility(self, elementName: str, visible: bool):
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

    def SetUIVisibility(self, elements: set[tuple[str, bool]]):
        """Set a list of UI element visible or hidden"""
        request = robotcontrolapp_pb2.AppAction()
        for element in elements:
            uiElement = request.ui_changes.add()
            uiElement.element_name = element[0]
            uiElement.is_visible = element[1]
        self.SendAction(request)

    def QueueSetUIVisibility(self, elements: set[tuple[str, bool]]):
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
        for entry in selectableEntries:
            uiElement.state.dropdown_state.options.append(entry)
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
            for entry in selectableEntries:
                uiElement.state.dropdown_state.options.append(entry)

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
        """Sets the image of an image element in the UI"""
        request = robotcontrolapp_pb2.AppAction()
        uiElement = request.ui_changes.add()
        uiElement.element_name = elementName
        uiElement.state.image_state.image_data.height = uiHeight
        uiElement.state.image_state.image_data.width = uiWidth
        uiElement.state.image_state.image_data.encoding = encoding
        uiElement.state.image_state.image_data.data = imageData
        self.SendAction(request)

    def QueueSetImage(
        self,
        elementName: str,
        uiWidth: int,
        uiHeight: int,
        imageData: bytearray,
        encoding: robotcontrolapp_pb2.ImageState.ImageData.ImageEncoding,
    ):
        """Queues setting the image of an image element in the UI"""
        with self.__queuedUIUpdatesMutex:
            uiElement = self.__queuedUIUpdates.ui_changes.add()
            uiElement.element_name = elementName
            uiElement.state.image_state.image_data.height = uiHeight
            uiElement.state.image_state.image_data.width = uiWidth
            uiElement.state.image_state.image_data.encoding = encoding
            uiElement.state.image_state.image_data.data = imageData

    def _AppFunctionHandler(self, function: robotcontrolapp_pb2.AppFunction):
        """
        Gets called on remote app function calls received from the robot control.
        Override this in your app!
        """
        raise NotImplementedError()

    def _UiUpdateHandler(self, updates: protobufContainers.RepeatedCompositeFieldContainer[robotcontrolapp_pb2.AppUIElement]):
        """
        Gets called on remote UI update requests received from the robot control.
        Override this in your app!
        """
        raise NotImplementedError()
