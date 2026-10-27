from irc_app.rpc import robotcontrolapp_pb2
from src.irc_app.RobotProgram.Command.Command import ICommand


class ProgramControl(ICommand):
    """Controls the motion program (stop/pause)"""

    def __init__(self):
        self.data = robotcontrolapp_pb2.CmdProgramControlParameters()

    def GetCmdParameters(self) -> robotcontrolapp_pb2.AddCommandRequest.CmdParameters:
        ret = robotcontrolapp_pb2.AddCommandRequest.CmdParameters()
        ret.program_control.CopyFrom(self.data)
        return ret


class Stop(ProgramControl):
    """Stops the motion program"""

    def __init__(self):
        super().__init__()
        self.data.type = robotcontrolapp_pb2.CmdProgramControlParameters.Stop


class Pause(ProgramControl):
    """Pauses the motion program"""

    def __init__(self):
        super().__init__()
        self.data.type = robotcontrolapp_pb2.CmdProgramControlParameters.Pause
