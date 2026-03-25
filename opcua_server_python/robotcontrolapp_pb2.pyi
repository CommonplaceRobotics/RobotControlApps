from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DIOState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    LOW: _ClassVar[DIOState]
    HIGH: _ClassVar[DIOState]

class HardwareState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    OKAY: _ClassVar[HardwareState]
    ERROR_OVERTEMP: _ClassVar[HardwareState]
    ERROR_ESTOP_LOW_VOLTAGE: _ClassVar[HardwareState]
    ERROR_MOTOR_NOT_ENABLED: _ClassVar[HardwareState]
    ERROR_COMMUNICATION: _ClassVar[HardwareState]
    ERROR_POSITION_LAG: _ClassVar[HardwareState]
    ERROR_ENCODER: _ClassVar[HardwareState]
    ERROR_OVERCURRENT: _ClassVar[HardwareState]
    ERROR_DRIVER: _ClassVar[HardwareState]
    ERROR_BUS_DEAD: _ClassVar[HardwareState]
    ERROR_MODULE_DEAD: _ClassVar[HardwareState]
    ERROR_NOTREADY: _ClassVar[HardwareState]

class KinematicState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    KINEMATIC_NORMAL: _ClassVar[KinematicState]
    KINEMATIC_ERROR_ErrGeneral: _ClassVar[KinematicState]
    KINEMATIC_ERROR_LINKAGE_LIMITED: _ClassVar[KinematicState]
    KINEMATIC_ERROR_JOINT_LIMIT_MIN: _ClassVar[KinematicState]
    KINEMATIC_ERROR_JOINT_LIMIT_MAX: _ClassVar[KinematicState]
    KINEMATIC_ERROR_JOINT_DIFF_MIN: _ClassVar[KinematicState]
    KINEMATIC_ERROR_JOINT_DIFF_MAX: _ClassVar[KinematicState]
    KINEMATIC_ERROR_CENTER_SINGULARITY: _ClassVar[KinematicState]
    KINEMATIC_ERROR_OUT_OF_REACH: _ClassVar[KinematicState]
    KINEMATIC_ERROR_WRIST_SINGULARITY: _ClassVar[KinematicState]
    KINEMATIC_ERROR_TRILATERATION: _ClassVar[KinematicState]
    KINEMATIC_ERROR_VIRTUAL_BOX_X_POS: _ClassVar[KinematicState]
    KINEMATIC_ERROR_VIRTUAL_BOX_X_NEG: _ClassVar[KinematicState]
    KINEMATIC_ERROR_VIRTUAL_BOX_Y_POS: _ClassVar[KinematicState]
    KINEMATIC_ERROR_VIRTUAL_BOX_Y_NEG: _ClassVar[KinematicState]
    KINEMATIC_ERROR_VIRTUAL_BOX_Z_POS: _ClassVar[KinematicState]
    KINEMATIC_ERROR_VIRTUAL_BOX_Z_NEG: _ClassVar[KinematicState]
    KINEMATIC_ERROR_JOINT_NAN: _ClassVar[KinematicState]
    KINEMATIC_ERROR_VELOCITY_LIMIT_EXCEEDED: _ClassVar[KinematicState]
    KINEMATIC_ERROR_VARIABLE_NOT_FOUND: _ClassVar[KinematicState]
    KINEMATIC_ERROR_BRAKE_ACTIVE: _ClassVar[KinematicState]
    KINEMATIC_ERROR_MOTION_NOT_ALLOWED: _ClassVar[KinematicState]

class ReferencingState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    NOT_REFERENCED: _ClassVar[ReferencingState]
    IS_REFERENCING: _ClassVar[ReferencingState]
    IS_REFERENCED: _ClassVar[ReferencingState]

class RunState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    NOT_RUNNING: _ClassVar[RunState]
    RUNNING: _ClassVar[RunState]
    PAUSED: _ClassVar[RunState]

class ReplayMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SINGLE: _ClassVar[ReplayMode]
    REPEAT: _ClassVar[ReplayMode]
    STEP: _ClassVar[ReplayMode]

class ButtonState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    NOT_CLICKED: _ClassVar[ButtonState]
    CLICKED: _ClassVar[ButtonState]

class CheckboxState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UNCHECKED: _ClassVar[CheckboxState]
    CHECKED: _ClassVar[CheckboxState]
LOW: DIOState
HIGH: DIOState
OKAY: HardwareState
ERROR_OVERTEMP: HardwareState
ERROR_ESTOP_LOW_VOLTAGE: HardwareState
ERROR_MOTOR_NOT_ENABLED: HardwareState
ERROR_COMMUNICATION: HardwareState
ERROR_POSITION_LAG: HardwareState
ERROR_ENCODER: HardwareState
ERROR_OVERCURRENT: HardwareState
ERROR_DRIVER: HardwareState
ERROR_BUS_DEAD: HardwareState
ERROR_MODULE_DEAD: HardwareState
ERROR_NOTREADY: HardwareState
KINEMATIC_NORMAL: KinematicState
KINEMATIC_ERROR_ErrGeneral: KinematicState
KINEMATIC_ERROR_LINKAGE_LIMITED: KinematicState
KINEMATIC_ERROR_JOINT_LIMIT_MIN: KinematicState
KINEMATIC_ERROR_JOINT_LIMIT_MAX: KinematicState
KINEMATIC_ERROR_JOINT_DIFF_MIN: KinematicState
KINEMATIC_ERROR_JOINT_DIFF_MAX: KinematicState
KINEMATIC_ERROR_CENTER_SINGULARITY: KinematicState
KINEMATIC_ERROR_OUT_OF_REACH: KinematicState
KINEMATIC_ERROR_WRIST_SINGULARITY: KinematicState
KINEMATIC_ERROR_TRILATERATION: KinematicState
KINEMATIC_ERROR_VIRTUAL_BOX_X_POS: KinematicState
KINEMATIC_ERROR_VIRTUAL_BOX_X_NEG: KinematicState
KINEMATIC_ERROR_VIRTUAL_BOX_Y_POS: KinematicState
KINEMATIC_ERROR_VIRTUAL_BOX_Y_NEG: KinematicState
KINEMATIC_ERROR_VIRTUAL_BOX_Z_POS: KinematicState
KINEMATIC_ERROR_VIRTUAL_BOX_Z_NEG: KinematicState
KINEMATIC_ERROR_JOINT_NAN: KinematicState
KINEMATIC_ERROR_VELOCITY_LIMIT_EXCEEDED: KinematicState
KINEMATIC_ERROR_VARIABLE_NOT_FOUND: KinematicState
KINEMATIC_ERROR_BRAKE_ACTIVE: KinematicState
KINEMATIC_ERROR_MOTION_NOT_ALLOWED: KinematicState
NOT_REFERENCED: ReferencingState
IS_REFERENCING: ReferencingState
IS_REFERENCED: ReferencingState
NOT_RUNNING: RunState
RUNNING: RunState
PAUSED: RunState
SINGLE: ReplayMode
REPEAT: ReplayMode
STEP: ReplayMode
NOT_CLICKED: ButtonState
CLICKED: ButtonState
UNCHECKED: CheckboxState
CHECKED: CheckboxState

class CapabilitiesRequest(_message.Message):
    __slots__ = ("app_name", "api_version_major", "api_version_minor", "api_version_patch")
    APP_NAME_FIELD_NUMBER: _ClassVar[int]
    API_VERSION_MAJOR_FIELD_NUMBER: _ClassVar[int]
    API_VERSION_MINOR_FIELD_NUMBER: _ClassVar[int]
    API_VERSION_PATCH_FIELD_NUMBER: _ClassVar[int]
    app_name: str
    api_version_major: int
    api_version_minor: int
    api_version_patch: int
    def __init__(self, app_name: _Optional[str] = ..., api_version_major: _Optional[int] = ..., api_version_minor: _Optional[int] = ..., api_version_patch: _Optional[int] = ...) -> None: ...

class CapabilitiesResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class SystemInfoRequest(_message.Message):
    __slots__ = ("app_name",)
    APP_NAME_FIELD_NUMBER: _ClassVar[int]
    app_name: str
    def __init__(self, app_name: _Optional[str] = ...) -> None: ...

class SystemInfo(_message.Message):
    __slots__ = ("version_major", "version_minor", "version_patch", "version", "system_type", "is_simulation", "project_file", "project_title", "project_author", "robot_type", "voltage", "device_id", "cycle_time_target", "cycle_time_avg", "cycle_time_max", "cycle_time_min", "workload", "robot_axis_count", "external_axis_count", "tool_axis_count", "platform_axis_count", "digital_io_module_count")
    class SystemType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        Other: _ClassVar[SystemInfo.SystemType]
        Windows: _ClassVar[SystemInfo.SystemType]
        Raspberry: _ClassVar[SystemInfo.SystemType]
        Linux_x86: _ClassVar[SystemInfo.SystemType]
    Other: SystemInfo.SystemType
    Windows: SystemInfo.SystemType
    Raspberry: SystemInfo.SystemType
    Linux_x86: SystemInfo.SystemType
    class Voltage(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        Voltage24V: _ClassVar[SystemInfo.Voltage]
        Voltage48V: _ClassVar[SystemInfo.Voltage]
    Voltage24V: SystemInfo.Voltage
    Voltage48V: SystemInfo.Voltage
    VERSION_MAJOR_FIELD_NUMBER: _ClassVar[int]
    VERSION_MINOR_FIELD_NUMBER: _ClassVar[int]
    VERSION_PATCH_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    SYSTEM_TYPE_FIELD_NUMBER: _ClassVar[int]
    IS_SIMULATION_FIELD_NUMBER: _ClassVar[int]
    PROJECT_FILE_FIELD_NUMBER: _ClassVar[int]
    PROJECT_TITLE_FIELD_NUMBER: _ClassVar[int]
    PROJECT_AUTHOR_FIELD_NUMBER: _ClassVar[int]
    ROBOT_TYPE_FIELD_NUMBER: _ClassVar[int]
    VOLTAGE_FIELD_NUMBER: _ClassVar[int]
    DEVICE_ID_FIELD_NUMBER: _ClassVar[int]
    CYCLE_TIME_TARGET_FIELD_NUMBER: _ClassVar[int]
    CYCLE_TIME_AVG_FIELD_NUMBER: _ClassVar[int]
    CYCLE_TIME_MAX_FIELD_NUMBER: _ClassVar[int]
    CYCLE_TIME_MIN_FIELD_NUMBER: _ClassVar[int]
    WORKLOAD_FIELD_NUMBER: _ClassVar[int]
    ROBOT_AXIS_COUNT_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_AXIS_COUNT_FIELD_NUMBER: _ClassVar[int]
    TOOL_AXIS_COUNT_FIELD_NUMBER: _ClassVar[int]
    PLATFORM_AXIS_COUNT_FIELD_NUMBER: _ClassVar[int]
    DIGITAL_IO_MODULE_COUNT_FIELD_NUMBER: _ClassVar[int]
    version_major: int
    version_minor: int
    version_patch: int
    version: str
    system_type: SystemInfo.SystemType
    is_simulation: bool
    project_file: str
    project_title: str
    project_author: str
    robot_type: str
    voltage: SystemInfo.Voltage
    device_id: str
    cycle_time_target: float
    cycle_time_avg: float
    cycle_time_max: float
    cycle_time_min: float
    workload: float
    robot_axis_count: int
    external_axis_count: int
    tool_axis_count: int
    platform_axis_count: int
    digital_io_module_count: int
    def __init__(self, version_major: _Optional[int] = ..., version_minor: _Optional[int] = ..., version_patch: _Optional[int] = ..., version: _Optional[str] = ..., system_type: _Optional[_Union[SystemInfo.SystemType, str]] = ..., is_simulation: bool = ..., project_file: _Optional[str] = ..., project_title: _Optional[str] = ..., project_author: _Optional[str] = ..., robot_type: _Optional[str] = ..., voltage: _Optional[_Union[SystemInfo.Voltage, str]] = ..., device_id: _Optional[str] = ..., cycle_time_target: _Optional[float] = ..., cycle_time_avg: _Optional[float] = ..., cycle_time_max: _Optional[float] = ..., cycle_time_min: _Optional[float] = ..., workload: _Optional[float] = ..., robot_axis_count: _Optional[int] = ..., external_axis_count: _Optional[int] = ..., tool_axis_count: _Optional[int] = ..., platform_axis_count: _Optional[int] = ..., digital_io_module_count: _Optional[int] = ...) -> None: ...

class RobotStateRequest(_message.Message):
    __slots__ = ("app_name",)
    APP_NAME_FIELD_NUMBER: _ClassVar[int]
    app_name: str
    def __init__(self, app_name: _Optional[str] = ...) -> None: ...

class ProgramVariablesRequest(_message.Message):
    __slots__ = ("app_name", "variable_names")
    APP_NAME_FIELD_NUMBER: _ClassVar[int]
    VARIABLE_NAMES_FIELD_NUMBER: _ClassVar[int]
    app_name: str
    variable_names: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, app_name: _Optional[str] = ..., variable_names: _Optional[_Iterable[str]] = ...) -> None: ...

class SetProgramVariablesRequest(_message.Message):
    __slots__ = ("app_name", "variables")
    APP_NAME_FIELD_NUMBER: _ClassVar[int]
    VARIABLES_FIELD_NUMBER: _ClassVar[int]
    app_name: str
    variables: _containers.RepeatedCompositeFieldContainer[ProgramVariable]
    def __init__(self, app_name: _Optional[str] = ..., variables: _Optional[_Iterable[_Union[ProgramVariable, _Mapping]]] = ...) -> None: ...

class SetProgramVariablesResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetTCPRequest(_message.Message):
    __slots__ = ("app_name",)
    APP_NAME_FIELD_NUMBER: _ClassVar[int]
    app_name: str
    def __init__(self, app_name: _Optional[str] = ...) -> None: ...

class GetMotionStateRequest(_message.Message):
    __slots__ = ("app_name",)
    APP_NAME_FIELD_NUMBER: _ClassVar[int]
    app_name: str
    def __init__(self, app_name: _Optional[str] = ...) -> None: ...

class Vector3(_message.Message):
    __slots__ = ("x", "y", "z")
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    Z_FIELD_NUMBER: _ClassVar[int]
    x: float
    y: float
    z: float
    def __init__(self, x: _Optional[float] = ..., y: _Optional[float] = ..., z: _Optional[float] = ...) -> None: ...

class Matrix44(_message.Message):
    __slots__ = ("data",)
    DATA_FIELD_NUMBER: _ClassVar[int]
    data: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, data: _Optional[_Iterable[float]] = ...) -> None: ...

class DIn(_message.Message):
    __slots__ = ("id", "state")
    ID_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    id: int
    state: DIOState
    def __init__(self, id: _Optional[int] = ..., state: _Optional[_Union[DIOState, str]] = ...) -> None: ...

class DOut(_message.Message):
    __slots__ = ("id", "state", "target_state")
    ID_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    TARGET_STATE_FIELD_NUMBER: _ClassVar[int]
    id: int
    state: DIOState
    target_state: DIOState
    def __init__(self, id: _Optional[int] = ..., state: _Optional[_Union[DIOState, str]] = ..., target_state: _Optional[_Union[DIOState, str]] = ...) -> None: ...

class GSig(_message.Message):
    __slots__ = ("id", "state", "target_state")
    ID_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    TARGET_STATE_FIELD_NUMBER: _ClassVar[int]
    id: int
    state: DIOState
    target_state: DIOState
    def __init__(self, id: _Optional[int] = ..., state: _Optional[_Union[DIOState, str]] = ..., target_state: _Optional[_Union[DIOState, str]] = ...) -> None: ...

class Joint(_message.Message):
    __slots__ = ("id", "name", "position", "state", "referencing_state", "temperature_board", "temperature_motor", "current", "target_velocity")
    class JointPosition(_message.Message):
        __slots__ = ("position", "target_position")
        POSITION_FIELD_NUMBER: _ClassVar[int]
        TARGET_POSITION_FIELD_NUMBER: _ClassVar[int]
        position: float
        target_position: float
        def __init__(self, position: _Optional[float] = ..., target_position: _Optional[float] = ...) -> None: ...
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    POSITION_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    REFERENCING_STATE_FIELD_NUMBER: _ClassVar[int]
    TEMPERATURE_BOARD_FIELD_NUMBER: _ClassVar[int]
    TEMPERATURE_MOTOR_FIELD_NUMBER: _ClassVar[int]
    CURRENT_FIELD_NUMBER: _ClassVar[int]
    TARGET_VELOCITY_FIELD_NUMBER: _ClassVar[int]
    id: int
    name: str
    position: Joint.JointPosition
    state: HardwareState
    referencing_state: ReferencingState
    temperature_board: float
    temperature_motor: float
    current: float
    target_velocity: float
    def __init__(self, id: _Optional[int] = ..., name: _Optional[str] = ..., position: _Optional[_Union[Joint.JointPosition, _Mapping]] = ..., state: _Optional[_Union[HardwareState, str]] = ..., referencing_state: _Optional[_Union[ReferencingState, str]] = ..., temperature_board: _Optional[float] = ..., temperature_motor: _Optional[float] = ..., current: _Optional[float] = ..., target_velocity: _Optional[float] = ...) -> None: ...

class PlatformPose(_message.Message):
    __slots__ = ("position", "heading")
    POSITION_FIELD_NUMBER: _ClassVar[int]
    HEADING_FIELD_NUMBER: _ClassVar[int]
    position: Vector3
    heading: float
    def __init__(self, position: _Optional[_Union[Vector3, _Mapping]] = ..., heading: _Optional[float] = ...) -> None: ...

class RobotState(_message.Message):
    __slots__ = ("tcp", "platform_pose", "joints", "DIns", "DOuts", "GSigs", "hardware_state_string", "kinematic_state", "velocity_override", "cartesian_velocity", "temperature_cpu", "supply_voltage", "current_all", "referencing_state")
    TCP_FIELD_NUMBER: _ClassVar[int]
    PLATFORM_POSE_FIELD_NUMBER: _ClassVar[int]
    JOINTS_FIELD_NUMBER: _ClassVar[int]
    DINS_FIELD_NUMBER: _ClassVar[int]
    DOUTS_FIELD_NUMBER: _ClassVar[int]
    GSIGS_FIELD_NUMBER: _ClassVar[int]
    HARDWARE_STATE_STRING_FIELD_NUMBER: _ClassVar[int]
    KINEMATIC_STATE_FIELD_NUMBER: _ClassVar[int]
    VELOCITY_OVERRIDE_FIELD_NUMBER: _ClassVar[int]
    CARTESIAN_VELOCITY_FIELD_NUMBER: _ClassVar[int]
    TEMPERATURE_CPU_FIELD_NUMBER: _ClassVar[int]
    SUPPLY_VOLTAGE_FIELD_NUMBER: _ClassVar[int]
    CURRENT_ALL_FIELD_NUMBER: _ClassVar[int]
    REFERENCING_STATE_FIELD_NUMBER: _ClassVar[int]
    tcp: Matrix44
    platform_pose: PlatformPose
    joints: _containers.RepeatedCompositeFieldContainer[Joint]
    DIns: _containers.RepeatedCompositeFieldContainer[DIn]
    DOuts: _containers.RepeatedCompositeFieldContainer[DOut]
    GSigs: _containers.RepeatedCompositeFieldContainer[GSig]
    hardware_state_string: str
    kinematic_state: KinematicState
    velocity_override: float
    cartesian_velocity: float
    temperature_cpu: float
    supply_voltage: float
    current_all: float
    referencing_state: ReferencingState
    def __init__(self, tcp: _Optional[_Union[Matrix44, _Mapping]] = ..., platform_pose: _Optional[_Union[PlatformPose, _Mapping]] = ..., joints: _Optional[_Iterable[_Union[Joint, _Mapping]]] = ..., DIns: _Optional[_Iterable[_Union[DIn, _Mapping]]] = ..., DOuts: _Optional[_Iterable[_Union[DOut, _Mapping]]] = ..., GSigs: _Optional[_Iterable[_Union[GSig, _Mapping]]] = ..., hardware_state_string: _Optional[str] = ..., kinematic_state: _Optional[_Union[KinematicState, str]] = ..., velocity_override: _Optional[float] = ..., cartesian_velocity: _Optional[float] = ..., temperature_cpu: _Optional[float] = ..., supply_voltage: _Optional[float] = ..., current_all: _Optional[float] = ..., referencing_state: _Optional[_Union[ReferencingState, str]] = ...) -> None: ...

class MotionState(_message.Message):
    __slots__ = ("current_source", "motion_ipo", "logic_ipo", "move_to_ipo", "position_interface", "request_successful")
    class MotionSource(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        JOG: _ClassVar[MotionState.MotionSource]
        IPO: _ClassVar[MotionState.MotionSource]
        MOVE_TO: _ClassVar[MotionState.MotionSource]
        POSITION_INTERFACE: _ClassVar[MotionState.MotionSource]
        PLATFORM: _ClassVar[MotionState.MotionSource]
    JOG: MotionState.MotionSource
    IPO: MotionState.MotionSource
    MOVE_TO: MotionState.MotionSource
    POSITION_INTERFACE: MotionState.MotionSource
    PLATFORM: MotionState.MotionSource
    class InterpolatorState(_message.Message):
        __slots__ = ("runstate", "replay_mode", "main_program_name", "current_program_name", "current_program_idx", "program_count", "current_command_idx", "command_count")
        RUNSTATE_FIELD_NUMBER: _ClassVar[int]
        REPLAY_MODE_FIELD_NUMBER: _ClassVar[int]
        MAIN_PROGRAM_NAME_FIELD_NUMBER: _ClassVar[int]
        CURRENT_PROGRAM_NAME_FIELD_NUMBER: _ClassVar[int]
        CURRENT_PROGRAM_IDX_FIELD_NUMBER: _ClassVar[int]
        PROGRAM_COUNT_FIELD_NUMBER: _ClassVar[int]
        CURRENT_COMMAND_IDX_FIELD_NUMBER: _ClassVar[int]
        COMMAND_COUNT_FIELD_NUMBER: _ClassVar[int]
        runstate: RunState
        replay_mode: ReplayMode
        main_program_name: str
        current_program_name: str
        current_program_idx: int
        program_count: int
        current_command_idx: int
        command_count: int
        def __init__(self, runstate: _Optional[_Union[RunState, str]] = ..., replay_mode: _Optional[_Union[ReplayMode, str]] = ..., main_program_name: _Optional[str] = ..., current_program_name: _Optional[str] = ..., current_program_idx: _Optional[int] = ..., program_count: _Optional[int] = ..., current_command_idx: _Optional[int] = ..., command_count: _Optional[int] = ...) -> None: ...
    class PositionInterfaceState(_message.Message):
        __slots__ = ("is_enabled", "is_in_use", "port")
        IS_ENABLED_FIELD_NUMBER: _ClassVar[int]
        IS_IN_USE_FIELD_NUMBER: _ClassVar[int]
        PORT_FIELD_NUMBER: _ClassVar[int]
        is_enabled: bool
        is_in_use: bool
        port: int
        def __init__(self, is_enabled: bool = ..., is_in_use: bool = ..., port: _Optional[int] = ...) -> None: ...
    CURRENT_SOURCE_FIELD_NUMBER: _ClassVar[int]
    MOTION_IPO_FIELD_NUMBER: _ClassVar[int]
    LOGIC_IPO_FIELD_NUMBER: _ClassVar[int]
    MOVE_TO_IPO_FIELD_NUMBER: _ClassVar[int]
    POSITION_INTERFACE_FIELD_NUMBER: _ClassVar[int]
    REQUEST_SUCCESSFUL_FIELD_NUMBER: _ClassVar[int]
    current_source: MotionState.MotionSource
    motion_ipo: MotionState.InterpolatorState
    logic_ipo: MotionState.InterpolatorState
    move_to_ipo: MotionState.InterpolatorState
    position_interface: MotionState.PositionInterfaceState
    request_successful: bool
    def __init__(self, current_source: _Optional[_Union[MotionState.MotionSource, str]] = ..., motion_ipo: _Optional[_Union[MotionState.InterpolatorState, _Mapping]] = ..., logic_ipo: _Optional[_Union[MotionState.InterpolatorState, _Mapping]] = ..., move_to_ipo: _Optional[_Union[MotionState.InterpolatorState, _Mapping]] = ..., position_interface: _Optional[_Union[MotionState.PositionInterfaceState, _Mapping]] = ..., request_successful: bool = ...) -> None: ...

class MotionInterpolatorRequest(_message.Message):
    __slots__ = ("app_name", "runstate", "replay_mode", "main_program", "start_at")
    class StartAt(_message.Message):
        __slots__ = ("program", "command")
        PROGRAM_FIELD_NUMBER: _ClassVar[int]
        COMMAND_FIELD_NUMBER: _ClassVar[int]
        program: str
        command: int
        def __init__(self, program: _Optional[str] = ..., command: _Optional[int] = ...) -> None: ...
    APP_NAME_FIELD_NUMBER: _ClassVar[int]
    RUNSTATE_FIELD_NUMBER: _ClassVar[int]
    REPLAY_MODE_FIELD_NUMBER: _ClassVar[int]
    MAIN_PROGRAM_FIELD_NUMBER: _ClassVar[int]
    START_AT_FIELD_NUMBER: _ClassVar[int]
    app_name: str
    runstate: RunState
    replay_mode: ReplayMode
    main_program: str
    start_at: MotionInterpolatorRequest.StartAt
    def __init__(self, app_name: _Optional[str] = ..., runstate: _Optional[_Union[RunState, str]] = ..., replay_mode: _Optional[_Union[ReplayMode, str]] = ..., main_program: _Optional[str] = ..., start_at: _Optional[_Union[MotionInterpolatorRequest.StartAt, _Mapping]] = ...) -> None: ...

class LogicInterpolatorRequest(_message.Message):
    __slots__ = ("app_name", "main_program")
    APP_NAME_FIELD_NUMBER: _ClassVar[int]
    MAIN_PROGRAM_FIELD_NUMBER: _ClassVar[int]
    app_name: str
    main_program: str
    def __init__(self, app_name: _Optional[str] = ..., main_program: _Optional[str] = ...) -> None: ...

class PositionInterfaceRequest(_message.Message):
    __slots__ = ("app_name", "is_enabled", "is_in_use")
    APP_NAME_FIELD_NUMBER: _ClassVar[int]
    IS_ENABLED_FIELD_NUMBER: _ClassVar[int]
    IS_IN_USE_FIELD_NUMBER: _ClassVar[int]
    app_name: str
    is_enabled: bool
    is_in_use: bool
    def __init__(self, app_name: _Optional[str] = ..., is_enabled: bool = ..., is_in_use: bool = ...) -> None: ...

class MoveToRequest(_message.Message):
    __slots__ = ("app_name", "joint", "joint_relative", "cart", "cart_relative_base", "cart_relative_tool", "stop")
    class MoveToJoint(_message.Message):
        __slots__ = ("robot_joints", "external_joints", "velocity", "acceleration")
        ROBOT_JOINTS_FIELD_NUMBER: _ClassVar[int]
        EXTERNAL_JOINTS_FIELD_NUMBER: _ClassVar[int]
        VELOCITY_FIELD_NUMBER: _ClassVar[int]
        ACCELERATION_FIELD_NUMBER: _ClassVar[int]
        robot_joints: _containers.RepeatedScalarFieldContainer[float]
        external_joints: _containers.RepeatedScalarFieldContainer[float]
        velocity: float
        acceleration: float
        def __init__(self, robot_joints: _Optional[_Iterable[float]] = ..., external_joints: _Optional[_Iterable[float]] = ..., velocity: _Optional[float] = ..., acceleration: _Optional[float] = ...) -> None: ...
    class MoveToCart(_message.Message):
        __slots__ = ("position", "orientation", "external_joints", "velocity", "acceleration", "frame")
        POSITION_FIELD_NUMBER: _ClassVar[int]
        ORIENTATION_FIELD_NUMBER: _ClassVar[int]
        EXTERNAL_JOINTS_FIELD_NUMBER: _ClassVar[int]
        VELOCITY_FIELD_NUMBER: _ClassVar[int]
        ACCELERATION_FIELD_NUMBER: _ClassVar[int]
        FRAME_FIELD_NUMBER: _ClassVar[int]
        position: Vector3
        orientation: Vector3
        external_joints: _containers.RepeatedScalarFieldContainer[float]
        velocity: float
        acceleration: float
        frame: str
        def __init__(self, position: _Optional[_Union[Vector3, _Mapping]] = ..., orientation: _Optional[_Union[Vector3, _Mapping]] = ..., external_joints: _Optional[_Iterable[float]] = ..., velocity: _Optional[float] = ..., acceleration: _Optional[float] = ..., frame: _Optional[str] = ...) -> None: ...
    class MoveToStop(_message.Message):
        __slots__ = ()
        def __init__(self) -> None: ...
    APP_NAME_FIELD_NUMBER: _ClassVar[int]
    JOINT_FIELD_NUMBER: _ClassVar[int]
    JOINT_RELATIVE_FIELD_NUMBER: _ClassVar[int]
    CART_FIELD_NUMBER: _ClassVar[int]
    CART_RELATIVE_BASE_FIELD_NUMBER: _ClassVar[int]
    CART_RELATIVE_TOOL_FIELD_NUMBER: _ClassVar[int]
    STOP_FIELD_NUMBER: _ClassVar[int]
    app_name: str
    joint: MoveToRequest.MoveToJoint
    joint_relative: MoveToRequest.MoveToJoint
    cart: MoveToRequest.MoveToCart
    cart_relative_base: MoveToRequest.MoveToCart
    cart_relative_tool: MoveToRequest.MoveToCart
    stop: MoveToRequest.MoveToStop
    def __init__(self, app_name: _Optional[str] = ..., joint: _Optional[_Union[MoveToRequest.MoveToJoint, _Mapping]] = ..., joint_relative: _Optional[_Union[MoveToRequest.MoveToJoint, _Mapping]] = ..., cart: _Optional[_Union[MoveToRequest.MoveToCart, _Mapping]] = ..., cart_relative_base: _Optional[_Union[MoveToRequest.MoveToCart, _Mapping]] = ..., cart_relative_tool: _Optional[_Union[MoveToRequest.MoveToCart, _Mapping]] = ..., stop: _Optional[_Union[MoveToRequest.MoveToStop, _Mapping]] = ...) -> None: ...

class EnableMotorsRequest(_message.Message):
    __slots__ = ("app_name", "enable")
    APP_NAME_FIELD_NUMBER: _ClassVar[int]
    ENABLE_FIELD_NUMBER: _ClassVar[int]
    app_name: str
    enable: bool
    def __init__(self, app_name: _Optional[str] = ..., enable: bool = ...) -> None: ...

class EnableMotorsResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ResetErrorsRequest(_message.Message):
    __slots__ = ("app_name",)
    APP_NAME_FIELD_NUMBER: _ClassVar[int]
    app_name: str
    def __init__(self, app_name: _Optional[str] = ...) -> None: ...

class ResetErrorsResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ReferenceJointsRequest(_message.Message):
    __slots__ = ("app_name", "reference_all", "referencing_program", "reference_robot_joints", "reference_external_joints")
    APP_NAME_FIELD_NUMBER: _ClassVar[int]
    REFERENCE_ALL_FIELD_NUMBER: _ClassVar[int]
    REFERENCING_PROGRAM_FIELD_NUMBER: _ClassVar[int]
    REFERENCE_ROBOT_JOINTS_FIELD_NUMBER: _ClassVar[int]
    REFERENCE_EXTERNAL_JOINTS_FIELD_NUMBER: _ClassVar[int]
    app_name: str
    reference_all: bool
    referencing_program: bool
    reference_robot_joints: _containers.RepeatedScalarFieldContainer[int]
    reference_external_joints: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, app_name: _Optional[str] = ..., reference_all: bool = ..., referencing_program: bool = ..., reference_robot_joints: _Optional[_Iterable[int]] = ..., reference_external_joints: _Optional[_Iterable[int]] = ...) -> None: ...

class ReferenceJointsResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class SetVelocityOverrideRequest(_message.Message):
    __slots__ = ("app_name", "velocity_override")
    APP_NAME_FIELD_NUMBER: _ClassVar[int]
    VELOCITY_OVERRIDE_FIELD_NUMBER: _ClassVar[int]
    app_name: str
    velocity_override: float
    def __init__(self, app_name: _Optional[str] = ..., velocity_override: _Optional[float] = ...) -> None: ...

class SetVelocityOverrideResponse(_message.Message):
    __slots__ = ("velocity_override",)
    VELOCITY_OVERRIDE_FIELD_NUMBER: _ClassVar[int]
    velocity_override: float
    def __init__(self, velocity_override: _Optional[float] = ...) -> None: ...

class IOStateRequest(_message.Message):
    __slots__ = ("app_name", "DIns", "DOuts", "GSigs")
    APP_NAME_FIELD_NUMBER: _ClassVar[int]
    DINS_FIELD_NUMBER: _ClassVar[int]
    DOUTS_FIELD_NUMBER: _ClassVar[int]
    GSIGS_FIELD_NUMBER: _ClassVar[int]
    app_name: str
    DIns: _containers.RepeatedCompositeFieldContainer[DIn]
    DOuts: _containers.RepeatedCompositeFieldContainer[DOut]
    GSigs: _containers.RepeatedCompositeFieldContainer[GSig]
    def __init__(self, app_name: _Optional[str] = ..., DIns: _Optional[_Iterable[_Union[DIn, _Mapping]]] = ..., DOuts: _Optional[_Iterable[_Union[DOut, _Mapping]]] = ..., GSigs: _Optional[_Iterable[_Union[GSig, _Mapping]]] = ...) -> None: ...

class IOStateResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class JointToCartRequest(_message.Message):
    __slots__ = ("app_name", "joints")
    APP_NAME_FIELD_NUMBER: _ClassVar[int]
    JOINTS_FIELD_NUMBER: _ClassVar[int]
    app_name: str
    joints: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, app_name: _Optional[str] = ..., joints: _Optional[_Iterable[float]] = ...) -> None: ...

class CartToJointRequest(_message.Message):
    __slots__ = ("app_name", "joints", "position", "orientation")
    APP_NAME_FIELD_NUMBER: _ClassVar[int]
    JOINTS_FIELD_NUMBER: _ClassVar[int]
    POSITION_FIELD_NUMBER: _ClassVar[int]
    ORIENTATION_FIELD_NUMBER: _ClassVar[int]
    app_name: str
    joints: _containers.RepeatedScalarFieldContainer[float]
    position: Vector3
    orientation: Vector3
    def __init__(self, app_name: _Optional[str] = ..., joints: _Optional[_Iterable[float]] = ..., position: _Optional[_Union[Vector3, _Mapping]] = ..., orientation: _Optional[_Union[Vector3, _Mapping]] = ...) -> None: ...

class JointToCartResponse(_message.Message):
    __slots__ = ("kinematicState", "position")
    KINEMATICSTATE_FIELD_NUMBER: _ClassVar[int]
    POSITION_FIELD_NUMBER: _ClassVar[int]
    kinematicState: KinematicState
    position: Matrix44
    def __init__(self, kinematicState: _Optional[_Union[KinematicState, str]] = ..., position: _Optional[_Union[Matrix44, _Mapping]] = ...) -> None: ...

class CartToJointResponse(_message.Message):
    __slots__ = ("kinematicState", "joints")
    KINEMATICSTATE_FIELD_NUMBER: _ClassVar[int]
    JOINTS_FIELD_NUMBER: _ClassVar[int]
    kinematicState: KinematicState
    joints: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, kinematicState: _Optional[_Union[KinematicState, str]] = ..., joints: _Optional[_Iterable[float]] = ...) -> None: ...

class UploadFileRequest(_message.Message):
    __slots__ = ("app_name", "filename", "data", "binary_mode")
    APP_NAME_FIELD_NUMBER: _ClassVar[int]
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    BINARY_MODE_FIELD_NUMBER: _ClassVar[int]
    app_name: str
    filename: str
    data: bytes
    binary_mode: bool
    def __init__(self, app_name: _Optional[str] = ..., filename: _Optional[str] = ..., data: _Optional[bytes] = ..., binary_mode: bool = ...) -> None: ...

class UploadFileResponse(_message.Message):
    __slots__ = ("success", "error")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    success: bool
    error: str
    def __init__(self, success: bool = ..., error: _Optional[str] = ...) -> None: ...

class DownloadFileRequest(_message.Message):
    __slots__ = ("app_name", "filename")
    APP_NAME_FIELD_NUMBER: _ClassVar[int]
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    app_name: str
    filename: str
    def __init__(self, app_name: _Optional[str] = ..., filename: _Optional[str] = ...) -> None: ...

class DownloadFileResponse(_message.Message):
    __slots__ = ("success", "error", "data")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    success: bool
    error: str
    data: bytes
    def __init__(self, success: bool = ..., error: _Optional[str] = ..., data: _Optional[bytes] = ...) -> None: ...

class ListFilesRequest(_message.Message):
    __slots__ = ("app_name", "path")
    APP_NAME_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    app_name: str
    path: str
    def __init__(self, app_name: _Optional[str] = ..., path: _Optional[str] = ...) -> None: ...

class ListFilesResponse(_message.Message):
    __slots__ = ("success", "error", "entries")
    class DirectoryEntry(_message.Message):
        __slots__ = ("name", "type")
        class Type(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = ()
            Other: _ClassVar[ListFilesResponse.DirectoryEntry.Type]
            File: _ClassVar[ListFilesResponse.DirectoryEntry.Type]
            Directory: _ClassVar[ListFilesResponse.DirectoryEntry.Type]
        Other: ListFilesResponse.DirectoryEntry.Type
        File: ListFilesResponse.DirectoryEntry.Type
        Directory: ListFilesResponse.DirectoryEntry.Type
        NAME_FIELD_NUMBER: _ClassVar[int]
        TYPE_FIELD_NUMBER: _ClassVar[int]
        name: str
        type: ListFilesResponse.DirectoryEntry.Type
        def __init__(self, name: _Optional[str] = ..., type: _Optional[_Union[ListFilesResponse.DirectoryEntry.Type, str]] = ...) -> None: ...
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    ENTRIES_FIELD_NUMBER: _ClassVar[int]
    success: bool
    error: str
    entries: _containers.RepeatedCompositeFieldContainer[ListFilesResponse.DirectoryEntry]
    def __init__(self, success: bool = ..., error: _Optional[str] = ..., entries: _Optional[_Iterable[_Union[ListFilesResponse.DirectoryEntry, _Mapping]]] = ...) -> None: ...

class RemoveFilesRequest(_message.Message):
    __slots__ = ("app_name", "files")
    APP_NAME_FIELD_NUMBER: _ClassVar[int]
    FILES_FIELD_NUMBER: _ClassVar[int]
    app_name: str
    files: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, app_name: _Optional[str] = ..., files: _Optional[_Iterable[str]] = ...) -> None: ...

class RemoveFilesResponse(_message.Message):
    __slots__ = ("success", "results")
    class DirectoryEntry(_message.Message):
        __slots__ = ("name", "success", "error")
        NAME_FIELD_NUMBER: _ClassVar[int]
        SUCCESS_FIELD_NUMBER: _ClassVar[int]
        ERROR_FIELD_NUMBER: _ClassVar[int]
        name: str
        success: bool
        error: str
        def __init__(self, name: _Optional[str] = ..., success: bool = ..., error: _Optional[str] = ...) -> None: ...
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    RESULTS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    results: _containers.RepeatedCompositeFieldContainer[RemoveFilesResponse.DirectoryEntry]
    def __init__(self, success: bool = ..., results: _Optional[_Iterable[_Union[RemoveFilesResponse.DirectoryEntry, _Mapping]]] = ...) -> None: ...

class DropdownState(_message.Message):
    __slots__ = ("options", "selected_option")
    OPTIONS_FIELD_NUMBER: _ClassVar[int]
    SELECTED_OPTION_FIELD_NUMBER: _ClassVar[int]
    options: _containers.RepeatedScalarFieldContainer[str]
    selected_option: str
    def __init__(self, options: _Optional[_Iterable[str]] = ..., selected_option: _Optional[str] = ...) -> None: ...

class TextfieldState(_message.Message):
    __slots__ = ("current_text",)
    CURRENT_TEXT_FIELD_NUMBER: _ClassVar[int]
    current_text: str
    def __init__(self, current_text: _Optional[str] = ...) -> None: ...

class NumberfieldState(_message.Message):
    __slots__ = ("current_number",)
    CURRENT_NUMBER_FIELD_NUMBER: _ClassVar[int]
    current_number: float
    def __init__(self, current_number: _Optional[float] = ...) -> None: ...

class ImageState(_message.Message):
    __slots__ = ("image_data", "clicked_at")
    class ImageData(_message.Message):
        __slots__ = ("encoding", "data", "width", "height")
        class ImageEncoding(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = ()
            JPEG: _ClassVar[ImageState.ImageData.ImageEncoding]
        JPEG: ImageState.ImageData.ImageEncoding
        ENCODING_FIELD_NUMBER: _ClassVar[int]
        DATA_FIELD_NUMBER: _ClassVar[int]
        WIDTH_FIELD_NUMBER: _ClassVar[int]
        HEIGHT_FIELD_NUMBER: _ClassVar[int]
        encoding: ImageState.ImageData.ImageEncoding
        data: bytes
        width: int
        height: int
        def __init__(self, encoding: _Optional[_Union[ImageState.ImageData.ImageEncoding, str]] = ..., data: _Optional[bytes] = ..., width: _Optional[int] = ..., height: _Optional[int] = ...) -> None: ...
    class ClickedAt(_message.Message):
        __slots__ = ("is_clicked", "x", "y")
        IS_CLICKED_FIELD_NUMBER: _ClassVar[int]
        X_FIELD_NUMBER: _ClassVar[int]
        Y_FIELD_NUMBER: _ClassVar[int]
        is_clicked: ButtonState
        x: float
        y: float
        def __init__(self, is_clicked: _Optional[_Union[ButtonState, str]] = ..., x: _Optional[float] = ..., y: _Optional[float] = ...) -> None: ...
    IMAGE_DATA_FIELD_NUMBER: _ClassVar[int]
    CLICKED_AT_FIELD_NUMBER: _ClassVar[int]
    image_data: ImageState.ImageData
    clicked_at: ImageState.ClickedAt
    def __init__(self, image_data: _Optional[_Union[ImageState.ImageData, _Mapping]] = ..., clicked_at: _Optional[_Union[ImageState.ClickedAt, _Mapping]] = ...) -> None: ...

class AppUIElement(_message.Message):
    __slots__ = ("element_name", "state", "is_visible")
    class AppUIState(_message.Message):
        __slots__ = ("button_state", "checkbox_state", "dropdown_state", "textfield_state", "numberfield_state", "image_state")
        BUTTON_STATE_FIELD_NUMBER: _ClassVar[int]
        CHECKBOX_STATE_FIELD_NUMBER: _ClassVar[int]
        DROPDOWN_STATE_FIELD_NUMBER: _ClassVar[int]
        TEXTFIELD_STATE_FIELD_NUMBER: _ClassVar[int]
        NUMBERFIELD_STATE_FIELD_NUMBER: _ClassVar[int]
        IMAGE_STATE_FIELD_NUMBER: _ClassVar[int]
        button_state: ButtonState
        checkbox_state: CheckboxState
        dropdown_state: DropdownState
        textfield_state: TextfieldState
        numberfield_state: NumberfieldState
        image_state: ImageState
        def __init__(self, button_state: _Optional[_Union[ButtonState, str]] = ..., checkbox_state: _Optional[_Union[CheckboxState, str]] = ..., dropdown_state: _Optional[_Union[DropdownState, _Mapping]] = ..., textfield_state: _Optional[_Union[TextfieldState, _Mapping]] = ..., numberfield_state: _Optional[_Union[NumberfieldState, _Mapping]] = ..., image_state: _Optional[_Union[ImageState, _Mapping]] = ...) -> None: ...
    ELEMENT_NAME_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    IS_VISIBLE_FIELD_NUMBER: _ClassVar[int]
    element_name: str
    state: AppUIElement.AppUIState
    is_visible: bool
    def __init__(self, element_name: _Optional[str] = ..., state: _Optional[_Union[AppUIElement.AppUIState, _Mapping]] = ..., is_visible: bool = ...) -> None: ...

class AppFunction(_message.Message):
    __slots__ = ("name", "call_id", "parameters", "label", "ui_hint")
    class Parameter(_message.Message):
        __slots__ = ("name", "bool_value", "int64_value", "double_value", "string_value", "vector3_value", "cartesian_value")
        NAME_FIELD_NUMBER: _ClassVar[int]
        BOOL_VALUE_FIELD_NUMBER: _ClassVar[int]
        INT64_VALUE_FIELD_NUMBER: _ClassVar[int]
        DOUBLE_VALUE_FIELD_NUMBER: _ClassVar[int]
        STRING_VALUE_FIELD_NUMBER: _ClassVar[int]
        VECTOR3_VALUE_FIELD_NUMBER: _ClassVar[int]
        CARTESIAN_VALUE_FIELD_NUMBER: _ClassVar[int]
        name: str
        bool_value: bool
        int64_value: int
        double_value: float
        string_value: str
        vector3_value: Vector3
        cartesian_value: Matrix44
        def __init__(self, name: _Optional[str] = ..., bool_value: bool = ..., int64_value: _Optional[int] = ..., double_value: _Optional[float] = ..., string_value: _Optional[str] = ..., vector3_value: _Optional[_Union[Vector3, _Mapping]] = ..., cartesian_value: _Optional[_Union[Matrix44, _Mapping]] = ...) -> None: ...
    NAME_FIELD_NUMBER: _ClassVar[int]
    CALL_ID_FIELD_NUMBER: _ClassVar[int]
    PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    LABEL_FIELD_NUMBER: _ClassVar[int]
    UI_HINT_FIELD_NUMBER: _ClassVar[int]
    name: str
    call_id: int
    parameters: _containers.RepeatedCompositeFieldContainer[AppFunction.Parameter]
    label: str
    ui_hint: str
    def __init__(self, name: _Optional[str] = ..., call_id: _Optional[int] = ..., parameters: _Optional[_Iterable[_Union[AppFunction.Parameter, _Mapping]]] = ..., label: _Optional[str] = ..., ui_hint: _Optional[str] = ...) -> None: ...

class Event(_message.Message):
    __slots__ = ("function", "ui_updates", "disconnect_request")
    class DisconnectRequest(_message.Message):
        __slots__ = ("reason",)
        REASON_FIELD_NUMBER: _ClassVar[int]
        reason: str
        def __init__(self, reason: _Optional[str] = ...) -> None: ...
    FUNCTION_FIELD_NUMBER: _ClassVar[int]
    UI_UPDATES_FIELD_NUMBER: _ClassVar[int]
    DISCONNECT_REQUEST_FIELD_NUMBER: _ClassVar[int]
    function: AppFunction
    ui_updates: _containers.RepeatedCompositeFieldContainer[AppUIElement]
    disconnect_request: Event.DisconnectRequest
    def __init__(self, function: _Optional[_Union[AppFunction, _Mapping]] = ..., ui_updates: _Optional[_Iterable[_Union[AppUIElement, _Mapping]]] = ..., disconnect_request: _Optional[_Union[Event.DisconnectRequest, _Mapping]] = ...) -> None: ...

class ShowDialogRequest(_message.Message):
    __slots__ = ("app_name", "message_dialog")
    class DialogType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        INFO: _ClassVar[ShowDialogRequest.DialogType]
        WARNING: _ClassVar[ShowDialogRequest.DialogType]
        ERROR: _ClassVar[ShowDialogRequest.DialogType]
    INFO: ShowDialogRequest.DialogType
    WARNING: ShowDialogRequest.DialogType
    ERROR: ShowDialogRequest.DialogType
    class MessageDialog(_message.Message):
        __slots__ = ("type", "title", "message")
        TYPE_FIELD_NUMBER: _ClassVar[int]
        TITLE_FIELD_NUMBER: _ClassVar[int]
        MESSAGE_FIELD_NUMBER: _ClassVar[int]
        type: ShowDialogRequest.DialogType
        title: str
        message: str
        def __init__(self, type: _Optional[_Union[ShowDialogRequest.DialogType, str]] = ..., title: _Optional[str] = ..., message: _Optional[str] = ...) -> None: ...
    APP_NAME_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_DIALOG_FIELD_NUMBER: _ClassVar[int]
    app_name: str
    message_dialog: ShowDialogRequest.MessageDialog
    def __init__(self, app_name: _Optional[str] = ..., message_dialog: _Optional[_Union[ShowDialogRequest.MessageDialog, _Mapping]] = ...) -> None: ...

class ShowDialogResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ProgramVariable(_message.Message):
    __slots__ = ("name", "number", "position")
    class ProgramVariablePosition(_message.Message):
        __slots__ = ("robot_joints", "cartesian", "both", "external_joints")
        class Joints(_message.Message):
            __slots__ = ("joints",)
            JOINTS_FIELD_NUMBER: _ClassVar[int]
            joints: _containers.RepeatedScalarFieldContainer[float]
            def __init__(self, joints: _Optional[_Iterable[float]] = ...) -> None: ...
        class CartAndJoints(_message.Message):
            __slots__ = ("robot_joints", "cartesian")
            ROBOT_JOINTS_FIELD_NUMBER: _ClassVar[int]
            CARTESIAN_FIELD_NUMBER: _ClassVar[int]
            robot_joints: ProgramVariable.ProgramVariablePosition.Joints
            cartesian: Matrix44
            def __init__(self, robot_joints: _Optional[_Union[ProgramVariable.ProgramVariablePosition.Joints, _Mapping]] = ..., cartesian: _Optional[_Union[Matrix44, _Mapping]] = ...) -> None: ...
        ROBOT_JOINTS_FIELD_NUMBER: _ClassVar[int]
        CARTESIAN_FIELD_NUMBER: _ClassVar[int]
        BOTH_FIELD_NUMBER: _ClassVar[int]
        EXTERNAL_JOINTS_FIELD_NUMBER: _ClassVar[int]
        robot_joints: ProgramVariable.ProgramVariablePosition.Joints
        cartesian: Matrix44
        both: ProgramVariable.ProgramVariablePosition.CartAndJoints
        external_joints: _containers.RepeatedScalarFieldContainer[float]
        def __init__(self, robot_joints: _Optional[_Union[ProgramVariable.ProgramVariablePosition.Joints, _Mapping]] = ..., cartesian: _Optional[_Union[Matrix44, _Mapping]] = ..., both: _Optional[_Union[ProgramVariable.ProgramVariablePosition.CartAndJoints, _Mapping]] = ..., external_joints: _Optional[_Iterable[float]] = ...) -> None: ...
    NAME_FIELD_NUMBER: _ClassVar[int]
    NUMBER_FIELD_NUMBER: _ClassVar[int]
    POSITION_FIELD_NUMBER: _ClassVar[int]
    name: str
    number: float
    position: ProgramVariable.ProgramVariablePosition
    def __init__(self, name: _Optional[str] = ..., number: _Optional[float] = ..., position: _Optional[_Union[ProgramVariable.ProgramVariablePosition, _Mapping]] = ...) -> None: ...

class FailedFunction(_message.Message):
    __slots__ = ("call_id", "reason")
    CALL_ID_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    call_id: int
    reason: str
    def __init__(self, call_id: _Optional[int] = ..., reason: _Optional[str] = ...) -> None: ...

class AppAction(_message.Message):
    __slots__ = ("app_name", "set_variables", "done_functions", "failed_functions", "ui_changes", "request_ui_state")
    APP_NAME_FIELD_NUMBER: _ClassVar[int]
    SET_VARIABLES_FIELD_NUMBER: _ClassVar[int]
    DONE_FUNCTIONS_FIELD_NUMBER: _ClassVar[int]
    FAILED_FUNCTIONS_FIELD_NUMBER: _ClassVar[int]
    UI_CHANGES_FIELD_NUMBER: _ClassVar[int]
    REQUEST_UI_STATE_FIELD_NUMBER: _ClassVar[int]
    app_name: str
    set_variables: _containers.RepeatedCompositeFieldContainer[ProgramVariable]
    done_functions: _containers.RepeatedScalarFieldContainer[int]
    failed_functions: _containers.RepeatedCompositeFieldContainer[FailedFunction]
    ui_changes: _containers.RepeatedCompositeFieldContainer[AppUIElement]
    request_ui_state: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, app_name: _Optional[str] = ..., set_variables: _Optional[_Iterable[_Union[ProgramVariable, _Mapping]]] = ..., done_functions: _Optional[_Iterable[int]] = ..., failed_functions: _Optional[_Iterable[_Union[FailedFunction, _Mapping]]] = ..., ui_changes: _Optional[_Iterable[_Union[AppUIElement, _Mapping]]] = ..., request_ui_state: _Optional[_Iterable[str]] = ...) -> None: ...
