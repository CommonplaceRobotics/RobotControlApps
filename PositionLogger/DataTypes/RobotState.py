from DataTypes.Matrix44 import Matrix44
import robotcontrolapp_pb2


class Joint:
    """This class describes the state of a joint"""

    def __init__(self):
        self.id = 0
        """Joint ID / index"""
        self.name = ""
        """Joint name"""
        self.actualPosition = 0
        """Actual position in degrees, mm or user defined units"""
        self.targetPosition = 0
        """Target position in degrees, mm or user defined units"""
        self.hardwareState = robotcontrolapp_pb2.HardwareState.ERROR_MODULE_DEAD
        """Hardware state"""
        self.referencingState = robotcontrolapp_pb2.ReferencingState.NOT_REFERENCED
        """Referencing state"""

        self.temperatureBoard = 0
        """Temperature of the electronics in °C"""
        self.temperatureMotor = 0
        """Temperature of the motor in °C (available for some robots only)"""
        self.current = 0
        """Current draw of this joint in mA"""

        self.targetVelocity = 0
        """Target velocity in degrees/s, mm/s or user defined units per second - only usable with external axes in velocity mode"""

    def FromGrpc(grpc: robotcontrolapp_pb2.Joint):
        """Initializes an object from GRPC MotionState"""
        result = Joint()
        result.id = grpc.id
        result.name = grpc.name
        result.actualPosition = grpc.position.position
        result.targetPosition = grpc.position.target_position
        result.hardwareState = grpc.state
        result.referencingState = grpc.referencing_state
        result.temperatureBoard = grpc.temperature_board
        result.temperatureMotor = grpc.temperature_motor
        result.current = grpc.current
        result.targetVelocity = grpc.target_velocity
        return result


class RobotState:
    """This class contains most relevant info about the robot's state, e.g. position, IO and errors"""

    def __init__(self):
        self.tcp = Matrix44()
        """Position and orientation of the TCP in cartesian space (position in mm)"""
        self.platformX = 0.0
        """Mobile platform position X"""
        self.platformY = 0.0
        """Mobile platform position Y"""
        self.platformHeading = 0.0
        """Mobile platform heading in rad"""

        self.joints = [
            Joint(),
            Joint(),
            Joint(),
            Joint(),
            Joint(),
            Joint(),
            Joint(),
            Joint(),
            Joint(),
        ]
        """Joint angles/positions in degrees, mm or user defined units. Indices 0-5 are robot joints, 6-8 are external joints."""
        self.joints[0].id = 0
        self.joints[1].id = 1
        self.joints[2].id = 2
        self.joints[3].id = 3
        self.joints[4].id = 4
        self.joints[5].id = 5
        self.joints[6].id = 6
        self.joints[7].id = 7
        self.joints[8].id = 8
        self.joints[0].name = "A1"
        self.joints[1].name = "A2"
        self.joints[2].name = "A3"
        self.joints[3].name = "A4"
        self.joints[4].name = "A5"
        self.joints[5].name = "A6"
        self.joints[6].name = "E1"
        self.joints[7].name = "E2"
        self.joints[8].name = "E3"

        self.digitalInputs = []
        """64 digital inputs"""
        self.digitalOutputs = []
        """64 digital outputs"""
        self.globalSignals = []
        """100 global signals"""

        while len(self.digitalInputs) < 64:
            self.digitalInputs.append(False)
        while len(self.digitalOutputs) < 64:
            self.digitalOutputs.append(False)
        while len(self.globalSignals) < 100:
            self.globalSignals.append(False)

        self.hardwareState = ""
        """A string describing the combined state of all modules"""
        self.kinematicState = robotcontrolapp_pb2.KinematicState.KINEMATIC_NORMAL
        """Kinematic state / error"""

        self.velocityOverride = 0
        """The velocity override in percent 0.0..100.0"""
        self.cartesianVelocity = 0
        """The actual cartesian velocity in mm/s"""

        self.temperatureCPU = 0
        """Temperature of the robot control computer's CPU in °C"""
        self.supplyVoltage = 0
        """Voltage of the motor power supply in mV"""
        self.currentAll = 0
        """Combined current of all motors and DIO in mA (available for some robots only)"""

        self.referencingState = robotcontrolapp_pb2.ReferencingState.NOT_REFERENCED
        """Combined referencing state of all axes"""

    def IsEnabled(self) -> bool:
        """Checks whether all motors and IO modules are enabled. If false motion is not possible."""
        return self.hardwareState == "NoError"

    def FromGrpc(grpc: robotcontrolapp_pb2.RobotState):
        """Initializes an object from GRPC MotionState"""
        result = RobotState()
        result.tcp = Matrix44.FromGrpc(grpc.tcp)
        result.platformX = grpc.platform_pose.position.x
        result.platformY = grpc.platform_pose.position.y
        result.platformHeading = grpc.platform_pose.heading

        for i in range(min(len(result.joints), len(grpc.joints))):
            result.joints[i] = Joint.FromGrpc(grpc.joints[i])

        result.digitalInputs = []
        result.digitalOutputs = []
        result.globalSignals = []
        for i in range(len(grpc.DIns)):
            result.digitalInputs.append(
                grpc.DIns[i].state == robotcontrolapp_pb2.DIOState.HIGH
            )
        for i in range(len(grpc.DOuts)):
            result.digitalOutputs.append(
                grpc.DOuts[i].state == robotcontrolapp_pb2.DIOState.HIGH
            )
        for i in range(len(grpc.GSigs)):
            result.globalSignals.append(
                grpc.GSigs[i].state == robotcontrolapp_pb2.DIOState.HIGH
            )

        while len(result.digitalInputs) < 64:
            result.digitalInputs.append(False)
        while len(result.digitalOutputs) < 64:
            result.digitalOutputs.append(False)
        while len(result.globalSignals) < 100:
            result.globalSignals.append(False)

        result.hardwareState = grpc.hardware_state_string
        result.kinematicState = grpc.kinematic_state
        result.velocityOverride = grpc.velocity_override
        result.cartesianVelocity = grpc.cartesian_velocity
        result.temperatureCPU = grpc.temperature_cpu
        result.supplyVoltage = grpc.supply_voltage
        result.currentAll = grpc.current_all
        result.referencingState = grpc.referencing_state
        return result
