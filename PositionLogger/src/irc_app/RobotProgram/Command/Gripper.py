from irc_app.rpc import robotcontrolapp_pb2
from src.irc_app.RobotProgram.Command.Command import ICommand


class Gripper(ICommand):
    """Sets the gripper state"""

    def __init__(self):
        self.data = robotcontrolapp_pb2.CmdGripperParameters()
        self.data.target_states.append(0)

    def GetCmdParameters(self) -> robotcontrolapp_pb2.AddCommandRequest.CmdParameters:
        ret = robotcontrolapp_pb2.AddCommandRequest.CmdParameters()
        ret.gripper.CopyFrom(self.data)
        return ret

    def GetTargetState(self) -> float:
        """Gets the target state of the gripper"""
        return self.data.target_states[0]

    def SetTargetState(self, state: float):
        """Sets the target state of the gripper"""
        self.data.target_states[0] = state
