from irc_app.rpc import robotcontrolapp_pb2
from src.irc_app.RobotProgram.Command.Command import ICommand


class SubProgram(ICommand):
    """Calls a sub program from a program file"""

    def __init__(self):
        self.data = robotcontrolapp_pb2.CmdSubprogramParameters()

    def GetCmdParameters(self) -> robotcontrolapp_pb2.AddCommandRequest.CmdParameters:
        ret = robotcontrolapp_pb2.AddCommandRequest.CmdParameters()
        ret.subprogram.CopyFrom(self.data)
        return ret

    def GetProgram(self) -> str:
        """
        Gets the program file name
        Returns:
            program file name, relative to the Data/Programs directory
        """
        return self.data.program_name

    def SetProgram(self, programFile: str):
        """
        Sets the program file name
        Parameters:
            programFile: sub program file name, relative to the Data/Programs directory
        """
        self.data.program_name = programFile
