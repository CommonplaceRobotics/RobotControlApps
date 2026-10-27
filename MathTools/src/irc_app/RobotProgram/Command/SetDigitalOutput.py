from irc_app.rpc import robotcontrolapp_pb2
from src.irc_app.RobotProgram.Command.Command import ICommand


class SetDigitalOutput(ICommand):
    """Sets a digital output"""

    def __init__(self):
        self.data = robotcontrolapp_pb2.CmdSetDigitalOutParameters()

    def GetCmdParameters(self) -> robotcontrolapp_pb2.AddCommandRequest.CmdParameters:
        ret = robotcontrolapp_pb2.AddCommandRequest.CmdParameters()
        ret.set_digital_out.CopyFrom(self.data)
        return ret

    def GetID(self) -> int:
        """
        Gets the digital output ID
        Returns:
            ID with index base 0 (i.e. index 0 refers to DOut1). Range 0..63
        """
        return self.data.output_number

    def SetID(self, id: int):
        """
        Sets the digital output ID
        Parameters:
            id: Digital output ID with index base 0 (i.e. index 0 refers to DOut1). Range 0..63
        """
        self.data.output_number = id

    def GetState(self) -> bool:
        """Gets the target state"""
        return self.data.target_state

    def SetState(self, state: bool):
        """Sets the target state"""
        self.data.target_state = state
