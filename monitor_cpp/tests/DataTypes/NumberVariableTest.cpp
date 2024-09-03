#include <gtest/gtest.h>

#include "../../src/DataTypes/ProgramVariable.h"

TEST(NumberVariableTest, Constructor)
{
    // name, default value
    {
        std::string name = "myVariableName";
        App::DataTypes::NumberVariable programVariable(name);
        EXPECT_STREQ(name.c_str(), programVariable.GetName().c_str());
        EXPECT_EQ(0, programVariable.GetValue());
    }

    // empty name, default value
    {
        std::string name = "";
        App::DataTypes::NumberVariable programVariable(name);
        EXPECT_STREQ(name.c_str(), programVariable.GetName().c_str());
        EXPECT_EQ(0, programVariable.GetValue());
    }

    // name, -1
    {
        std::string name = "myVariableName";
        App::DataTypes::NumberVariable programVariable(name, -1);
        EXPECT_STREQ(name.c_str(), programVariable.GetName().c_str());
        EXPECT_EQ(-1, programVariable.GetValue());
    }

    // name, 1234.5
    {
        std::string name = "myVariableName";
        App::DataTypes::NumberVariable programVariable(name, 1234.5);
        EXPECT_STREQ(name.c_str(), programVariable.GetName().c_str());
        EXPECT_EQ(1234.5, programVariable.GetValue());
    }
}

TEST(NumberVariableTest, GetName)
{
    std::string name = "myVariableName";
    App::DataTypes::NumberVariable programVariable(name);
    EXPECT_STREQ(name.c_str(), programVariable.GetName().c_str());
}

TEST(NumberVariableTest, SetName)
{
    std::string name = "myVariableName";
    std::string newName = "otherName";
    App::DataTypes::NumberVariable programVariable(name);
    programVariable.SetName(newName);
    EXPECT_STREQ(newName.c_str(), programVariable.GetName().c_str());
}

TEST(NumberVariableTest, GetSetValue)
{
    std::string name = "myVariableName";
    App::DataTypes::NumberVariable programVariable(name, 1234.5);

    {
        double expect = 4567.8;
        programVariable.SetValue(expect);
        EXPECT_EQ(expect, programVariable.GetValue());
    }

    {
        double expect = -45.6;
        programVariable.SetValue(expect);
        EXPECT_EQ(expect, programVariable.GetValue());
    }
}
