#include "RobotState.h"

namespace App
{
namespace DataTypes
{

/**
 * @brief Constructor
 */
RobotState::RobotState()
{
    digitalInputs.resize(64);
    digitalOutputs.resize(64);
    globalSignals.resize(100);
}

/**
 * @brief Constructor from GRPC RobotState
 * @param state 
 */
RobotState::RobotState(const robotcontrolapp::RobotState& state) 
{
    tcp = Matrix44(state.tcp());
    
    if (state.has_platform_pose())
    {
        platformX = state.platform_pose().position().x();
        platformY = state.platform_pose().position().y();
        platformHeading = state.platform_pose().heading();
    }

    for (int i = 0; i < state.joints_size(); i++)
    {
        joints[i] = Joint(state.joints(i));
    }

    digitalInputs.resize(64);
    digitalOutputs.resize(64);
    globalSignals.resize(100);
    for (size_t i = 0; (int)i < state.dins_size() && i < digitalInputs.size(); i++)
    {
        digitalInputs[i] = state.dins((int)i).state() == robotcontrolapp::DIOState::HIGH;
    }
    for (size_t i = 0; (int)i < state.douts_size() && i < digitalOutputs.size(); i++)
    {
        digitalOutputs[i] = state.douts((int)i).state() == robotcontrolapp::DIOState::HIGH;
    }
    for (size_t i = 0; (int)i < state.gsigs_size() && i < globalSignals.size(); i++)
    {
        globalSignals[i] = state.gsigs((int)i).state() == robotcontrolapp::DIOState::HIGH;
    }

    hardwareState = state.hardware_state_string();
    kinematicState = state.kinematic_state();
    velocityOverride = state.velocity_override();
    cartesianVelocity = state.cartesian_velocity();
    temperatureCPU = state.temperature_cpu();
    supplyVoltage = state.supply_voltage();
    currentAll = state.current_all();
    
    switch (state.referencing_state())
    {
        case robotcontrolapp::ReferencingState::IS_REFERENCED:
            referencingState = ReferencingState::IS_REFERENCED;
            break;
        case robotcontrolapp::ReferencingState::IS_REFERENCING:
            referencingState = ReferencingState::IS_REFERENCING;
            break;
        default:
        case robotcontrolapp::ReferencingState::NOT_REFERENCED:
            referencingState = ReferencingState::NOT_REFERENCED;
            break;
    }
}

/**
 * @brief Constructor from GRPC Joint
 * @param joint 
 */
RobotState::Joint::Joint(const robotcontrolapp::Joint& joint) {
    id = joint.id();
    name = joint.name();
    actualPosition = joint.position().position();
    targetPosition = joint.position().target_position();

    hardwareState = static_cast<DataTypes::RobotState::HardwareState>(joint.state());

    switch (joint.referencing_state())
    {
        case robotcontrolapp::ReferencingState::IS_REFERENCED:
            referencingState = ReferencingState::IS_REFERENCED;
            break;
        case robotcontrolapp::ReferencingState::IS_REFERENCING:
            referencingState = ReferencingState::IS_REFERENCING;
            break;
        default:
        case robotcontrolapp::ReferencingState::NOT_REFERENCED:
            referencingState = ReferencingState::NOT_REFERENCED;
            break;
    }

    temperatureBoard = joint.temperature_board();
    temperatureMotor = joint.temperature_motor();
    current = joint.current();
    targetVelocity = joint.target_velocity();
}

} // namespace DataTypes
} // namespace App