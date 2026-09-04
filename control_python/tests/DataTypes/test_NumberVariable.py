import unittest

from irc_app.DataTypes.ProgramVariable import NumberVariable


class NumberVariableTest(unittest.TestCase):
    def test_init(self):
        name = "varName"
        value = 1234.5
        var = NumberVariable(name, value)
        self.assertEqual(name, var.name)
        self.assertEqual(value, var.value)

        name = "varName"
        var2 = NumberVariable(name)
        self.assertEqual(name, var2.name)
        self.assertEqual(0, var2.value)


if __name__ == "__main__":
    unittest.main()
