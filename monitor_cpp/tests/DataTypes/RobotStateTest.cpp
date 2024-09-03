#include <gtest/gtest.h>
#include <robotcontrolapp.grpc.pb.h>

#include "../../src/DataTypes/RobotState.h"

TEST(RobotStateJointTest, ConstructorDefault)
{
    App::DataTypes::RobotState::Joint joint;

    EXPECT_EQ(0, joint.id);
    EXPECT_TRUE(joint.name.empty());
    EXPECT_DOUBLE_EQ(0, joint.actualPosition);
    EXPECT_DOUBLE_EQ(0, joint.targetPosition);
    EXPECT_EQ(App::DataTypes::RobotState::HardwareState::OKAY, joint.hardwareState);
    EXPECT_EQ(App::DataTypes::RobotState::ReferencingState::NOT_REFERENCED, joint.referencingState);
    EXPECT_FLOAT_EQ(0, joint.temperatureBoard);
    EXPECT_FLOAT_EQ(0, joint.temperatureMotor);
    EXPECT_FLOAT_EQ(0, joint.current);
    EXPECT_FLOAT_EQ(0, joint.targetVelocity);
}

TEST(RobotStateJointTest, ConstructorGRPC)
{
    {
        robotcontrolapp::Joint jointGrpc;
        jointGrpc.set_id(4);
        jointGrpc.set_name("A4");
        jointGrpc.mutable_position()->set_position(123.4);
        jointGrpc.mutable_position()->set_target_position(234.5);
        jointGrpc.set_state(robotcontrolapp::HardwareState::ERROR_ESTOP_LOW_VOLTAGE);
        jointGrpc.set_referencing_state(robotcontrolapp::ReferencingState::IS_REFERENCING);
        jointGrpc.set_temperature_board(45.6f);
        jointGrpc.set_temperature_motor(56.7f);
        jointGrpc.set_current(123.4f);
        jointGrpc.set_target_velocity(78.9f);

        App::DataTypes::RobotState::Joint joint(jointGrpc);

        EXPECT_EQ(4, joint.id);
        EXPECT_STREQ("A4", joint.name.c_str());
        EXPECT_DOUBLE_EQ(123.4, joint.actualPosition);
        EXPECT_DOUBLE_EQ(234.5, joint.targetPosition);
        EXPECT_EQ(App::DataTypes::RobotState::HardwareState::ERROR_ESTOP_LOW_VOLTAGE, joint.hardwareState);
        EXPECT_EQ(App::DataTypes::RobotState::ReferencingState::IS_REFERENCING, joint.referencingState);
        EXPECT_FLOAT_EQ(45.6f, joint.temperatureBoard);
        EXPECT_FLOAT_EQ(56.7f, joint.temperatureMotor);
        EXPECT_FLOAT_EQ(123.4f, joint.current);
        EXPECT_FLOAT_EQ(78.9f, joint.targetVelocity);
    }

    {
        robotcontrolapp::Joint jointGrpc;
        robotcontrolapp::HardwareState state =
            (robotcontrolapp::HardwareState)(robotcontrolapp::HardwareState::ERROR_MOTOR_NOT_ENABLED | robotcontrolapp::HardwareState::ERROR_DRIVER);
        jointGrpc.set_state(state);
        jointGrpc.set_referencing_state(robotcontrolapp::ReferencingState::NOT_REFERENCED);

        App::DataTypes::RobotState::Joint joint(jointGrpc);

        App::DataTypes::RobotState::HardwareState expectState = (App::DataTypes::RobotState::HardwareState)(
            (int)App::DataTypes::RobotState::HardwareState::ERROR_MOTOR_NOT_ENABLED | (int)App::DataTypes::RobotState::HardwareState::ERROR_DRIVER);
        EXPECT_EQ(expectState, joint.hardwareState);
        EXPECT_EQ(App::DataTypes::RobotState::ReferencingState::NOT_REFERENCED, joint.referencingState);
    }

    {
        robotcontrolapp::Joint jointGrpc;
        jointGrpc.set_state(robotcontrolapp::HardwareState::OKAY);
        jointGrpc.set_referencing_state(robotcontrolapp::ReferencingState::IS_REFERENCED);

        App::DataTypes::RobotState::Joint joint(jointGrpc);

        EXPECT_EQ(App::DataTypes::RobotState::HardwareState::OKAY, joint.hardwareState);
        EXPECT_EQ(App::DataTypes::RobotState::ReferencingState::IS_REFERENCED, joint.referencingState);
    }
}

TEST(RobotStateTest, ConstructorDefault)
{
    App::DataTypes::RobotState robotState;

    EXPECT_DOUBLE_EQ(0, robotState.tcp.GetX());
    EXPECT_DOUBLE_EQ(0, robotState.tcp.GetY());
    EXPECT_DOUBLE_EQ(0, robotState.tcp.GetZ());
    EXPECT_DOUBLE_EQ(0, robotState.tcp.GetA());
    EXPECT_DOUBLE_EQ(0, robotState.tcp.GetB());
    EXPECT_DOUBLE_EQ(0, robotState.tcp.GetC());

    EXPECT_DOUBLE_EQ(0, robotState.platformX);
    EXPECT_DOUBLE_EQ(0, robotState.platformY);
    EXPECT_FLOAT_EQ(0, robotState.platformHeading);

    ASSERT_EQ(9, robotState.joints.size());
    EXPECT_EQ(0, robotState.joints[0].id);
    EXPECT_EQ(0, robotState.joints[1].id);
    EXPECT_EQ(0, robotState.joints[2].id);
    EXPECT_EQ(0, robotState.joints[3].id);
    EXPECT_EQ(0, robotState.joints[4].id);
    EXPECT_EQ(0, robotState.joints[5].id);
    EXPECT_EQ(0, robotState.joints[6].id);
    EXPECT_EQ(0, robotState.joints[7].id);
    EXPECT_EQ(0, robotState.joints[8].id);

    ASSERT_EQ(64, robotState.digitalInputs.size());
    ASSERT_EQ(64, robotState.digitalOutputs.size());
    for (size_t i = 0; i < robotState.digitalInputs.size(); i++)
    {
        EXPECT_FALSE(robotState.digitalInputs[i]);
        EXPECT_FALSE(robotState.digitalOutputs[i]);
    }
    ASSERT_EQ(100, robotState.globalSignals.size());
    for (size_t i = 0; i < robotState.globalSignals.size(); i++)
    {
        EXPECT_FALSE(robotState.globalSignals[i]);
    }

    EXPECT_TRUE(robotState.hardwareState.empty());
    EXPECT_EQ(robotcontrolapp::KinematicState::KINEMATIC_NORMAL, robotState.kinematicState);
    EXPECT_FLOAT_EQ(0, robotState.velocityOverride);
    EXPECT_FLOAT_EQ(0, robotState.cartesianVelocity);
    EXPECT_FLOAT_EQ(0, robotState.temperatureCPU);
    EXPECT_FLOAT_EQ(0, robotState.supplyVoltage);
    EXPECT_FLOAT_EQ(0, robotState.currentAll);
    EXPECT_EQ(App::DataTypes::RobotState::ReferencingState::NOT_REFERENCED, robotState.referencingState);
}

TEST(RobotStateTest, ConstructorGRPC)
{
    {
        robotcontrolapp::RobotState robotStateGrpc;

        App::DataTypes::Matrix44 tcp;
        tcp.SetOrientation(10, 20, 30);
        tcp.Translate(100, 200, 300);
        *robotStateGrpc.mutable_tcp() = tcp.ToGrpc();
        robotStateGrpc.mutable_platform_pose()->mutable_position()->set_x(1.2);
        robotStateGrpc.mutable_platform_pose()->mutable_position()->set_y(3.4);
        robotStateGrpc.mutable_platform_pose()->mutable_position()->set_z(5.6);
        robotStateGrpc.mutable_platform_pose()->set_heading(78.9f);

        for (unsigned i = 0; i < 9; i++) robotStateGrpc.add_joints()->set_id(i + 1);

        for (int i = 0; i < 64; i++)
        {
            robotcontrolapp::DIn* din = robotStateGrpc.add_dins();
            din->set_id(i);
            din->set_state(i % 2 == 0 ? robotcontrolapp::DIOState::HIGH : robotcontrolapp::DIOState::LOW);
            robotcontrolapp::DOut* dout = robotStateGrpc.add_douts();
            dout->set_id(i);
            dout->set_state(i % 2 != 0 ? robotcontrolapp::DIOState::HIGH : robotcontrolapp::DIOState::LOW);
        }

        for (int i = 0; i < 100; i++)
        {
            robotcontrolapp::GSig* gsig = robotStateGrpc.add_gsigs();
            gsig->set_id(i);
            gsig->set_state(i % 2 == 0 ? robotcontrolapp::DIOState::HIGH : robotcontrolapp::DIOState::LOW);
        }

        robotStateGrpc.set_hardware_state_string("MNE_ENC");
        robotStateGrpc.set_kinematic_state(robotcontrolapp::KinematicState::KINEMATIC_ERROR_BRAKE_ACTIVE);
        robotStateGrpc.set_velocity_override(0.8f);
        robotStateGrpc.set_cartesian_velocity(45.6f);
        robotStateGrpc.set_temperature_cpu(34.5f);
        robotStateGrpc.set_supply_voltage(24.1f);
        robotStateGrpc.set_current_all(1234.5f);
        robotStateGrpc.set_referencing_state(robotcontrolapp::ReferencingState::IS_REFERENCING);

        // Test
        App::DataTypes::RobotState robotState(robotStateGrpc);

        EXPECT_DOUBLE_EQ(tcp.GetX(), robotState.tcp.GetX());
        EXPECT_DOUBLE_EQ(tcp.GetY(), robotState.tcp.GetY());
        EXPECT_DOUBLE_EQ(tcp.GetZ(), robotState.tcp.GetZ());
        EXPECT_DOUBLE_EQ(tcp.GetA(), robotState.tcp.GetA());
        EXPECT_DOUBLE_EQ(tcp.GetB(), robotState.tcp.GetB());
        EXPECT_DOUBLE_EQ(tcp.GetC(), robotState.tcp.GetC());

        EXPECT_DOUBLE_EQ(1.2, robotState.platformX);
        EXPECT_DOUBLE_EQ(3.4, robotState.platformY);
        EXPECT_FLOAT_EQ(78.9f, robotState.platformHeading);

        ASSERT_EQ(9, robotState.joints.size());
        EXPECT_EQ(1, robotState.joints[0].id);
        EXPECT_EQ(2, robotState.joints[1].id);
        EXPECT_EQ(3, robotState.joints[2].id);
        EXPECT_EQ(4, robotState.joints[3].id);
        EXPECT_EQ(5, robotState.joints[4].id);
        EXPECT_EQ(6, robotState.joints[5].id);
        EXPECT_EQ(7, robotState.joints[6].id);
        EXPECT_EQ(8, robotState.joints[7].id);
        EXPECT_EQ(9, robotState.joints[8].id);

        ASSERT_EQ(64, robotState.digitalInputs.size());
        ASSERT_EQ(64, robotState.digitalOutputs.size());
        for (size_t i = 0; i < robotState.digitalInputs.size(); i++)
        {
            EXPECT_EQ(i % 2 == 0, robotState.digitalInputs[i]);
            EXPECT_EQ(i % 2 != 0, robotState.digitalOutputs[i]);
        }
        ASSERT_EQ(100, robotState.globalSignals.size());
        for (size_t i = 0; i < robotState.globalSignals.size(); i++)
        {
            EXPECT_EQ(i % 2 == 0, robotState.globalSignals[i]);
        }

        EXPECT_STREQ("MNE_ENC", robotState.hardwareState.c_str());
        EXPECT_EQ(robotcontrolapp::KinematicState::KINEMATIC_ERROR_BRAKE_ACTIVE, robotState.kinematicState);
        EXPECT_FLOAT_EQ(0.8f, robotState.velocityOverride);
        EXPECT_FLOAT_EQ(45.6f, robotState.cartesianVelocity);
        EXPECT_FLOAT_EQ(34.5f, robotState.temperatureCPU);
        EXPECT_FLOAT_EQ(24.1f, robotState.supplyVoltage);
        EXPECT_FLOAT_EQ(1234.5f, robotState.currentAll);
        EXPECT_EQ(App::DataTypes::RobotState::ReferencingState::IS_REFERENCING, robotState.referencingState);
    }

    // less DIO than expected
    {
        robotcontrolapp::RobotState robotStateGrpc;

        App::DataTypes::Matrix44 tcp;
        tcp.SetOrientation(10, 20, 30);
        tcp.Translate(100, 200, 300);
        *robotStateGrpc.mutable_tcp() = tcp.ToGrpc();

        for (int i = 0; i < 10; i++)
        {
            robotcontrolapp::DIn* din = robotStateGrpc.add_dins();
            din->set_id(i);
            din->set_state(i % 2 == 0 ? robotcontrolapp::DIOState::HIGH : robotcontrolapp::DIOState::LOW);
            robotcontrolapp::DOut* dout = robotStateGrpc.add_douts();
            dout->set_id(i);
            dout->set_state(i % 2 != 0 ? robotcontrolapp::DIOState::HIGH : robotcontrolapp::DIOState::LOW);
        }

        for (int i = 0; i < 20; i++)
        {
            robotcontrolapp::GSig* gsig = robotStateGrpc.add_gsigs();
            gsig->set_id(i);
            gsig->set_state(i % 2 == 0 ? robotcontrolapp::DIOState::HIGH : robotcontrolapp::DIOState::LOW);
        }

        robotStateGrpc.set_referencing_state(robotcontrolapp::ReferencingState::NOT_REFERENCED);

        // Test
        App::DataTypes::RobotState robotState(robotStateGrpc);

        ASSERT_EQ(64, robotState.digitalInputs.size());
        ASSERT_EQ(64, robotState.digitalOutputs.size());
        for (size_t i = 0; i < robotState.digitalInputs.size(); i++)
        {
            if (i < 10)
            {
                EXPECT_EQ(i % 2 == 0, robotState.digitalInputs[i]);
                EXPECT_EQ(i % 2 != 0, robotState.digitalOutputs[i]);
            }
            else
            {
                EXPECT_FALSE(robotState.digitalInputs[i]);
                EXPECT_FALSE(robotState.digitalOutputs[i]);
            }
        }
        ASSERT_EQ(100, robotState.globalSignals.size());
        for (size_t i = 0; i < robotState.globalSignals.size(); i++)
        {
            if (i < 20)
            {
                EXPECT_EQ(i % 2 == 0, robotState.globalSignals[i]);
            }
            else
            {
                EXPECT_FALSE(robotState.globalSignals[i]);
            }
        }

        EXPECT_EQ(App::DataTypes::RobotState::ReferencingState::NOT_REFERENCED, robotState.referencingState);
    }

    // more DIO than expected
    {
        robotcontrolapp::RobotState robotStateGrpc;

        App::DataTypes::Matrix44 tcp;
        tcp.SetOrientation(10, 20, 30);
        tcp.Translate(100, 200, 300);

        *robotStateGrpc.mutable_tcp() = tcp.ToGrpc();
        for (int i = 0; i < 100; i++)
        {
            robotcontrolapp::DIn* din = robotStateGrpc.add_dins();
            din->set_id(i);
            din->set_state(i % 2 == 0 ? robotcontrolapp::DIOState::HIGH : robotcontrolapp::DIOState::LOW);
            robotcontrolapp::DOut* dout = robotStateGrpc.add_douts();
            dout->set_id(i);
            dout->set_state(i % 2 != 0 ? robotcontrolapp::DIOState::HIGH : robotcontrolapp::DIOState::LOW);
        }

        for (int i = 0; i < 200; i++)
        {
            robotcontrolapp::GSig* gsig = robotStateGrpc.add_gsigs();
            gsig->set_id(i);
            gsig->set_state(i % 2 == 0 ? robotcontrolapp::DIOState::HIGH : robotcontrolapp::DIOState::LOW);
        }

        robotStateGrpc.set_referencing_state(robotcontrolapp::ReferencingState::IS_REFERENCED);

        // Test
        App::DataTypes::RobotState robotState(robotStateGrpc);

        ASSERT_EQ(64, robotState.digitalInputs.size());
        ASSERT_EQ(64, robotState.digitalOutputs.size());
        for (size_t i = 0; i < robotState.digitalInputs.size(); i++)
        {
            EXPECT_EQ(i % 2 == 0, robotState.digitalInputs[i]);
            EXPECT_EQ(i % 2 != 0, robotState.digitalOutputs[i]);
        }
        ASSERT_EQ(100, robotState.globalSignals.size());
        for (size_t i = 0; i < robotState.globalSignals.size(); i++)
        {
            EXPECT_EQ(i % 2 == 0, robotState.globalSignals[i]);
        }

        EXPECT_EQ(App::DataTypes::RobotState::ReferencingState::IS_REFERENCED, robotState.referencingState);
    }
}