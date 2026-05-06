/**
 * @brief The Statistics class contains statistics data
 * @author MAB
 */

#pragma once

#include <robotcontrolapp.grpc.pb.h>

namespace App
{
namespace DataTypes
{

class Statistics
{
public:
    /**
     * @brief Default constructor
     */
    Statistics() = default;
    /**
     * @brief Constructor, copies the data from a GRPC object
     * @param grpc
     */
    Statistics(const robotcontrolapp::StatisticsResponse& grpc);

    // Total uptime in minutes
    uint32_t uptimeComplete = 0;
    // Uptime till previous shutdown in minutes
    uint32_t uptimeLast = 0;
    // Total time in motors enabled state in minutes
    uint32_t uptimeEnabled = 0;
    // Total time with axes in motion in minutes
    uint32_t uptimeMotion = 0;

    // Total number of program starts
    uint32_t programStartsTotal = 0;
    // Number of program starts since startup
    uint32_t programStartsLast = 0;
    // Duration of the previous program run in seconds
    double programDurationLast = 0;

    // Number of good parts (number variable #parts-good)
    double partsGood = 0;
    // Number of bad parts (number variable #parts-bad)
    double partsBad = 0;

    // Number of direction changes of the robot axes
    std::array<uint32_t, 6> robotAxisDirectionChanges = {};
    // Number of direction changes of the external axes
    std::array<uint32_t, 3> externalAxisDirectionChanges = {};
};

} // namespace DataTypes
} // namespace App
