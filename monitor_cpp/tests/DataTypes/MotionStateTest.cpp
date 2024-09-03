#include <gtest/gtest.h>

#include "../../src/DataTypes/MotionState.h"

#include <robotcontrolapp.grpc.pb.h>

TEST(MotionStateTest, ConstructorDefault) {
    App::DataTypes::MotionState ms;

    // motion program
    EXPECT_EQ(App::DataTypes::MotionState::RunState::NOT_RUNNING, ms.motionProgram.runState);
    EXPECT_EQ(App::DataTypes::MotionState::ReplayMode::SINGLE, ms.motionProgram.replayMode);
    EXPECT_TRUE(ms.motionProgram.mainProgram.empty());
    EXPECT_TRUE(ms.motionProgram.currentProgram.empty());
    EXPECT_EQ(0, ms.motionProgram.currentProgramIndex);
    EXPECT_EQ(0, ms.motionProgram.programCount);
    EXPECT_EQ(0, ms.motionProgram.currentCommandIndex);
    EXPECT_EQ(0, ms.motionProgram.commandCount);

    // logic program
    EXPECT_EQ(App::DataTypes::MotionState::RunState::NOT_RUNNING, ms.logicProgram.runState);
    EXPECT_EQ(App::DataTypes::MotionState::ReplayMode::SINGLE, ms.logicProgram.replayMode);
    EXPECT_TRUE(ms.logicProgram.mainProgram.empty());
    EXPECT_TRUE(ms.logicProgram.currentProgram.empty());
    EXPECT_EQ(0, ms.logicProgram.currentProgramIndex);
    EXPECT_EQ(0, ms.logicProgram.programCount);
    EXPECT_EQ(0, ms.logicProgram.currentCommandIndex);
    EXPECT_EQ(0, ms.logicProgram.commandCount);

    // move-to ipo
    EXPECT_EQ(App::DataTypes::MotionState::RunState::NOT_RUNNING, ms.moveTo.runState);
    EXPECT_EQ(App::DataTypes::MotionState::ReplayMode::SINGLE, ms.moveTo.replayMode);
    EXPECT_TRUE(ms.moveTo.mainProgram.empty());
    EXPECT_TRUE(ms.moveTo.currentProgram.empty());
    EXPECT_EQ(0, ms.moveTo.currentProgramIndex);
    EXPECT_EQ(0, ms.moveTo.programCount);
    EXPECT_EQ(0, ms.moveTo.currentCommandIndex);
    EXPECT_EQ(0, ms.moveTo.commandCount);

    // position interface
    EXPECT_FALSE(ms.positionInterface.isEnabled);
    EXPECT_FALSE(ms.positionInterface.isInUse);
    EXPECT_EQ(0, ms.positionInterface.port);
}


TEST(MotionStateTest, ConstructorGRPC)
{
    {
        robotcontrolapp::MotionState grpcState;
        grpcState.set_current_source(robotcontrolapp::MotionState_MotionSource_JOG);

        // motion program
        grpcState.mutable_motion_ipo()->set_runstate(robotcontrolapp::RunState::RUNNING);
        grpcState.mutable_motion_ipo()->set_replay_mode(robotcontrolapp::ReplayMode::STEP);
        grpcState.mutable_motion_ipo()->set_main_program_name("MyMotionProg");
        grpcState.mutable_motion_ipo()->set_current_program_name("MyMotionSub");
        grpcState.mutable_motion_ipo()->set_current_program_idx(12);
        grpcState.mutable_motion_ipo()->set_program_count(34);
        grpcState.mutable_motion_ipo()->set_current_command_idx(56);
        grpcState.mutable_motion_ipo()->set_command_count(78);

        // logic program
        grpcState.mutable_logic_ipo()->set_runstate(robotcontrolapp::RunState::RUNNING);
        grpcState.mutable_logic_ipo()->set_replay_mode(robotcontrolapp::ReplayMode::REPEAT);
        grpcState.mutable_logic_ipo()->set_main_program_name("MyLogicProg");
        grpcState.mutable_logic_ipo()->set_current_program_name("MyLogicSub");
        grpcState.mutable_logic_ipo()->set_current_program_idx(112);
        grpcState.mutable_logic_ipo()->set_program_count(134);
        grpcState.mutable_logic_ipo()->set_current_command_idx(156);
        grpcState.mutable_logic_ipo()->set_command_count(178);

        // move-to ipo
        grpcState.mutable_move_to_ipo()->set_runstate(robotcontrolapp::RunState::PAUSED);
        grpcState.mutable_move_to_ipo()->set_replay_mode(robotcontrolapp::ReplayMode::STEP);
        grpcState.mutable_move_to_ipo()->set_main_program_name("MyMoveToProg");
        grpcState.mutable_move_to_ipo()->set_current_program_name("MyMoveToSub");
        grpcState.mutable_move_to_ipo()->set_current_program_idx(212);
        grpcState.mutable_move_to_ipo()->set_program_count(234);
        grpcState.mutable_move_to_ipo()->set_current_command_idx(256);
        grpcState.mutable_move_to_ipo()->set_command_count(278);

        // position interface
        grpcState.mutable_position_interface()->set_is_enabled(true);
        grpcState.mutable_position_interface()->set_is_in_use(true);
        grpcState.mutable_position_interface()->set_port(258);

        // Test
        App::DataTypes::MotionState ms(grpcState);

        // motion program
        EXPECT_EQ(App::DataTypes::MotionState::RunState::RUNNING, ms.motionProgram.runState);
        EXPECT_EQ(App::DataTypes::MotionState::ReplayMode::STEP, ms.motionProgram.replayMode);
        EXPECT_STREQ("MyMotionProg", ms.motionProgram.mainProgram.c_str());
        EXPECT_STREQ("MyMotionSub", ms.motionProgram.currentProgram.c_str());
        EXPECT_EQ(12, ms.motionProgram.currentProgramIndex);
        EXPECT_EQ(34, ms.motionProgram.programCount);
        EXPECT_EQ(56, ms.motionProgram.currentCommandIndex);
        EXPECT_EQ(78, ms.motionProgram.commandCount);

        // logic program
        EXPECT_EQ(App::DataTypes::MotionState::RunState::RUNNING, ms.logicProgram.runState);
        EXPECT_EQ(App::DataTypes::MotionState::ReplayMode::REPEAT, ms.logicProgram.replayMode);
        EXPECT_STREQ("MyLogicProg", ms.logicProgram.mainProgram.c_str());
        EXPECT_STREQ("MyLogicSub", ms.logicProgram.currentProgram.c_str());
        EXPECT_EQ(112, ms.logicProgram.currentProgramIndex);
        EXPECT_EQ(134, ms.logicProgram.programCount);
        EXPECT_EQ(156, ms.logicProgram.currentCommandIndex);
        EXPECT_EQ(178, ms.logicProgram.commandCount);

        // move-to ipo
        EXPECT_EQ(App::DataTypes::MotionState::RunState::PAUSED, ms.moveTo.runState);
        EXPECT_EQ(App::DataTypes::MotionState::ReplayMode::STEP, ms.moveTo.replayMode);
        EXPECT_STREQ("MyMoveToProg", ms.moveTo.mainProgram.c_str());
        EXPECT_STREQ("MyMoveToSub", ms.moveTo.currentProgram.c_str());
        EXPECT_EQ(212, ms.moveTo.currentProgramIndex);
        EXPECT_EQ(234, ms.moveTo.programCount);
        EXPECT_EQ(256, ms.moveTo.currentCommandIndex);
        EXPECT_EQ(278, ms.moveTo.commandCount);

        // position interface
        EXPECT_TRUE(ms.positionInterface.isEnabled);
        EXPECT_TRUE(ms.positionInterface.isInUse);
        EXPECT_EQ(258, ms.positionInterface.port);
    }

    {
        robotcontrolapp::MotionState grpcState;
        grpcState.set_current_source(robotcontrolapp::MotionState_MotionSource_PLATFORM);

        // motion program
        grpcState.mutable_motion_ipo()->set_runstate(robotcontrolapp::RunState::PAUSED);
        grpcState.mutable_motion_ipo()->set_replay_mode(robotcontrolapp::ReplayMode::SINGLE);

        // logic program
        grpcState.mutable_logic_ipo()->set_runstate(robotcontrolapp::RunState::NOT_RUNNING);
        grpcState.mutable_logic_ipo()->set_replay_mode(robotcontrolapp::ReplayMode::STEP);

        // move-to ipo
        grpcState.mutable_move_to_ipo()->set_runstate(robotcontrolapp::RunState::RUNNING);
        grpcState.mutable_move_to_ipo()->set_replay_mode(robotcontrolapp::ReplayMode::STEP);

        // position interface
        grpcState.mutable_position_interface()->set_is_enabled(true);
        grpcState.mutable_position_interface()->set_is_in_use(false);

        // Test
        App::DataTypes::MotionState ms(grpcState);

        // motion program
        EXPECT_EQ(App::DataTypes::MotionState::RunState::PAUSED, ms.motionProgram.runState);
        EXPECT_EQ(App::DataTypes::MotionState::ReplayMode::SINGLE, ms.motionProgram.replayMode);

        // logic program
        EXPECT_EQ(App::DataTypes::MotionState::RunState::NOT_RUNNING, ms.logicProgram.runState);
        EXPECT_EQ(App::DataTypes::MotionState::ReplayMode::STEP, ms.logicProgram.replayMode);

        // move-to ipo
        EXPECT_EQ(App::DataTypes::MotionState::RunState::RUNNING, ms.moveTo.runState);
        EXPECT_EQ(App::DataTypes::MotionState::ReplayMode::STEP, ms.moveTo.replayMode);

        // position interface
        EXPECT_TRUE(ms.positionInterface.isEnabled);
        EXPECT_FALSE(ms.positionInterface.isInUse);
    }

    {
        robotcontrolapp::MotionState grpcState;
        grpcState.set_current_source(robotcontrolapp::MotionState_MotionSource_POSITION_INTERFACE);

        // position interface
        grpcState.mutable_position_interface()->set_is_enabled(false);
        grpcState.mutable_position_interface()->set_is_in_use(true);

        // Test
        App::DataTypes::MotionState ms(grpcState);

        // position interface
        EXPECT_FALSE(ms.positionInterface.isEnabled);
        EXPECT_TRUE(ms.positionInterface.isInUse);
    }
}