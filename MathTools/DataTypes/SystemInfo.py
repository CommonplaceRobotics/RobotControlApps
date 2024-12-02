# This class contains system information that usually does not change (except for the cycle time statistics)
import robotcontrolapp_pb2

class SystemInfo:
    """This class contains system information that usually does not change (except for the cycle time statistics)"""

    def __init__(self):
        self.versionMajor = 0
        self.versionMinor = 0
        self.versionPatch = 0
        self.version = ""

        self.projectFile = ""
        self.projectTitle = ""
        self.projectAuthor = ""
        self.robotType = ""

        self.voltage = robotcontrolapp_pb2.SystemInfo.Voltage24V
        self.systemType = robotcontrolapp_pb2.SystemInfo.Other
        self.deviceID = ""
        self.isSimulation = False

        self.cycleTimeTarget = 0
        self.cycleTimeAverage = 0
        self.cycleTimeMax = 0
        self.cycleTimeMin = 0

        self.robotAxisCount = 0
        self.externalAxisCount = 0
        self.toolAxisCount = 0
        self.platformAxisCount = 0
        self.digitalIOModuleCount = 0

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

        self.robotAxisCount = grpc.robot_axis_count
        self.externalAxisCount = grpc.external_axis_count
        self.toolAxisCount = grpc.tool_axis_count
        self.platformAxisCount = grpc.platform_axis_count
        self.digitalIOModuleCount = grpc.digital_io_module_count
        return self