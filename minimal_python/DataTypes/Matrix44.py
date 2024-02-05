from math import atan2, cos, fabs, sin, sqrt
import math

from DataTypes.MathDefinitions import DEG2RAD, RAD2DEG
import robotcontrolapp_pb2


class Matrix44:
    # Initializes a 4x4 matrix data as a unit matrix
    def __init__(self):
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

    # Constructor, copies values from GRPC matrix
    def FromGrpc(grpcMatrix: robotcontrolapp_pb2.Matrix44):
        if len(grpcMatrix.data) != 16:
            raise Exception(
                "could not initialize Matrix44, GRPC matrix had invalid element count "
                + len(grpcMatrix.data)
            )
        result = Matrix44()
        for i in range(16):
            result._data[i] = grpcMatrix.data[i]
        return result

    # Creates a GRPC matrix and copies the values
    def ToGrpc(self) -> robotcontrolapp_pb2.Matrix44:
        result = robotcontrolapp_pb2.Matrix44()
        for value in self._data:
            result.data.append(value)
        return result

    # Gets a value by row and column index
    def Get(self, row: int, column: int) -> float:
        return self._data[4 * row + column]

    # Sets a value by row and column index
    def Set(self, row: int, column: int, value: float):
        self._data[4 * row + column] = value

    # Gets the X position (in mm)
    def GetX(self) -> float:
        return self._data[3]

    # Gets the Y position (in mm)
    def GetY(self) -> float:
        return self._data[7]

    # Gets the Z position (in mm)
    def GetZ(self) -> float:
        return self._data[11]

    # Sets the X position (in mm)
    def SetX(self, x: float):
        self._data[3] = x

    # Sets the Y position (in mm)
    def SetY(self, y: float):
        self._data[7] = y

    # Sets the Z position (in mm)
    def SetZ(self, z: float):
        self._data[11] = z

    # Adds the given values to the position values (in mm)
    def Translate(self, x: float, y: float, z: float):
        self.SetX(self.GetX() + x)
        self.SetY(self.GetY() + y)
        self.SetZ(self.GetZ() + z)

    # Gets the A orientation (in degrees)
    def GetA(self) -> float:
        abc = self.GetOrientation()
        return abc[0]

    # Gets the B orientation (in degrees)
    def GetB(self) -> float:
        abc = self.GetOrientation()
        return abc[1]

    # Gets the C orientation (in degrees)
    def GetC(self) -> float:
        abc = self.GetOrientation()
        return abc[2]

    # Sets the A orientation (in degrees)
    def SetA(self, a: float):
        self.SetOrientation(a, self.GetB(), self.GetC())

    # Sets the A orientation (in degrees)
    def SetB(self, b: float):
        self.SetOrientation(self.GetA(), b, self.GetC())

    # Sets the A orientation (in degrees)
    def SetC(self, c: float):
        self.SetOrientation(self.GetA(), self.GetB(), c)

    # Gets the orientation (as 3-element tuple in degrees)
    def GetOrientation(self) -> tuple[float, float, float]:
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

    # Sets the orientation (in degrees)
    def SetOrientation(self, a: float, b: float, c: float):
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
