import unittest

from DataTypes.SystemInfo import SystemInfo
import robotcontrolapp_pb2

class SystemInfoTest(unittest.TestCase):
    def test_init(self):
        sysInfo = SystemInfo()
        self.assertEqual(0, sysInfo.versionMajor)
        self.assertEqual(0, sysInfo.versionMinor)
        self.assertEqual(0, sysInfo.versionPatch)
        self.assertEqual("", sysInfo.version)
        
        self.assertEqual("", sysInfo.projectFile)
        self.assertEqual("", sysInfo.projectTitle)
        self.assertEqual("", sysInfo.projectAuthor)
        self.assertEqual("", sysInfo.robotType)

        self.assertEqual(robotcontrolapp_pb2.SystemInfo.Voltage24V, sysInfo.voltage)
        self.assertEqual(robotcontrolapp_pb2.SystemInfo.Other, sysInfo.systemType)
        self.assertEqual("", sysInfo.deviceID)
        self.assertFalse(sysInfo.isSimulation)

        self.assertEqual(0, sysInfo.cycleTimeTarget)
        self.assertEqual(0, sysInfo.cycleTimeAverage)
        self.assertEqual(0, sysInfo.cycleTimeMax)
        self.assertEqual(0, sysInfo.cycleTimeMin)

        self.assertEqual(0, sysInfo.robotAxisCount)
        self.assertEqual(0, sysInfo.externalAxisCount)
        self.assertEqual(0, sysInfo.toolAxisCount)
        self.assertEqual(0, sysInfo.platformAxisCount)
        self.assertEqual(0, sysInfo.digitalIOModuleCount)

    def test_FromGrpc(self):
        grpc = robotcontrolapp_pb2.SystemInfo()
        grpc.version_major = 14
        grpc.version_minor = 4
        grpc.version_patch = 1
        grpc.version = "14-004-1-test"

        grpc.project_file = "Foo"
        grpc.project_title = "Bar"
        grpc.project_author = "Baz"
        grpc.robot_type = "Rebel"

        grpc.voltage = robotcontrolapp_pb2.SystemInfo.Voltage48V
        grpc.system_type = robotcontrolapp_pb2.SystemInfo.Raspberry
        grpc.device_id = "ABCDEF"
        grpc.is_simulation = True

        grpc.cycle_time_target = 10
        grpc.cycle_time_avg = 10.1
        grpc.cycle_time_max = 10.2
        grpc.cycle_time_min = 9.9

        grpc.robot_axis_count = 6
        grpc.external_axis_count = 1
        grpc.tool_axis_count = 2
        grpc.platform_axis_count = 4
        grpc.digital_io_module_count = 3

        sysInfo = SystemInfo.FromGrpc(grpc)
        self.assertEqual(14, sysInfo.versionMajor)
        self.assertEqual(4, sysInfo.versionMinor)
        self.assertEqual(1, sysInfo.versionPatch)
        self.assertEqual("14-004-1-test", sysInfo.version)
        
        self.assertEqual("Foo", sysInfo.projectFile)
        self.assertEqual("Bar", sysInfo.projectTitle)
        self.assertEqual("Baz", sysInfo.projectAuthor)
        self.assertEqual("Rebel", sysInfo.robotType)

        self.assertEqual(robotcontrolapp_pb2.SystemInfo.Voltage48V, sysInfo.voltage)
        self.assertEqual(robotcontrolapp_pb2.SystemInfo.Raspberry, sysInfo.systemType)
        self.assertEqual("ABCDEF", sysInfo.deviceID)
        self.assertTrue(sysInfo.isSimulation)

        self.assertAlmostEqual(10, sysInfo.cycleTimeTarget, 4)
        self.assertAlmostEqual(10.1, sysInfo.cycleTimeAverage, 4)
        self.assertAlmostEqual(10.2, sysInfo.cycleTimeMax, 4)
        self.assertAlmostEqual(9.9, sysInfo.cycleTimeMin, 4)

        self.assertEqual(6, sysInfo.robotAxisCount)
        self.assertEqual(1, sysInfo.externalAxisCount)
        self.assertEqual(2, sysInfo.toolAxisCount)
        self.assertEqual(4, sysInfo.platformAxisCount)
        self.assertEqual(3, sysInfo.digitalIOModuleCount)

if __name__ == "__main__":
    unittest.main()
