import unittest

from src.irc_app.RobotProgram.Command.SetGlobalSignal import SetGlobalSignal


class SetGlobalSignalTest(unittest.TestCase):
    def test_constructor(self):
        cmd = SetGlobalSignal()
        self.assertEqual(0.0, cmd.GetID())
        self.assertEqual(0.0, cmd.data.output_number)
        self.assertEqual(0.0, cmd.GetState())
        self.assertEqual(0.0, cmd.data.target_state)

    def test_GetCmdParameters(self):
        cmd = SetGlobalSignal()
        cmd.SetID(12)
        cmd.SetState(True)

        param = cmd.GetCmdParameters()

        self.assertEqual(12, param.set_global_signal.output_number)
        self.assertTrue(param.set_global_signal.target_state)

    def testSetID(self):
        cmd = SetGlobalSignal()
        cmd.SetID(78)
        self.assertEqual(78, cmd.GetID())
        self.assertEqual(78, cmd.data.output_number)
        self.assertFalse(cmd.GetState())
        self.assertFalse(cmd.data.target_state)

    def testSetTargetStateTrue(self):
        cmd = SetGlobalSignal()
        cmd.SetState(True)
        self.assertEqual(0, cmd.GetID())
        self.assertEqual(0, cmd.data.output_number)
        self.assertTrue(cmd.GetState())
        self.assertTrue(cmd.data.target_state)

    def testSetTargetStateFalse(self):
        cmd = SetGlobalSignal()
        cmd.SetState(False)
        self.assertEqual(0, cmd.GetID())
        self.assertEqual(0, cmd.data.output_number)
        self.assertFalse(cmd.GetState())
        self.assertFalse(cmd.data.target_state)
