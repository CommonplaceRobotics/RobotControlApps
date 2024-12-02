from DataTypes.Matrix44 import Matrix44

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
        self.hardwareState = ""
        # Referencing state
        self.referencingState = ""

        # Temperature of the electronics in °C
        self.temperatureBoard = 0
        # Temperature of the motor in °C (available for some robots only)
        self.temperatureMotor = 0
        # Current draw of this joint in mA
        self.current = 0

        # Target velocity in degrees/s, mm/s or user defined units per second - only usable with external axes in velocity mode
        self.targetVelocity = 0
        
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
        self.joints[0].id = 1
        self.joints[0].id = 2
        self.joints[0].id = 3
        self.joints[0].id = 4
        self.joints[0].id = 5
        self.joints[0].id = 6
        self.joints[0].id = 7
        self.joints[0].id = 8
        self.joints[0].name = "A1"
        self.joints[0].name = "A2"
        self.joints[0].name = "A3"
        self.joints[0].name = "A4"
        self.joints[0].name = "A5"
        self.joints[0].name = "A6"
        self.joints[0].name = "E1"
        self.joints[0].name = "E2"
        self.joints[0].name = "E3"

        # 64 digital inputs
        self.digitalInputs = []
        # 64 digital outputs
        self.digitalOutputs = []
        # 100 global signals
        self.globalSignals = []

        # A string describing the combined state of all modules
        self.hardwareState = ""
        # Kinematic state / error
        self.kinematicState = ""
        
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
        self.referencingState = ""
