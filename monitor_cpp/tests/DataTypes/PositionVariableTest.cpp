#include <gtest/gtest.h>

#include "../../src/DataTypes/ProgramVariable.h"

TEST(PositionVariableTest, ConstructorCartesian)
{
    {
        std::string name = "myVariableName";
        App::DataTypes::Matrix44 cartesianPos;
        std::array<double, 3> externalJoints{0};
        App::DataTypes::PositionVariable programVariable(name, cartesianPos, externalJoints);

        EXPECT_STREQ(name.c_str(), programVariable.GetName().c_str());
        for (size_t i = 0; i < 16; i++) EXPECT_EQ(cartesianPos[i], programVariable.GetCartesian()[i]);
        for (size_t i = 0; i < programVariable.GetRobotAxes().size(); i++) EXPECT_EQ(0, programVariable.GetRobotAxes()[i]);
        EXPECT_EQ(externalJoints[0], programVariable.GetExternalAxes()[0]);
        EXPECT_EQ(externalJoints[1], programVariable.GetExternalAxes()[1]);
        EXPECT_EQ(externalJoints[2], programVariable.GetExternalAxes()[2]);
    }

    // empty name, values
    {
        std::string name = "";
        App::DataTypes::Matrix44 cartesianPos;
        cartesianPos.Translate(1, 2, 3);
        cartesianPos.SetOrientation(10, 20, 30);
        std::array<double, 3> externalJoints{100, 200, 300};
        App::DataTypes::PositionVariable programVariable(name, cartesianPos, externalJoints);

        EXPECT_STREQ(name.c_str(), programVariable.GetName().c_str());
        for (size_t i = 0; i < 16; i++) EXPECT_EQ(cartesianPos[i], programVariable.GetCartesian()[i]);
        for (size_t i = 0; i < programVariable.GetRobotAxes().size(); i++) EXPECT_EQ(0, programVariable.GetRobotAxes()[i]);
        EXPECT_EQ(externalJoints[0], programVariable.GetExternalAxes()[0]);
        EXPECT_EQ(externalJoints[1], programVariable.GetExternalAxes()[1]);
        EXPECT_EQ(externalJoints[2], programVariable.GetExternalAxes()[2]);
    }
}

TEST(PositionVariableTest, ConstructorJoints)
{
    // name, default value
    {
        std::string name = "myVariableName";
        std::array<double, 6> robotJoints{0};
        std::array<double, 3> externalJoints{0};
        App::DataTypes::PositionVariable programVariable(name, robotJoints, externalJoints);

        App::DataTypes::Matrix44 cartesianExpect;
        for (size_t i = 0; i < 16; i++) EXPECT_EQ(cartesianExpect[i], programVariable.GetCartesian()[i]);
        for (size_t i = 0; i < programVariable.GetRobotAxes().size(); i++) EXPECT_EQ(0, programVariable.GetRobotAxes()[i]);
        EXPECT_EQ(externalJoints[0], programVariable.GetExternalAxes()[0]);
        EXPECT_EQ(externalJoints[1], programVariable.GetExternalAxes()[1]);
        EXPECT_EQ(externalJoints[2], programVariable.GetExternalAxes()[2]);
    }

    // empty name, default value
    {
        std::string name = "";
        std::array<double, 6> robotJoints{10, 20, 30, 40, 50, 60};
        std::array<double, 3> externalJoints{70, 80, 90};
        App::DataTypes::PositionVariable programVariable(name, robotJoints, externalJoints);

        App::DataTypes::Matrix44 cartesianExpect;
        for (size_t i = 0; i < 16; i++) EXPECT_EQ(cartesianExpect[i], programVariable.GetCartesian()[i]);
        for (size_t i = 0; i < programVariable.GetRobotAxes().size(); i++) EXPECT_EQ(robotJoints[i], programVariable.GetRobotAxes()[i]);
        EXPECT_EQ(externalJoints[0], programVariable.GetExternalAxes()[0]);
        EXPECT_EQ(externalJoints[1], programVariable.GetExternalAxes()[1]);
        EXPECT_EQ(externalJoints[2], programVariable.GetExternalAxes()[2]);
    }
}

TEST(PositionVariableTest, ConstructorBoth)
{
    {
        std::string name = "myVariableName";
        App::DataTypes::Matrix44 cartesianPos;
        std::array<double, 6> robotJoints{0};
        std::array<double, 3> externalJoints{0};
        App::DataTypes::PositionVariable programVariable(name, cartesianPos, robotJoints, externalJoints);

        EXPECT_STREQ(name.c_str(), programVariable.GetName().c_str());
        for (size_t i = 0; i < 16; i++) EXPECT_EQ(cartesianPos[i], programVariable.GetCartesian()[i]);
        for (size_t i = 0; i < programVariable.GetRobotAxes().size(); i++) EXPECT_EQ(0, programVariable.GetRobotAxes()[i]);
        EXPECT_EQ(externalJoints[0], programVariable.GetExternalAxes()[0]);
        EXPECT_EQ(externalJoints[1], programVariable.GetExternalAxes()[1]);
        EXPECT_EQ(externalJoints[2], programVariable.GetExternalAxes()[2]);
    }

    // empty name, values
    {
        std::string name = "";
        App::DataTypes::Matrix44 cartesianPos;
        cartesianPos.Translate(1, 2, 3);
        cartesianPos.SetOrientation(10, 20, 30);
        std::array<double, 6> robotJoints{10, 20, 30, 40, 50, 60};
        std::array<double, 3> externalJoints{100, 200, 300};
        App::DataTypes::PositionVariable programVariable(name, cartesianPos, robotJoints, externalJoints);

        EXPECT_STREQ(name.c_str(), programVariable.GetName().c_str());
        for (size_t i = 0; i < 16; i++) EXPECT_EQ(cartesianPos[i], programVariable.GetCartesian()[i]);
        for (size_t i = 0; i < programVariable.GetRobotAxes().size(); i++) EXPECT_EQ(robotJoints[i], programVariable.GetRobotAxes()[i]);
        EXPECT_EQ(externalJoints[0], programVariable.GetExternalAxes()[0]);
        EXPECT_EQ(externalJoints[1], programVariable.GetExternalAxes()[1]);
        EXPECT_EQ(externalJoints[2], programVariable.GetExternalAxes()[2]);
    }
}

TEST(PositionVariableTest, GetName)
{
    std::string name = "myVariableName";
    std::array<double, 6> robotJoints{0};
    std::array<double, 3> externalJoints{0};
    App::DataTypes::PositionVariable programVariable(name, robotJoints, externalJoints);

    EXPECT_STREQ(name.c_str(), programVariable.GetName().c_str());
}

TEST(PositionVariableTest, SetName)
{
    std::string name = "myVariableName";
    std::string newName = "otherName";
    std::array<double, 6> robotJoints{0};
    std::array<double, 3> externalJoints{0};
    App::DataTypes::PositionVariable programVariable(name, robotJoints, externalJoints);

    programVariable.SetName(newName);
    EXPECT_STREQ(newName.c_str(), programVariable.GetName().c_str());
}

TEST(PositionVariableTest, GetSetRobotAxes)
{
    std::string name = "myVariableName";
    std::array<double, 6> robotJoints{0};
    std::array<double, 3> externalJoints{0};
    App::DataTypes::PositionVariable programVariable(name, robotJoints, externalJoints);

    std::array<double, 6> newRobotJoints{110, 220, 330, 440, 550, 660};
    programVariable.SetRobotAxes(newRobotJoints);

    App::DataTypes::Matrix44 cartesianExpect;
    for (size_t i = 0; i < 16; i++) EXPECT_EQ(cartesianExpect[i], programVariable.GetCartesian()[i]);
    for (size_t i = 0; i < programVariable.GetRobotAxes().size(); i++) EXPECT_EQ(newRobotJoints[i], programVariable.GetRobotAxes()[i]);
    EXPECT_EQ(externalJoints[0], programVariable.GetExternalAxes()[0]);
    EXPECT_EQ(externalJoints[1], programVariable.GetExternalAxes()[1]);
    EXPECT_EQ(externalJoints[2], programVariable.GetExternalAxes()[2]);
}

TEST(PositionVariableTest, GetSetExternalAxes)
{
    std::string name = "myVariableName";
    std::array<double, 6> robotJoints{0};
    std::array<double, 3> externalJoints{0};
    App::DataTypes::PositionVariable programVariable(name, robotJoints, externalJoints);

    std::array<double, 3> newExternalJoints{110, 220, 330};
    programVariable.SetExternalAxes(newExternalJoints);

    App::DataTypes::Matrix44 cartesianExpect;
    for (size_t i = 0; i < 16; i++) EXPECT_EQ(cartesianExpect[i], programVariable.GetCartesian()[i]);
    for (size_t i = 0; i < programVariable.GetRobotAxes().size(); i++) EXPECT_EQ(robotJoints[i], programVariable.GetRobotAxes()[i]);
    EXPECT_EQ(newExternalJoints[0], programVariable.GetExternalAxes()[0]);
    EXPECT_EQ(newExternalJoints[1], programVariable.GetExternalAxes()[1]);
    EXPECT_EQ(newExternalJoints[2], programVariable.GetExternalAxes()[2]);
}

TEST(PositionVariableTest, GetSetCartesian)
{
    std::string name = "myVariableName";
    std::array<double, 6> robotJoints{0};
    std::array<double, 3> externalJoints{0};
    App::DataTypes::PositionVariable programVariable(name, robotJoints, externalJoints);

    App::DataTypes::Matrix44 cartesianExpect;
    cartesianExpect.Translate(1, 2, 3);
    cartesianExpect.SetOrientation(10, 20, 30);
    programVariable.SetCartesian(cartesianExpect);

    for (size_t i = 0; i < 16; i++) EXPECT_EQ(cartesianExpect[i], programVariable.GetCartesian()[i]);
    for (size_t i = 0; i < programVariable.GetRobotAxes().size(); i++) EXPECT_EQ(robotJoints[i], programVariable.GetRobotAxes()[i]);
    EXPECT_EQ(externalJoints[0], programVariable.GetExternalAxes()[0]);
    EXPECT_EQ(externalJoints[1], programVariable.GetExternalAxes()[1]);
    EXPECT_EQ(externalJoints[2], programVariable.GetExternalAxes()[2]);
}
