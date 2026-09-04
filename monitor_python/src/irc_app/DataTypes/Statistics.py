from dataclasses import dataclass, field

from ..rpc import robotcontrolapp_pb2


@dataclass
class Statistics:
    """This class contains statistics data"""

    uptimeComplete: int = 0
    """Total uptime in minutes"""
    uptimeLast: int = 0
    """Uptime till previous shutdown in minutes"""
    uptimeEnabled: int = 0
    """Total time in motors enabled state in minutes"""
    uptimeMotion: int = 0
    """Total time with axes in motion in minutes"""

    programStartsTotal: int = 0
    """Total number of program starts"""
    programStartsLast: int = 0
    """Number of program starts since startup"""
    programDurationLast: float = 0
    """Duration of the previous program run in seconds"""

    partsGood: float = 0.0
    """Number of good parts (number variable #parts-good)"""
    partsBad: float = 0.0
    """Number of bad parts (number variable #parts-bad)"""

    robotAxisDirectionChanges: list[int] = field(default_factory=list)
    """Number of direction changes of the robot axes"""
    externalAxisDirectionChanges: list[int] = field(default_factory=list)
    """Number of direction changes of the external axes"""


def StatisticsFromGrpc(grpc: robotcontrolapp_pb2.StatisticsResponse) -> Statistics:
    """Initializes an Statistics object from GRPC StatisticsResponse"""
    result = Statistics()

    result.uptimeComplete = grpc.uptime_complete
    result.uptimeLast = grpc.uptime_last
    result.uptimeEnabled = grpc.uptime_enabled
    result.uptimeMotion = grpc.uptime_motion

    result.programStartsTotal = grpc.program_starts_total
    result.programStartsLast = grpc.program_starts_last
    result.programDurationLast = grpc.program_duration_last

    result.partsGood = grpc.parts_good
    result.partsBad = grpc.parts_bad

    for a in grpc.robot_axis_direction_changes:
        result.robotAxisDirectionChanges.append(a)
    for a in grpc.external_axis_direction_changes:
        result.externalAxisDirectionChanges.append(a)

    return result
