/**
 * @brief The MotionState contains the state of the motion interpolators (i.e. programs, move-to commands and the position interface)
 * @author MAB
 */

#pragma once

#include <robotcontrolapp.grpc.pb.h>

#include <string>

namespace App
{
namespace DataTypes
{

/**
 * @brief This class contains the state of the motion interpolators (which run the robot programs)
 */
class MotionState
{
public:
    /// Is a program running or paused?
    enum class RunState
    {
        NOT_RUNNING,
        PAUSED,
        RUNNING
    };
    /// Repeat the program?
    enum class ReplayMode
    {
        SINGLE,
        REPEAT,
        STEP
    };

    /**
     * @brief This describes the state of one motion interpolator
     */
    struct InterpolatorState
    {
        /**
         * @brief Is the program running or paused?
         */
        RunState runState = RunState::NOT_RUNNING;
        /**
         * @brief Should the program repeat or be run step by step?
         */
        ReplayMode replayMode = ReplayMode::SINGLE;
        /**
         * @brief Name of the main program
         */
        std::string mainProgram;
        /**
         * @brief Name of the (sub-)program that is currently being executed
         */
        std::string currentProgram;

        /**
         * @brief Index of the (sub-)program that is currently being executed: 0 is the main program, higher numbers are sub-programs
         */
        int currentProgramIndex = 0;
        /**
         * @brief Number of loaded programs: 0 - no programs, 1 - only the main program, higher values - the main and sub programs are loaded
         */
        int programCount = 0;
        /**
         * @brief Index of the current command that is being executed. 0 is the first command in the current (sub-)program, -1 when not running.
         */
        int currentCommandIndex = 0;
        /**
         * @brief Number of commands in the current (sub-)program
         */
        int commandCount = 0;

        /**
         * @brief Default constructor
         */
        InterpolatorState() = default;
        /**
         * @brief Constructor from GRPC InterpolatorState
         * @param state
         */
        InterpolatorState(const robotcontrolapp::MotionState_InterpolatorState& state);
    };

    /**
     * @brief This describes the state of the fast position interface
     */
    struct PositionInterfaceState
    {
        // Position interface is enabled - you can connect
        bool isEnabled = false;
        // Position interface is in use - you can move the robot
        bool isInUse = false;
        // TCP/IP port number of the position interface
        unsigned port = 0;
    };

    /**
     * @brief State of the motion program
     */
    InterpolatorState motionProgram;
    /**
     * @brief State of the logic program
     */
    InterpolatorState logicProgram;
    /**
     * @brief State of the Move-To interpolator (expect 0 or 1 program with only 1 command)
     */
    InterpolatorState moveTo;
    /**
     * @brief State of the fast position interface
     */
    PositionInterfaceState positionInterface;

    /**
     * @brief If this MotionState was sent in response to a request (specifically program load, start and move-to starts) this value is set true if the request
     * was successful
     */
    bool requestSuccessful = false;

    /**
     * @brief Default constructor
     */
    MotionState() = default;
    /**
     * @brief Constructor from GRPC MotionState
     * @param state
     */
    MotionState(const robotcontrolapp::MotionState& state);
};

} // namespace DataTypes
} // namespace App
