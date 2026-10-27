import unittest

from src.irc_app.RobotProgram.Command.Wait import Wait


class WaitTest(unittest.TestCase):
    def test_constructor(self):
        cmd = Wait()
        self.assertFalse(cmd.IsCondition())
        self.assertFalse(cmd.IsDuration())
        self.assertEqual("", cmd.GetCondition())
        self.assertEqual(0, cmd.GetDuration())

    def test_GetCmdParameters_Condition(self):
        cmd = Wait()
        cmd.SetCondition("Foo")
        param = cmd.GetCmdParameters()
        self.assertEqual("Foo", param.wait.condition)

    def test_GetCmdParameters_Duration(self):
        cmd = Wait()
        cmd.SetDuration(123)
        param = cmd.GetCmdParameters()
        self.assertEqual(123 * 1000, param.wait.duration)

    def test_SetDuration_SetCondition(self):
        cmd = Wait()
        cmd.SetDuration(42)
        self.assertTrue(cmd.IsDuration())
        self.assertFalse(cmd.IsCondition())
        self.assertEqual(42, cmd.GetDuration())
        self.assertEqual("", cmd.GetCondition())

        cmd.SetCondition("DIn22")
        self.assertFalse(cmd.IsDuration())
        self.assertTrue(cmd.IsCondition())
        self.assertEqual(0, cmd.GetDuration())
        self.assertEqual("DIn22", cmd.GetCondition())

        cmd.SetDuration(142)
        self.assertTrue(cmd.IsDuration())
        self.assertFalse(cmd.IsCondition())
        self.assertEqual(142, cmd.GetDuration())
        self.assertEqual("", cmd.GetCondition())
