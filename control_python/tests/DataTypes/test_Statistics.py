import unittest

from DataTypes import Statistics
import robotcontrolapp_pb2


class StatisticsTest(unittest.TestCase):
    def test_init(self):
        stat = Statistics.Statistics()
        self.assertEqual(0, len(stat.externalAxisDirectionChanges))
        # self.assertEqual(0, stat.externalAxisDirectionChanges[0])
        # self.assertEqual(0, stat.externalAxisDirectionChanges[1])
        # self.assertEqual(0, stat.externalAxisDirectionChanges[2])

        self.assertEqual(0, len(stat.robotAxisDirectionChanges))
        # self.assertEqual(0, stat.robotAxisDirectionChanges[0])
        # self.assertEqual(0, stat.robotAxisDirectionChanges[1])
        # self.assertEqual(0, stat.robotAxisDirectionChanges[2])
        # self.assertEqual(0, stat.robotAxisDirectionChanges[3])
        # self.assertEqual(0, stat.robotAxisDirectionChanges[4])
        # self.assertEqual(0, stat.robotAxisDirectionChanges[5])

        self.assertEqual(0, stat.partsBad)
        self.assertEqual(0, stat.partsGood)

        self.assertEqual(0, stat.programDurationLast)
        self.assertEqual(0, stat.programStartsLast)
        self.assertEqual(0, stat.programStartsTotal)
        self.assertEqual(0, stat.uptimeComplete)
        self.assertEqual(0, stat.uptimeEnabled)
        self.assertEqual(0, stat.uptimeLast)
        self.assertEqual(0, stat.uptimeMotion)

    def test_FromGrpc(self):
        grpc1 = robotcontrolapp_pb2.StatisticsResponse()
        grpc1.uptime_complete = 10
        grpc1.uptime_last = 20
        grpc1.uptime_enabled = 30
        grpc1.uptime_motion = 40

        grpc1.program_starts_total = 50
        grpc1.program_starts_last = 60
        grpc1.program_duration_last = 70

        grpc1.parts_good = 80
        grpc1.parts_bad = 90

        grpc1.robot_axis_direction_changes.append(100)
        grpc1.robot_axis_direction_changes.append(110)
        grpc1.robot_axis_direction_changes.append(120)
        grpc1.robot_axis_direction_changes.append(130)
        grpc1.robot_axis_direction_changes.append(140)
        grpc1.robot_axis_direction_changes.append(150)
        grpc1.external_axis_direction_changes.append(160)
        grpc1.external_axis_direction_changes.append(170)
        grpc1.external_axis_direction_changes.append(180)

        stat = Statistics.Statistics.FromGrpc(grpc1)
        self.assertEqual(3, len(stat.externalAxisDirectionChanges))
        self.assertEqual(160, stat.externalAxisDirectionChanges[0])
        self.assertEqual(170, stat.externalAxisDirectionChanges[1])
        self.assertEqual(180, stat.externalAxisDirectionChanges[2])

        self.assertEqual(6, len(stat.robotAxisDirectionChanges))
        self.assertEqual(100, stat.robotAxisDirectionChanges[0])
        self.assertEqual(110, stat.robotAxisDirectionChanges[1])
        self.assertEqual(120, stat.robotAxisDirectionChanges[2])
        self.assertEqual(130, stat.robotAxisDirectionChanges[3])
        self.assertEqual(140, stat.robotAxisDirectionChanges[4])
        self.assertEqual(150, stat.robotAxisDirectionChanges[5])

        self.assertEqual(90, stat.partsBad)
        self.assertEqual(80, stat.partsGood)

        self.assertEqual(70, stat.programDurationLast)
        self.assertEqual(60, stat.programStartsLast)
        self.assertEqual(50, stat.programStartsTotal)
        self.assertEqual(10, stat.uptimeComplete)
        self.assertEqual(30, stat.uptimeEnabled)
        self.assertEqual(20, stat.uptimeLast)
        self.assertEqual(40, stat.uptimeMotion)


if __name__ == "__main__":
    unittest.main()
