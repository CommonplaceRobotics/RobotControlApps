import unittest

from DataTypes.Matrix44 import Matrix44
from DataTypes.RobotState import RobotState, Joint
import robotcontrolapp_pb2

class JointTest(unittest.TestCase):
    def test_init(self):
        joint = Joint()

        self.assertEqual(0, joint.id)
        self.assertEqual("", joint.name)
        self.assertEqual(0, joint.actualPosition)
        self.assertEqual(0, joint.targetPosition)
        self.assertEqual(robotcontrolapp_pb2.HardwareState.ERROR_MODULE_DEAD, joint.hardwareState)
        self.assertEqual(robotcontrolapp_pb2.ReferencingState.NOT_REFERENCED, joint.referencingState)
        self.assertEqual(0, joint.temperatureBoard)
        self.assertEqual(0, joint.temperatureMotor)
        self.assertEqual(0, joint.current)
        self.assertEqual(0, joint.targetVelocity)

    def test_FromGrpc(self):
        grpc = robotcontrolapp_pb2.Joint()
        grpc.id = 123
        grpc.name = "A5"
        grpc.position.position =12.3
        grpc.position.target_position = 34.5
        grpc.state = robotcontrolapp_pb2.HardwareState.ERROR_MOTOR_NOT_ENABLED | robotcontrolapp_pb2.HardwareState.ERROR_ENCODER
        grpc.referencing_state = robotcontrolapp_pb2.ReferencingState.IS_REFERENCED
        grpc.temperature_board = 25.1
        grpc.temperature_motor = 27.2
        grpc.current = 1234.5
        grpc.target_velocity = 87.6

        joint = Joint.FromGrpc(grpc)
        self.assertEqual(123, joint.id)
        self.assertEqual("A5", joint.name)
        self.assertAlmostEqual(12.3, joint.actualPosition, 4)
        self.assertAlmostEqual(34.5, joint.targetPosition, 4)
        self.assertEqual(0x24, joint.hardwareState)
        self.assertEqual(robotcontrolapp_pb2.ReferencingState.IS_REFERENCED, joint.referencingState)
        self.assertAlmostEqual(25.1, joint.temperatureBoard, 4)
        self.assertAlmostEqual(27.2, joint.temperatureMotor, 4)
        self.assertAlmostEqual(1234.5, joint.current, 4)
        self.assertAlmostEqual(87.6, joint.targetVelocity, 4)

class RobotStateTest(unittest.TestCase):
    def test_init(self):
        state = RobotState()

        self.assertEqual(0, state.tcp.GetX())
        self.assertEqual(0, state.tcp.GetY())
        self.assertEqual(0, state.tcp.GetZ())
        self.assertEqual(0, state.tcp.GetA())
        self.assertEqual(0, state.tcp.GetB())
        self.assertEqual(0, state.tcp.GetC())

        self.assertEqual(0, state.platformX)
        self.assertEqual(0, state.platformY)
        self.assertEqual(0, state.platformHeading)

        self.assertEqual(9, len(state.joints))
        self.assertEqual(0, state.joints[0].id)
        self.assertEqual(1, state.joints[1].id)
        self.assertEqual(2, state.joints[2].id)
        self.assertEqual(3, state.joints[3].id)
        self.assertEqual(4, state.joints[4].id)
        self.assertEqual(5, state.joints[5].id)
        self.assertEqual(6, state.joints[6].id)
        self.assertEqual(7, state.joints[7].id)
        self.assertEqual(8, state.joints[8].id)
        self.assertEqual("A1", state.joints[0].name)
        self.assertEqual("A2", state.joints[1].name)
        self.assertEqual("A3", state.joints[2].name)
        self.assertEqual("A4", state.joints[3].name)
        self.assertEqual("A5", state.joints[4].name)
        self.assertEqual("A6", state.joints[5].name)
        self.assertEqual("E1", state.joints[6].name)
        self.assertEqual("E2", state.joints[7].name)
        self.assertEqual("E3", state.joints[8].name)

        self.assertEqual(64, len(state.digitalInputs))
        self.assertEqual(64, len(state.digitalOutputs))
        self.assertEqual(100, len(state.globalSignals))
        self.assertEqual(64, state.digitalInputs.count(False))
        self.assertEqual(64, state.digitalOutputs.count(False))
        self.assertEqual(100, state.globalSignals.count(False))
        self.assertFalse(state.digitalInputs[0])
        self.assertFalse(state.digitalInputs[63])
        self.assertFalse(state.digitalOutputs[0])
        self.assertFalse(state.digitalOutputs[63])
        self.assertFalse(state.globalSignals[0])
        self.assertFalse(state.globalSignals[99])

        self.assertEqual("", state.hardwareState)
        self.assertEqual(robotcontrolapp_pb2.KINEMATIC_NORMAL, state.kinematicState)

        self.assertEqual(0, state.velocityOverride)
        self.assertEqual(0, state.cartesianVelocity)

        self.assertEqual(0, state.temperatureCPU)
        self.assertEqual(0, state.supplyVoltage)
        self.assertEqual(0, state.currentAll)

        self.assertEqual(robotcontrolapp_pb2.ReferencingState.NOT_REFERENCED, state.referencingState)

    def test_FromGrpc(self):
        grpc = robotcontrolapp_pb2.RobotState()
        matrix = Matrix44()
        matrix.SetOrientation(90, 45, 0)
        matrix.SetX(123)
        matrix.SetY(456)
        matrix.SetZ(789)
        matrixGrpc = matrix.ToGrpc()
        for i in range(0, len(matrixGrpc.data)):
            grpc.tcp.data.append(matrixGrpc.data[i])

        grpc.platform_pose.position.x = 1234.5
        grpc.platform_pose.position.y = -567.8
        grpc.platform_pose.heading = 95.6

        a1 = grpc.joints.add()
        a1.id = 0
        a1.name = "A1"
        a1.position.position = 98
        a2 = grpc.joints.add()
        a2.id = 1
        a2.name = "A2"
        a2.position.position = 23
        grpc.joints.add()
        grpc.joints.add()
        grpc.joints.add()
        grpc.joints.add()
        grpc.joints.add()
        grpc.joints.add()
        e3 = grpc.joints.add()
        e3.id = 8
        e3.name = "E3"
        e3.position.position = 546

        grpc.DIns.add().state = robotcontrolapp_pb2.DIOState.HIGH
        grpc.DIns.add().state = robotcontrolapp_pb2.DIOState.LOW
        grpc.DOuts.add().state = robotcontrolapp_pb2.DIOState.LOW
        grpc.DOuts.add().state = robotcontrolapp_pb2.DIOState.HIGH
        grpc.GSigs.add().state = robotcontrolapp_pb2.DIOState.HIGH
        grpc.GSigs.add().state = robotcontrolapp_pb2.DIOState.HIGH
        grpc.GSigs.add().state = robotcontrolapp_pb2.DIOState.LOW
        grpc.GSigs.add().state = robotcontrolapp_pb2.DIOState.LOW

        grpc.hardware_state_string = "MNE_ENC"
        grpc.kinematic_state = robotcontrolapp_pb2.KINEMATIC_ERROR_JOINT_LIMIT_MAX

        grpc.velocity_override = 0.34
        grpc.cartesian_velocity = 45.6

        grpc.temperature_cpu = 46.8
        grpc.supply_voltage = 24.5
        grpc.current_all = 1267.8

        grpc.referencing_state = robotcontrolapp_pb2.ReferencingState.IS_REFERENCING

        state = RobotState.FromGrpc(grpc)
        self.assertEqual(123, state.tcp.GetX())
        self.assertEqual(456, state.tcp.GetY())
        self.assertEqual(789, state.tcp.GetZ())
        self.assertEqual(90, state.tcp.GetA())
        self.assertEqual(45, state.tcp.GetB())
        self.assertEqual(0, state.tcp.GetC())

        self.assertAlmostEqual(1234.5, state.platformX, 4)
        self.assertAlmostEqual(-567.8, state.platformY, 4)
        self.assertAlmostEqual(95.6, state.platformHeading, 4)

        self.assertEqual(9, len(state.joints))
        self.assertEqual(0, state.joints[0].id)
        self.assertEqual(1, state.joints[1].id)
        self.assertEqual(8, state.joints[8].id)
        self.assertEqual("A1", state.joints[0].name)
        self.assertEqual("A2", state.joints[1].name)
        self.assertEqual("E3", state.joints[8].name)
        self.assertAlmostEqual(98, state.joints[0].actualPosition, 4)
        self.assertAlmostEqual(23, state.joints[1].actualPosition, 4)
        self.assertAlmostEqual(546, state.joints[8].actualPosition, 4)

        self.assertEqual(64, len(state.digitalInputs))
        self.assertEqual(64, len(state.digitalOutputs))
        self.assertEqual(100, len(state.globalSignals))
        self.assertTrue(state.digitalInputs[0])
        self.assertFalse(state.digitalInputs[1])
        self.assertFalse(state.digitalOutputs[0])
        self.assertTrue(state.digitalOutputs[1])
        self.assertTrue(state.globalSignals[0])
        self.assertTrue(state.globalSignals[1])
        self.assertFalse(state.globalSignals[2])
        self.assertFalse(state.globalSignals[3])

        self.assertEqual("MNE_ENC", state.hardwareState)
        self.assertEqual(robotcontrolapp_pb2.KINEMATIC_ERROR_JOINT_LIMIT_MAX, state.kinematicState)

        self.assertAlmostEqual(0.34, state.velocityOverride, 4)
        self.assertAlmostEqual(45.6, state.cartesianVelocity, 4)

        self.assertAlmostEqual(46.8, state.temperatureCPU, 4)
        self.assertAlmostEqual(24.5, state.supplyVoltage, 4)
        self.assertAlmostEqual(1267.8, state.currentAll, 4)

        self.assertEqual(robotcontrolapp_pb2.ReferencingState.IS_REFERENCING, state.referencingState)

if __name__ == "__main__":
    unittest.main()
