from typing import List

from DataTypes.Matrix44 import Matrix44


class ProgramVariable:
    """Program variable base type"""

    def __init__(self, name: str):
        self.__name = name

    def GetName(self) -> str:
        """Gets the variable name"""
        return self.__name

    def SetName(self, name: str):
        """Sets the variable name"""
        self.__name = name


class NumberVariable(ProgramVariable):
    """Number variable"""

    __value: float

    def __init__(self, name: str, value: float = 0):
        ProgramVariable.__init__(self, name)
        self.__value = value

    def GetValue(self) -> float:
        """Gets the variable value"""
        return self.__value

    def SetValue(self, value: float):
        """Sets the variable value"""
        self.__value = value


class PositionVariable(ProgramVariable):
    """Position variable"""

    def __init__(self, name: str):
        ProgramVariable.__init__(self, name)
        self.__cartesian = Matrix44()
        self.__robotAxes = [0, 0, 0, 0, 0, 0]
        self.__externalAxes = [0, 0, 0]

    def MakeJoint(
        name: str, robotAxes: List[int], externalAxes: List[int]
    ) -> ProgramVariable:
        """Makes a joint position variable"""
        result = PositionVariable(name)
        result.SetRobotAxes(robotAxes)
        if not externalAxes is None:
            result.SetExternalAxes(externalAxes)
        return result

    def MakeCartesian(
        name: str,
        cartesian: Matrix44,
        externalAxes: List[int],
    ) -> ProgramVariable:
        """Makes a cartesian position variable"""
        result = PositionVariable(name)
        result.SetCartesian(cartesian)

        if not externalAxes is None:
            result.SetExternalAxes(externalAxes)
        return result

    def MakeBoth(
        name: str, cartesian: Matrix44, robotAxes: List[int], externalAxes: List[int]
    ) -> ProgramVariable:
        """Makes a position variable with both joints and cartesian values"""
        result = PositionVariable(name)
        result.SetCartesian(cartesian)

        result.SetRobotAxes(robotAxes)
        if not externalAxes is None:
            result.SetExternalAxes(externalAxes)
        return result

    def GetCartesian(self) -> Matrix44:
        """Gets the cartesian position and orientation"""
        return self.__cartesian

    def SetCartesian(self, cartesian: Matrix44):
        """Sets the cartesian position and orientation"""
        self.__cartesian = cartesian

    def GetRobotAxes(self):
        """Gets the robot axes"""
        return self.__robotAxes

    def SetRobotAxes(self, robotAxes: List[int]):
        """Sets the robot axes"""
        length = min(len(self.__robotAxes), len(robotAxes))
        for i in range(length, len(self.__robotAxes)):
            self.__robotAxes[i] = 0
        for i in range(length):
            self.__robotAxes[i] = robotAxes[i]

    def GetExternalAxes(self):
        """Sets the external axes"""
        return self.__externalAxes

    def SetExternalAxes(self, externalAxes: list[int]):
        """Sets the external axes"""
        length = min(len(self.__externalAxes), len(externalAxes))
        for i in range(length, 3):
            self.__externalAxes[i] = 0
        for i in range(length):
            self.__externalAxes[i] = externalAxes[i]
