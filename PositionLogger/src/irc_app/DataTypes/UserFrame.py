#
from dataclasses import dataclass

from ..rpc import robotcontrolapp_pb2


@dataclass
class UserFrame:
    """This class defines a user frame"""

    name: str = ""
    """Name of the user frame"""

    pointAX: float = 0
    """User frame origin position X"""
    pointAY: float = 0
    """User frame origin position Y"""
    pointAZ: float = 0
    """User frame origin position Z"""

    pointBX: float = 0
    """User frame "left" direction X"""
    pointBY: float = 0
    """User frame "left" direction Y"""
    pointBZ: float = 0
    """User frame "left" direction Z"""

    pointCX: float = 0
    """User frame "up" direction X"""
    pointCY: float = 0
    """User frame "up" direction Y"""
    pointCZ: float = 0
    """User frame "up" direction Z"""

    def ToGrpc(self) -> robotcontrolapp_pb2.UserFrame:
        """Converts the data to a GRPC object"""
        ret = robotcontrolapp_pb2.UserFrame()

        ret.name = self.name

        ret.point_a.x = self.pointAX
        ret.point_a.y = self.pointAY
        ret.point_a.z = self.pointAZ

        ret.point_b.x = self.pointBX
        ret.point_b.y = self.pointBY
        ret.point_b.z = self.pointBZ

        ret.point_c.x = self.pointCX
        ret.point_c.y = self.pointCY
        ret.point_c.z = self.pointCZ
        return ret


def UserFrameFromGrpc(grpc: robotcontrolapp_pb2.UserFrame) -> UserFrame:
    """Constructs a UserFrame from GRPC"""
    ret = UserFrame()

    ret.name = grpc.name

    ret.pointAX = grpc.point_a.x
    ret.pointAY = grpc.point_a.y
    ret.pointAZ = grpc.point_a.z

    ret.pointBX = grpc.point_b.x
    ret.pointBY = grpc.point_b.y
    ret.pointBZ = grpc.point_b.z

    ret.pointCX = grpc.point_c.x
    ret.pointCY = grpc.point_c.y
    ret.pointCZ = grpc.point_c.z

    return ret
