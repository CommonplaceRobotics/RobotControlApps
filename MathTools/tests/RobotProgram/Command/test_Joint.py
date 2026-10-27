import unittest

from src.irc_app.RobotProgram.Command.Joint import Joint


class JointTest(unittest.TestCase):
    def test_constructor(self):
        cmd = Joint()

        self.assertTrue(cmd.IsPositionConstant())
        self.assertFalse(cmd.IsPositionFromVariable())

        self.assertEqual(0, cmd.GetA1())
        self.assertEqual(0, cmd.GetA2())
        self.assertEqual(0, cmd.GetA3())
        self.assertEqual(0, cmd.GetA4())
        self.assertEqual(0, cmd.GetA5())
        self.assertEqual(0, cmd.GetA6())
        self.assertEqual(0, cmd.GetE1())
        self.assertEqual(0, cmd.GetE2())
        self.assertEqual(0, cmd.GetE3())

        self.assertEqual(40, cmd.GetVelocity())
        self.assertEqual(40, cmd.GetAcceleration())
        self.assertEqual(0, cmd.GetSmoothing())
        self.assertEqual("false", cmd.GetAbortCondition())

        self.assertEqual(9, len(cmd.data.target_pos))
        self.assertEqual(0, cmd.data.target_pos[0])
        self.assertEqual(0, cmd.data.target_pos[1])
        self.assertEqual(0, cmd.data.target_pos[2])
        self.assertEqual(0, cmd.data.target_pos[3])
        self.assertEqual(0, cmd.data.target_pos[4])
        self.assertEqual(0, cmd.data.target_pos[5])
        self.assertEqual(0, cmd.data.target_pos[6])
        self.assertEqual(0, cmd.data.target_pos[7])
        self.assertEqual(0, cmd.data.target_pos[8])

        self.assertFalse(cmd.data.HasField("target_pos_variable"))

        self.assertEqual(40, cmd.data.velocity_percent)
        self.assertEqual(40, cmd.data.acceleration_percent)
        self.assertEqual(0, cmd.data.smoothing_percent)
        self.assertEqual("false", cmd.data.abort_condition)

    def test_GetCmdParameters_Constant(self):
        cmd = Joint()
        cmd.SetA1(1)
        cmd.SetA2(2)
        cmd.SetA3(3)
        cmd.SetA4(4)
        cmd.SetA5(5)
        cmd.SetA6(6)
        cmd.SetE1(7)
        cmd.SetE2(8)
        cmd.SetE3(9)
        cmd.SetVelocity(10)
        cmd.SetAcceleration(20)
        cmd.SetSmooting(30)
        cmd.SetAbortCondition("DIn21")

        param = cmd.GetCmdParameters()
        self.assertEqual(9, len(param.joint.target_pos))
        self.assertEqual(1, param.joint.target_pos[0])
        self.assertEqual(2, param.joint.target_pos[1])
        self.assertEqual(3, param.joint.target_pos[2])
        self.assertEqual(4, param.joint.target_pos[3])
        self.assertEqual(5, param.joint.target_pos[4])
        self.assertEqual(6, param.joint.target_pos[5])
        self.assertEqual(7, param.joint.target_pos[6])
        self.assertEqual(8, param.joint.target_pos[7])
        self.assertEqual(9, param.joint.target_pos[8])

        self.assertFalse(param.joint.HasField("target_pos_variable"))

        self.assertEqual(10, param.joint.velocity_percent)
        self.assertEqual(20, param.joint.acceleration_percent)
        self.assertEqual(30, param.joint.smoothing_percent)
        self.assertEqual("DIn21", param.joint.abort_condition)

    def test_GetCmdParameters_Variable(self):
        cmd = Joint()
        cmd.SetVariable("MyVar")
        cmd.SetVelocity(10)
        cmd.SetAcceleration(20)
        cmd.SetSmooting(30)
        cmd.SetAbortCondition("DIn21")

        param = cmd.GetCmdParameters()
        self.assertEqual(9, len(param.joint.target_pos))

        self.assertTrue(param.joint.HasField("target_pos_variable"))
        self.assertEqual("MyVar", param.joint.target_pos_variable)

        self.assertEqual(10, param.joint.velocity_percent)
        self.assertEqual(20, param.joint.acceleration_percent)
        self.assertEqual(30, param.joint.smoothing_percent)
        self.assertEqual("DIn21", param.joint.abort_condition)

    def testSetVariable(self):
        cmd = Joint()

        cmd.SetVariable("MyVar")
        self.assertTrue(cmd.IsPositionFromVariable())
        self.assertFalse(cmd.IsPositionConstant())

        self.assertEqual("MyVar", cmd.GetVariable())
        self.assertEqual("MyVar", cmd.data.target_pos_variable)

    def testSetA1(self):
        cmd = Joint()
        cmd.SetVariable("MyVar")

        value = 100
        cmd.SetA1(value)

        self.assertFalse(cmd.IsPositionFromVariable())
        self.assertTrue(cmd.IsPositionConstant())
        self.assertEqual(value, cmd.GetA1())
        self.assertEqual(0, cmd.GetA2())
        self.assertEqual(0, cmd.GetA3())
        self.assertEqual(0, cmd.GetA4())
        self.assertEqual(0, cmd.GetA5())
        self.assertEqual(0, cmd.GetA6())
        self.assertEqual(0, cmd.GetE1())
        self.assertEqual(0, cmd.GetE2())
        self.assertEqual(0, cmd.GetE3())

        self.assertEqual(value, cmd.data.target_pos[0])
        self.assertEqual(0, cmd.data.target_pos[1])
        self.assertEqual(0, cmd.data.target_pos[2])
        self.assertEqual(0, cmd.data.target_pos[3])
        self.assertEqual(0, cmd.data.target_pos[4])
        self.assertEqual(0, cmd.data.target_pos[5])
        self.assertEqual(0, cmd.data.target_pos[6])
        self.assertEqual(0, cmd.data.target_pos[7])
        self.assertEqual(0, cmd.data.target_pos[8])

    def testSetA2(self):
        cmd = Joint()
        cmd.SetVariable("MyVar")

        value = 200
        cmd.SetA2(value)

        self.assertFalse(cmd.IsPositionFromVariable())
        self.assertTrue(cmd.IsPositionConstant())
        self.assertEqual(0, cmd.GetA1())
        self.assertEqual(value, cmd.GetA2())
        self.assertEqual(0, cmd.GetA3())
        self.assertEqual(0, cmd.GetA4())
        self.assertEqual(0, cmd.GetA5())
        self.assertEqual(0, cmd.GetA6())
        self.assertEqual(0, cmd.GetE1())
        self.assertEqual(0, cmd.GetE2())
        self.assertEqual(0, cmd.GetE3())

        self.assertEqual(0, cmd.data.target_pos[0])
        self.assertEqual(value, cmd.data.target_pos[1])
        self.assertEqual(0, cmd.data.target_pos[2])
        self.assertEqual(0, cmd.data.target_pos[3])
        self.assertEqual(0, cmd.data.target_pos[4])
        self.assertEqual(0, cmd.data.target_pos[5])
        self.assertEqual(0, cmd.data.target_pos[6])
        self.assertEqual(0, cmd.data.target_pos[7])
        self.assertEqual(0, cmd.data.target_pos[8])

    def testSetA3(self):
        cmd = Joint()
        cmd.SetVariable("MyVar")

        value = 300
        cmd.SetA3(value)

        self.assertFalse(cmd.IsPositionFromVariable())
        self.assertTrue(cmd.IsPositionConstant())
        self.assertEqual(0, cmd.GetA1())
        self.assertEqual(0, cmd.GetA2())
        self.assertEqual(value, cmd.GetA3())
        self.assertEqual(0, cmd.GetA4())
        self.assertEqual(0, cmd.GetA5())
        self.assertEqual(0, cmd.GetA6())
        self.assertEqual(0, cmd.GetE1())
        self.assertEqual(0, cmd.GetE2())
        self.assertEqual(0, cmd.GetE3())

        self.assertEqual(0, cmd.data.target_pos[0])
        self.assertEqual(0, cmd.data.target_pos[1])
        self.assertEqual(value, cmd.data.target_pos[2])
        self.assertEqual(0, cmd.data.target_pos[3])
        self.assertEqual(0, cmd.data.target_pos[4])
        self.assertEqual(0, cmd.data.target_pos[5])
        self.assertEqual(0, cmd.data.target_pos[6])
        self.assertEqual(0, cmd.data.target_pos[7])
        self.assertEqual(0, cmd.data.target_pos[8])

    def testSetA4(self):
        cmd = Joint()
        cmd.SetVariable("MyVar")

        value = 400
        cmd.SetA4(value)

        self.assertFalse(cmd.IsPositionFromVariable())
        self.assertTrue(cmd.IsPositionConstant())
        self.assertEqual(0, cmd.GetA1())
        self.assertEqual(0, cmd.GetA2())
        self.assertEqual(0, cmd.GetA3())
        self.assertEqual(value, cmd.GetA4())
        self.assertEqual(0, cmd.GetA5())
        self.assertEqual(0, cmd.GetA6())
        self.assertEqual(0, cmd.GetE1())
        self.assertEqual(0, cmd.GetE2())
        self.assertEqual(0, cmd.GetE3())

        self.assertEqual(0, cmd.data.target_pos[0])
        self.assertEqual(0, cmd.data.target_pos[1])
        self.assertEqual(0, cmd.data.target_pos[2])
        self.assertEqual(value, cmd.data.target_pos[3])
        self.assertEqual(0, cmd.data.target_pos[4])
        self.assertEqual(0, cmd.data.target_pos[5])
        self.assertEqual(0, cmd.data.target_pos[6])
        self.assertEqual(0, cmd.data.target_pos[7])
        self.assertEqual(0, cmd.data.target_pos[8])

    def testSetA5(self):
        cmd = Joint()
        cmd.SetVariable("MyVar")

        value = 500
        cmd.SetA5(value)

        self.assertFalse(cmd.IsPositionFromVariable())
        self.assertTrue(cmd.IsPositionConstant())
        self.assertEqual(0, cmd.GetA1())
        self.assertEqual(0, cmd.GetA2())
        self.assertEqual(0, cmd.GetA3())
        self.assertEqual(0, cmd.GetA4())
        self.assertEqual(value, cmd.GetA5())
        self.assertEqual(0, cmd.GetA6())
        self.assertEqual(0, cmd.GetE1())
        self.assertEqual(0, cmd.GetE2())
        self.assertEqual(0, cmd.GetE3())

        self.assertEqual(0, cmd.data.target_pos[0])
        self.assertEqual(0, cmd.data.target_pos[1])
        self.assertEqual(0, cmd.data.target_pos[2])
        self.assertEqual(0, cmd.data.target_pos[3])
        self.assertEqual(value, cmd.data.target_pos[4])
        self.assertEqual(0, cmd.data.target_pos[5])
        self.assertEqual(0, cmd.data.target_pos[6])
        self.assertEqual(0, cmd.data.target_pos[7])
        self.assertEqual(0, cmd.data.target_pos[8])

    def testSetA6(self):
        cmd = Joint()
        cmd.SetVariable("MyVar")

        value = 600
        cmd.SetA6(value)

        self.assertFalse(cmd.IsPositionFromVariable())
        self.assertTrue(cmd.IsPositionConstant())
        self.assertEqual(0, cmd.GetA1())
        self.assertEqual(0, cmd.GetA2())
        self.assertEqual(0, cmd.GetA3())
        self.assertEqual(0, cmd.GetA4())
        self.assertEqual(0, cmd.GetA5())
        self.assertEqual(value, cmd.GetA6())
        self.assertEqual(0, cmd.GetE1())
        self.assertEqual(0, cmd.GetE2())
        self.assertEqual(0, cmd.GetE3())

        self.assertEqual(0, cmd.data.target_pos[0])
        self.assertEqual(0, cmd.data.target_pos[1])
        self.assertEqual(0, cmd.data.target_pos[2])
        self.assertEqual(0, cmd.data.target_pos[3])
        self.assertEqual(0, cmd.data.target_pos[4])
        self.assertEqual(value, cmd.data.target_pos[5])
        self.assertEqual(0, cmd.data.target_pos[6])
        self.assertEqual(0, cmd.data.target_pos[7])
        self.assertEqual(0, cmd.data.target_pos[8])

    def testSetE1(self):
        cmd = Joint()
        cmd.SetVariable("MyVar")

        value = 700
        cmd.SetE1(value)

        self.assertFalse(cmd.IsPositionFromVariable())
        self.assertTrue(cmd.IsPositionConstant())
        self.assertEqual(0, cmd.GetA1())
        self.assertEqual(0, cmd.GetA2())
        self.assertEqual(0, cmd.GetA3())
        self.assertEqual(0, cmd.GetA4())
        self.assertEqual(0, cmd.GetA5())
        self.assertEqual(0, cmd.GetA6())
        self.assertEqual(value, cmd.GetE1())
        self.assertEqual(0, cmd.GetE2())
        self.assertEqual(0, cmd.GetE3())

        self.assertEqual(0, cmd.data.target_pos[0])
        self.assertEqual(0, cmd.data.target_pos[1])
        self.assertEqual(0, cmd.data.target_pos[2])
        self.assertEqual(0, cmd.data.target_pos[3])
        self.assertEqual(0, cmd.data.target_pos[4])
        self.assertEqual(0, cmd.data.target_pos[5])
        self.assertEqual(value, cmd.data.target_pos[6])
        self.assertEqual(0, cmd.data.target_pos[7])
        self.assertEqual(0, cmd.data.target_pos[8])

    def testSetE2(self):
        cmd = Joint()
        cmd.SetVariable("MyVar")

        value = 800
        cmd.SetE2(value)

        self.assertFalse(cmd.IsPositionFromVariable())
        self.assertTrue(cmd.IsPositionConstant())
        self.assertEqual(0, cmd.GetA1())
        self.assertEqual(0, cmd.GetA2())
        self.assertEqual(0, cmd.GetA3())
        self.assertEqual(0, cmd.GetA4())
        self.assertEqual(0, cmd.GetA5())
        self.assertEqual(0, cmd.GetA6())
        self.assertEqual(0, cmd.GetE1())
        self.assertEqual(value, cmd.GetE2())
        self.assertEqual(0, cmd.GetE3())

        self.assertEqual(0, cmd.data.target_pos[0])
        self.assertEqual(0, cmd.data.target_pos[1])
        self.assertEqual(0, cmd.data.target_pos[2])
        self.assertEqual(0, cmd.data.target_pos[3])
        self.assertEqual(0, cmd.data.target_pos[4])
        self.assertEqual(0, cmd.data.target_pos[5])
        self.assertEqual(0, cmd.data.target_pos[6])
        self.assertEqual(value, cmd.data.target_pos[7])
        self.assertEqual(0, cmd.data.target_pos[8])

    def testSetE3(self):
        cmd = Joint()
        cmd.SetVariable("MyVar")

        value = 900
        cmd.SetE3(value)

        self.assertFalse(cmd.IsPositionFromVariable())
        self.assertTrue(cmd.IsPositionConstant())
        self.assertEqual(0, cmd.GetA1())
        self.assertEqual(0, cmd.GetA2())
        self.assertEqual(0, cmd.GetA3())
        self.assertEqual(0, cmd.GetA4())
        self.assertEqual(0, cmd.GetA5())
        self.assertEqual(0, cmd.GetA6())
        self.assertEqual(0, cmd.GetE1())
        self.assertEqual(0, cmd.GetE2())
        self.assertEqual(value, cmd.GetE3())

        self.assertEqual(0, cmd.data.target_pos[0])
        self.assertEqual(0, cmd.data.target_pos[1])
        self.assertEqual(0, cmd.data.target_pos[2])
        self.assertEqual(0, cmd.data.target_pos[3])
        self.assertEqual(0, cmd.data.target_pos[4])
        self.assertEqual(0, cmd.data.target_pos[5])
        self.assertEqual(0, cmd.data.target_pos[6])
        self.assertEqual(0, cmd.data.target_pos[7])
        self.assertEqual(value, cmd.data.target_pos[8])

    def testSetVelocity(self):
        cmd = Joint()
        cmd.SetVelocity(12)
        self.assertEqual(12, cmd.GetVelocity())
        self.assertEqual(12, cmd.data.velocity_percent)

        self.assertEqual(40, cmd.GetAcceleration())
        self.assertEqual(40, cmd.data.acceleration_percent)
        self.assertEqual(0, cmd.GetSmoothing())
        self.assertEqual(0, cmd.data.smoothing_percent)

    def testSetAcceleration(self):
        cmd = Joint()
        cmd.SetAcceleration(78)
        self.assertEqual(78, cmd.GetAcceleration())
        self.assertEqual(78, cmd.data.acceleration_percent)

        self.assertEqual(40, cmd.GetVelocity())
        self.assertEqual(40, cmd.data.velocity_percent)
        self.assertEqual(0, cmd.GetSmoothing())
        self.assertEqual(0, cmd.data.smoothing_percent)

    def testSetSmoothing(self):
        cmd = Joint()
        cmd.SetSmooting(45)
        self.assertEqual(45, cmd.GetSmoothing())
        self.assertEqual(45, cmd.data.smoothing_percent)

        self.assertEqual(40, cmd.GetVelocity())
        self.assertEqual(40, cmd.data.velocity_percent)
        self.assertEqual(40, cmd.GetAcceleration())
        self.assertEqual(40, cmd.data.acceleration_percent)

    def testSetAbortCondition(self):
        cmd = Joint()
        cmd.SetAbortCondition("GSig32")
        self.assertEqual("GSig32", cmd.GetAbortCondition())
        self.assertEqual("GSig32", cmd.data.abort_condition)
