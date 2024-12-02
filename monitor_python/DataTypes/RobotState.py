from DataTypes.Matrix44 import Matrix44
import robotcontrolapp_pb2

class Joint:
    """This class describes the state of a joint"""
    def __init__(self):
        # Joint ID / index
        self.id = 0
        # Joint name
        self.name = ""
        # Actual position in degrees, mm or user defined units
        self.actualPosition = 0
        # Target position in degrees, mm or user defined units
        self.targetPosition = 0
        # Hardware state
        self.hardwareState = robotcontrolapp_pb2.HardwareState.ERROR_MODULE_DEAD
        # Referencing state
        self.referencingState = robotcontrolapp_pb2.ReferencingState.NOT_REFERENCED

        # Temperature of the electronics in °C
        self.temperatureBoard = 0
        # Temperature of the motor in °C (available for some robots only)
        self.temperatureMotor = 0
        # Current draw of this joint in mA
        self.current = 0

        # Target velocity in degrees/s, mm/s or user defined units per second - only usable with external axes in velocity mode
        self.targetVelocity = 0

    def FromGrpc(grpc: robotcontrolapp_pb2.Joint):
        """Constructs a Joint from a GRPC object"""
        joint = Joint()
        joint.id = grpc.id
        joint.name = grpc.name
        joint.actualPosition = grpc.position.position
        joint.targetPosition = grpc.position.target_position
        joint.hardwareState = grpc.state
        joint.referencingState = grpc.referencing_state
        joint.temperatureBoard = grpc.temperature_board
        joint.temperatureMotor = grpc.temperature_motor
        joint.current = grpc.current
        joint.targetVelocity = grpc.target_velocity
        return joint
        
class RobotState:
    """This class contains most relevant info about the robot's state, e.g. position, IO and errors"""
    def __init__(self):
        # Position and orientation of the TCP in cartesian space (position in mm)
        self.tcp = Matrix44()
        # Mobile platform position X
        self.platformX = 0.0
        # Mobile platform position Y
        self.platformY = 0.0
        # Mobile platform heading in rad
        self.platformHeading = 0.0

        # Joint angles/positions in degrees, mm or user defined units. Indices 0-5 are robot joints, 6-8 are external joints.
        self.joints = [
            Joint(),
            Joint(),
            Joint(),
            Joint(),
            Joint(),
            Joint(),
            Joint(),
            Joint(),
            Joint()
        ]
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

        # 64 digital inputs
        self.digitalInputs = []
        # 64 digital outputs
        self.digitalOutputs = []
        # 100 global signals
        self.globalSignals = []
        # Fill arrays
        for a in range(64):
            self.digitalInputs.append(False)
            self.digitalOutputs.append(False)
        for a in range(100):
            self.globalSignals.append(False)

        # A string describing the combined state of all modules
        self.hardwareState = ""
        # Kinematic state / error
        self.kinematicState = robotcontrolapp_pb2.KINEMATIC_NORMAL
        
        # The velocity override in percent 0.0..1.0
        self.velocityOverride = 0
        # The actual cartesian velocity in mm/s
        self.cartesianVelocity = 0

        # Temperature of the robot control computer's CPU in °C
        self.temperatureCPU = 0
        # Voltage of the motor power supply in mV
        self.supplyVoltage = 0
        # Combined current of all motors and DIO in mA (available for some robots only)
        self.currentAll = 0

        # Combined referencing state of all axes
        self.referencingState = robotcontrolapp_pb2.ReferencingState.NOT_REFERENCED

    def FromGrpc(grpc: robotcontrolapp_pb2.RobotState):
        """Constructs a RobotState from a GRPC object"""
        state = RobotState()
        state.tcp = Matrix44.FromGrpc(grpc.tcp)
        state.platformX = grpc.platform_pose.position.x
        state.platformY = grpc.platform_pose.position.y
        state.platformHeading = grpc.platform_pose.heading
        
        for i in range(0, min(9, len(grpc.joints))):
            state.joints[i] = Joint.FromGrpc(grpc.joints[i])
        
        for i in range(0, min(64, len(grpc.DIns))):
            state.digitalInputs[i] = grpc.DIns[i].state == robotcontrolapp_pb2.HIGH
        for i in range(0, min(64, len(grpc.DOuts))):
            state.digitalOutputs[i] = grpc.DOuts[i].state == robotcontrolapp_pb2.HIGH
        for i in range(0, min(100, len(grpc.GSigs))):
            state.globalSignals[i] = grpc.GSigs[i].state == robotcontrolapp_pb2.HIGH

        state.hardwareState = grpc.hardware_state_string
        state.kinematicState = grpc.kinematic_state
        
        state.velocityOverride = grpc.velocity_override
        state.cartesianVelocity = grpc.cartesian_velocity

        state.temperatureCPU = grpc.temperature_cpu
        state.supplyVoltage = grpc.supply_voltage
        state.currentAll = grpc.current_all

        state.referencingState = grpc.referencing_state
        return state
