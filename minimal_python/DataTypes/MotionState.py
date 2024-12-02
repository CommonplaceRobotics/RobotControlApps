# This describes the state of one motion interpolator
import robotcontrolapp_pb2

class InterpolatorState:
    """This describes the state of one motion interpolator"""
    def __init__(self):
        # Is the program running or paused?
        self.runState = robotcontrolapp_pb2.NOT_RUNNING
        # Should the program repeat or be run step by step?
        self.replayMode = robotcontrolapp_pb2.SINGLE
        # Name of the main program
        self.mainProgram = ""
        # Name of the (sub-)program that is currently being executed
        self.currentProgram = ""

        # Index of the (sub-)program that is currently being executed: 0 is the main program, higher numbers are sub-programs
        self.currentProgramIndex = 0
        # Number of loaded programs: 0 - no programs, 1 - only the main program, higher values - the main and sub programs are loaded
        self.programCount = 0
        # Index of the current command that is being executed. 0 is the first command in the current (sub-)program
        self.currentCommandIndex = 0
        # Number of commands in the current (sub-)program
        self.commandCount = 0

    def FromGrpc(grpc: robotcontrolapp_pb2.MotionState.InterpolatorState) -> InterpolatorState:
        """Initializes an object from GRPC InterpolatorState"""
        self = InterpolatorState()
        self.runState = grpc.runstate
        self.replayMode = grpc.replay_mode
        self.mainProgram = grpc.main_program_name
        self.currentProgram = grpc.current_program_name
        self.currentCommandIndex = grpc.current_command_idx
        self.programCount = grpc.program_count
        self.currentCommandIndex = grpc.current_command_idx
        self.commandCount = grpc.command_count
        return self

class PositionInterfaceState:
    """This describes the state of the fast position interface"""
    def __init__(self):
        self.isEnabled = False
        self.isInUse = False
        self.port = 0

    def FromGrpc(grpc: robotcontrolapp_pb2.MotionState.PositionInterfaceState) -> PositionInterfaceState:
        """Initializes an object from GRPC PositionInterfaceState"""
        self = PositionInterfaceState()
        self.isEnabled = grpc.is_enabled
        self.isInUse = grpc.is_in_use
        self.port = grpc.port
        return self

class MotionState:
    """This class contains the state of the motion interpolators (which run the robot programs)"""
    def __init__(self):
        self.motionProgram = InterpolatorState()
        self.logicProgram = InterpolatorState()
        self.moveTo = InterpolatorState()
        self.positionInterface = PositionInterfaceState()

    def FromGrpc(grpc: robotcontrolapp_pb2.MotionState) -> MotionState:
        """Initializes an object from GRPC MotionState"""
        self = MotionState()
        self.motionProgram = InterpolatorState.FromGrpc(grpc.motion_ipo)
        self.logicProgram = InterpolatorState.FromGrpc(grpc.logic_ipo)
        self.moveTo = InterpolatorState.FromGrpc(grpc.move_to_ipo)
        self.positionInterface = PositionInterfaceState.FromGrpc(grpc.position_interface)
        return self