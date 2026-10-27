from irc_app.rpc import robotcontrolapp_pb2
from src.irc_app.RobotProgram.Command.Command import ICommand


class SetGlobalSignal(ICommand):
    """Sets a global signal"""

    def __init__(self):
        self.data = robotcontrolapp_pb2.CmdSetGlobalSignalParameters()

    def GetCmdParameters(self) -> robotcontrolapp_pb2.AddCommandRequest.CmdParameters:
        ret = robotcontrolapp_pb2.AddCommandRequest.CmdParameters()
        ret.set_global_signal.CopyFrom(self.data)
        return ret

    def GetID(self) -> int:
        """
        Gets the global signal ID
        Returns:
            ID with index base 0 (i.e. index 0 refers to GSig1). Range 0..99
        """
        return self.data.output_number

    def SetID(self, id: int):
        """
        Sets the global signal ID
        Parameters:
            id: Global signal ID with index base 0 (i.e. index 0 refers to GSig1). Range 0..99
        """
        self.data.output_number = id

    def GetState(self) -> bool:
        """Gets the target state"""
        return self.data.target_state

    def SetState(self, state: bool):
        """Sets the target state"""
        self.data.target_state = state
