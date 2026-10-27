import unittest

from src.irc_app.RobotProgram.Command.CopyUserFrame import CopyUserFrame


class CopyUserFrameTest(unittest.TestCase):
    def test_constructor(self):
        cmd = CopyUserFrame()
        self.assertEqual("", cmd.GetFrom())
        self.assertEqual("", cmd.data.from_frame)
        self.assertEqual("", cmd.GetTo())
        self.assertEqual("", cmd.data.to_frame)

    def test_GetCmdParameters(self):
        cmd = CopyUserFrame()
        cmd.SetFrom("Foo")
        cmd.SetTo("Bar")

        param = cmd.GetCmdParameters()

        self.assertEqual("Foo", param.copy_user_frame.from_frame)
        self.assertEqual("Bar", param.copy_user_frame.to_frame)

    def test_SetFrom(self):
        cmd = CopyUserFrame()
        cmd.SetFrom("Foo")

        self.assertEqual("Foo", cmd.GetFrom())
        self.assertEqual("Foo", cmd.data.from_frame)
        self.assertEqual("", cmd.GetTo())
        self.assertEqual("", cmd.data.to_frame)

    def test_SetTo(self):
        cmd = CopyUserFrame()
        cmd.SetTo("Bar")

        self.assertEqual("", cmd.GetFrom())
        self.assertEqual("", cmd.data.from_frame)
        self.assertEqual("Bar", cmd.GetTo())
        self.assertEqual("Bar", cmd.data.to_frame)
