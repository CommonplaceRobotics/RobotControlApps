import unittest

from src.irc_app.RobotProgram.Command.Gripper import Gripper


class GripperTest(unittest.TestCase):
    def test_constructor(self):
        cmd = Gripper()
        self.assertEqual(0.0, cmd.GetTargetState())
        self.assertLessEqual(1, len(cmd.data.target_states))
        self.assertEqual(0.0, cmd.data.target_states[0])

    def test_GetCmdParameters(self):
        cmd = Gripper()
        cmd.SetTargetState(42.0)

        param = cmd.GetCmdParameters()

        self.assertLessEqual(1, len(param.gripper.target_states))
        self.assertEqual(42.0, param.gripper.target_states[0])

    def testSetTargetState(self):
        cmd = Gripper()
        cmd.SetTargetState(42.0)

        self.assertEqual(42.0, cmd.GetTargetState())
        self.assertLessEqual(1, len(cmd.data.target_states))
        self.assertEqual(42.0, cmd.data.target_states[0])
