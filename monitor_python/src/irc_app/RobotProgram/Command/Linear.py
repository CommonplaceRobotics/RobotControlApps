from irc_app.rpc import robotcontrolapp_pb2
from src.irc_app.RobotProgram.Command.Command import ICommand


class Linear(ICommand):
    """A linear motion command"""

    def __init__(self):
        self.data = robotcontrolapp_pb2.CmdLinearParameters()
        for i in range(3):
            self.data.target_pos_ext_joints.append(0)
        self.SetVelocity(100)
        self.SetAcceleration(40)
        self.SetSmooting(0)
        self.SetAbortCondition("false")

    def GetCmdParameters(self) -> robotcontrolapp_pb2.AddCommandRequest.CmdParameters:
        ret = robotcontrolapp_pb2.AddCommandRequest.CmdParameters()
        ret.linear.CopyFrom(self.data)
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

    def GetX(self) -> float:
        """
        Gets the target X position
        Returns:
            position in mm
        """
        return self.data.target_x

    def SetX(self, pos: float):
        """
        Sets the target X position
        Parameters:
            pos: position in mm
        """
        self.data.target_x = pos
        self.data.ClearField("target_pos_variable")

    def GetY(self) -> float:
        """
        Gets the target Y position
        Returns:
            position in mm
        """
        return self.data.target_y

    def SetY(self, pos: float):
        """
        Sets the target Y position
        Parameters:
            pos: position in mm
        """
        self.data.target_y = pos
        self.data.ClearField("target_pos_variable")

    def GetZ(self) -> float:
        """
        Gets the target Z position
        Returns:
            position in mm
        """
        return self.data.target_z

    def SetZ(self, pos: float):
        """
        Sets the target Z position
        Parameters:
            pos: position in mm
        """
        self.data.target_z = pos
        self.data.ClearField("target_pos_variable")

    def GetA(self) -> float:
        """
        Gets the target A orientation
        Returns:
            orientation in degrees
        """
        return self.data.target_a

    def SetA(self, ori: float):
        """
        Sets the target A orientation
        Parameters:
            ori: orientation in degrees
        """
        self.data.target_a = ori
        self.data.ClearField("target_pos_variable")

    def GetB(self) -> float:
        """
        Gets the target B orientation
        Returns:
            orientation in degrees
        """
        return self.data.target_b

    def SetB(self, ori: float):
        """
        Sets the target B orientation
        Parameters:
            ori: orientation in degrees
        """
        self.data.target_b = ori
        self.data.ClearField("target_pos_variable")

    def GetC(self) -> float:
        """
        Gets the target C orientation
        Returns:
            orientation in degrees
        """
        return self.data.target_c

    def SetC(self, ori: float):
        """
        Sets the target C orientation
        Parameters:
            ori: orientation in degrees
        """
        self.data.target_c = ori
        self.data.ClearField("target_pos_variable")

    def GetE1(self) -> float:
        """
        Gets the target position for E1
        Returns:
            position in mm or degrees
        """
        return self.data.target_pos_ext_joints[0]

    def SetE1(self, pos: float):
        """
        Sets the target position for E1
        Parameters:
            pos: position in mm or degrees
        """
        self.data.target_pos_ext_joints[0] = pos
        self.data.ClearField("target_pos_variable")

    def GetE2(self) -> float:
        """
        Gets the target position for E2
        Returns:
            position in mm or degrees
        """
        return self.data.target_pos_ext_joints[1]

    def SetE2(self, pos: float):
        """
        Sets the target position for E2
        Parameters:
            pos: position in mm or degrees
        """
        self.data.target_pos_ext_joints[1] = pos
        self.data.ClearField("target_pos_variable")

    def GetE3(self) -> float:
        """
        Gets the target position for E3
        Returns:
            position in mm or degrees
        """
        return self.data.target_pos_ext_joints[2]

    def SetE3(self, pos: float):
        """
        Sets the target position for E3
        Parameters:
            pos: position in mm or degrees
        """
        self.data.target_pos_ext_joints[2] = pos
        self.data.ClearField("target_pos_variable")

    def GetVelocity(self) -> float:
        """Gets the velocity in mm/s"""
        return self.data.velocity_mms

    def SetVelocity(self, vel: float):
        """Sets the velocity in mm/s"""
        self.data.velocity_mms = vel

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

    def GetReferenceFrame(self) -> str:
        """Gets the reference frame"""
        if self.data.HasField("reference_frame"):
            return self.data.reference_frame
        else:
            return "#base"

    def SetReferenceFrame(self, frame: str):
        """Sets the reference frame"""
        self.data.reference_frame = frame
