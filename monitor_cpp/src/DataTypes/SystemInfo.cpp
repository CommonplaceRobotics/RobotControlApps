#include "SystemInfo.h"

namespace App
{
namespace DataTypes
{

/**
 * @brief Constructor from GRPC SystemInfo
 * @param info
 */
SystemInfo::SystemInfo(const robotcontrolapp::SystemInfo& info) 
{
    versionMajor = info.version_major();
    versionMinor = info.version_minor();
    versionPatch = info.version_patch();
    version = info.version();

    systemType = info.system_type();

    projectFile = info.project_file();
    projectTitle = info.project_title();
    projectAuthor = info.project_author();
    robotType = info.robot_type();

    voltage = info.voltage();

    deviceID = info.device_id();

    cycleTimeTarget = info.cycle_time_target();
    cycleTimeAverage = info.cycle_time_avg();
    cycleTimeMin = info.cycle_time_min();
    cycleTimeMax = info.cycle_time_max();
    workload = info.workload();

    robotAxisCount = info.robot_axis_count();
    externalAxisCount = info.external_axis_count();
    toolAxisCount = info.tool_axis_count();
    platformAxisCount = info.platform_axis_count();
    digitalIOModuleCount = info.digital_io_module_count();
}

} // namespace DataTypes
} // namespace App