from dataclasses import dataclass

from .Matrix44 import Matrix44, Matrix44FromGrpc
from ..rpc import robotcontrolapp_pb2


@dataclass
class Joint:
    """This class describes the state of a joint"""

    id: int = 0
    """Joint ID / index"""
    name: str = ""
    """Joint name"""
    actualPosition: float = 0.0
    """
        Actual hardware position in degrees, mm or user defined units.
        Consider using targetPosition for calculating motion to prevent creating a control loop.
    """
    targetPosition: float = 0.0
    """Target position in degrees, mm or user defined units"""
    hardwareState = robotcontrolapp_pb2.HardwareState.ERROR_MODULE_DEAD
    """Hardware state"""
    referencingState = robotcontrolapp_pb2.ReferencingState.NOT_REFERENCED
    """Referencing state"""

    temperatureBoard: float = 0.0
    """Temperature of the electronics in °C"""
    temperatureMotor: float = 0.0
    """Temperature of the motor in °C (available for some robots only)"""
    current: float = 0.0
    """Current draw of this joint in mA"""

    targetVelocity: float = 0.0
    """
    Target velocity in degrees/s, mm/s or user defined units per second - only usable with external axes in velocity
    mode
    """


def JointFromGrpc(grpc: robotcontrolapp_pb2.Joint) -> Joint:
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


@dataclass
class RobotState:
    """This class contains most relevant info about the robot's state, e.g. position, IO and errors"""

    def __init__(self):
        self.tcp: Matrix44 = Matrix44()
        """Position and orientation of the TCP in cartesian space (position in mm)"""
        self.platformX: float = 0.0
        """Mobile platform position X"""
        self.platformY: float = 0.0
        """Mobile platform position Y"""
        self.platformHeading: float = 0.0
        """Mobile platform heading in rad"""

        self.joints = [
            Joint(0, "A1"),
            Joint(1, "A2"),
            Joint(2, "A3"),
            Joint(3, "A4"),
            Joint(4, "A5"),
            Joint(5, "A6"),
            Joint(6, "E1"),
            Joint(7, "E2"),
            Joint(8, "E3"),
        ]
        """
        Joint angles/positions in degrees, mm or user defined units. Indices 0-5 are robot joints, 6-8 are external joints.
        """

        self.digitalInputs = [False] * 64
        """64 digital inputs"""
        self.digitalOutputs = [False] * 64
        """64 digital outputs"""
        self.globalSignals = [False] * 100
        """100 global signals"""

        self.hardwareState: str = ""
        """A string describing the combined state of all modules"""
        self.kinematicState = robotcontrolapp_pb2.KinematicState.KINEMATIC_NORMAL
        """Kinematic state / error"""

        self.velocityOverride: float = 0.0
        """The velocity override in percent 0.0..100.0"""
        self.cartesianVelocity: float = 0.0
        """The actual cartesian velocity in mm/s"""

        self.temperatureCPU: float = 0.0
        """Temperature of the robot control computer's CPU in °C"""
        self.supplyVoltage: float = 0.0
        """Voltage of the motor power supply in mV"""
        self.currentAll: float = 0.0
        """Combined current of all motors and DIO in mA (available for some robots only)"""

        self.referencingState = robotcontrolapp_pb2.ReferencingState.NOT_REFERENCED
        """Combined referencing state of all axes"""

    def IsEnabled(self) -> bool:
        """Checks whether all motors and IO modules are enabled. If false motion is not possible."""
        return self.hardwareState == "NoError"


def RobotStateFromGrpc(grpc: robotcontrolapp_pb2.RobotState) -> RobotState:
    """Initializes an object from GRPC MotionState"""
    result = RobotState()
    result.tcp = Matrix44FromGrpc(grpc.tcp)
    result.platformX = grpc.platform_pose.position.x
    result.platformY = grpc.platform_pose.position.y
    result.platformHeading = grpc.platform_pose.heading

    for i in range(min(len(result.joints), len(grpc.joints))):
        result.joints[i] = JointFromGrpc(grpc.joints[i])

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
