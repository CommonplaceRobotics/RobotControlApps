#include <gtest/gtest.h>
#include <robotcontrolapp.grpc.pb.h>

#include "../../src/DataTypes/Statistics.h"

TEST(App_StatisticsTest, ConstructorDefault)
{
    App::DataTypes::Statistics stat;
    ASSERT_EQ(3, stat.externalAxisDirectionChanges.size());
    EXPECT_EQ(0, stat.externalAxisDirectionChanges[0]);
    EXPECT_EQ(0, stat.externalAxisDirectionChanges[1]);
    EXPECT_EQ(0, stat.externalAxisDirectionChanges[2]);

    ASSERT_EQ(6, stat.robotAxisDirectionChanges.size());
    EXPECT_EQ(0, stat.robotAxisDirectionChanges[0]);
    EXPECT_EQ(0, stat.robotAxisDirectionChanges[1]);
    EXPECT_EQ(0, stat.robotAxisDirectionChanges[2]);
    EXPECT_EQ(0, stat.robotAxisDirectionChanges[3]);
    EXPECT_EQ(0, stat.robotAxisDirectionChanges[4]);
    EXPECT_EQ(0, stat.robotAxisDirectionChanges[5]);

    EXPECT_EQ(0, stat.partsBad);
    EXPECT_EQ(0, stat.partsGood);

    EXPECT_EQ(0, stat.programDurationLast);
    EXPECT_EQ(0, stat.programStartsLast);
    EXPECT_EQ(0, stat.programStartsTotal);
    EXPECT_EQ(0, stat.uptimeComplete);
    EXPECT_EQ(0, stat.uptimeEnabled);
    EXPECT_EQ(0, stat.uptimeLast);
    EXPECT_EQ(0, stat.uptimeMotion);
}

TEST(App_StatisticsTest, ConstructorGRPC)
{
    robotcontrolapp::StatisticsResponse response;
    response.set_uptime_complete(10);
    response.set_uptime_last(20);
    response.set_uptime_enabled(30);
    response.set_uptime_motion(40);

    response.set_program_starts_total(50);
    response.set_program_starts_last(60);
    response.set_program_duration_last(70);

    response.set_parts_good(80);
    response.set_parts_bad(90);

    response.add_robot_axis_direction_changes(100);
    response.add_robot_axis_direction_changes(110);
    response.add_robot_axis_direction_changes(120);
    response.add_robot_axis_direction_changes(130);
    response.add_robot_axis_direction_changes(140);
    response.add_robot_axis_direction_changes(150);
    response.add_external_axis_direction_changes(160);
    response.add_external_axis_direction_changes(170);
    response.add_external_axis_direction_changes(180);

    App::DataTypes::Statistics stat(response);
    ASSERT_EQ(3, stat.externalAxisDirectionChanges.size());
    EXPECT_EQ(160, stat.externalAxisDirectionChanges[0]);
    EXPECT_EQ(170, stat.externalAxisDirectionChanges[1]);
    EXPECT_EQ(180, stat.externalAxisDirectionChanges[2]);

    ASSERT_EQ(6, stat.robotAxisDirectionChanges.size());
    EXPECT_EQ(100, stat.robotAxisDirectionChanges[0]);
    EXPECT_EQ(110, stat.robotAxisDirectionChanges[1]);
    EXPECT_EQ(120, stat.robotAxisDirectionChanges[2]);
    EXPECT_EQ(130, stat.robotAxisDirectionChanges[3]);
    EXPECT_EQ(140, stat.robotAxisDirectionChanges[4]);
    EXPECT_EQ(150, stat.robotAxisDirectionChanges[5]);

    EXPECT_EQ(90, stat.partsBad);
    EXPECT_EQ(80, stat.partsGood);

    EXPECT_EQ(70, stat.programDurationLast);
    EXPECT_EQ(60, stat.programStartsLast);
    EXPECT_EQ(50, stat.programStartsTotal);
    EXPECT_EQ(10, stat.uptimeComplete);
    EXPECT_EQ(30, stat.uptimeEnabled);
    EXPECT_EQ(20, stat.uptimeLast);
    EXPECT_EQ(40, stat.uptimeMotion);
}
