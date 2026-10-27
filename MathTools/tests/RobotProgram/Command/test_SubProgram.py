import unittest

from src.irc_app.RobotProgram.Command.SubProgram import SubProgram


class SetVelocityTest(unittest.TestCase):
    def test_constructor(self):
        cmd = SubProgram()
        self.assertEqual("", cmd.GetProgram())

    def test_GetCmdParameters(self):
        cmd = SubProgram()
        cmd.SetProgram("Foo")
        param = cmd.GetCmdParameters()
        self.assertEqual("Foo", param.subprogram.program_name)

    def test_SetProgram(self):
        cmd = SubProgram()
        cmd.SetProgram("Bar")
        self.assertEqual("Bar", cmd.GetProgram())
