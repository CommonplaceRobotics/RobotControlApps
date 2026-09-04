from dataclasses import dataclass
from typing import List

from .Matrix44 import Matrix44


@dataclass
class ProgramVariable:
    """Program variable base type"""

    name: str = ""
    """Name of the variable. Case insensitive, must not contain spaces or special characters."""


@dataclass
class NumberVariable(ProgramVariable):
    """Number variable"""

    value: float = 0.0
    """Value of the number variable"""

    def __init__(self, name: str, value: float = 0.0):
        """
        Constructor
        Parameters:
            name: Name of the variable. Case insensitive, must not contain spaces or special characters.
            value: Value of the variable
        """
        ProgramVariable.__init__(self, name)
        self.value = value


class PositionVariable(ProgramVariable):
    """Position variable"""

    def __init__(self, name: str):
        """
        Constructor
        Parameters:
            name: Name of the variable. Case insensitive, must not contain spaces or special characters.
        """
        ProgramVariable.__init__(self, name)
        self.cartesian = Matrix44()
        self.robotAxes = [0, 0, 0, 0, 0, 0]
        self.externalAxes = [0, 0, 0]

    def SetRobotAxes(self, robotAxes: List[int]):
        """Sets the robot axes"""
        self.robotAxes = [0] * 6
        length = min(len(self.robotAxes), len(robotAxes))
        for i in range(length):
            self.robotAxes[i] = robotAxes[i]

    def SetExternalAxes(self, externalAxes: list[int]):
        """Sets the external axes"""
        self.externalAxes = [0] * 3
        length = min(len(self.externalAxes), len(externalAxes))
        for i in range(length):
            self.externalAxes[i] = externalAxes[i]


def MakePositionVariableJoint(
    name: str, robotAxes: List[int], externalAxes: List[int]
) -> PositionVariable:
    """
    Makes a joint position variable with joint position only
    Parameters:
        name: Name of the variable. Case insensitive, must not contain spaces or special characters.
        robotAxes: Up to 6 robot axis values
        externalAxes: Up to 3 external axis values
    """
    result = PositionVariable(name)
    result.SetRobotAxes(robotAxes)
    if externalAxes is not None:
        result.SetExternalAxes(externalAxes)
    return result


def MakePositionVariableCartesian(
    name: str, cartesian: Matrix44, externalAxes: List[int]
) -> PositionVariable:
    """
    Makes a joint position variable with cartesian and external axes position only
    Parameters:
        name: Name of the variable. Case insensitive, must not contain spaces or special characters.
        cartesian: Matrix defining the cartesian position and orientation
        externalAxes: Up to 3 external axis values
    """
    """Makes a cartesian position variable"""
    result = PositionVariable(name)
    result.cartesian = cartesian

    if externalAxes is not None:
        result.SetExternalAxes(externalAxes)
    return result


def MakePositionVariableBoth(
    name: str, cartesian: Matrix44, robotAxes: List[int], externalAxes: List[int]
) -> PositionVariable:
    """
    Makes a joint position variable with both cartesian and joint position
    Parameters:
        name: Name of the variable. Case insensitive, must not contain spaces or special characters.
        cartesian: Matrix defining the cartesian position and orientation
        robotAxes: Up to 6 robot axis values
        externalAxes: Up to 3 external axis values
    """
    """Makes a position variable with both joints and cartesian values"""
    result = PositionVariable(name)
    result.cartesian = cartesian

    result.SetRobotAxes(robotAxes)
    if externalAxes is not None:
        result.SetExternalAxes(externalAxes)
    return result
