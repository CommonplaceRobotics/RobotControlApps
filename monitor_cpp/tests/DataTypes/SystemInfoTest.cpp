#include <gtest/gtest.h>
#include <robotcontrolapp.grpc.pb.h>

#include "../../src/DataTypes/SystemInfo.h"

TEST(SystemInfoTest, ConstructorDefault)
{
    App::DataTypes::SystemInfo sysInfo;

    EXPECT_EQ(0, sysInfo.versionMajor);
    EXPECT_EQ(0, sysInfo.versionMinor);
    EXPECT_EQ(0, sysInfo.versionPatch);
    EXPECT_TRUE(sysInfo.version.empty());

    EXPECT_TRUE(sysInfo.projectFile.empty());
    EXPECT_TRUE(sysInfo.projectTitle.empty());
    EXPECT_TRUE(sysInfo.projectAuthor.empty());
    EXPECT_TRUE(sysInfo.robotType.empty());
    
    EXPECT_EQ(robotcontrolapp::SystemInfo_Voltage_Voltage24V, sysInfo.voltage);
    EXPECT_EQ(robotcontrolapp::SystemInfo_SystemType_Other, sysInfo.systemType);
    EXPECT_FALSE(sysInfo.isSimulation);

    EXPECT_TRUE(sysInfo.deviceID.empty());

    EXPECT_FLOAT_EQ(0, sysInfo.cycleTimeTarget);
    EXPECT_FLOAT_EQ(0, sysInfo.cycleTimeAverage);
    EXPECT_FLOAT_EQ(0, sysInfo.cycleTimeMax);
    EXPECT_FLOAT_EQ(0, sysInfo.cycleTimeMin);
    EXPECT_FLOAT_EQ(0, sysInfo.workload);

    EXPECT_EQ(0, sysInfo.robotAxisCount);
    EXPECT_EQ(0, sysInfo.externalAxisCount);
    EXPECT_EQ(0, sysInfo.toolAxisCount);
    EXPECT_EQ(0, sysInfo.platformAxisCount);
    EXPECT_EQ(0, sysInfo.digitalIOModuleCount);
}

TEST(SystemInfoTest, ConstructorGRPC)
{
    robotcontrolapp::SystemInfo sysInfoGrpc;

    sysInfoGrpc.set_version_major(12);
    sysInfoGrpc.set_version_minor(34);
    sysInfoGrpc.set_version_patch(56);
    sysInfoGrpc.set_version("V123-045-6 RC1");
    
    sysInfoGrpc.set_project_file("Type/MyProjectFile.prj");
    sysInfoGrpc.set_project_title("My Rebel");
    sysInfoGrpc.set_project_author("MAB");
    sysInfoGrpc.set_robot_type("Rebel");

    sysInfoGrpc.set_voltage(robotcontrolapp::SystemInfo_Voltage_Voltage48V);
    sysInfoGrpc.set_system_type(robotcontrolapp::SystemInfo_SystemType_Raspberry);
    sysInfoGrpc.set_is_simulation(true);

    sysInfoGrpc.set_device_id("ABCDEF012345657");

    sysInfoGrpc.set_cycle_time_target(10);
    sysInfoGrpc.set_cycle_time_avg(10.1);
    sysInfoGrpc.set_cycle_time_max(11);
    sysInfoGrpc.set_cycle_time_min(9);
    sysInfoGrpc.set_workload(0.5);

    sysInfoGrpc.set_robot_axis_count(6);
    sysInfoGrpc.set_external_axis_count(3);
    sysInfoGrpc.set_tool_axis_count(1);
    sysInfoGrpc.set_platform_axis_count(4);
    sysInfoGrpc.set_digital_io_module_count(3);


    App::DataTypes::SystemInfo sysInfo(sysInfoGrpc);

    EXPECT_EQ(12, sysInfo.versionMajor);
    EXPECT_EQ(34, sysInfo.versionMinor);
    EXPECT_EQ(56, sysInfo.versionPatch);
    EXPECT_STREQ("V123-045-6 RC1", sysInfo.version.c_str());

    EXPECT_STREQ("Type/MyProjectFile.prj", sysInfo.projectFile.c_str());
    EXPECT_STREQ("My Rebel", sysInfo.projectTitle.c_str());
    EXPECT_STREQ("MAB", sysInfo.projectAuthor.c_str());
    EXPECT_STREQ("Rebel", sysInfo.robotType.c_str());

    EXPECT_EQ(robotcontrolapp::SystemInfo_Voltage_Voltage48V, sysInfo.voltage);
    EXPECT_EQ(robotcontrolapp::SystemInfo_SystemType_Raspberry, sysInfo.systemType);
    EXPECT_TRUE(sysInfo.isSimulation);

    EXPECT_STREQ("ABCDEF012345657", sysInfo.deviceID.c_str());

    EXPECT_FLOAT_EQ(10, sysInfo.cycleTimeTarget);
    EXPECT_FLOAT_EQ(10.1, sysInfo.cycleTimeAverage);
    EXPECT_FLOAT_EQ(11, sysInfo.cycleTimeMax);
    EXPECT_FLOAT_EQ(9, sysInfo.cycleTimeMin);
    EXPECT_FLOAT_EQ(0.5, sysInfo.workload);

    EXPECT_EQ(6, sysInfo.robotAxisCount);
    EXPECT_EQ(3, sysInfo.externalAxisCount);
    EXPECT_EQ(1, sysInfo.toolAxisCount);
    EXPECT_EQ(4, sysInfo.platformAxisCount);
    EXPECT_EQ(3, sysInfo.digitalIOModuleCount);
}