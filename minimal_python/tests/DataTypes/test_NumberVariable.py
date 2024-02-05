import unittest

from DataTypes.Matrix44 import Matrix44
from DataTypes.ProgramVariable import NumberVariable


class NumberVariableTest(unittest.TestCase):
    def test_init(self):
        name = "varName"
        value = 1234.5
        var = NumberVariable(name, value)
        self.assertEqual(name, var.GetName())
        self.assertEqual(value, var.GetValue())

        name = "varName"
        var2 = NumberVariable(name)
        self.assertEqual(name, var2.GetName())
        self.assertEqual(0, var2.GetValue())

    def test_GetName(self):
        name = "varName"
        var = NumberVariable(name, 123)
        self.assertEqual(name, var.GetName())

    def test_SetName(self):
        name = "varName"
        newName = "newName"
        var = NumberVariable(name, 123)
        var.SetName(newName)
        self.assertEqual(newName, var.GetName())

    def test_GetValue(self):
        name = "varName"
        value = 1234.5
        var = NumberVariable(name, value)
        self.assertEqual(value, var.GetValue())

    def test_SetValue(self):
        name = "varName"
        value = 1234.5
        newValue = 23456.78
        var = NumberVariable(name, value)
        var.SetValue(newValue)
        self.assertEqual(newValue, var.GetValue())


if __name__ == "__main__":
    unittest.main()
