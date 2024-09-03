/**
 * @brief The SystemInfo contains information that usually does not change (except for the cycle time statistics)
 * @author MAB
 */
#pragma once

#include <string>
#include <robotcontrolapp.grpc.pb.h>

#include "Matrix44.h"

namespace App
{
namespace DataTypes
{

/**
 * @brief This class contains system information that usually does not change (except for the cycle time statistics)
 */
class SystemInfo
{
public:
    // Robot control software version major, e.g. V14-003-1 -> 14
    int versionMajor = 0;
    // Robot control software version minor, e.g. V14-003-1 -> 3
    int versionMinor = 0;
    // Robot control software version patch, e.g. V14-003-1 -> 1
    int versionPatch = 0;
    // Robot control software version string, possibly with suffix, e.g. "V14-003-1-RC1"
    std::string version;

    // Project file, e.g. "igus-REBEL/REBEL-6DOF-01.prj"
    std::string projectFile;
    // User defined project title
    std::string projectTitle;
    // User defined project author
    std::string projectAuthor;
    // Robot type, e.g. "igus-REBEL/REBEL-6DOF-01"
    std::string robotType;

    // Voltage configuration of the robot - this selects the velocity limits
    robotcontrolapp::SystemInfo_Voltage voltage = robotcontrolapp::SystemInfo_Voltage_Voltage24V;

    // System type of the robot control
    robotcontrolapp::SystemInfo::SystemType systemType = robotcontrolapp::SystemInfo_SystemType_Other;

    // unique device ID
    std::string deviceID;
    
    // Robot main loop cycle time (hardware IO, kinematics, program execution) target in ms
    float cycleTimeTarget = 0;
    // Average robot main loop cycle time average in ms
    float cycleTimeAverage = 0;
    // Average robot main loop cycle time recent maximum in ms
    float cycleTimeMax = 0;
    // Average robot main loop cycle time recent minimum in ms
    float cycleTimeMin = 0;
    // Average workload in percent (how much of the available time is used vs. waited)
    float workload = 0;

    // number of robot joints
    int robotAxisCount = 0;
    // number of external axes
    int externalAxisCount = 0;
    // number of tool axes
    int toolAxisCount = 0;
    // number of platform axes
    int platformAxisCount = 0;
    // number of digital IO modules
    int digitalIOModuleCount = 0;

    /**
     * @brief Default constructor
     */
    SystemInfo() = default;
    /**
     * @brief Constructor from GRPC SystemInfo
     * @param info 
     */
    SystemInfo(const robotcontrolapp::SystemInfo& info);
};

}
} // namespace App