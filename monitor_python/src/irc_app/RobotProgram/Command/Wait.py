from irc_app.rpc import robotcontrolapp_pb2
from src.irc_app.RobotProgram.Command.Command import ICommand


class Wait(ICommand):
    """Waits by a delay or condition"""

    def __init__(self):
        self.data = robotcontrolapp_pb2.CmdWaitParameters()

    def GetCmdParameters(self) -> robotcontrolapp_pb2.AddCommandRequest.CmdParameters:
        ret = robotcontrolapp_pb2.AddCommandRequest.CmdParameters()
        ret.wait.CopyFrom(self.data)
        return ret

    def IsDuration(self) -> bool:
        """Is this a wait by duration?"""
        return self.data.HasField("duration")

    def IsCondition(self) -> bool:
        """Is this a wait by condition?"""
        return self.data.HasField("condition")

    def GetDuration(self) -> float:
        """
        Gets the wait duration
        Returns:
            duration in seconds
        """
        return self.data.duration / 1000.0

    def SetDuration(self, duration: float):
        """
        Sets the wait duration
        Parameters:
            duration: duration in seconds
        """
        self.data.duration = duration * 1000.0

    def GetCondition(self) -> str:
        """Gets the wait condition"""
        return self.data.condition

    def SetCondition(self, condition: str):
        """
        Sets the wait condition
        Parameters:
            condition: wait condition. Once it evaluates TRUE the command finishes.
        """
        self.data.condition = condition
