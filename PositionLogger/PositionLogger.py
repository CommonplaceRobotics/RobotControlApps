import os
from AppClient import AppClient
from DataTypes.Matrix44 import Matrix44
from robotcontrolapp_pb2 import AppFunction, AppUIElement
from google.protobuf.internal import containers as protobufContainers


class PositionLogger(AppClient):
    """This is an example app implementation"""

    logFile = "positionlog.csv"

    def __init__(self, appName: str, target: str):
        """Initializes the app. Pass the app name (as defined in rcapp.xml) and socket to connect to (default: "localhost:5000")"""
        AppClient.__init__(self, appName, target)

    def _AppFunctionHandler(self, function: AppFunction):
        """Gets called on remote app function calls received from the robot control"""
        # This prints the received function data
        # print("Received app function:")
        # print(function)

        # Select the app function to call
        try:
            if function.name == "clear":
                self.ClearLog(function)
            elif function.name == "add_tcp":
                self.AddTCPToLog(function)
            elif function.name == "add_variable":
                self.AddPosVarToLog(function)
            else:
                self.SendFunctionFailed(function.call_id, "unknown app function")
        except Exception as ex:
            self.SendFunctionFailed(function.call_id, ex)

    def _UiUpdateHandler(
        self, updates: protobufContainers.RepeatedCompositeFieldContainer[AppUIElement]
    ):
        """Gets called on remote UI update requests received from the robot control"""
        return

    def ClearLog(self, function):
        """Deletes the log file"""
        if os.path.isfile(self.logFile):
            os.remove(self.logFile)
        self.SendFunctionDone(function.call_id)

    def AddToLog(self, position: Matrix44):
        """Opens a CSV file (creates it if necessary) and and adds the given position"""

        with open(self.logFile, "a") as f:
            f.write(
                "{0:f};{1:f};{2:f};{3:f};{4:f};{5:f}\n".format(
                    position.GetX(),
                    position.GetY(),
                    position.GetZ(),
                    position.GetA(),
                    position.GetB(),
                    position.GetC(),
                )
            )

    def AddTCPToLog(self, function):
        """Adds the current TCP position to the CSV log"""
        self.AddToLog(self.GetTCP())
        self.SendFunctionDone(function.call_id)

    def AddPosVarToLog(self, function):
        """Adds a position from a variable to the CSV log"""
        for parameter in function.parameters:
            if parameter.name == "varname" and parameter.HasField("string_value"):
                varName = parameter.string_value

        try:
            posVar = self.GetPositionVariable(varName)
            self.AddToLog(posVar.GetCartesian())
        except RuntimeError as ex:
            self.SendFunctionFailed(function.call_id, ex)
            return

        self.SendFunctionDone(function.call_id)
