from typing import List

from DataTypes.Matrix44 import Matrix44


# Program variable base type
class ProgramVariable:
    # Constructor
    def __init__(self, name: str):
        self.__name = name

    # Gets the variable name
    def GetName(self) -> str:
        return self.__name

    # Sets the variable name
    def SetName(self, name: str):
        self.__name = name


# Number variable
class NumberVariable(ProgramVariable):
    __value: float

    # Constructor
    def __init__(self, name: str, value: float = 0):
        ProgramVariable.__init__(self, name)
        self.__value = value

    # Gets the variable value
    def GetValue(self) -> float:
        return self.__value

    # Sets the variable value
    def SetValue(self, value: float):
        self.__value = value


# Position variable
class PositionVariable(ProgramVariable):
    # Constructor
    def __init__(self, name: str):
        ProgramVariable.__init__(self, name)
        self.__cartesian = Matrix44()
        self.__robotAxes = [0, 0, 0, 0, 0, 0]
        self.__externalAxes = [0, 0, 0]

    # Makes a joint position variable
    def MakeJoint(
        name: str, robotAxes: List[int], externalAxes: List[int]
    ) -> ProgramVariable:
        result = PositionVariable(name)
        result.SetRobotAxes(robotAxes)
        if not externalAxes is None:
            result.SetExternalAxes(externalAxes)
        return result

    # Makes a cartesian position variable
    def MakeCartesian(
        name: str,
        cartesian: Matrix44,
        externalAxes: List[int],
    ) -> ProgramVariable:
        result = PositionVariable(name)
        result.SetCartesian(cartesian)

        if not externalAxes is None:
            result.SetExternalAxes(externalAxes)
        return result

    # Makes a position variable with both joints and cartesian values
    def MakeBoth(
        name: str, cartesian: Matrix44, robotAxes: List[int], externalAxes: List[int]
    ) -> ProgramVariable:
        result = PositionVariable(name)
        result.SetCartesian(cartesian)

        result.SetRobotAxes(robotAxes)
        if not externalAxes is None:
            result.SetExternalAxes(externalAxes)
        return result

    # Gets the cartesian position and orientation
    def GetCartesian(self) -> Matrix44:
        return self.__cartesian

    # Sets the cartesian position and orientation
    def SetCartesian(self, cartesian: Matrix44):
        self.__cartesian = cartesian

    # Gets the robot axes
    def GetRobotAxes(self):
        return self.__robotAxes

    # Sets the robot axes
    def SetRobotAxes(self, robotAxes: List[int]):
        length = min(len(self.__robotAxes), len(robotAxes))
        for i in range(length, len(self.__robotAxes)):
            self.__robotAxes[i] = 0
        for i in range(length):
            self.__robotAxes[i] = robotAxes[i]

    # Sets the external axes
    def GetExternalAxes(self):
        return self.__externalAxes

    # Sets the external axes
    def SetExternalAxes(self, externalAxes: list[int]):
        length = min(len(self.__externalAxes), len(externalAxes))
        for i in range(length, 3):
            self.__externalAxes[i] = 0
        for i in range(length):
            self.__externalAxes[i] = externalAxes[i]
