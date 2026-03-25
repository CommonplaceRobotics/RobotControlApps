# OPC UA Server Bridge for igus Robot Control

This app bridges the igus Robot Control gRPC interface to an OPC UA server,
allowing any OPC UA client (SCADA, PLC, HMI, etc.) to monitor and control the robot.

## Prerequisites

- Python 3.9+
- igus Robot Control with gRPC App Interface enabled
- App registered in the robot control (see `rcapp.xml`)

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python app.py
```

With options:
```bash
python app.py --grpc-target localhost:50051 --opcua-port 4840 --update-interval 0.1
```

| Argument | Default | Description |
|---|---|---|
| `--grpc-target` | `localhost:50051` | gRPC target of the robot control |
| `--opcua-port` | `4840` | Port for the OPC UA server |
| `--app-name` | `OpcUaServer-Python` | Must match `rcapp.xml` |
| `--update-interval` | `0.2` | Robot state polling interval (seconds) |

## OPC UA Node Structure

```
Objects/
└── Robot/
    ├── SystemInfo/          (static, read on connect)
    │   ├── Version
    │   ├── RobotType
    │   ├── DeviceId
    │   ├── IsSimulation
    │   ├── CycleTimeAvg_ms
    │   ├── Workload
    │   ├── RobotAxisCount
    │   └── ExternalAxisCount
    ├── RobotState/          (updated every update-interval)
    │   ├── HardwareStateString
    │   ├── KinematicState
    │   ├── VelocityOverride
    │   ├── CartesianVelocity_mm_s
    │   ├── TemperatureCPU
    │   ├── SupplyVoltage_mV
    │   ├── CurrentAll_mA
    │   ├── ReferencingState
    │   ├── TCP_X/Y/Z_mm
    │   ├── TCP_A/B/C_deg
    │   └── Joints/Joint_0..8/
    │       ├── Name, Position, TargetPosition
    │       └── Temperature_C, Current_mA, HardwareState
    ├── MotionControl/
    │   ├── CurrentMotionSource  (read)
    │   ├── MotionProgram_RunState (read)
    │   ├── MotionProgram_Name  (read)
    │   ├── MotionProgram_Command (read)
    │   └── VelocityOverride    (**writable** → calls SetVelocityOverride)
    └── Methods/
        ├── EnableMotors(enable: Boolean)
        ├── ResetErrors()
        ├── ReferenceAllJoints(withProgram: Boolean)
        ├── LoadMotionProgram(program: String)
        ├── StartMotionProgram()
        ├── StopMotionProgram()
        ├── PauseMotionProgram()
        ├── MoveToJoint(velocity, a1..a6, e1..e3)
        ├── MoveToLinear(velocity, x,y,z,a,b,c, e1..e3, frame)
        └── MoveToStop()
```

## Architecture

```
OPC UA Client
     │  opc.tcp://
     ▼
OpcUaServer.py  ←── polling thread ──→  AppClient.py (gRPC)
     │                                         │
     │  asyncua (Python OPC UA)                │  grpc
     │                                         ▼
     └────────────────────────────────  igus Robot Control
```

## Notes

- Shared modules (`AppClient.py`, `DataTypes/`, proto stubs) are loaded at runtime from
  `../control_python/` via `sys.path` — no duplication needed.
- The `VelocityOverride` node under `MotionControl/` is writable:
  writing to it from any OPC UA client will call `SetVelocityOverride` on the robot.
- All control methods run in an executor to avoid blocking the async event loop.