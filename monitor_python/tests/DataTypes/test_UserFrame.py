import unittest

from irc_app.DataTypes.UserFrame import UserFrame, UserFrameFromGrpc
from irc_app.rpc import robotcontrolapp_pb2


class UserFrameTest(unittest.TestCase):
    def test_constructor(self):
        frame = UserFrame()

        self.assertEqual("", frame.name)

        self.assertEqual(0, frame.pointAX)
        self.assertEqual(0, frame.pointAY)
        self.assertEqual(0, frame.pointAZ)

        self.assertEqual(0, frame.pointBX)
        self.assertEqual(0, frame.pointBY)
        self.assertEqual(0, frame.pointBZ)

        self.assertEqual(0, frame.pointCX)
        self.assertEqual(0, frame.pointCY)
        self.assertEqual(0, frame.pointCZ)

    def test_to_grpc(self):
        frame = UserFrame()

        frame.name = "Foo"

        frame.pointAX = 1
        frame.pointAY = 2
        frame.pointAZ = 3

        frame.pointBX = 4
        frame.pointBY = 5
        frame.pointBZ = 6

        frame.pointCX = 7
        frame.pointCY = 8
        frame.pointCZ = 9

        grpc = frame.ToGrpc()

        self.assertEqual("Foo", grpc.name)

        self.assertEqual(1, grpc.point_a.x)
        self.assertEqual(2, grpc.point_a.y)
        self.assertEqual(3, grpc.point_a.z)

        self.assertEqual(4, grpc.point_b.x)
        self.assertEqual(5, grpc.point_b.y)
        self.assertEqual(6, grpc.point_b.z)

        self.assertEqual(7, grpc.point_c.x)
        self.assertEqual(8, grpc.point_c.y)
        self.assertEqual(9, grpc.point_c.z)

    def test_from_grpc(self):
        grpc = robotcontrolapp_pb2.UserFrame()

        grpc.name = "Bar"

        grpc.point_a.x = 10
        grpc.point_a.y = 20
        grpc.point_a.z = 30

        grpc.point_b.x = 40
        grpc.point_b.y = 50
        grpc.point_b.z = 60

        grpc.point_c.x = 70
        grpc.point_c.y = 80
        grpc.point_c.z = 90

        frame = UserFrameFromGrpc(grpc)

        self.assertEqual("Bar", frame.name)

        self.assertEqual(10, frame.pointAX)
        self.assertEqual(20, frame.pointAY)
        self.assertEqual(30, frame.pointAZ)

        self.assertEqual(40, frame.pointBX)
        self.assertEqual(50, frame.pointBY)
        self.assertEqual(60, frame.pointBZ)

        self.assertEqual(70, frame.pointCX)
        self.assertEqual(80, frame.pointCY)
        self.assertEqual(90, frame.pointCZ)
