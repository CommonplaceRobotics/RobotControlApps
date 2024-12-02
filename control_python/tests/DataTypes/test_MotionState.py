import unittest

from DataTypes.MotionState import InterpolatorState, MotionState, PositionInterfaceState
import robotcontrolapp_pb2

class MotionStateTest(unittest.TestCase):
    def testInterpolatorState_init(self):
        state = InterpolatorState()
        self.assertEqual(robotcontrolapp_pb2.NOT_RUNNING, state.runState)
        self.assertEqual(robotcontrolapp_pb2.SINGLE, state.replayMode)
        self.assertEqual("", state.mainProgram)
        self.assertEqual("", state.currentProgram)
        self.assertEqual(0, state.currentProgramIndex)
        self.assertEqual(0, state.programCount)
        self.assertEqual(0, state.currentCommandIndex)
        self.assertEqual(0, state.commandCount)
    
    def testInterpolatorState_FromGrpc(self):
        grpc = robotcontrolapp_pb2.MotionState.InterpolatorState()
        grpc.runstate = robotcontrolapp_pb2.PAUSED
        grpc.replay_mode = robotcontrolapp_pb2.REPEAT
        grpc.main_program_name = "Foo"
        grpc.current_program_name = "Bar"
        grpc.current_program_idx = 1
        grpc.program_count = 2
        grpc.current_command_idx = 3
        grpc.command_count = 4

        state = InterpolatorState.FromGrpc(grpc)
        self.assertEqual(robotcontrolapp_pb2.PAUSED, state.runState)
        self.assertEqual(robotcontrolapp_pb2.REPEAT, state.replayMode)
        self.assertEqual("Foo", state.mainProgram)
        self.assertEqual("Bar", state.currentProgram)
        self.assertEqual(1, state.currentProgramIndex)
        self.assertEqual(2, state.programCount)
        self.assertEqual(3, state.currentCommandIndex)
        self.assertEqual(4, state.commandCount)

        grpc = robotcontrolapp_pb2.MotionState.InterpolatorState()
        grpc.runstate = robotcontrolapp_pb2.RUNNING
        grpc.replay_mode = robotcontrolapp_pb2.STEP
        grpc.main_program_name = "Foo"
        grpc.current_program_name = "Bar"
        grpc.current_program_idx = 1
        grpc.program_count = 2
        grpc.current_command_idx = 3
        grpc.command_count = 4

        state = InterpolatorState.FromGrpc(grpc)
        self.assertEqual(robotcontrolapp_pb2.RUNNING, state.runState)
        self.assertEqual(robotcontrolapp_pb2.STEP, state.replayMode)
        self.assertEqual("Foo", state.mainProgram)
        self.assertEqual("Bar", state.currentProgram)
        self.assertEqual(1, state.currentProgramIndex)
        self.assertEqual(2, state.programCount)
        self.assertEqual(3, state.currentCommandIndex)
        self.assertEqual(4, state.commandCount)

        grpc = robotcontrolapp_pb2.MotionState.InterpolatorState()
        grpc.runstate = robotcontrolapp_pb2.NOT_RUNNING
        grpc.replay_mode = robotcontrolapp_pb2.SINGLE
        grpc.main_program_name = "Foo"
        grpc.current_program_name = "Bar"
        grpc.current_program_idx = 1
        grpc.program_count = 2
        grpc.current_command_idx = 3
        grpc.command_count = 4

        state = InterpolatorState.FromGrpc(grpc)
        self.assertEqual(robotcontrolapp_pb2.NOT_RUNNING, state.runState)
        self.assertEqual(robotcontrolapp_pb2.SINGLE, state.replayMode)
        self.assertEqual("Foo", state.mainProgram)
        self.assertEqual("Bar", state.currentProgram)
        self.assertEqual(1, state.currentProgramIndex)
        self.assertEqual(2, state.programCount)
        self.assertEqual(3, state.currentCommandIndex)
        self.assertEqual(4, state.commandCount)
    
    def testPositionInterfaceState_init(self):
        state = PositionInterfaceState()
        self.assertFalse(state.isEnabled)
        self.assertFalse(state.isInUse)
        self.assertEqual(0, state.port)
    
    def testPositionInterfaceState_FromGrpc(self):
        grpc1 = robotcontrolapp_pb2.MotionState.PositionInterfaceState()
        grpc1.is_enabled = True
        grpc1.is_in_use = True
        grpc1.port = 123
        state1 = PositionInterfaceState.FromGrpc(grpc1)
        self.assertTrue(state1.isEnabled)
        self.assertTrue(state1.isInUse)
        self.assertEqual(123, state1.port)

        grpc2 = robotcontrolapp_pb2.MotionState.PositionInterfaceState()
        grpc2.is_enabled = False
        grpc2.is_in_use = True
        grpc2.port = 123
        state2 = PositionInterfaceState.FromGrpc(grpc2)
        self.assertFalse(state2.isEnabled)
        self.assertTrue(state2.isInUse)
        self.assertEqual(123, state2.port)

        grpc3 = robotcontrolapp_pb2.MotionState.PositionInterfaceState()
        grpc3.is_enabled = True
        grpc3.is_in_use = False
        grpc3.port = 456
        state3 = PositionInterfaceState.FromGrpc(grpc3)
        self.assertTrue(state3.isEnabled)
        self.assertFalse(state3.isInUse)
        self.assertEqual(456, state3.port)
    
    def testMotionState_init(self):
        state = MotionState()
        self.assertEqual("", state.motionProgram.mainProgram)
        self.assertEqual("", state.logicProgram.mainProgram)
        self.assertEqual("", state.moveTo.mainProgram)
        self.assertEqual(0, state.positionInterface.port)

    def testMotionState_FromGrpc(self):
        grpc = robotcontrolapp_pb2.MotionState()
        grpc.motion_ipo.main_program_name = "Foo"
        grpc.logic_ipo.main_program_name = "Bar"
        grpc.move_to_ipo.main_program_name = "Baz"
        grpc.position_interface.port = 789

        state = MotionState.FromGrpc(grpc)
        self.assertEqual("Foo", state.motionProgram.mainProgram)
        self.assertEqual("Bar", state.logicProgram.mainProgram)
        self.assertEqual("Baz", state.moveTo.mainProgram)
        self.assertEqual(789, state.positionInterface.port)

if __name__ == "__main__":
    unittest.main()