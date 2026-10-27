from irc_app.rpc import robotcontrolapp_pb2
from src.irc_app.RobotProgram.Command.Command import ICommand


class SetVelocity(ICommand):
    """Sets the velocity of external axes in velocity mode (e.g. conveyor)"""

    def __init__(self):
        self.data = robotcontrolapp_pb2.CmdSetVelocityParameters()

    def GetCmdParameters(self) -> robotcontrolapp_pb2.AddCommandRequest.CmdParameters:
        ret = robotcontrolapp_pb2.AddCommandRequest.CmdParameters()
        ret.set_velocity.CopyFrom(self.data)
        return ret

    def GetE1(self) -> float:
        """
        Gets the velocity for E1
        Returns:
            velocity in user-defined units
        """
        return self.data.velocity_e1

    def GetE2(self) -> float:
        """
        Gets the velocity for E2
        Returns:
            velocity in user-defined units
        """
        return self.data.velocity_e2

    def GetE3(self) -> float:
        """
        Gets the velocity for E3
        Returns:
            velocity in user-defined units
        """
        return self.data.velocity_e3

    def SetE1(self, velocity: float):
        """
        Sets the velocity for E1
        Returns:
            velocity in user-defined units
        """
        self.data.velocity_e1 = velocity

    def SetE2(self, velocity: float):
        """
        Sets the velocity for E2
        Returns:
            velocity in user-defined units
        """
        self.data.velocity_e2 = velocity

    def SetE3(self, velocity: float):
        """
        Sets the velocity for E3
        Returns:
            velocity in user-defined units
        """
        self.data.velocity_e3 = velocity
