#include "Statistics.h"

namespace App
{
namespace DataTypes
{

/**
 * @brief Constructor, copies the data from a GRPC object
 * @param grpc
 */
Statistics::Statistics(const robotcontrolapp::StatisticsResponse& grpc)
{
    uptimeComplete = grpc.uptime_complete();
    uptimeLast = grpc.uptime_last();
    uptimeEnabled = grpc.uptime_enabled();
    uptimeMotion = grpc.uptime_motion();

    programStartsTotal = grpc.program_starts_total();
    programStartsLast = grpc.program_starts_last();
    programDurationLast = grpc.program_duration_last();

    partsGood = grpc.parts_good();
    partsBad = grpc.parts_bad();

    for (int i = 0; i < (int)robotAxisDirectionChanges.size() && i < grpc.robot_axis_direction_changes_size(); i++)
    {
        robotAxisDirectionChanges[i] = grpc.robot_axis_direction_changes(i);
    }
    for (int i = 0; i < (int)externalAxisDirectionChanges.size() && i < grpc.external_axis_direction_changes_size(); i++)
    {
        externalAxisDirectionChanges[i] = grpc.external_axis_direction_changes(i);
    }
}

} // namespace DataTypes
} // namespace App
