from math import atan2, cos, fabs, sin, sqrt
import math

from DataTypes.MathDefinitions import DEG2RAD, RAD2DEG
import robotcontrolapp_pb2


class Matrix44:
    """A 4x4 matrix for cartesian positions and transformations. Values are to be interpreted as mm for positions and degrees for angles."""

    def __init__(self):
        """Initializes a 4x4 matrix data as a unit matrix"""
        self._data = [
            1.0,
            0.0,
            0.0,
            0.0,
            0.0,
            1.0,
            0.0,
            0.0,
            0.0,
            0.0,
            1.0,
            0.0,
            0.0,
            0.0,
            0.0,
            1.0,
        ]

    def FromGrpc(grpcMatrix: robotcontrolapp_pb2.Matrix44):
        """Constructor, copies values from GRPC matrix"""
        if len(grpcMatrix.data) != 16:
            raise Exception(
                "could not initialize Matrix44, GRPC matrix had invalid element count "
                + len(grpcMatrix.data)
            )
        result = Matrix44()
        for i in range(16):
            result._data[i] = grpcMatrix.data[i]
        return result

    def ToGrpc(self) -> robotcontrolapp_pb2.Matrix44:
        """Creates a GRPC matrix and copies the values"""
        result = robotcontrolapp_pb2.Matrix44()
        for value in self._data:
            result.data.append(value)
        return result

    def Get(self, row: int, column: int) -> float:
        """Gets a value by row and column index"""
        return self._data[4 * row + column]

    def Set(self, row: int, column: int, value: float):
        """Sets a value by row and column index"""
        self._data[4 * row + column] = value

    def GetX(self) -> float:
        """Gets the X position (in mm)"""
        return self._data[3]

    def GetY(self) -> float:
        """Gets the Y position (in mm)"""
        return self._data[7]

    def GetZ(self) -> float:
        """Gets the Z position (in mm)"""
        return self._data[11]

    def SetX(self, x: float):
        """Sets the X position (in mm)"""
        self._data[3] = x

    def SetY(self, y: float):
        """Sets the Y position (in mm)"""
        self._data[7] = y

    def SetZ(self, z: float):
        """Sets the Z position (in mm)"""
        self._data[11] = z

    def Translate(self, x: float, y: float, z: float):
        """Adds the given values to the position values (in mm)"""
        self.SetX(self.GetX() + x)
        self.SetY(self.GetY() + y)
        self.SetZ(self.GetZ() + z)

    def GetA(self) -> float:
        """Gets the A orientation (in degrees)"""
        abc = self.GetOrientation()
        return abc[0]

    def GetB(self) -> float:
        """Gets the B orientation (in degrees)"""
        abc = self.GetOrientation()
        return abc[1]

    def GetC(self) -> float:
        """Gets the C orientation (in degrees)"""
        abc = self.GetOrientation()
        return abc[2]

    def SetA(self, a: float):
        """Sets the A orientation (in degrees)"""
        self.SetOrientation(a, self.GetB(), self.GetC())

    def SetB(self, b: float):
        """Sets the A orientation (in degrees)"""
        self.SetOrientation(self.GetA(), b, self.GetC())

    def SetC(self, c: float):
        """Sets the A orientation (in degrees)"""
        self.SetOrientation(self.GetA(), self.GetB(), c)

    def GetOrientation(self) -> tuple[float, float, float]:
        """Gets the orientation (as 3-element tuple in degrees)"""
        eps = 0.001
        b = atan2(
            -self._data[8],
            sqrt((self._data[0] * self._data[0] + self._data[4] * self._data[4])),
        )

        if fabs(b - math.pi / 2.0) < eps:  # singularity b = Pi/2
            a = 0.0
            c = atan2(self._data[1], self._data[5])
        elif fabs(b + math.pi / 2.0) < eps:  # singularity b = - PI/2
            a = 0.0
            c = -atan2(self._data[1], self._data[5])
        else:  # normal case
            cb = cos(b)
            a = atan2(self._data[4] / cb, self._data[0] / cb)
            c = atan2(self._data[9] / cb, self._data[10] / cb)

        a *= RAD2DEG
        b *= RAD2DEG
        c *= RAD2DEG

        return (a, b, c)

    def SetOrientation(self, a: float, b: float, c: float):
        """Sets the orientation (in degrees)"""
        alpha = a * DEG2RAD
        beta = b * DEG2RAD
        gamma = c * DEG2RAD

        sa = sin(alpha)
        ca = cos(alpha)
        sb = sin(beta)
        cb = cos(beta)
        sg = sin(gamma)
        cg = cos(gamma)

        self._data[0] = ca * cb
        self._data[1] = ca * sb * sg - sa * cg
        self._data[2] = ca * sb * cg + sa * sg
        self._data[4] = sa * cb
        self._data[5] = sa * sb * sg + ca * cg
        self._data[6] = sa * sb * cg - ca * sg
        self._data[8] = -sb
        self._data[9] = cb * sg
        self._data[10] = cb * cg
