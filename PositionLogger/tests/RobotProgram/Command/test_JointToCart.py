import unittest

from src.irc_app.RobotProgram.Command.JointToCart import JointToCart


class JointTest(unittest.TestCase):
    def test_constructor(self):
        cmd = JointToCart()

        self.assertTrue(cmd.IsPositionConstant())
        self.assertFalse(cmd.IsPositionFromVariable())

        self.assertEqual(0, cmd.GetX())
        self.assertEqual(0, cmd.GetY())
        self.assertEqual(0, cmd.GetZ())
        self.assertEqual(0, cmd.GetA())
        self.assertEqual(0, cmd.GetB())
        self.assertEqual(0, cmd.GetC())
        self.assertEqual(0, cmd.GetE1())
        self.assertEqual(0, cmd.GetE2())
        self.assertEqual(0, cmd.GetE3())

        self.assertEqual(40, cmd.GetVelocity())
        self.assertEqual(40, cmd.GetAcceleration())
        self.assertEqual(0, cmd.GetSmoothing())
        self.assertEqual("false", cmd.GetAbortCondition())

        self.assertEqual(0, cmd.data.target_x)
        self.assertEqual(0, cmd.data.target_y)
        self.assertEqual(0, cmd.data.target_z)
        self.assertEqual(0, cmd.data.target_a)
        self.assertEqual(0, cmd.data.target_b)
        self.assertEqual(0, cmd.data.target_c)
        self.assertEqual(3, len(cmd.data.target_pos_ext_joints))
        self.assertEqual(0, cmd.data.target_pos_ext_joints[0])
        self.assertEqual(0, cmd.data.target_pos_ext_joints[1])
        self.assertEqual(0, cmd.data.target_pos_ext_joints[2])

        self.assertFalse(cmd.data.HasField("target_pos_variable"))

        self.assertEqual(40, cmd.data.velocity_percent)
        self.assertEqual(40, cmd.data.acceleration_percent)
        self.assertEqual(0, cmd.data.smoothing_percent)
        self.assertEqual("false", cmd.data.abort_condition)

    def test_GetCmdParameters_Constant(self):
        cmd = JointToCart()
        cmd.SetX(1)
        cmd.SetY(2)
        cmd.SetZ(3)
        cmd.SetA(4)
        cmd.SetB(5)
        cmd.SetC(6)
        cmd.SetE1(7)
        cmd.SetE2(8)
        cmd.SetE3(9)
        cmd.SetVelocity(10)
        cmd.SetAcceleration(20)
        cmd.SetSmooting(30)
        cmd.SetAbortCondition("DIn21")

        param = cmd.GetCmdParameters()
        self.assertEqual(1, param.joint_to_cart.target_x)
        self.assertEqual(2, param.joint_to_cart.target_y)
        self.assertEqual(3, param.joint_to_cart.target_z)
        self.assertEqual(4, param.joint_to_cart.target_a)
        self.assertEqual(5, param.joint_to_cart.target_b)
        self.assertEqual(6, param.joint_to_cart.target_c)
        self.assertEqual(3, len(param.joint_to_cart.target_pos_ext_joints))
        self.assertEqual(7, param.joint_to_cart.target_pos_ext_joints[0])
        self.assertEqual(8, param.joint_to_cart.target_pos_ext_joints[1])
        self.assertEqual(9, param.joint_to_cart.target_pos_ext_joints[2])

        self.assertFalse(param.joint_to_cart.HasField("target_pos_variable"))

        self.assertEqual(10, param.joint_to_cart.velocity_percent)
        self.assertEqual(20, param.joint_to_cart.acceleration_percent)
        self.assertEqual(30, param.joint_to_cart.smoothing_percent)
        self.assertEqual("DIn21", param.joint_to_cart.abort_condition)

    def test_GetCmdParameters_Variable(self):
        cmd = JointToCart()
        cmd.SetVariable("MyVar")
        cmd.SetVelocity(10)
        cmd.SetAcceleration(20)
        cmd.SetSmooting(30)
        cmd.SetAbortCondition("DIn21")

        param = cmd.GetCmdParameters()
        self.assertEqual(3, len(param.joint_to_cart.target_pos_ext_joints))

        self.assertTrue(param.joint_to_cart.HasField("target_pos_variable"))
        self.assertEqual("MyVar", param.joint_to_cart.target_pos_variable)

        self.assertEqual(10, param.joint_to_cart.velocity_percent)
        self.assertEqual(20, param.joint_to_cart.acceleration_percent)
        self.assertEqual(30, param.joint_to_cart.smoothing_percent)
        self.assertEqual("DIn21", param.joint_to_cart.abort_condition)

    def testSetVariable(self):
        cmd = JointToCart()

        cmd.SetVariable("MyVar")
        self.assertTrue(cmd.IsPositionFromVariable())
        self.assertFalse(cmd.IsPositionConstant())

        self.assertEqual("MyVar", cmd.GetVariable())
        self.assertEqual("MyVar", cmd.data.target_pos_variable)

    def testSetX(self):
        cmd = JointToCart()
        cmd.SetVariable("MyVar")

        value = 100
        cmd.SetX(value)

        self.assertFalse(cmd.IsPositionFromVariable())
        self.assertTrue(cmd.IsPositionConstant())
        self.assertEqual(value, cmd.GetX())
        self.assertEqual(0, cmd.GetY())
        self.assertEqual(0, cmd.GetZ())
        self.assertEqual(0, cmd.GetA())
        self.assertEqual(0, cmd.GetB())
        self.assertEqual(0, cmd.GetC())
        self.assertEqual(0, cmd.GetE1())
        self.assertEqual(0, cmd.GetE2())
        self.assertEqual(0, cmd.GetE3())

        self.assertEqual(value, cmd.data.target_x)
        self.assertEqual(0, cmd.data.target_y)
        self.assertEqual(0, cmd.data.target_z)
        self.assertEqual(0, cmd.data.target_a)
        self.assertEqual(0, cmd.data.target_b)
        self.assertEqual(0, cmd.data.target_c)
        self.assertEqual(0, cmd.data.target_pos_ext_joints[0])
        self.assertEqual(0, cmd.data.target_pos_ext_joints[0])
        self.assertEqual(0, cmd.data.target_pos_ext_joints[0])

    def testSetY(self):
        cmd = JointToCart()
        cmd.SetVariable("MyVar")

        value = 200
        cmd.SetY(value)

        self.assertFalse(cmd.IsPositionFromVariable())
        self.assertTrue(cmd.IsPositionConstant())
        self.assertEqual(0, cmd.GetX())
        self.assertEqual(value, cmd.GetY())
        self.assertEqual(0, cmd.GetZ())
        self.assertEqual(0, cmd.GetA())
        self.assertEqual(0, cmd.GetB())
        self.assertEqual(0, cmd.GetC())
        self.assertEqual(0, cmd.GetE1())
        self.assertEqual(0, cmd.GetE2())
        self.assertEqual(0, cmd.GetE3())

        self.assertEqual(0, cmd.data.target_x)
        self.assertEqual(value, cmd.data.target_y)
        self.assertEqual(0, cmd.data.target_z)
        self.assertEqual(0, cmd.data.target_a)
        self.assertEqual(0, cmd.data.target_b)
        self.assertEqual(0, cmd.data.target_c)
        self.assertEqual(0, cmd.data.target_pos_ext_joints[0])
        self.assertEqual(0, cmd.data.target_pos_ext_joints[0])
        self.assertEqual(0, cmd.data.target_pos_ext_joints[0])

    def testSetZ(self):
        cmd = JointToCart()
        cmd.SetVariable("MyVar")

        value = 300
        cmd.SetZ(value)

        self.assertFalse(cmd.IsPositionFromVariable())
        self.assertTrue(cmd.IsPositionConstant())
        self.assertEqual(0, cmd.GetX())
        self.assertEqual(0, cmd.GetY())
        self.assertEqual(value, cmd.GetZ())
        self.assertEqual(0, cmd.GetA())
        self.assertEqual(0, cmd.GetB())
        self.assertEqual(0, cmd.GetC())
        self.assertEqual(0, cmd.GetE1())
        self.assertEqual(0, cmd.GetE2())
        self.assertEqual(0, cmd.GetE3())

        self.assertEqual(0, cmd.data.target_x)
        self.assertEqual(0, cmd.data.target_y)
        self.assertEqual(value, cmd.data.target_z)
        self.assertEqual(0, cmd.data.target_a)
        self.assertEqual(0, cmd.data.target_b)
        self.assertEqual(0, cmd.data.target_c)
        self.assertEqual(0, cmd.data.target_pos_ext_joints[0])
        self.assertEqual(0, cmd.data.target_pos_ext_joints[0])
        self.assertEqual(0, cmd.data.target_pos_ext_joints[0])

    def testSetA(self):
        cmd = JointToCart()
        cmd.SetVariable("MyVar")

        value = 400
        cmd.SetA(value)

        self.assertFalse(cmd.IsPositionFromVariable())
        self.assertTrue(cmd.IsPositionConstant())
        self.assertEqual(0, cmd.GetX())
        self.assertEqual(0, cmd.GetY())
        self.assertEqual(0, cmd.GetZ())
        self.assertEqual(value, cmd.GetA())
        self.assertEqual(0, cmd.GetB())
        self.assertEqual(0, cmd.GetC())
        self.assertEqual(0, cmd.GetE1())
        self.assertEqual(0, cmd.GetE2())
        self.assertEqual(0, cmd.GetE3())

        self.assertEqual(0, cmd.data.target_x)
        self.assertEqual(0, cmd.data.target_y)
        self.assertEqual(0, cmd.data.target_z)
        self.assertEqual(value, cmd.data.target_a)
        self.assertEqual(0, cmd.data.target_b)
        self.assertEqual(0, cmd.data.target_c)
        self.assertEqual(0, cmd.data.target_pos_ext_joints[0])
        self.assertEqual(0, cmd.data.target_pos_ext_joints[0])
        self.assertEqual(0, cmd.data.target_pos_ext_joints[0])

    def testSetB(self):
        cmd = JointToCart()
        cmd.SetVariable("MyVar")

        value = 500
        cmd.SetB(value)

        self.assertFalse(cmd.IsPositionFromVariable())
        self.assertTrue(cmd.IsPositionConstant())
        self.assertEqual(0, cmd.GetX())
        self.assertEqual(0, cmd.GetY())
        self.assertEqual(0, cmd.GetZ())
        self.assertEqual(0, cmd.GetA())
        self.assertEqual(value, cmd.GetB())
        self.assertEqual(0, cmd.GetC())
        self.assertEqual(0, cmd.GetE1())
        self.assertEqual(0, cmd.GetE2())
        self.assertEqual(0, cmd.GetE3())

        self.assertEqual(0, cmd.data.target_x)
        self.assertEqual(0, cmd.data.target_y)
        self.assertEqual(0, cmd.data.target_z)
        self.assertEqual(0, cmd.data.target_a)
        self.assertEqual(value, cmd.data.target_b)
        self.assertEqual(0, cmd.data.target_c)
        self.assertEqual(0, cmd.data.target_pos_ext_joints[0])
        self.assertEqual(0, cmd.data.target_pos_ext_joints[0])
        self.assertEqual(0, cmd.data.target_pos_ext_joints[0])

    def testSetC(self):
        cmd = JointToCart()
        cmd.SetVariable("MyVar")

        value = 600
        cmd.SetC(value)

        self.assertFalse(cmd.IsPositionFromVariable())
        self.assertTrue(cmd.IsPositionConstant())
        self.assertEqual(0, cmd.GetX())
        self.assertEqual(0, cmd.GetY())
        self.assertEqual(0, cmd.GetZ())
        self.assertEqual(0, cmd.GetA())
        self.assertEqual(0, cmd.GetB())
        self.assertEqual(value, cmd.GetC())
        self.assertEqual(0, cmd.GetE1())
        self.assertEqual(0, cmd.GetE2())
        self.assertEqual(0, cmd.GetE3())

        self.assertEqual(0, cmd.data.target_x)
        self.assertEqual(0, cmd.data.target_y)
        self.assertEqual(0, cmd.data.target_z)
        self.assertEqual(0, cmd.data.target_a)
        self.assertEqual(0, cmd.data.target_b)
        self.assertEqual(value, cmd.data.target_c)
        self.assertEqual(0, cmd.data.target_pos_ext_joints[0])
        self.assertEqual(0, cmd.data.target_pos_ext_joints[0])
        self.assertEqual(0, cmd.data.target_pos_ext_joints[0])

    def testSetE1(self):
        cmd = JointToCart()
        cmd.SetVariable("MyVar")

        value = 700
        cmd.SetE1(value)

        self.assertFalse(cmd.IsPositionFromVariable())
        self.assertTrue(cmd.IsPositionConstant())
        self.assertEqual(0, cmd.GetX())
        self.assertEqual(0, cmd.GetY())
        self.assertEqual(0, cmd.GetZ())
        self.assertEqual(0, cmd.GetA())
        self.assertEqual(0, cmd.GetB())
        self.assertEqual(0, cmd.GetC())
        self.assertEqual(value, cmd.GetE1())
        self.assertEqual(0, cmd.GetE2())
        self.assertEqual(0, cmd.GetE3())

        self.assertEqual(0, cmd.data.target_x)
        self.assertEqual(0, cmd.data.target_y)
        self.assertEqual(0, cmd.data.target_z)
        self.assertEqual(0, cmd.data.target_a)
        self.assertEqual(0, cmd.data.target_b)
        self.assertEqual(0, cmd.data.target_c)
        self.assertEqual(value, cmd.data.target_pos_ext_joints[0])
        self.assertEqual(0, cmd.data.target_pos_ext_joints[1])
        self.assertEqual(0, cmd.data.target_pos_ext_joints[2])

    def testSetE2(self):
        cmd = JointToCart()
        cmd.SetVariable("MyVar")

        value = 800
        cmd.SetE2(value)

        self.assertFalse(cmd.IsPositionFromVariable())
        self.assertTrue(cmd.IsPositionConstant())
        self.assertEqual(0, cmd.GetX())
        self.assertEqual(0, cmd.GetY())
        self.assertEqual(0, cmd.GetZ())
        self.assertEqual(0, cmd.GetA())
        self.assertEqual(0, cmd.GetB())
        self.assertEqual(0, cmd.GetC())
        self.assertEqual(0, cmd.GetE1())
        self.assertEqual(value, cmd.GetE2())
        self.assertEqual(0, cmd.GetE3())

        self.assertEqual(0, cmd.data.target_x)
        self.assertEqual(0, cmd.data.target_y)
        self.assertEqual(0, cmd.data.target_z)
        self.assertEqual(0, cmd.data.target_a)
        self.assertEqual(0, cmd.data.target_b)
        self.assertEqual(0, cmd.data.target_c)
        self.assertEqual(0, cmd.data.target_pos_ext_joints[0])
        self.assertEqual(value, cmd.data.target_pos_ext_joints[1])
        self.assertEqual(0, cmd.data.target_pos_ext_joints[2])

    def testSetE3(self):
        cmd = JointToCart()
        cmd.SetVariable("MyVar")

        value = 900
        cmd.SetE3(value)

        self.assertFalse(cmd.IsPositionFromVariable())
        self.assertTrue(cmd.IsPositionConstant())
        self.assertEqual(0, cmd.GetX())
        self.assertEqual(0, cmd.GetY())
        self.assertEqual(0, cmd.GetZ())
        self.assertEqual(0, cmd.GetA())
        self.assertEqual(0, cmd.GetB())
        self.assertEqual(0, cmd.GetC())
        self.assertEqual(0, cmd.GetE1())
        self.assertEqual(0, cmd.GetE2())
        self.assertEqual(value, cmd.GetE3())

        self.assertEqual(0, cmd.data.target_x)
        self.assertEqual(0, cmd.data.target_y)
        self.assertEqual(0, cmd.data.target_z)
        self.assertEqual(0, cmd.data.target_a)
        self.assertEqual(0, cmd.data.target_b)
        self.assertEqual(0, cmd.data.target_c)
        self.assertEqual(0, cmd.data.target_pos_ext_joints[0])
        self.assertEqual(0, cmd.data.target_pos_ext_joints[1])
        self.assertEqual(value, cmd.data.target_pos_ext_joints[2])

    def testSetVelocity(self):
        cmd = JointToCart()
        cmd.SetVelocity(12)
        self.assertEqual(12, cmd.GetVelocity())
        self.assertEqual(12, cmd.data.velocity_percent)

        self.assertEqual(40, cmd.GetAcceleration())
        self.assertEqual(40, cmd.data.acceleration_percent)
        self.assertEqual(0, cmd.GetSmoothing())
        self.assertEqual(0, cmd.data.smoothing_percent)

    def testSetAcceleration(self):
        cmd = JointToCart()
        cmd.SetAcceleration(78)
        self.assertEqual(78, cmd.GetAcceleration())
        self.assertEqual(78, cmd.data.acceleration_percent)

        self.assertEqual(40, cmd.GetVelocity())
        self.assertEqual(40, cmd.data.velocity_percent)
        self.assertEqual(0, cmd.GetSmoothing())
        self.assertEqual(0, cmd.data.smoothing_percent)

    def testSetSmoothing(self):
        cmd = JointToCart()
        cmd.SetSmooting(45)
        self.assertEqual(45, cmd.GetSmoothing())
        self.assertEqual(45, cmd.data.smoothing_percent)

        self.assertEqual(40, cmd.GetVelocity())
        self.assertEqual(40, cmd.data.velocity_percent)
        self.assertEqual(40, cmd.GetAcceleration())
        self.assertEqual(40, cmd.data.acceleration_percent)

    def testSetAbortCondition(self):
        cmd = JointToCart()
        cmd.SetAbortCondition("GSig32")
        self.assertEqual("GSig32", cmd.GetAbortCondition())
        self.assertEqual("GSig32", cmd.data.abort_condition)

    def testSetReferenceFrame(self):
        cmd = JointToCart()
        cmd.SetReferenceFrame("MyFrame")
        self.assertEqual("MyFrame", cmd.GetReferenceFrame())
        self.assertEqual("MyFrame", cmd.data.reference_frame)
