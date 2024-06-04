from queue import Queue
import sys
from threading import Thread
import threading
from typing import List
import grpc
from DataTypes.Matrix44 import Matrix44
from DataTypes.ProgramVariable import NumberVariable, PositionVariable, ProgramVariable
import robotcontrolapp_pb2
from robotcontrolapp_pb2_grpc import RobotControlAppStub


class AppClient:
    # Constructor, arguments are the name of the app and the target socket
    def __init__(self, appName: str, target: str):
        self.__appName = appName
        self.__targetSocket = target
        self.__grpcChannel = grpc.insecure_channel(self.__targetSocket)
        self.__grpcStub = RobotControlAppStub(self.__grpcChannel)
        self.__stopThreads = True

    def __enter__(self):
        self.Connect()

    def __exit__(self):
        self.Disconnect()

    # Gets the name of the app
    def GetAppName(self) -> str:
        return self.__appName

    # Connects the app
    def Connect(self):
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

    # Disconnects the app
    def Disconnect(self):
        if self.IsConnected():
            print(f"Disconnecting app '{self.GetAppName()}'")
            self.__stopThreads = True
            self.__grpcChannel.close()
            if threading.current_thread != self.__eventReaderThread:
                self.__eventReaderThread.join()

    # Gets the connection state
    def IsConnected(self) -> bool:
        return not self.__stopThreads

    # Queues an action to be sent to the robot control
    def SendAction(self, action: robotcontrolapp_pb2.AppAction):
        action.app_name = self.GetAppName()
        self.__actionsQueue.put(action)

    # This thread handles reading the received actions
    def EventReaderThread(self):
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

    # Gets the tool center point position and orientation
    def GetTcp(self) -> Matrix44:
        if not self.IsConnected():
            raise RuntimeError("not connected")

        request = robotcontrolapp_pb2.GetTCPRequest()
        request.app_name = self.GetAppName()
        response = self.__grpcStub.GetTCP(request)
        return Matrix44.FromGrpc(response)

    # Gets the program variable, throws exception on error, e.g. if the variable does not exist
    def GetProgramVariable(self, variableName: str) -> ProgramVariable:
        if len(variableName) == 0:
            raise RuntimeError("requested variable with empty name")

        names = {variableName}
        result = self.GetProgramVariables(names)
        if len(result) == 0:
            raise RuntimeError(
                f"failed to get variable '{variableName}': variable does not exist"
            )
        return result.pop()

    # Gets the given number variable, throws on error, e.g. if the variable does not exist or is of a different type
    def GetNumberVariable(self, variableName: str) -> NumberVariable:
        variable = self.GetProgramVariable(variableName)
        if not isinstance(variable, NumberVariable):
            raise RuntimeError(
                "requested variable '" + variableName + "' is no number variable"
            )
        return variable

    # Gets the given position variable, throws on error, e.g. if the variable does not exist or is of a different type
    def GetPositionVariable(self, variableName: str) -> PositionVariable:
        variable = self.GetProgramVariable(variableName)
        if not isinstance(variable, PositionVariable):
            raise RuntimeError(
                "requested variable '" + variableName + "' is no position variable"
            )
        return variable

    # Gets program variables
    def GetProgramVariables(self, variableNames: set[str]) -> set[ProgramVariable]:
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

    # Sets a number variable
    def SetNumberVariable(self, name: str, value: float):
        if not self.IsConnected():
            raise RuntimeError("not connected")

        request = robotcontrolapp_pb2.SetProgramVariablesRequest()
        request.app_name = self.GetAppName()
        variable = request.variables.add()
        variable.name = name
        variable.number = value
        self.__grpcStub.SetProgramVariables(request)

    # Sets a position variable with joint angles. The robot control will try to convert these to cartesian.
    def SetPositionVariable(
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

    # Sets a position variable with a cartesian position. The robot control will try to convert this to joint angles
    def SetPositionVariable(
        self, name: str, cartesianPosition: Matrix44, e1: float, e2: float, e3: float
    ):
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

    # Sets a position variable with joint angles and cartesian position. Warning: joint angles and cartesian may refer to different positions!
    def SetPositionVariable(
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

    # Announces to the robot control that the app function call finished. This allows the robot program to continue with the next command.
    def SendFunctionDone(self, callId: int):
        response = robotcontrolapp_pb2.AppAction()
        response.done_functions.append(callId)
        self.SendAction(response)

    # Announces to the robot control that the app function call failed. This will abort the program with an error message.
    # This is supported from V14-003
    def SendFunctionFailed(self, callId: int, reason: str):
        response = robotcontrolapp_pb2.AppAction()
        failedFunction = robotcontrolapp_pb2.FailedFunction()
        failedFunction.call_id = callId
        failedFunction.reason = reason
        response.failed_functions.append(failedFunction)
        self.SendAction(response)

    # Requests the state of a UI element. The robot control will respond with a call of UiUpdateHandler() if the element exists and if it was changed after
    def RequestUIElementState(self, elementName: str):
        request = robotcontrolapp_pb2.AppAction()
        request.request_ui_state.append(elementName)
        self.SendAction(request)

    # Requests the state of several UI elements. The robot control will respond with a call of UiUpdateHandler() if the element exists and if it was changed
    def RequestUIElementStates(self, elementNames: set[str]):
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

    # Set a list of UI element visible or hidden
    def SetUIVisibility(self, elements: set[tuple[str, bool]]):
        request = robotcontrolapp_pb2.AppAction()
        for element in elements:
            uiElement = request.ui_changes.add()
            uiElement.element_name = element[0]
            uiElement.is_visible = element[1]
        self.SendAction(request)

    # Sets the checked state of a checkbox
    def SetCheckboxState(self, elementName: str, isChecked: bool):
        request = robotcontrolapp_pb2.AppAction()
        uiElement = request.ui_changes.add()
        uiElement.element_name = elementName
        if isChecked:
            uiElement.state.checkbox_state = robotcontrolapp_pb2.CHECKED
        else:
            uiElement.state.checkbox_state = robotcontrolapp_pb2.UNCHECKED
        self.SendAction(request)

    # Sets the selected value of a drop down box
    def SetDropDownState(self, elementName: str, selectedValue: str):
        request = robotcontrolapp_pb2.AppAction()
        uiElement = request.ui_changes.add()
        uiElement.element_name = elementName
        uiElement.state.dropdown_state.selected_option = selectedValue
        self.SendAction(request)

    # Sets the selected value and the list of selectable values of a drop down box
    def SetDropDownState(
        self, elementName: str, selectedValue: str, selectableEntries: List[str]
    ):
        request = robotcontrolapp_pb2.AppAction()
        uiElement = request.ui_changes.add()
        uiElement.element_name = elementName
        uiElement.state.dropdown_state.selected_option = selectedValue
        for entry in selectableEntries:
            uiElement.state.dropdown_state.options.append(entry)
        self.SendAction(request)

    # Sets the text of a text box, label, etc.
    def SetText(self, elementName: str, value: str):
        request = robotcontrolapp_pb2.AppAction()
        uiElement = request.ui_changes.add()
        uiElement.element_name = elementName
        uiElement.state.textfield_state.current_text = value
        self.SendAction(request)

    # Sets the number value of a number box, text box, label, etc.
    def SetNumber(self, elementName: str, value: float):
        request = robotcontrolapp_pb2.AppAction()
        uiElement = request.ui_changes.add()
        uiElement.element_name = elementName
        uiElement.state.numberfield_state.current_number = value
        self.SendAction(request)

    # Sets the image of an image element in the UI
    def SetImage(
        self,
        elementName: str,
        uiWidth: int,
        uiHeight: int,
        imageData: bytearray,
        encoding: robotcontrolapp_pb2.ImageState.ImageData.ImageEncoding,
    ):
        request = robotcontrolapp_pb2.AppAction()
        uiElement = request.ui_changes.add()
        uiElement.element_name = elementName
        uiElement.state.image_state.image_data.height = uiHeight
        uiElement.state.image_state.image_data.width = uiWidth
        uiElement.state.image_state.image_data.encoding = encoding
        uiElement.state.image_state.image_data.data = imageData
        self.SendAction(request)

    # Gets called on remote app function calls received from the robot control
    def _AppFunctionHandler(self, function: robotcontrolapp_pb2.AppFunction):
        raise NotImplementedError()  # derive this method in your app!

    # Gets called on remote UI update requests received from the robot control
    def _UiUpdateHandler(self, updates):
        raise NotImplementedError()  # derive this method in your app!
