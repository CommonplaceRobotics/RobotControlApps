# This class contains system information that usually does not change (except for the cycle time statistics)
import robotcontrolapp_pb2


class SystemInfo:
    """This class contains system information that usually does not change (except for the cycle time statistics)"""

    versionMajor: int = 0
    """Robot control software version major, e.g. V14-003-1 -> 14"""
    versionMinor: int = 0
    """Robot control software version minor, e.g. V14-003-1 -> 3"""
    versionPatch: int = 0
    """Robot control software version patch, e.g. V14-003-1 -> 1"""
    version: str = ""
    """Robot control software version string, possibly with suffix, e.g. "V14-003-1-RC1"""

    projectFile: str = ""
    """Project file, e.g. "igus-REBEL/REBEL-6DOF-01.prj"""
    projectTitle: str = ""
    """User defined project title"""
    projectAuthor: str = ""
    """User defined project author"""
    robotType: str = ""
    """Robot type, e.g. "igus-REBEL/REBEL-6DOF-01"""

    voltage = robotcontrolapp_pb2.SystemInfo.Voltage24V
    """Voltage configuration of the robot - this selects the velocity limits"""
    systemType = robotcontrolapp_pb2.SystemInfo.Other
    """System type of the robot control"""
    deviceID: str = ""
    """Unique device ID"""
    isSimulation: bool = False
    """Is this robot simulated?"""

    cycleTimeTarget: float = 0.0
    """Robot main loop cycle time (hardware IO, kinematics, program execution) target in ms"""
    cycleTimeAverage: float = 0.0
    """Robot main loop cycle time average in ms"""
    cycleTimeMax: float = 0.0
    """Robot main loop cycle time recent maximum in ms"""
    cycleTimeMin: float = 0.0
    """Robot main loop cycle time recent minimum in ms"""
    workload: float = 0.0
    """Average workload in percent (how much of the available time is used vs. waited)"""

    robotAxisCount: int = 0
    """Number of robot joints"""
    externalAxisCount: int = 0
    """Number of external axes"""
    toolAxisCount: int = 0
    """Number of tool axes"""
    platformAxisCount: int = 0
    """Number of platform axes"""
    digitalIOModuleCount: int = 0
    """Number of digital IO modules"""


def SystemInfoFromGrpc(grpc: robotcontrolapp_pb2.SystemInfo) -> SystemInfo:
    """Creates an object from a GRPC SystemInfo"""
    self = SystemInfo()
    self.versionMajor = grpc.version_major
    self.versionMinor = grpc.version_minor
    self.versionPatch = grpc.version_patch
    self.version = grpc.version

    self.projectFile = grpc.project_file
    self.projectTitle = grpc.project_title
    self.projectAuthor = grpc.project_author
    self.robotType = grpc.robot_type

    self.voltage = grpc.voltage
    self.systemType = grpc.system_type
    self.deviceID = grpc.device_id
    self.isSimulation = grpc.is_simulation

    self.cycleTimeTarget = grpc.cycle_time_target
    self.cycleTimeAverage = grpc.cycle_time_avg
    self.cycleTimeMax = grpc.cycle_time_max
    self.cycleTimeMin = grpc.cycle_time_min
    self.workload = grpc.workload

    self.robotAxisCount = grpc.robot_axis_count
    self.externalAxisCount = grpc.external_axis_count
    self.toolAxisCount = grpc.tool_axis_count
    self.platformAxisCount = grpc.platform_axis_count
    self.digitalIOModuleCount = grpc.digital_io_module_count
    return self
