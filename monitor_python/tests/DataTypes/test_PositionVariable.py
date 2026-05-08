import unittest

from DataTypes.Matrix44 import Matrix44
from DataTypes.ProgramVariable import (
    MakePositionVariableBoth,
    MakePositionVariableCartesian,
    MakePositionVariableJoint,
    PositionVariable,
)


class PositionVariableTest(unittest.TestCase):
    def test_init(self):
        name = "varName"
        var = PositionVariable(name)
        self.assertEqual(name, var.name)

        self.assertEqual([0, 0, 0, 0, 0, 0], var.robotAxes)
        self.assertEqual([0, 0, 0], var.externalAxes)
        self.assertEqual(
            [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1], var.cartesian._data
        )

    def test_MakeJoint(self):
        name = "varName"
        var = MakePositionVariableJoint(name, [10, 20, 30, 40, 50, 60], [100, 200, 300])
        self.assertEqual(name, var.name)
        self.assertEqual([10, 20, 30, 40, 50, 60], var.robotAxes)
        self.assertEqual([100, 200, 300], var.externalAxes)
        self.assertEqual(
            [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1], var.cartesian._data
        )

    def test_MakeCartesian(self):
        name = "varName"
        matrix = Matrix44()
        for i in range(16):
            matrix._data[i] = 10 * (i + 1)
        var = MakePositionVariableCartesian(name, matrix, [100, 200, 300])
        self.assertEqual([0, 0, 0, 0, 0, 0], var.robotAxes)
        self.assertEqual([100, 200, 300], var.externalAxes)
        self.assertEqual(matrix._data, var.cartesian._data)

    def test_MakeBoth(self):
        name = "varName"
        matrix = Matrix44()
        for i in range(16):
            matrix._data[i] = 10 * (i + 1)
        var = MakePositionVariableBoth(
            name, matrix, [10, 20, 30, 40, 50, 60], [100, 200, 300]
        )
        self.assertEqual([10, 20, 30, 40, 50, 60], var.robotAxes)
        self.assertEqual([100, 200, 300], var.externalAxes)
        self.assertEqual(matrix._data, var.cartesian._data)

    def test_GetCartesian(self):
        name = "varName"
        matrix = Matrix44()
        for i in range(16):
            matrix._data[i] = 10 * (i + 1)
        var = MakePositionVariableCartesian(name, matrix, [100, 200, 300])
        self.assertEqual(matrix._data, var.cartesian._data)

    def test_SetCartesian(self):
        name = "varName"
        matrix = Matrix44()
        for i in range(16):
            matrix._data[i] = 100 * (i + 1)
        var = PositionVariable(name)
        var.cartesian = matrix
        self.assertEqual(matrix._data, var.cartesian._data)

    def test_GetRobotAxes(self):
        name = "varName"
        var = MakePositionVariableJoint(name, [10, 20, 30, 40, 50, 60], [100, 200, 300])
        self.assertEqual([10, 20, 30, 40, 50, 60], var.robotAxes)

    def test_SetRobotAxes(self):
        name = "varName"
        var = PositionVariable(name)
        var.SetRobotAxes([100, 200, 300, 400, 500, 600])
        self.assertEqual([100, 200, 300, 400, 500, 600], var.robotAxes)

        # less than 6 elements (should set all others to 0)
        var.SetRobotAxes([1, 2, 3])
        self.assertEqual([1, 2, 3, 0, 0, 0], var.robotAxes)

        # no elements
        var.SetRobotAxes([])
        self.assertEqual([0, 0, 0, 0, 0, 0], var.robotAxes)

        # more than 7 elements
        var.SetRobotAxes([1, 2, 3, 4, 5, 6, 7])
        self.assertEqual([1, 2, 3, 4, 5, 6], var.robotAxes)

    def test_GetExternalAxes(self):
        name = "varName"
        var = PositionVariable(name)
        var.SetExternalAxes([1000, 2000, 3000])
        self.assertEqual([1000, 2000, 3000], var.externalAxes)

        # less than 3 elements (should set all others to 0)
        var.SetExternalAxes([100, 200])
        self.assertEqual([100, 200, 0], var.externalAxes)

        # no elements
        var.SetExternalAxes([])
        self.assertEqual([0, 0, 0], var.externalAxes)

        # more than 3 elements
        var.SetExternalAxes([100, 200, 300, 400])
        self.assertEqual([100, 200, 300], var.externalAxes)


if __name__ == "__main__":
    unittest.main()
