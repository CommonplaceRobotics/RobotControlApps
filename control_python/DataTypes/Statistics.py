import robotcontrolapp_pb2


class Statistics:
    """This class contains statistics data"""

    def __init__(self):
        self.uptimeComplete = 0
        """Total uptime in minutes"""
        self.uptimeLast = 0
        """Uptime till previous shutdown in minutes"""
        self.uptimeEnabled = 0
        """Total time in motors enabled state in minutes"""
        self.uptimeMotion = 0
        """Total time with axes in motion in minutes"""

        self.programStartsTotal = 0
        """Total number of program starts"""
        self.programStartsLast = 0
        """Number of program starts since startup"""
        self.programDurationLast = 0
        """Duration of the previous program run in seconds"""

        self.partsGood = 0.0
        """Number of good parts (number variable #parts-good)"""
        self.partsBad = 0.0
        """Number of bad parts (number variable #parts-bad)"""

        self.robotAxisDirectionChanges = []
        """Number of direction changes of the robot axes"""
        self.externalAxisDirectionChanges = []
        """Number of direction changes of the external axes"""

    def FromGrpc(grpc: robotcontrolapp_pb2.StatisticsResponse):
        """Initializes an object from GRPC StatisticsResponse"""
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
