import unittest

from src.irc_app.RobotProgram.Command.ProgramControl import ProgramControl, Stop, Pause
from src.irc_app.rpc import robotcontrolapp_pb2


class ProgramControlTest(unittest.TestCase):
    def test_constructor(self):
        cmd = ProgramControl()
        self.assertEqual(
            robotcontrolapp_pb2.CmdProgramControlParameters.Pause, cmd.data.type
        )

    def test_GetCmdParameters(self):
        cmd = ProgramControl()
        param = cmd.GetCmdParameters()
        self.assertEqual(
            robotcontrolapp_pb2.CmdProgramControlParameters.Pause,
            param.program_control.type,
        )


class StopTest(unittest.TestCase):
    def test_constructor(self):
        cmd = Stop()
        self.assertEqual(
            robotcontrolapp_pb2.CmdProgramControlParameters.Stop, cmd.data.type
        )

    def test_GetCmdParameters(self):
        cmd = Stop()
        param = cmd.GetCmdParameters()
        self.assertEqual(
            robotcontrolapp_pb2.CmdProgramControlParameters.Stop,
            param.program_control.type,
        )


class PauseTest(unittest.TestCase):
    def test_constructor(self):
        cmd = Pause()
        self.assertEqual(
            robotcontrolapp_pb2.CmdProgramControlParameters.Pause, cmd.data.type
        )

    def test_GetCmdParameters(self):
        cmd = Pause()
        param = cmd.GetCmdParameters()
        self.assertEqual(
            robotcontrolapp_pb2.CmdProgramControlParameters.Pause,
            param.program_control.type,
        )
