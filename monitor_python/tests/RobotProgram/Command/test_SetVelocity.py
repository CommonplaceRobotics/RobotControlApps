import unittest

from src.irc_app.RobotProgram.Command.SetVelocity import SetVelocity


class SetVelocityTest(unittest.TestCase):
    def test_constructor(self):
        cmd = SetVelocity()
        self.assertEqual(0.0, cmd.GetE1())
        self.assertEqual(0.0, cmd.data.velocity_e1)
        self.assertEqual(0.0, cmd.GetE2())
        self.assertEqual(0.0, cmd.data.velocity_e2)
        self.assertEqual(0.0, cmd.GetE3())
        self.assertEqual(0.0, cmd.data.velocity_e3)

    def test_GetCmdParameters(self):
        cmd = SetVelocity()
        cmd.SetE1(10)
        cmd.SetE2(20)
        cmd.SetE3(30)

        param = cmd.GetCmdParameters()

        self.assertEqual(10, param.set_velocity.velocity_e1)
        self.assertEqual(20, param.set_velocity.velocity_e2)
        self.assertEqual(30, param.set_velocity.velocity_e3)

    def test_SetE1(self):
        cmd = SetVelocity()
        cmd.SetE1(1000.0)
        self.assertEqual(1000.0, cmd.GetE1())
        self.assertEqual(1000.0, cmd.data.velocity_e1)
        self.assertEqual(0.0, cmd.GetE2())
        self.assertEqual(0.0, cmd.data.velocity_e2)
        self.assertEqual(0.0, cmd.GetE3())
        self.assertEqual(0.0, cmd.data.velocity_e3)

    def test_SetE2(self):
        cmd = SetVelocity()
        cmd.SetE2(1000.0)
        self.assertEqual(0.0, cmd.GetE1())
        self.assertEqual(0.0, cmd.data.velocity_e1)
        self.assertEqual(1000.0, cmd.GetE2())
        self.assertEqual(1000.0, cmd.data.velocity_e2)
        self.assertEqual(0.0, cmd.GetE3())
        self.assertEqual(0.0, cmd.data.velocity_e3)

    def test_SetE3(self):
        cmd = SetVelocity()
        cmd.SetE3(1000.0)
        self.assertEqual(0.0, cmd.GetE1())
        self.assertEqual(0.0, cmd.data.velocity_e1)
        self.assertEqual(0.0, cmd.GetE2())
        self.assertEqual(0.0, cmd.data.velocity_e2)
        self.assertEqual(1000.0, cmd.GetE3())
        self.assertEqual(1000.0, cmd.data.velocity_e3)
