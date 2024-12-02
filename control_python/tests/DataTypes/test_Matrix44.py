import unittest

from DataTypes.Matrix44 import Matrix44
import robotcontrolapp_pb2


class Matrix44Test(unittest.TestCase):
    def test_init(self):
        result = Matrix44()
        self.assertEqual(1, result._data[0])
        self.assertEqual(0, result._data[1])
        self.assertEqual(0, result._data[2])
        self.assertEqual(0, result._data[3])

        self.assertEqual(0, result._data[4])
        self.assertEqual(1, result._data[5])
        self.assertEqual(0, result._data[6])
        self.assertEqual(0, result._data[7])

        self.assertEqual(0, result._data[8])
        self.assertEqual(0, result._data[9])
        self.assertEqual(1, result._data[10])
        self.assertEqual(0, result._data[11])

        self.assertEqual(0, result._data[12])
        self.assertEqual(0, result._data[13])
        self.assertEqual(0, result._data[14])
        self.assertEqual(1, result._data[15])

    def test_FromGrpc(self):
        original = robotcontrolapp_pb2.Matrix44()
        for i in range(16):
            original.data.append(10 * (i + 1))

        result = Matrix44.FromGrpc(original)
        self.assertTrue(isinstance(result, Matrix44))

        self.assertEqual(10, result._data[0])
        self.assertEqual(20, result._data[1])
        self.assertEqual(30, result._data[2])
        self.assertEqual(40, result._data[3])

        self.assertEqual(50, result._data[4])
        self.assertEqual(60, result._data[5])
        self.assertEqual(70, result._data[6])
        self.assertEqual(80, result._data[7])

        self.assertEqual(90, result._data[8])
        self.assertEqual(100, result._data[9])
        self.assertEqual(110, result._data[10])
        self.assertEqual(120, result._data[11])

        self.assertEqual(130, result._data[12])
        self.assertEqual(140, result._data[13])
        self.assertEqual(150, result._data[14])
        self.assertEqual(160, result._data[15])

    def test_ToGrpc(self):
        original = Matrix44()
        for i in range(16):
            original._data[i] = 100 * (i + 1)

        result = original.ToGrpc()
        self.assertTrue(isinstance(result, robotcontrolapp_pb2.Matrix44))

        self.assertEqual(100, result.data[0])
        self.assertEqual(200, result.data[1])
        self.assertEqual(300, result.data[2])
        self.assertEqual(400, result.data[3])

        self.assertEqual(500, result.data[4])
        self.assertEqual(600, result.data[5])
        self.assertEqual(700, result.data[6])
        self.assertEqual(800, result.data[7])

        self.assertEqual(900, result.data[8])
        self.assertEqual(1000, result.data[9])
        self.assertEqual(1100, result.data[10])
        self.assertEqual(1200, result.data[11])

        self.assertEqual(1300, result.data[12])
        self.assertEqual(1400, result.data[13])
        self.assertEqual(1500, result.data[14])
        self.assertEqual(1600, result.data[15])

    def test_Get(self):
        matrix = Matrix44()
        for i in range(16):
            matrix._data[i] = 10 * (i + 1)

        self.assertEqual(10, matrix.Get(0, 0))
        self.assertEqual(20, matrix.Get(0, 1))
        self.assertEqual(30, matrix.Get(0, 2))
        self.assertEqual(40, matrix.Get(0, 3))

        self.assertEqual(50, matrix.Get(1, 0))
        self.assertEqual(60, matrix.Get(1, 1))
        self.assertEqual(70, matrix.Get(1, 2))
        self.assertEqual(80, matrix.Get(1, 3))

        self.assertEqual(90, matrix.Get(2, 0))
        self.assertEqual(100, matrix.Get(2, 1))
        self.assertEqual(110, matrix.Get(2, 2))
        self.assertEqual(120, matrix.Get(2, 3))

        self.assertEqual(130, matrix.Get(3, 0))
        self.assertEqual(140, matrix.Get(3, 1))
        self.assertEqual(150, matrix.Get(3, 2))
        self.assertEqual(160, matrix.Get(3, 3))

        try:
            matrix.Get(-1, 0)
            self.fail()
        except:
            pass

        try:
            matrix.Get(0, -1)
            self.fail()
        except:
            pass

        try:
            matrix.Get(4, 0)
            self.fail()
        except:
            pass

        try:
            matrix.Get(0, 4)
            self.fail()
        except:
            pass

    def test_Set(self):
        matrix = Matrix44()
        for i in range(4):
            for j in range(4):
                matrix.Set(i, j, 10 * (i + 1) + 100 * (j + 1))

        self.assertEqual(110, matrix._data[0])
        self.assertEqual(210, matrix._data[1])
        self.assertEqual(310, matrix._data[2])
        self.assertEqual(410, matrix._data[3])

        self.assertEqual(120, matrix._data[4])
        self.assertEqual(220, matrix._data[5])
        self.assertEqual(320, matrix._data[6])
        self.assertEqual(420, matrix._data[7])

        self.assertEqual(130, matrix._data[8])
        self.assertEqual(230, matrix._data[9])
        self.assertEqual(330, matrix._data[10])
        self.assertEqual(430, matrix._data[11])

        self.assertEqual(140, matrix._data[12])
        self.assertEqual(240, matrix._data[13])
        self.assertEqual(340, matrix._data[14])
        self.assertEqual(440, matrix._data[15])

        try:
            matrix.Set(-1, 0, 1234)
            self.fail()
        except:
            pass

        try:
            matrix.Set(0, -1, 1234)
            self.fail()
        except:
            pass

        try:
            matrix.Set(4, 0, 1234)
            self.fail()
        except:
            pass

        try:
            matrix.Set(0, 4, 1234)
            self.fail()
        except:
            pass

    def test_GetX(self):
        matrix = Matrix44()
        matrix.Set(0, 3, 10)
        self.assertEqual(10, matrix.GetX())

    def test_GetY(self):
        matrix = Matrix44()
        matrix.Set(1, 3, 20)
        self.assertEqual(20, matrix.GetY())

    def test_GetZ(self):
        matrix = Matrix44()
        matrix.Set(2, 3, 30)
        self.assertEqual(30, matrix.GetZ())

    def test_SetX(self):
        matrix = Matrix44()
        matrix.SetX(100)
        self.assertEqual(100, matrix._data[3])

    def test_SetY(self):
        matrix = Matrix44()
        matrix.SetY(200)
        self.assertEqual(200, matrix._data[7])

    def test_SetZ(self):
        matrix = Matrix44()
        matrix.SetZ(300)
        self.assertEqual(300, matrix._data[11])

    def test_Translate(self):
        matrix = Matrix44()
        matrix.SetX(100)
        matrix.SetY(200)
        matrix.SetZ(300)

        matrix.Translate(10, 20, 30)
        self.assertEqual(110, matrix.GetX())
        self.assertEqual(220, matrix.GetY())
        self.assertEqual(330, matrix.GetZ())

    def test_GetA(self):
        matrix = Matrix44()
        matrix.SetOrientation(10, 0, 0)
        self.assertAlmostEqual(10, matrix.GetA())

    def test_GetB(self):
        matrix = Matrix44()
        matrix.SetOrientation(0, 20, 0)
        self.assertAlmostEqual(20, matrix.GetB())

    def test_GetA(self):
        matrix = Matrix44()
        matrix.SetOrientation(0, 0, 30)
        self.assertAlmostEqual(30, matrix.GetC())

    def test_SetA(self):
        matrix = Matrix44()

        matrix.SetA(100)
        self.assertAlmostEqual(100, matrix.GetA())
        self.assertAlmostEqual(0, matrix.GetB())
        self.assertAlmostEqual(0, matrix.GetC())

        matrix.SetA(180)
        self.assertAlmostEqual(180, matrix.GetA())
        self.assertAlmostEqual(0, matrix.GetB())
        self.assertAlmostEqual(0, matrix.GetC())

        matrix.SetA(-180)
        self.assertAlmostEqual(-180, matrix.GetA())
        self.assertAlmostEqual(0, matrix.GetB())
        self.assertAlmostEqual(0, matrix.GetC())

        matrix.SetA(181)
        self.assertAlmostEqual(-179, matrix.GetA())
        self.assertAlmostEqual(0, matrix.GetB())
        self.assertAlmostEqual(0, matrix.GetC())

        matrix.SetA(-181)
        self.assertAlmostEqual(179, matrix.GetA())
        self.assertAlmostEqual(0, matrix.GetB())
        self.assertAlmostEqual(0, matrix.GetC())

    def test_SetB(self):
        # Note: different but effectively equivalent angles are returned due to how ABC is calculated from the matrix representation.

        matrix = Matrix44()
        matrix.SetB(100)
        self.assertAlmostEqual(80, matrix.GetB())
        self.assertAlmostEqual(-180, matrix.GetA())
        self.assertAlmostEqual(-180, matrix.GetC())

        matrix = Matrix44()
        matrix.SetB(180)
        self.assertAlmostEqual(0, matrix.GetB())
        self.assertAlmostEqual(-180, matrix.GetA())
        self.assertAlmostEqual(-180, matrix.GetC())

        matrix = Matrix44()
        matrix.SetB(-180)
        self.assertAlmostEqual(0, matrix.GetB())
        self.assertAlmostEqual(-180, matrix.GetA())
        self.assertAlmostEqual(-180, matrix.GetC())

        matrix = Matrix44()
        matrix.SetB(181)
        self.assertAlmostEqual(-1, matrix.GetB())
        self.assertAlmostEqual(-180, matrix.GetA())
        self.assertAlmostEqual(-180, matrix.GetC())

        matrix = Matrix44()
        matrix.SetB(-181)
        self.assertAlmostEqual(1, matrix.GetB())
        self.assertAlmostEqual(-180, matrix.GetA())
        self.assertAlmostEqual(-180, matrix.GetC())

    def test_SetC(self):
        matrix = Matrix44()

        matrix.SetC(100)
        self.assertAlmostEqual(100, matrix.GetC())
        self.assertAlmostEqual(0, matrix.GetA())
        self.assertAlmostEqual(0, matrix.GetB())

        matrix.SetC(180)
        self.assertAlmostEqual(180, matrix.GetC())
        self.assertAlmostEqual(0, matrix.GetA())
        self.assertAlmostEqual(0, matrix.GetB())

        matrix.SetC(-180)
        self.assertAlmostEqual(-180, matrix.GetC())
        self.assertAlmostEqual(0, matrix.GetA())
        self.assertAlmostEqual(0, matrix.GetB())

        matrix.SetC(181)
        self.assertAlmostEqual(-179, matrix.GetC())
        self.assertAlmostEqual(0, matrix.GetA())
        self.assertAlmostEqual(0, matrix.GetB())

        matrix.SetC(-181)
        self.assertAlmostEqual(179, matrix.GetC())
        self.assertAlmostEqual(0, matrix.GetA())
        self.assertAlmostEqual(0, matrix.GetB())

    def test_GetOrientation(self):
        matrix = Matrix44()
        matrix.SetOrientation(10, 20, 30)

        result = matrix.GetOrientation()
        self.assertAlmostEqual(10, result[0])
        self.assertAlmostEqual(20, result[1])
        self.assertAlmostEqual(30, result[2])

    def test_SetOrientation(self):
        matrix = Matrix44()
        matrix.SetOrientation(10, 20, 30)

        self.assertAlmostEqual(10, matrix.GetA())
        self.assertAlmostEqual(20, matrix.GetB())
        self.assertAlmostEqual(30, matrix.GetC())


if __name__ == "__main__":
    unittest.main()
