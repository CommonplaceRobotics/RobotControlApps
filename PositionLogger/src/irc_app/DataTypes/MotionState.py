# This describes the state of one motion interpolator
from dataclasses import dataclass

from ..rpc import robotcontrolapp_pb2


@dataclass
class InterpolatorState:
    """This describes the state of one motion interpolator"""

    runState = robotcontrolapp_pb2.NOT_RUNNING
    """Is the program running or paused?"""
    replayMode = robotcontrolapp_pb2.SINGLE
    """Should the program repeat or be run step by step?"""
    mainProgram: str = ""
    """Name of the main program"""
    currentProgram: str = ""
    """Name of the (sub-)program that is currently being executed"""

    currentProgramIndex: int = 0
    """
    Index of the (sub-)program that is currently being executed: 0 is the main program, higher numbers are sub-programs
    """
    programCount: int = 0
    """
    Number of loaded programs: 0 - no programs, 1 - only the main program, higher values - the main and sub programs are
    loaded
    """
    currentCommandIndex: int = 0
    """
    Index of the current command that is being executed. 0 is the first command in the current (sub-)program, -1 when
    not running.
    """
    commandCount: int = 0
    """Number of commands in the current (sub-)program"""


def InterpolatorStateFromGrpc(
    grpc: robotcontrolapp_pb2.MotionState.InterpolatorState,
) -> InterpolatorState:
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


@dataclass
class PositionInterfaceState:
    """This describes the state of the fast position interface"""

    isEnabled: bool = False
    """Position interface is enabled - you can connect"""
    isInUse: bool = False
    """Position interface is in use - you can move the robot"""
    port: int = 0
    """TCP/IP port number of the position interface"""


def PositionInterfaceStateFromGrpc(
    grpc: robotcontrolapp_pb2.MotionState.PositionInterfaceState,
) -> PositionInterfaceState:
    """Initializes an object from GRPC PositionInterfaceState"""
    result = PositionInterfaceState()
    result.isEnabled = grpc.is_enabled
    result.isInUse = grpc.is_in_use
    result.port = grpc.port
    return result


@dataclass
class MotionState:
    """This class contains the state of the motion interpolators (which run the robot programs)"""

    motionProgram = InterpolatorState()
    """State of the motion program"""
    logicProgram = InterpolatorState()
    """State of the logic program"""
    moveTo = InterpolatorState()
    """State of the Move-To interpolator (expect 0 or 1 program with only 1 command)"""
    positionInterface = PositionInterfaceState()
    """State of the fast position interface"""
    requestSuccessful: bool = False
    """
    If this MotionState was sent in response to a request (specifically program load, start and move-to starts) this value
    is set true if the request was successful
    """


def MotionStateFromGrpc(grpc: robotcontrolapp_pb2.MotionState) -> MotionState:
    """Initializes an object from GRPC MotionState"""
    result = MotionState()
    result.motionProgram = InterpolatorStateFromGrpc(grpc.motion_ipo)
    result.logicProgram = InterpolatorStateFromGrpc(grpc.logic_ipo)
    result.moveTo = InterpolatorStateFromGrpc(grpc.move_to_ipo)
    result.positionInterface = PositionInterfaceStateFromGrpc(grpc.position_interface)
    if grpc.HasField("request_successful"):
        result.requestSuccessful = grpc.request_successful
    return result
