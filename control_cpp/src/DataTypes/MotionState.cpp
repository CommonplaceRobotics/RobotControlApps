#include "MotionState.h"

namespace App
{
namespace DataTypes
{

/**
 * @brief Constructor from GRPC InterpolatorState
 * @param state
 */
MotionState::InterpolatorState::InterpolatorState(const robotcontrolapp::MotionState_InterpolatorState& state) {
    switch (state.runstate())
    {
        default:
        case robotcontrolapp::RunState::NOT_RUNNING:
            runState = MotionState::RunState::NOT_RUNNING;
            break;
        case robotcontrolapp::RunState::PAUSED:
            runState = MotionState::RunState::PAUSED;
            break;
        case robotcontrolapp::RunState::RUNNING:
            runState = MotionState::RunState::RUNNING;
            break;
    }

    switch (state.replay_mode())
    {
        default:
        case robotcontrolapp::ReplayMode::SINGLE:
            replayMode = MotionState::ReplayMode::SINGLE;
            break;
        case robotcontrolapp::ReplayMode::REPEAT:
            replayMode = MotionState::ReplayMode::REPEAT;
            break;
        case robotcontrolapp::ReplayMode::STEP:
            replayMode = MotionState::ReplayMode::STEP;
            break;
    }

    mainProgram = state.main_program_name();
    currentProgram = state.current_program_name();
    currentProgramIndex = state.current_program_idx();
    currentCommandIndex = state.current_command_idx();
    programCount = state.program_count();
    commandCount = state.command_count();
}

/**
 * @brief Constructor from GRPC MotionState
 * @param state
 */
MotionState::MotionState(const robotcontrolapp::MotionState& state) :motionProgram(state.motion_ipo()), logicProgram(state.logic_ipo()), moveTo(state.move_to_ipo()) {
    positionInterface.isEnabled = state.position_interface().is_enabled();
    positionInterface.isInUse = state.position_interface().is_in_use();
    positionInterface.port = state.position_interface().port();
}

} // namespace DataTypes
} // namespace App