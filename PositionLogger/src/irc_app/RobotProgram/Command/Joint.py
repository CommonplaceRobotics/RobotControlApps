from irc_app.rpc import robotcontrolapp_pb2
from src.irc_app.RobotProgram.Command.Command import ICommand


class Joint(ICommand):
    """A joint motion command"""

    def __init__(self):
        self.data = robotcontrolapp_pb2.CmdJointParameters()
        for i in range(9):
            self.data.target_pos.append(0)
        self.SetVelocity(40)
        self.SetAcceleration(40)
        self.SetSmooting(0)
        self.SetAbortCondition("false")

    def GetCmdParameters(self) -> robotcontrolapp_pb2.AddCommandRequest.CmdParameters:
        ret = robotcontrolapp_pb2.AddCommandRequest.CmdParameters()
        ret.joint.CopyFrom(self.data)
        return ret

    def IsPositionFromVariable(self) -> bool:
        """Returns true if the position is read from a variable"""
        return self.data.HasField("target_pos_variable")

    def IsPositionConstant(self) -> bool:
        """Returns true if the constant position values are used"""
        return not self.IsPositionFromVariable()

    def GetVariable(self) -> str:
        """
        Gets the position variable name
        Returns:
            name of the position variable
        """
        if self.data.HasField("target_pos_variable"):
            return self.data.target_pos_variable
        else:
            return ""

    def SetVariable(self, variable: str):
        """
        Sets the position variable name
        Parameters:
            variable: name of the position variable
        """
        self.data.target_pos_variable = variable

    def GetA1(self) -> float:
        """
        Gets the target position for A1
        Returns:
            position in mm or degrees
        """
        return self.data.target_pos[0]

    def SetA1(self, pos: float):
        """
        Sets the target position for A1
        Parameters:
            pos: position in mm or degrees
        """
        self.data.target_pos[0] = pos
        self.data.ClearField("target_pos_variable")

    def GetA2(self) -> float:
        """
        Gets the target position for A2
        Returns:
            position in mm or degrees
        """
        return self.data.target_pos[1]

    def SetA2(self, pos: float):
        """
        Sets the target position for A2
        Parameters:
            pos: position in mm or degrees
        """
        self.data.target_pos[1] = pos
        self.data.ClearField("target_pos_variable")

    def GetA3(self) -> float:
        """
        Gets the target position for A3
        Returns:
            position in mm or degrees
        """
        return self.data.target_pos[2]

    def SetA3(self, pos: float):
        """
        Sets the target position for A3
        Parameters:
            pos: position in mm or degrees
        """
        self.data.target_pos[2] = pos
        self.data.ClearField("target_pos_variable")

    def GetA4(self) -> float:
        """
        Gets the target position for A4
        Returns:
            position in mm or degrees
        """
        return self.data.target_pos[3]

    def SetA4(self, pos: float):
        """
        Sets the target position for A4
        Parameters:
            pos: position in mm or degrees
        """
        self.data.target_pos[3] = pos
        self.data.ClearField("target_pos_variable")

    def GetA5(self) -> float:
        """
        Gets the target position for A5
        Returns:
            position in mm or degrees
        """
        return self.data.target_pos[4]

    def SetA5(self, pos: float):
        """
        Sets the target position for A5
        Parameters:
            pos: position in mm or degrees
        """
        self.data.target_pos[4] = pos
        self.data.ClearField("target_pos_variable")

    def GetA6(self) -> float:
        """
        Gets the target position for A6
        Returns:
            position in mm or degrees
        """
        return self.data.target_pos[5]

    def SetA6(self, pos: float):
        """
        Sets the target position for A6
        Parameters:
            pos: position in mm or degrees
        """
        self.data.target_pos[5] = pos
        self.data.ClearField("target_pos_variable")

    def GetE1(self) -> float:
        """
        Gets the target position for E1
        Returns:
            position in mm or degrees
        """
        return self.data.target_pos[6]

    def SetE1(self, pos: float):
        """
        Sets the target position for E1
        Parameters:
            pos: position in mm or degrees
        """
        self.data.target_pos[6] = pos
        self.data.ClearField("target_pos_variable")

    def GetE2(self) -> float:
        """
        Gets the target position for E2
        Returns:
            position in mm or degrees
        """
        return self.data.target_pos[7]

    def SetE2(self, pos: float):
        """
        Sets the target position for E2
        Parameters:
            pos: position in mm or degrees
        """
        self.data.target_pos[7] = pos
        self.data.ClearField("target_pos_variable")

    def GetE3(self) -> float:
        """
        Gets the target position for E3
        Returns:
            position in mm or degrees
        """
        return self.data.target_pos[8]

    def SetE3(self, pos: float):
        """
        Sets the target position for E3
        Parameters:
            pos: position in mm or degrees
        """
        self.data.target_pos[8] = pos
        self.data.ClearField("target_pos_variable")

    def GetVelocity(self) -> float:
        """Gets the velocity in percent (0..100)"""
        return self.data.velocity_percent

    def SetVelocity(self, vel: float):
        """Sets the velocity in percent (0..100)"""
        self.data.velocity_percent = vel

    def GetAcceleration(self) -> float:
        """Gets the acceleration in percent (0..100)"""
        return self.data.acceleration_percent

    def SetAcceleration(self, acc: float):
        """Sets the acceleration in percent (0..100)"""
        self.data.acceleration_percent = acc

    def GetSmoothing(self) -> float:
        """Gets the smoothing in percent (0..100)"""
        return self.data.smoothing_percent

    def SetSmooting(self, smooth: float):
        """Sets the smoothing in percent (0..100)"""
        self.data.smoothing_percent = smooth

    def GetAbortCondition(self) -> str:
        """Gets the abort condition"""
        return self.data.abort_condition

    def SetAbortCondition(self, condition: str):
        """
        Sets the abort condition
        Parameters:
            condition: abort condition, if true the motion is aborted
        """
        self.data.abort_condition = condition
