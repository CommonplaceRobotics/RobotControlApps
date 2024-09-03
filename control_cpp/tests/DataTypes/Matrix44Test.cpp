#include <gtest/gtest.h>

#include "../../src/DataTypes/Matrix44.h"

TEST(Matrix44Test, ConstructorDefault)
{
    App::DataTypes::Matrix44 matrix;
    // expecting the unit matrix
    EXPECT_EQ(1.0, matrix[0]);
    EXPECT_EQ(0.0, matrix[1]);
    EXPECT_EQ(0.0, matrix[2]);
    EXPECT_EQ(0.0, matrix[3]);

    EXPECT_EQ(0.0, matrix[4]);
    EXPECT_EQ(1.0, matrix[5]);
    EXPECT_EQ(0.0, matrix[6]);
    EXPECT_EQ(0.0, matrix[7]);

    EXPECT_EQ(0.0, matrix[8]);
    EXPECT_EQ(0.0, matrix[9]);
    EXPECT_EQ(1.0, matrix[10]);
    EXPECT_EQ(0.0, matrix[11]);

    EXPECT_EQ(0.0, matrix[12]);
    EXPECT_EQ(0.0, matrix[13]);
    EXPECT_EQ(0.0, matrix[14]);
    EXPECT_EQ(1.0, matrix[15]);
}

TEST(Matrix44Test, ConstructorCopy)
{
    App::DataTypes::Matrix44 matrix;
    for (int i = 0; i < 16; i++) matrix[i] = 10 * (i + 1); // 10, 20, 30,... 160

    App::DataTypes::Matrix44 result = App::DataTypes::Matrix44(matrix);
    EXPECT_EQ(10.0, result[0]);
    EXPECT_EQ(20.0, result[1]);
    EXPECT_EQ(30.0, result[2]);
    EXPECT_EQ(40.0, result[3]);

    EXPECT_EQ(50.0, result[4]);
    EXPECT_EQ(60.0, result[5]);
    EXPECT_EQ(70.0, result[6]);
    EXPECT_EQ(80.0, result[7]);

    EXPECT_EQ(90.0, result[8]);
    EXPECT_EQ(100.0, result[9]);
    EXPECT_EQ(110.0, result[10]);
    EXPECT_EQ(120.0, result[11]);

    EXPECT_EQ(130.0, result[12]);
    EXPECT_EQ(140.0, result[13]);
    EXPECT_EQ(150.0, result[14]);
    EXPECT_EQ(160.0, result[15]);
}

TEST(Matrix44Test, OperatorElementAccess)
{
    App::DataTypes::Matrix44 matrix;
    // write access
    // this test uses the same operator for writes so it does not actually check
    // whether it writes to the correct indices. This is cross-checked with
    // operator() below.
    for (int i = 0; i < 16; i++) matrix[i] = 10 * (i + 1); // 10, 20, 30,... 160

    // read access
    EXPECT_EQ(10.0, matrix[0]);
    EXPECT_EQ(20.0, matrix[1]);
    EXPECT_EQ(30.0, matrix[2]);
    EXPECT_EQ(40.0, matrix[3]);

    EXPECT_EQ(50.0, matrix[4]);
    EXPECT_EQ(60.0, matrix[5]);
    EXPECT_EQ(70.0, matrix[6]);
    EXPECT_EQ(80.0, matrix[7]);

    EXPECT_EQ(90.0, matrix[8]);
    EXPECT_EQ(100.0, matrix[9]);
    EXPECT_EQ(110.0, matrix[10]);
    EXPECT_EQ(120.0, matrix[11]);

    EXPECT_EQ(130.0, matrix[12]);
    EXPECT_EQ(140.0, matrix[13]);
    EXPECT_EQ(150.0, matrix[14]);
    EXPECT_EQ(160.0, matrix[15]);

    try
    {
        matrix[-1];
        FAIL();
    }
    catch (...)
    {}

    try
    {
        matrix[16];
        FAIL();
    }
    catch (...)
    {}

    // const read access
    const App::DataTypes::Matrix44 matrixConst = matrix;

    EXPECT_EQ(10.0, matrixConst[0]);
    EXPECT_EQ(20.0, matrixConst[1]);
    EXPECT_EQ(30.0, matrixConst[2]);
    EXPECT_EQ(40.0, matrixConst[3]);

    EXPECT_EQ(50.0, matrixConst[4]);
    EXPECT_EQ(60.0, matrixConst[5]);
    EXPECT_EQ(70.0, matrixConst[6]);
    EXPECT_EQ(80.0, matrixConst[7]);

    EXPECT_EQ(90.0, matrixConst[8]);
    EXPECT_EQ(100.0, matrixConst[9]);
    EXPECT_EQ(110.0, matrixConst[10]);
    EXPECT_EQ(120.0, matrixConst[11]);

    EXPECT_EQ(130.0, matrixConst[12]);
    EXPECT_EQ(140.0, matrixConst[13]);
    EXPECT_EQ(150.0, matrixConst[14]);
    EXPECT_EQ(160.0, matrixConst[15]);

    try
    {
        matrixConst[-1];
        FAIL();
    }
    catch (...)
    {}

    try
    {
        matrixConst[16];
        FAIL();
    }
    catch (...)
    {}
}

TEST(Matrix44Test, OperatorElementAccessXYReadConst)
{
    App::DataTypes::Matrix44 matrixNonConst;
    for (int i = 0; i < 16; i++) matrixNonConst[i] = 10 * (i + 1); // 10, 20, 30,... 160
    const App::DataTypes::Matrix44 matrix = matrixNonConst;

    EXPECT_EQ(10.0, matrix(0, 0));
    EXPECT_EQ(20.0, matrix(0, 1));
    EXPECT_EQ(30.0, matrix(0, 2));
    EXPECT_EQ(40.0, matrix(0, 3));

    EXPECT_EQ(50.0, matrix(1, 0));
    EXPECT_EQ(60.0, matrix(1, 1));
    EXPECT_EQ(70.0, matrix(1, 2));
    EXPECT_EQ(80.0, matrix(1, 3));

    EXPECT_EQ(90.0, matrix(2, 0));
    EXPECT_EQ(100.0, matrix(2, 1));
    EXPECT_EQ(110.0, matrix(2, 2));
    EXPECT_EQ(120.0, matrix(2, 3));

    EXPECT_EQ(130.0, matrix(3, 0));
    EXPECT_EQ(140.0, matrix(3, 1));
    EXPECT_EQ(150.0, matrix(3, 2));
    EXPECT_EQ(160.0, matrix(3, 3));

    try
    {
        matrix(-1, 3);
        FAIL();
    }
    catch (...)
    {}

    try
    {
        matrix(3, -1);
        FAIL();
    }
    catch (...)
    {}

    try
    {
        matrix(4, 0);
        FAIL();
    }
    catch (...)
    {}

    try
    {
        matrix(0, 4);
        FAIL();
    }
    catch (...)
    {}
}

TEST(Matrix44Test, OperatorElementAccessXYRead)
{
    App::DataTypes::Matrix44 matrix;
    for (int i = 0; i < 16; i++) matrix[i] = 10 * (i + 1); // 10, 20, 30,... 160

    EXPECT_EQ(10.0, matrix(0, 0));
    EXPECT_EQ(20.0, matrix(0, 1));
    EXPECT_EQ(30.0, matrix(0, 2));
    EXPECT_EQ(40.0, matrix(0, 3));

    EXPECT_EQ(50.0, matrix(1, 0));
    EXPECT_EQ(60.0, matrix(1, 1));
    EXPECT_EQ(70.0, matrix(1, 2));
    EXPECT_EQ(80.0, matrix(1, 3));

    EXPECT_EQ(90.0, matrix(2, 0));
    EXPECT_EQ(100.0, matrix(2, 1));
    EXPECT_EQ(110.0, matrix(2, 2));
    EXPECT_EQ(120.0, matrix(2, 3));

    EXPECT_EQ(130.0, matrix(3, 0));
    EXPECT_EQ(140.0, matrix(3, 1));
    EXPECT_EQ(150.0, matrix(3, 2));
    EXPECT_EQ(160.0, matrix(3, 3));

    try
    {
        matrix(-1, 3);
        FAIL();
    }
    catch (...)
    {}

    try
    {
        matrix(3, -1);
        FAIL();
    }
    catch (...)
    {}

    try
    {
        matrix(4, 0);
        FAIL();
    }
    catch (...)
    {}

    try
    {
        matrix(0, 4);
        FAIL();
    }
    catch (...)
    {}
}

TEST(Matrix44Test, OperatorElementAccessXYWrite)
{
    App::DataTypes::Matrix44 matrix;

    matrix(0, 0) = 100;
    matrix(0, 1) = 110;
    matrix(0, 2) = 120;
    matrix(0, 3) = 130;

    matrix(1, 0) = 200;
    matrix(1, 1) = 210;
    matrix(1, 2) = 220;
    matrix(1, 3) = 230;

    matrix(2, 0) = 300;
    matrix(2, 1) = 310;
    matrix(2, 2) = 320;
    matrix(2, 3) = 330;

    matrix(3, 0) = 400;
    matrix(3, 1) = 410;
    matrix(3, 2) = 420;
    matrix(3, 3) = 430;

    EXPECT_EQ(100.0, matrix[0]);
    EXPECT_EQ(110.0, matrix[1]);
    EXPECT_EQ(120.0, matrix[2]);
    EXPECT_EQ(130.0, matrix[3]);

    EXPECT_EQ(200.0, matrix[4]);
    EXPECT_EQ(210.0, matrix[5]);
    EXPECT_EQ(220.0, matrix[6]);
    EXPECT_EQ(230.0, matrix[7]);

    EXPECT_EQ(300.0, matrix[8]);
    EXPECT_EQ(310.0, matrix[9]);
    EXPECT_EQ(320.0, matrix[10]);
    EXPECT_EQ(330.0, matrix[11]);

    EXPECT_EQ(400.0, matrix[12]);
    EXPECT_EQ(410.0, matrix[13]);
    EXPECT_EQ(420.0, matrix[14]);
    EXPECT_EQ(430.0, matrix[15]);

    try
    {
        matrix(-1, 3) = 1;
        FAIL();
    }
    catch (...)
    {}

    try
    {
        matrix(3, -1) = 1;
        FAIL();
    }
    catch (...)
    {}

    try
    {
        matrix(4, 0) = 1;
        FAIL();
    }
    catch (...)
    {}

    try
    {
        matrix(0, 4) = 1;
        FAIL();
    }
    catch (...)
    {}
}

TEST(Matrix44Test, GetX)
{
    App::DataTypes::Matrix44 matrix;
    matrix(0, 3) = 10;
    EXPECT_EQ(10, matrix.GetX());
}

TEST(Matrix44Test, GetY)
{
    App::DataTypes::Matrix44 matrix;
    matrix(1, 3) = 20;
    EXPECT_EQ(20, matrix.GetY());
}

TEST(Matrix44Test, GetZ)
{
    App::DataTypes::Matrix44 matrix;
    matrix(2, 3) = 30;
    EXPECT_EQ(30, matrix.GetZ());
}

TEST(Matrix44Test, SetX)
{
    App::DataTypes::Matrix44 matrix;
    matrix.SetX(100);
    EXPECT_EQ(100, matrix.GetX());
}

TEST(Matrix44Test, SetY)
{
    App::DataTypes::Matrix44 matrix;
    matrix.SetY(200);
    EXPECT_EQ(200, matrix.GetY());
}

TEST(Matrix44Test, SetZ)
{
    App::DataTypes::Matrix44 matrix;
    matrix.SetZ(300);
    EXPECT_EQ(300, matrix.GetZ());
}

TEST(Matrix44Test, GetA)
{
    App::DataTypes::Matrix44 matrix;
    matrix.SetOrientation(10, 0, 0);
    EXPECT_NEAR(10, matrix.GetA(), 0.0001);
}

TEST(Matrix44Test, GetB)
{
    App::DataTypes::Matrix44 matrix;
    matrix.SetOrientation(0, 20, 0);
    EXPECT_NEAR(20, matrix.GetB(), 0.0001);
}

TEST(Matrix44Test, GetC)
{
    App::DataTypes::Matrix44 matrix;
    matrix.SetOrientation(0, 0, 30);
    EXPECT_NEAR(30, matrix.GetC(), 0.0001);
}

TEST(Matrix44Test, SetA)
{
    {
        App::DataTypes::Matrix44 matrix;
        matrix.SetA(100);
        EXPECT_NEAR(100, matrix.GetA(), 0.0001);
        EXPECT_NEAR(0, matrix.GetB(), 0.0001);
        EXPECT_NEAR(0, matrix.GetC(), 0.0001);
    }

    {
        App::DataTypes::Matrix44 matrix;
        matrix.SetA(180);
        EXPECT_NEAR(180, matrix.GetA(), 0.0001);
        EXPECT_NEAR(0, matrix.GetB(), 0.0001);
        EXPECT_NEAR(0, matrix.GetC(), 0.0001);
    }

    {
        App::DataTypes::Matrix44 matrix;
        matrix.SetA(-180);
        EXPECT_NEAR(-180, matrix.GetA(), 0.0001);
        EXPECT_NEAR(0, matrix.GetB(), 0.0001);
        EXPECT_NEAR(0, matrix.GetC(), 0.0001);
    }

    {
        App::DataTypes::Matrix44 matrix;
        matrix.SetA(181);
        EXPECT_NEAR(-179, matrix.GetA(), 0.0001);
        EXPECT_NEAR(0, matrix.GetB(), 0.0001);
        EXPECT_NEAR(0, matrix.GetC(), 0.0001);
    }

    {
        App::DataTypes::Matrix44 matrix;
        matrix.SetA(-181);
        EXPECT_NEAR(179, matrix.GetA(), 0.0001);
        EXPECT_NEAR(0, matrix.GetB(), 0.0001);
        EXPECT_NEAR(0, matrix.GetC(), 0.0001);
    }
}

TEST(Matrix44Test, SetB)
{
    // Note: different but effectively equivalent angles are returned due to how ABC is calculated from the matrix representation.
    {
        App::DataTypes::Matrix44 matrix;
        matrix.SetB(100);
        EXPECT_NEAR(80, matrix.GetB(), 0.0001);
        EXPECT_NEAR(-180, matrix.GetA(), 0.0001);
        EXPECT_NEAR(-180, matrix.GetC(), 0.0001);
    }

    {
        App::DataTypes::Matrix44 matrix;
        matrix.SetB(180);
        EXPECT_NEAR(0, matrix.GetB(), 0.0001);
        EXPECT_NEAR(-180, matrix.GetA(), 0.0001);
        EXPECT_NEAR(-180, matrix.GetC(), 0.0001);
    }

    {
        App::DataTypes::Matrix44 matrix;
        matrix.SetB(-180);
        EXPECT_NEAR(0, matrix.GetB(), 0.0001);
        EXPECT_NEAR(-180, matrix.GetA(), 0.0001);
        EXPECT_NEAR(-180, matrix.GetC(), 0.0001);
    }

    {
        App::DataTypes::Matrix44 matrix;
        matrix.SetB(181);
        EXPECT_NEAR(-1, matrix.GetB(), 0.0001);
        EXPECT_NEAR(-180, matrix.GetA(), 0.0001);
        EXPECT_NEAR(-180, matrix.GetC(), 0.0001);
    }

    {
        App::DataTypes::Matrix44 matrix;
        matrix.SetB(-181);
        EXPECT_NEAR(1, matrix.GetB(), 0.0001);
        EXPECT_NEAR(-180, matrix.GetA(), 0.0001);
        EXPECT_NEAR(-180, matrix.GetC(), 0.0001);
    }
}

TEST(Matrix44Test, SetC)
{
    {
        App::DataTypes::Matrix44 matrix;
        matrix.SetC(100);
        EXPECT_NEAR(100, matrix.GetC(), 0.0001);
        EXPECT_NEAR(0, matrix.GetA(), 0.0001);
        EXPECT_NEAR(0, matrix.GetB(), 0.0001);
    }

    {
        App::DataTypes::Matrix44 matrix;
        matrix.SetC(180);
        EXPECT_NEAR(180, matrix.GetC(), 0.0001);
        EXPECT_NEAR(0, matrix.GetA(), 0.0001);
        EXPECT_NEAR(0, matrix.GetB(), 0.0001);
    }

    {
        App::DataTypes::Matrix44 matrix;
        matrix.SetC(-180);
        EXPECT_NEAR(-180, matrix.GetC(), 0.0001);
        EXPECT_NEAR(0, matrix.GetA(), 0.0001);
        EXPECT_NEAR(0, matrix.GetB(), 0.0001);
    }

    {
        App::DataTypes::Matrix44 matrix;
        matrix.SetC(181);
        EXPECT_NEAR(-179, matrix.GetC(), 0.0001);
        EXPECT_NEAR(0, matrix.GetA(), 0.0001);
        EXPECT_NEAR(0, matrix.GetB(), 0.0001);
    }

    {
        App::DataTypes::Matrix44 matrix;
        matrix.SetC(-181);
        EXPECT_NEAR(179, matrix.GetC(), 0.0001);
        EXPECT_NEAR(0, matrix.GetA(), 0.0001);
        EXPECT_NEAR(0, matrix.GetB(), 0.0001);
    }
}

TEST(Matrix44Test, Translate)
{
    App::DataTypes::Matrix44 matrix;
    matrix(0, 3) = 10;
    matrix(1, 3) = 20;
    matrix(2, 3) = 30;
    matrix.Translate(100, 200, 300);
    EXPECT_EQ(110, matrix.GetX());
    EXPECT_EQ(220, matrix.GetY());
    EXPECT_EQ(330, matrix.GetZ());
}

TEST(Matrix44Test, GetOrientation)
{
    App::DataTypes::Matrix44 matrix;
    matrix.SetOrientation(10, 20, 30);

    double resA = 0, resB = 0, resC = 0;
    matrix.GetOrientation(resA, resB, resC);
    EXPECT_NEAR(10, resA, 0.0001);
    EXPECT_NEAR(20, resB, 0.0001);
    EXPECT_NEAR(30, resC, 0.0001);
}

TEST(Matrix44Test, SetOrientation)
{
    App::DataTypes::Matrix44 matrix;
    matrix.SetOrientation(10, 20, 30);
    EXPECT_NEAR(10, matrix.GetA(), 0.0001);
    EXPECT_NEAR(20, matrix.GetB(), 0.0001);
    EXPECT_NEAR(30, matrix.GetC(), 0.0001);
}

TEST(Matrix44Test, ToGrpc)
{
    App::DataTypes::Matrix44 matrix;
    for (int i = 0; i < 16; i++) matrix[i] = 10 * (i + 1); // 10, 20, 30,... 160

    robotcontrolapp::Matrix44 result = matrix.ToGrpc();
    ASSERT_EQ(10, result.data().at(0));
    ASSERT_EQ(20, result.data().at(1));
    ASSERT_EQ(30, result.data().at(2));
    ASSERT_EQ(40, result.data().at(3));

    ASSERT_EQ(50, result.data().at(4));
    ASSERT_EQ(60, result.data().at(5));
    ASSERT_EQ(70, result.data().at(6));
    ASSERT_EQ(80, result.data().at(7));

    ASSERT_EQ(90, result.data().at(8));
    ASSERT_EQ(100, result.data().at(9));
    ASSERT_EQ(110, result.data().at(10));
    ASSERT_EQ(120, result.data().at(11));

    ASSERT_EQ(130, result.data().at(12));
    ASSERT_EQ(140, result.data().at(13));
    ASSERT_EQ(150, result.data().at(14));
    ASSERT_EQ(160, result.data().at(15));
}
