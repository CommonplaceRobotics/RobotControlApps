# This class contains system information that usually does not change (except for the cycle time statistics)
import robotcontrolapp_pb2


class SystemInfo:
    """This class contains system information that usually does not change (except for the cycle time statistics)"""

    def __init__(self):
        self.versionMajor = 0
        """Robot control software version major, e.g. V14-003-1 -> 14"""
        self.versionMinor = 0
        """Robot control software version minor, e.g. V14-003-1 -> 3"""
        self.versionPatch = 0
        """Robot control software version patch, e.g. V14-003-1 -> 1"""
        self.version = ""
        """Robot control software version string, possibly with suffix, e.g. "V14-003-1-RC1"""

        self.projectFile = ""
        """Project file, e.g. "igus-REBEL/REBEL-6DOF-01.prj"""
        self.projectTitle = ""
        """User defined project title"""
        self.projectAuthor = ""
        """User defined project author"""
        self.robotType = ""
        """Robot type, e.g. "igus-REBEL/REBEL-6DOF-01"""

        self.voltage = robotcontrolapp_pb2.SystemInfo.Voltage24V
        """Voltage configuration of the robot - this selects the velocity limits"""
        self.systemType = robotcontrolapp_pb2.SystemInfo.Other
        """System type of the robot control"""
        self.deviceID = ""
        """Unique device ID"""
        self.isSimulation = False
        """Is this robot simulated?"""

        self.cycleTimeTarget = 0
        """Robot main loop cycle time (hardware IO, kinematics, program execution) target in ms"""
        self.cycleTimeAverage = 0
        """Robot main loop cycle time average in ms"""
        self.cycleTimeMax = 0
        """Robot main loop cycle time recent maximum in ms"""
        self.cycleTimeMin = 0
        """Robot main loop cycle time recent minimum in ms"""
        self.workload = 0
        """Average workload in percent (how much of the available time is used vs. waited)"""

        self.robotAxisCount = 0
        """Number of robot joints"""
        self.externalAxisCount = 0
        """Number of external axes"""
        self.toolAxisCount = 0
        """Number of tool axes"""
        self.platformAxisCount = 0
        """Number of platform axes"""
        self.digitalIOModuleCount = 0
        """Number of digital IO modules"""

    def FromGrpc(grpc: robotcontrolapp_pb2.SystemInfo):
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
