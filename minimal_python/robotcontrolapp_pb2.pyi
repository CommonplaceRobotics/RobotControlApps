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

class DInSpecialFunction(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    NORMAL_DIN: _ClassVar[DInSpecialFunction]
    PLC_ENABLE: _ClassVar[DInSpecialFunction]

class DOutSpecialFunction(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    NORMAL_DOUT: _ClassVar[DOutSpecialFunction]
    PLC_ENABLED: _ClassVar[DOutSpecialFunction]

class HardwareState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ERROR_DEAD: _ClassVar[HardwareState]
    ENABLED: _ClassVar[HardwareState]
    OK: _ClassVar[HardwareState]
    ERROR_MOTOR_NOT_ENABLED: _ClassVar[HardwareState]
    ERROR_COMMUNICATION: _ClassVar[HardwareState]
    ERROR_OVERCURRENT: _ClassVar[HardwareState]
    ERROR_POSITION_LAG: _ClassVar[HardwareState]
    ERROR_ESTOP: _ClassVar[HardwareState]
    ERROR_DRIVER: _ClassVar[HardwareState]
    ERROR_ENCODER: _ClassVar[HardwareState]
    ERROR_OVERTEMP: _ClassVar[HardwareState]

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
NORMAL_DIN: DInSpecialFunction
PLC_ENABLE: DInSpecialFunction
NORMAL_DOUT: DOutSpecialFunction
PLC_ENABLED: DOutSpecialFunction
ERROR_DEAD: HardwareState
ENABLED: HardwareState
OK: HardwareState
ERROR_MOTOR_NOT_ENABLED: HardwareState
ERROR_COMMUNICATION: HardwareState
ERROR_OVERCURRENT: HardwareState
ERROR_POSITION_LAG: HardwareState
ERROR_ESTOP: HardwareState
ERROR_DRIVER: HardwareState
ERROR_ENCODER: HardwareState
ERROR_OVERTEMP: HardwareState
NOT_CLICKED: ButtonState
CLICKED: ButtonState
UNCHECKED: CheckboxState
CHECKED: CheckboxState

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
    __slots__ = ("id", "name", "state", "function")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    FUNCTION_FIELD_NUMBER: _ClassVar[int]
    id: int
    name: str
    state: DIOState
    function: DInSpecialFunction
    def __init__(self, id: _Optional[int] = ..., name: _Optional[str] = ..., state: _Optional[_Union[DIOState, str]] = ..., function: _Optional[_Union[DInSpecialFunction, str]] = ...) -> None: ...

class DOut(_message.Message):
    __slots__ = ("id", "name", "state", "target_state", "function")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    TARGET_STATE_FIELD_NUMBER: _ClassVar[int]
    FUNCTION_FIELD_NUMBER: _ClassVar[int]
    id: int
    name: str
    state: DIOState
    target_state: DIOState
    function: DOutSpecialFunction
    def __init__(self, id: _Optional[int] = ..., name: _Optional[str] = ..., state: _Optional[_Union[DIOState, str]] = ..., target_state: _Optional[_Union[DIOState, str]] = ..., function: _Optional[_Union[DOutSpecialFunction, str]] = ...) -> None: ...

class Joint(_message.Message):
    __slots__ = ("id", "name", "position", "state")
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
    id: int
    name: str
    position: Joint.JointPosition
    state: HardwareState
    def __init__(self, id: _Optional[int] = ..., name: _Optional[str] = ..., position: _Optional[_Union[Joint.JointPosition, _Mapping]] = ..., state: _Optional[_Union[HardwareState, str]] = ...) -> None: ...

class RobotState(_message.Message):
    __slots__ = ("tcp", "joints", "DIns", "DOuts")
    TCP_FIELD_NUMBER: _ClassVar[int]
    JOINTS_FIELD_NUMBER: _ClassVar[int]
    DINS_FIELD_NUMBER: _ClassVar[int]
    DOUTS_FIELD_NUMBER: _ClassVar[int]
    tcp: Matrix44
    joints: _containers.RepeatedCompositeFieldContainer[Joint]
    DIns: _containers.RepeatedCompositeFieldContainer[DIn]
    DOuts: _containers.RepeatedCompositeFieldContainer[DOut]
    def __init__(self, tcp: _Optional[_Union[Matrix44, _Mapping]] = ..., joints: _Optional[_Iterable[_Union[Joint, _Mapping]]] = ..., DIns: _Optional[_Iterable[_Union[DIn, _Mapping]]] = ..., DOuts: _Optional[_Iterable[_Union[DOut, _Mapping]]] = ...) -> None: ...

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
