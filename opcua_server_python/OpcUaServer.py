"""
OPC UA Server Bridge for igus Robot Control.

Builds an OPC UA address space mirroring the robot state and
exposes control methods. Uses the existing AppClient from control_python.
"""

import asyncio
import logging
import threading
import time
from typing import Optional

from asyncua import Server, ua
from asyncua.common.node import Node
from google.protobuf.internal import containers as protobufContainers

# Shared modules from control_python (added to path in app.py)
from AppClient import AppClient
import robotcontrolapp_pb2
from DataTypes.ProgramVariable import NumberVariable, PositionVariable

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# AppClient subclass — no-op UI/function handlers
# ---------------------------------------------------------------------------

class RobotAppClient(AppClient):
    """AppClient with no-op handlers for UI updates and app functions."""

    def _AppFunctionHandler(self, function: robotcontrolapp_pb2.AppFunction):
        logger.debug(f"AppFunction received (ignored): {function.name}")

    def _UiUpdateHandler(self, updates: protobufContainers.RepeatedCompositeFieldContainer):
        logger.debug(f"UI update received (ignored): {len(updates)} updates")


# ---------------------------------------------------------------------------
# OPC UA Server
# ---------------------------------------------------------------------------

class OpcUaServer:
    """OPC UA Server that bridges the igus Robot Control gRPC API to OPC UA."""

    NAMESPACE_URI = "urn:cpr-robotics:opcua-bridge"

    def __init__(
        self,
        app_name: str = "OpcUaServer-Python",
        grpc_target: str = "localhost:50051",
        opcua_port: int = 4840,
        update_interval: float = 0.2,
    ):
        self._app_name = app_name
        self._grpc_target = grpc_target
        self._opcua_port = opcua_port
        self._update_interval = update_interval
        self._running = False
        self._loop: Optional[asyncio.AbstractEventLoop] = None
        self._nodes: dict = {}
        self._robot: Optional[RobotAppClient] = None

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def run(self):
        """Start the server (blocking)."""
        asyncio.run(self._async_run())

    def stop(self):
        """Request the server to stop."""
        self._running = False

    # ------------------------------------------------------------------
    # Async main
    # ------------------------------------------------------------------

    async def _async_run(self):
        self._loop = asyncio.get_running_loop()
        self._running = True

        # Build the OPC UA server object and address space before starting to listen.
        # All of these are fast async operations that don't block the event loop.
        server = Server()
        await server.init()
        server.set_endpoint(f"opc.tcp://0.0.0.0:{self._opcua_port}/freeopcua/server/")
        server.set_server_name("igus Robot Control OPC UA Bridge")

        idx = await server.register_namespace(self.NAMESPACE_URI)
        logger.info(f"OPC UA namespace index: {idx}")

        objects = server.nodes.objects
        await self._build_address_space(server, idx, objects)

        # Create the robot client but do NOT call Connect() here.
        # AppClient.Connect() + GetSystemInfo() are blocking synchronous gRPC calls.
        # Running them on the asyncio event loop thread would stall the server and
        # cause UAExpert's FindServers to time out (BadTimeout).  The polling thread
        # is a real OS thread and handles all gRPC work safely.
        self._robot = RobotAppClient(self._app_name, self._grpc_target)

        poll_thread = threading.Thread(target=self._polling_thread, daemon=True)
        poll_thread.start()

        # Enter the context manager LAST — this is the point where asyncua binds the
        # TCP socket and begins accepting OPC UA connections.  Everything above is
        # pure setup that never touches the network on the OPC UA side.
        async with server:
            logger.info(f"OPC UA server running on port {self._opcua_port}")
            print(f"OPC UA server running at opc.tcp://0.0.0.0:{self._opcua_port}")
            while self._running:
                await asyncio.sleep(0.5)

        self._running = False
        if self._robot and self._robot.IsConnected():
            self._robot.Disconnect()
        logger.info("OPC UA server stopped.")

    # ------------------------------------------------------------------
    # Address space builder
    # ------------------------------------------------------------------

    async def _build_address_space(self, server: Server, idx: int, objects: Node):
        robot_obj = await objects.add_object(idx, "Robot")

        # SystemInfo
        sysinfo_obj = await robot_obj.add_object(idx, "SystemInfo")
        self._nodes["sysinfo/Version"]           = await sysinfo_obj.add_variable(idx, "Version", "")
        self._nodes["sysinfo/RobotType"]         = await sysinfo_obj.add_variable(idx, "RobotType", "")
        self._nodes["sysinfo/DeviceId"]          = await sysinfo_obj.add_variable(idx, "DeviceId", "")
        self._nodes["sysinfo/IsSimulation"]      = await sysinfo_obj.add_variable(idx, "IsSimulation", False)
        self._nodes["sysinfo/CycleTimeAvg_ms"]   = await sysinfo_obj.add_variable(idx, "CycleTimeAvg_ms", 0.0)
        self._nodes["sysinfo/Workload"]          = await sysinfo_obj.add_variable(idx, "Workload", 0.0)
        self._nodes["sysinfo/RobotAxisCount"]    = await sysinfo_obj.add_variable(idx, "RobotAxisCount", ua.UInt32(0))
        self._nodes["sysinfo/ExternalAxisCount"] = await sysinfo_obj.add_variable(idx, "ExternalAxisCount", ua.UInt32(0))

        # RobotState
        state_obj = await robot_obj.add_object(idx, "RobotState")
        self._nodes["state/HardwareStateString"]    = await state_obj.add_variable(idx, "HardwareStateString", "")
        self._nodes["state/KinematicState"]         = await state_obj.add_variable(idx, "KinematicState", 0)
        self._nodes["state/VelocityOverride"]       = await state_obj.add_variable(idx, "VelocityOverride", 0.0)
        self._nodes["state/CartesianVelocity_mm_s"] = await state_obj.add_variable(idx, "CartesianVelocity_mm_s", 0.0)
        self._nodes["state/TemperatureCPU"]         = await state_obj.add_variable(idx, "TemperatureCPU", 0.0)
        self._nodes["state/SupplyVoltage_mV"]       = await state_obj.add_variable(idx, "SupplyVoltage_mV", 0.0)
        self._nodes["state/CurrentAll_mA"]          = await state_obj.add_variable(idx, "CurrentAll_mA", 0.0)
        self._nodes["state/ReferencingState"]       = await state_obj.add_variable(idx, "ReferencingState", 0)
        self._nodes["state/TCP_X_mm"]               = await state_obj.add_variable(idx, "TCP_X_mm", 0.0)
        self._nodes["state/TCP_Y_mm"]               = await state_obj.add_variable(idx, "TCP_Y_mm", 0.0)
        self._nodes["state/TCP_Z_mm"]               = await state_obj.add_variable(idx, "TCP_Z_mm", 0.0)
        self._nodes["state/TCP_A_deg"]              = await state_obj.add_variable(idx, "TCP_A_deg", 0.0)
        self._nodes["state/TCP_B_deg"]              = await state_obj.add_variable(idx, "TCP_B_deg", 0.0)
        self._nodes["state/TCP_C_deg"]              = await state_obj.add_variable(idx, "TCP_C_deg", 0.0)

        joints_obj = await state_obj.add_object(idx, "Joints")
        for i in range(9):
            j_obj = await joints_obj.add_object(idx, f"Joint_{i}")
            self._nodes[f"joint/{i}/Name"]           = await j_obj.add_variable(idx, "Name", f"Joint_{i}")
            self._nodes[f"joint/{i}/Position"]       = await j_obj.add_variable(idx, "Position", 0.0)
            self._nodes[f"joint/{i}/TargetPosition"] = await j_obj.add_variable(idx, "TargetPosition", 0.0)
            self._nodes[f"joint/{i}/Temperature_C"]  = await j_obj.add_variable(idx, "Temperature_C", 0.0)
            self._nodes[f"joint/{i}/Current_mA"]     = await j_obj.add_variable(idx, "Current_mA", 0.0)
            self._nodes[f"joint/{i}/HardwareState"]  = await j_obj.add_variable(idx, "HardwareState", 0)

        # MotionControl
        motion_obj = await robot_obj.add_object(idx, "MotionControl")
        self._nodes["motion/CurrentMotionSource"]    = await motion_obj.add_variable(idx, "CurrentMotionSource", 0)
        self._nodes["motion/MotionProgram_RunState"] = await motion_obj.add_variable(idx, "MotionProgram_RunState", 0)
        self._nodes["motion/MotionProgram_Name"]     = await motion_obj.add_variable(idx, "MotionProgram_Name", "")
        self._nodes["motion/MotionProgram_Command"]  = await motion_obj.add_variable(idx, "MotionProgram_Command", 0)

        vo_node = await motion_obj.add_variable(idx, "VelocityOverride", 100.0)
        await vo_node.set_writable()
        self._nodes["motion/VelocityOverride"] = vo_node

        handler = VelocityOverrideHandler(self._robot, self._loop)
        sub = await server.create_subscription(500, handler)
        await sub.subscribe_data_change(vo_node)

        # Methods
        methods_obj = await robot_obj.add_object(idx, "Methods")

        await methods_obj.add_method(idx, "EnableMotors",
            self._method_enable_motors, [ua.VariantType.Boolean], [])
        await methods_obj.add_method(idx, "ResetErrors",
            self._method_reset_errors, [], [])
        await methods_obj.add_method(idx, "ReferenceAllJoints",
            self._method_reference_all_joints, [ua.VariantType.Boolean], [])
        await methods_obj.add_method(idx, "LoadMotionProgram",
            self._method_load_motion_program, [ua.VariantType.String], [])
        await methods_obj.add_method(idx, "StartMotionProgram",
            self._method_start_motion_program, [], [])
        await methods_obj.add_method(idx, "StopMotionProgram",
            self._method_stop_motion_program, [], [])
        await methods_obj.add_method(idx, "PauseMotionProgram",
            self._method_pause_motion_program, [], [])
        await methods_obj.add_method(idx, "MoveToStop",
            self._method_move_to_stop, [], [])
        await methods_obj.add_method(idx, "MoveToJoint",
            self._method_move_to_joint,
            [ua.VariantType.Float,
             ua.VariantType.Double, ua.VariantType.Double, ua.VariantType.Double,
             ua.VariantType.Double, ua.VariantType.Double, ua.VariantType.Double,
             ua.VariantType.Double, ua.VariantType.Double, ua.VariantType.Double],
            [])
        await methods_obj.add_method(idx, "MoveToLinear",
            self._method_move_to_linear,
            [ua.VariantType.Float,
             ua.VariantType.Double, ua.VariantType.Double, ua.VariantType.Double,
             ua.VariantType.Double, ua.VariantType.Double, ua.VariantType.Double,
             ua.VariantType.Double, ua.VariantType.Double, ua.VariantType.Double,
             ua.VariantType.String],
            [])
        await methods_obj.add_method(idx, "SetDigitalOutput",
            self._method_set_digital_output,
            [ua.VariantType.UInt32, ua.VariantType.Boolean], [])
        await methods_obj.add_method(idx, "SetGlobalSignal",
            self._method_set_global_signal,
            [ua.VariantType.UInt32, ua.VariantType.Boolean], [])

        # ProgramVariables — dynamic named variables inside the robot program
        progvar_obj = await robot_obj.add_object(idx, "ProgramVariables")
        await progvar_obj.add_method(idx, "GetNumberVariable",
            self._method_get_number_variable,
            [ua.VariantType.String], [ua.VariantType.Double])
        await progvar_obj.add_method(idx, "SetNumberVariable",
            self._method_set_number_variable,
            [ua.VariantType.String, ua.VariantType.Double], [])

        # DigitalIO — read-only inputs, readable outputs + global signals
        # Outputs and global signals can also be written via Methods above.
        dio_obj = await robot_obj.add_object(idx, "DigitalIO")

        din_obj = await dio_obj.add_object(idx, "DigitalInputs")
        for i in range(64):
            self._nodes[f"din/{i}"] = await din_obj.add_variable(idx, f"DIn_{i}", False)

        dout_obj = await dio_obj.add_object(idx, "DigitalOutputs")
        for i in range(64):
            self._nodes[f"dout/{i}"] = await dout_obj.add_variable(idx, f"DOut_{i}", False)

        gsig_obj = await dio_obj.add_object(idx, "GlobalSignals")
        for i in range(100):
            self._nodes[f"gsig/{i}"] = await gsig_obj.add_variable(idx, f"GSig_{i}", False)

        logger.info("OPC UA address space built successfully.")

    # ------------------------------------------------------------------
    # System info updater
    # ------------------------------------------------------------------

    async def _update_system_info(self, sys_info):
        await self._nodes["sysinfo/Version"].write_value(sys_info.version)
        await self._nodes["sysinfo/RobotType"].write_value(sys_info.robotType)
        await self._nodes["sysinfo/DeviceId"].write_value(sys_info.deviceID)
        await self._nodes["sysinfo/IsSimulation"].write_value(sys_info.isSimulation)
        await self._nodes["sysinfo/CycleTimeAvg_ms"].write_value(float(sys_info.cycleTimeAverage))
        await self._nodes["sysinfo/Workload"].write_value(float(sys_info.workload))
        await self._nodes["sysinfo/RobotAxisCount"].write_value(ua.UInt32(sys_info.robotAxisCount))
        await self._nodes["sysinfo/ExternalAxisCount"].write_value(ua.UInt32(sys_info.externalAxisCount))

    # ------------------------------------------------------------------
    # Polling thread
    # ------------------------------------------------------------------

    def _polling_thread(self):
        """Worker thread: owns all gRPC I/O so the asyncio event loop is never blocked."""
        logger.info("Polling thread started.")
        while self._running:
            try:
                if not self._robot.IsConnected():
                    # AppClient.Disconnect() closes the gRPC channel permanently, so
                    # we must create a fresh instance rather than reusing the old one.
                    self._robot = RobotAppClient(self._app_name, self._grpc_target)
                    self._robot.Connect()
                    logger.info(f"Connected to robot at {self._grpc_target}")
                    sys_info = self._robot.GetSystemInfo()
                    future = asyncio.run_coroutine_threadsafe(
                        self._update_system_info(sys_info), self._loop
                    )
                    future.result(timeout=2.0)

                robot_state = self._robot.GetRobotState()
                motion_state = self._robot.GetMotionState()
                future = asyncio.run_coroutine_threadsafe(
                    self._update_nodes(robot_state, motion_state),
                    self._loop
                )
                future.result(timeout=2.0)
            except Exception as e:
                logger.warning(f"Polling error (will retry): {e}")
            time.sleep(self._update_interval)
        logger.info("Polling thread stopped.")

    async def _update_nodes(self, robot_state, motion_state):
        try:
            await self._nodes["state/HardwareStateString"].write_value(str(robot_state.hardwareState))
            await self._nodes["state/KinematicState"].write_value(int(robot_state.kinematicState))
            await self._nodes["state/VelocityOverride"].write_value(float(robot_state.velocityOverride))
            await self._nodes["state/CartesianVelocity_mm_s"].write_value(float(robot_state.cartesianVelocity))
            await self._nodes["state/TemperatureCPU"].write_value(float(robot_state.temperatureCPU))
            await self._nodes["state/SupplyVoltage_mV"].write_value(float(robot_state.supplyVoltage))
            await self._nodes["state/CurrentAll_mA"].write_value(float(robot_state.currentAll))
            await self._nodes["state/ReferencingState"].write_value(int(robot_state.referencingState))

            tcp = robot_state.tcp
            if tcp is not None:
                await self._nodes["state/TCP_X_mm"].write_value(float(tcp.GetX()))
                await self._nodes["state/TCP_Y_mm"].write_value(float(tcp.GetY()))
                await self._nodes["state/TCP_Z_mm"].write_value(float(tcp.GetZ()))
                try:
                    a, b, c = tcp.GetOrientation()
                    await self._nodes["state/TCP_A_deg"].write_value(float(a))
                    await self._nodes["state/TCP_B_deg"].write_value(float(b))
                    await self._nodes["state/TCP_C_deg"].write_value(float(c))
                except Exception:
                    pass

            for i, joint in enumerate(robot_state.joints):
                if i >= 9:
                    break
                await self._nodes[f"joint/{i}/Name"].write_value(str(joint.name))
                await self._nodes[f"joint/{i}/Position"].write_value(float(joint.actualPosition))
                await self._nodes[f"joint/{i}/TargetPosition"].write_value(float(joint.targetPosition))
                await self._nodes[f"joint/{i}/Temperature_C"].write_value(float(joint.temperatureBoard))
                await self._nodes[f"joint/{i}/Current_mA"].write_value(float(joint.current))
                await self._nodes[f"joint/{i}/HardwareState"].write_value(int(joint.hardwareState))

            await self._nodes["motion/MotionProgram_RunState"].write_value(int(motion_state.motionProgram.runState))
            await self._nodes["motion/MotionProgram_Name"].write_value(str(motion_state.motionProgram.mainProgram))
            await self._nodes["motion/MotionProgram_Command"].write_value(int(motion_state.motionProgram.currentCommandIndex))

            for i, val in enumerate(robot_state.digitalInputs[:64]):
                await self._nodes[f"din/{i}"].write_value(bool(val))
            for i, val in enumerate(robot_state.digitalOutputs[:64]):
                await self._nodes[f"dout/{i}"].write_value(bool(val))
            for i, val in enumerate(robot_state.globalSignals[:100]):
                await self._nodes[f"gsig/{i}"].write_value(bool(val))

        except Exception as e:
            logger.warning(f"Node update error: {e}")

    # ------------------------------------------------------------------
    # OPC UA Method handlers
    # ------------------------------------------------------------------

    async def _run_in_executor(self, fn, *args):
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, fn, *args)

    async def _method_enable_motors(self, parent, enable: ua.Variant):
        try:
            if enable.Value:
                await self._run_in_executor(self._robot.EnableMotors)
            else:
                await self._run_in_executor(self._robot.DisableMotors)
        except Exception as e:
            logger.error(f"EnableMotors failed: {e}")
            raise ua.UaStatusCodeError(ua.StatusCodes.BadInternalError)
        return []

    async def _method_reset_errors(self, parent):
        try:
            await self._run_in_executor(self._robot.ResetErrors)
        except Exception as e:
            logger.error(f"ResetErrors failed: {e}")
            raise ua.UaStatusCodeError(ua.StatusCodes.BadInternalError)
        return []

    async def _method_reference_all_joints(self, parent, with_program: ua.Variant):
        try:
            await self._run_in_executor(self._robot.ReferenceAllJoints, with_program.Value)
        except Exception as e:
            logger.error(f"ReferenceAllJoints failed: {e}")
            raise ua.UaStatusCodeError(ua.StatusCodes.BadInternalError)
        return []

    async def _method_load_motion_program(self, parent, program: ua.Variant):
        try:
            await self._run_in_executor(self._robot.LoadMotionProgram, program.Value)
        except Exception as e:
            logger.error(f"LoadMotionProgram failed: {e}")
            raise ua.UaStatusCodeError(ua.StatusCodes.BadInternalError)
        return []

    async def _method_start_motion_program(self, parent):
        try:
            await self._run_in_executor(self._robot.StartMotionProgram)
        except Exception as e:
            logger.error(f"StartMotionProgram failed: {e}")
            raise ua.UaStatusCodeError(ua.StatusCodes.BadInternalError)
        return []

    async def _method_stop_motion_program(self, parent):
        try:
            await self._run_in_executor(self._robot.StopMotionProgram)
        except Exception as e:
            logger.error(f"StopMotionProgram failed: {e}")
            raise ua.UaStatusCodeError(ua.StatusCodes.BadInternalError)
        return []

    async def _method_pause_motion_program(self, parent):
        try:
            await self._run_in_executor(self._robot.PauseMotionProgram)
        except Exception as e:
            logger.error(f"PauseMotionProgram failed: {e}")
            raise ua.UaStatusCodeError(ua.StatusCodes.BadInternalError)
        return []

    async def _method_move_to_stop(self, parent):
        try:
            await self._run_in_executor(self._robot.MoveToStop)
        except Exception as e:
            logger.error(f"MoveToStop failed: {e}")
            raise ua.UaStatusCodeError(ua.StatusCodes.BadInternalError)
        return []

    async def _method_move_to_joint(self, parent,
                                     velocity, a1, a2, a3, a4, a5, a6, e1, e2, e3):
        try:
            await self._run_in_executor(
                self._robot.MoveToJoint,
                float(velocity.Value), -1.0,
                float(a1.Value), float(a2.Value), float(a3.Value),
                float(a4.Value), float(a5.Value), float(a6.Value),
                float(e1.Value), float(e2.Value), float(e3.Value),
            )
        except Exception as e:
            logger.error(f"MoveToJoint failed: {e}")
            raise ua.UaStatusCodeError(ua.StatusCodes.BadInternalError)
        return []

    async def _method_move_to_linear(self, parent,
                                      velocity, x, y, z, a, b, c, e1, e2, e3, frame):
        try:
            await self._run_in_executor(
                self._robot.MoveToLinear,
                float(velocity.Value), -1.0,
                float(x.Value), float(y.Value), float(z.Value),
                float(a.Value), float(b.Value), float(c.Value),
                float(e1.Value), float(e2.Value), float(e3.Value),
                str(frame.Value),
            )
        except Exception as e:
            logger.error(f"MoveToLinear failed: {e}")
            raise ua.UaStatusCodeError(ua.StatusCodes.BadInternalError)
        return []

    async def _method_set_digital_output(self, parent, number: ua.Variant, state: ua.Variant):
        try:
            await self._run_in_executor(
                self._robot.SetDigitalOutput, int(number.Value), bool(state.Value)
            )
        except Exception as e:
            logger.error(f"SetDigitalOutput failed: {e}")
            raise ua.UaStatusCodeError(ua.StatusCodes.BadInternalError)
        return []

    async def _method_set_global_signal(self, parent, number: ua.Variant, state: ua.Variant):
        try:
            await self._run_in_executor(
                self._robot.SetGlobalSignal, int(number.Value), bool(state.Value)
            )
        except Exception as e:
            logger.error(f"SetGlobalSignal failed: {e}")
            raise ua.UaStatusCodeError(ua.StatusCodes.BadInternalError)
        return []

    async def _method_get_number_variable(self, parent, name: ua.Variant):
        try:
            var = await self._run_in_executor(
                self._robot.GetNumberVariable, str(name.Value)
            )
            return [ua.Variant(float(var.GetValue()), ua.VariantType.Double)]
        except Exception as e:
            logger.error(f"GetNumberVariable failed: {e}")
            raise ua.UaStatusCodeError(ua.StatusCodes.BadInternalError)

    async def _method_set_number_variable(self, parent, name: ua.Variant, value: ua.Variant):
        try:
            await self._run_in_executor(
                self._robot.SetNumberVariable, str(name.Value), float(value.Value)
            )
        except Exception as e:
            logger.error(f"SetNumberVariable failed: {e}")
            raise ua.UaStatusCodeError(ua.StatusCodes.BadInternalError)
        return []


# ---------------------------------------------------------------------------
# DataChange handler for writable VelocityOverride node
# ---------------------------------------------------------------------------

class VelocityOverrideHandler:
    """Handles writes to the OPC UA VelocityOverride node and forwards to robot."""

    def __init__(self, robot: RobotAppClient, loop: asyncio.AbstractEventLoop):
        self._robot = robot
        self._loop = loop

    def datachange_notification(self, node, val, data):
        try:
            if self._robot and self._robot.IsConnected():
                self._robot.SetVelocityOverride(float(val))
                logger.info(f"VelocityOverride set to {val}% via OPC UA write")
        except Exception as e:
            logger.warning(f"Failed to set velocity override: {e}")