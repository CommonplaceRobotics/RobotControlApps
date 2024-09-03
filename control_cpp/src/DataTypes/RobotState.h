/**
 * @brief The RobotState contains the most relevant, quickly changing state info of the robot, e.g. its position and joint angles, IO, etc.
 * @author MAB
 */

#pragma once

#include "Matrix44.h"
#include <robotcontrolapp.grpc.pb.h>

namespace App
{
namespace DataTypes
{

/**
 * @brief This class contains most relevant info about the robot's state, e.g. position, IO and errors
 */
class RobotState
{
public:
    /**
     * @brief Position and orientation of the TCP in cartesian space (position in mm)
     */
    Matrix44 tcp;
    
    // Mobile platform position X
    double platformX = 0;
    // Mobile platform position Y
    double platformY = 0;
    // Mobile platform heading in rad
    float platformHeading = 0;

    // Describes the state of the axis and IO hardware
    enum class HardwareState
    {
        OKAY = 0,
        ERROR_OVERTEMP = 1,
        ERROR_ESTOP_LOW_VOLTAGE = 2,
        ERROR_MOTOR_NOT_ENABLED = 4,
        ERROR_COMMUNICATION = 8,
        ERROR_POSITION_LAG = 16,
        ERROR_ENCODER = 32,
        ERROR_OVERCURRENT = 64,
        ERROR_DRIVER = 128,
        ERROR_BUS_DEAD = 256,
        ERROR_MODULE_DEAD = 512,
        ERROR_NOTREADY = 4096
    };

    // Describes the referencing state of an axis
    enum class ReferencingState
    {
        NOT_REFERENCED,
        IS_REFERENCED,
        IS_REFERENCING
    };

    struct Joint
    {
        /**
         * @brief Joint ID / index
         */
        int id = 0;

        /**
         * @brief Joint name
         */
        std::string name;

        /**
         * @brief Actual position in degrees, mm or user defined units
         */
        double actualPosition = 0;
        /**
         * @brief Target position in degrees, mm or user defined units
         */
        double targetPosition = 0;

        /**
         * @brief 
         */
        HardwareState hardwareState = HardwareState::OKAY;

        /**
         * @brief Referencing state
         */
        ReferencingState referencingState = ReferencingState::NOT_REFERENCED;

        /**
         * @brief Temperature of the electronics in °C
         */
        float temperatureBoard = 0;
        /**
         * @brief Temperature of the motor in °C (available for some robots only)
         */
        float temperatureMotor = 0;
        /**
         * @brief Current draw of this joint in mA
         */
        float current = 0;

        /**
         * @brief Target velocity in degrees/s, mm/s or user defined units per second - only usable with external axes in velocity mode
         */
        float targetVelocity = 0;

        /**
         * @brief Default constructor
         */
        Joint() = default;
        /**
         * @brief Constructor from GRPC Joint
         * @param joint 
         */
        Joint(const robotcontrolapp::Joint& joint);
    };
    /**
     * @brief Joint angles/positions in degrees, mm or user defined units. Indices 0-5 are robot joints, 6-8 are external joints.
     */
    std::array<Joint, 9> joints;

    /**
     * @brief 64 digital inputs
     */
    std::vector<bool> digitalInputs;
    /**
     * @brief 64 digital outputs
     */
    std::vector<bool> digitalOutputs;
    /**
     * @brief 100 global signals
     */
    std::vector<bool> globalSignals;

    /**
     * @brief A string describing the combined state of all modules
     */
    std::string hardwareState;
    /**
     * @brief Kinematic state / error
     */
    robotcontrolapp::KinematicState kinematicState = robotcontrolapp::KinematicState::KINEMATIC_NORMAL;

    /**
     * @brief The velocity override in percent 0.0..1.0
     */
    float velocityOverride = 0;
    /**
     * @brief The actual cartesian velocity in mm/s
     */
    float cartesianVelocity = 0;

    /**
     * @brief Temperature of the robot control computer's CPU in °C
     */
    float temperatureCPU = 0;
    /**
     * @brief Voltage of the motor power supply in mV
     */
    float supplyVoltage = 0;
    /**
     * @brief Combined current of all motors and DIO in mA (available for some robots only)
     */
    float currentAll = 0;

    /**
     * @brief Combined referencing state of all axes
     */
    ReferencingState referencingState = ReferencingState::NOT_REFERENCED;

    /**
     * @brief Default constructor
     */
    RobotState();
    /**
     * @brief Constructor from GRPC Joint
     * @param joint
     */
    RobotState(const robotcontrolapp::RobotState& state);
};

} // namespace DataTypes
} // namespace App