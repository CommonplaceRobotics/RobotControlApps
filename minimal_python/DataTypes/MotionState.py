# This describes the state of one motion interpolator
import robotcontrolapp_pb2


class InterpolatorState:
    """This describes the state of one motion interpolator"""

    def __init__(self):
        self.runState = robotcontrolapp_pb2.NOT_RUNNING
        """Is the program running or paused?"""
        self.replayMode = robotcontrolapp_pb2.SINGLE
        """Should the program repeat or be run step by step?"""
        self.mainProgram = ""
        """Name of the main program"""
        self.currentProgram = ""
        """Name of the (sub-)program that is currently being executed"""

        self.currentProgramIndex = 0
        """Index of the (sub-)program that is currently being executed: 0 is the main program, higher numbers are sub-programs"""
        self.programCount = 0
        """Number of loaded programs: 0 - no programs, 1 - only the main program, higher values - the main and sub programs are loaded"""
        self.currentCommandIndex = 0
        """Index of the current command that is being executed. 0 is the first command in the current (sub-)program, -1 when not running."""
        self.commandCount = 0
        """Number of commands in the current (sub-)program"""

    def FromGrpc(grpc: robotcontrolapp_pb2.MotionState.InterpolatorState):
        """Initializes an object from GRPC InterpolatorState"""
        result = InterpolatorState()
        result.runState = grpc.runstate
        result.replayMode = grpc.replay_mode
        result.mainProgram = grpc.main_program_name
        result.currentProgram = grpc.current_program_name
        result.currentProgramIndex = grpc.current_program_idx
        result.programCount = grpc.program_count
        result.currentCommandIndex = grpc.current_command_idx
        result.commandCount = grpc.command_count
        return result


class PositionInterfaceState:
    """This describes the state of the fast position interface"""

    def __init__(self):
        self.isEnabled = False
        """Position interface is enabled - you can connect"""
        self.isInUse = False
        """Position interface is in use - you can move the robot"""
        self.port = 0
        """TCP/IP port number of the position interface"""

    def FromGrpc(grpc: robotcontrolapp_pb2.MotionState.PositionInterfaceState):
        """Initializes an object from GRPC PositionInterfaceState"""
        result = PositionInterfaceState()
        result.isEnabled = grpc.is_enabled
        result.isInUse = grpc.is_in_use
        result.port = grpc.port
        return result


class MotionState:
    """This class contains the state of the motion interpolators (which run the robot programs)"""

    def __init__(self):
        self.motionProgram = InterpolatorState()
        """State of the motion program"""
        self.logicProgram = InterpolatorState()
        """State of the logic program"""
        self.moveTo = InterpolatorState()
        """State of the Move-To interpolator (expect 0 or 1 program with only 1 command)"""
        self.positionInterface = PositionInterfaceState()
        """State of the fast position interface"""
        self.requestSuccessful = False
        """If this MotionState was sent in response to a request (specifically program load, start and move-to starts) this value is set true if the request was successful"""

    def FromGrpc(grpc: robotcontrolapp_pb2.MotionState):
        """Initializes an object from GRPC MotionState"""
        result = MotionState()
        result.motionProgram = InterpolatorState.FromGrpc(grpc.motion_ipo)
        result.logicProgram = InterpolatorState.FromGrpc(grpc.logic_ipo)
        result.moveTo = InterpolatorState.FromGrpc(grpc.move_to_ipo)
        result.positionInterface = PositionInterfaceState.FromGrpc(
            grpc.position_interface
        )
        if grpc.HasField("request_successful"):
            result.requestSuccessful = grpc.request_successful
        return result
