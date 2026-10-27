from irc_app.rpc import robotcontrolapp_pb2
from src.irc_app.RobotProgram.Command.Command import ICommand


class CopyUserFrame(ICommand):
    """Copies a user frame into another"""

    def __init__(self):
        self.data = robotcontrolapp_pb2.CmdCopyUserFrameParameters()

    def GetCmdParameters(self) -> robotcontrolapp_pb2.AddCommandRequest.CmdParameters:
        ret = robotcontrolapp_pb2.AddCommandRequest.CmdParameters()
        ret.copy_user_frame.CopyFrom(self.data)
        return ret

    def GetFrom(self) -> str:
        """Gets the user frame to copy from"""
        return self.data.from_frame

    def GetTo(self) -> str:
        """Gets the user frame to copy to"""
        return self.data.to_frame

    def SetFrom(self, from_frame: str):
        """Sets the user frame to copy from"""
        self.data.from_frame = from_frame

    def SetTo(self, to_frame: str):
        """Sets the user frame to copy to"""
        self.data.to_frame = to_frame
