/**
 * @brief The LicenseInfo contains info about the licensed features of the robot control.
 * @author MAB
 */
#pragma once

#include <robotcontrolapp.grpc.pb.h>

namespace App
{
namespace DataTypes
{

/**
 * @brief Contains info about a specific licensed feature
 */
class LicenseDetails
{
public:
    // Feature ID
    std::string featureID;
    // True if the feature is licensed and not expired
    bool isLicensed = false;
    // Expiry date and time or empty string if the feature does not expire
    std::string expiryDate;

    /**
     * @brief Default constructor
     */
    LicenseDetails() = default;
    /**
     * @brief Constructor from GRPC LicenseDetails
     */
    LicenseDetails(const robotcontrolapp::LicenseInfoResponse_LicenseDetails& info);
};

/**
 * @brief Contains info about the licensed features of the robot control.
 */
class LicenseInfo
{
public:
    // Number of remaining seconds in the feature test duration or 0 if expired. Within this duration some features can be tested without a license.
    unsigned testDurationRemaining = 0;
    // Licensed features and their validity
    std::map<std::string, LicenseDetails> features;

    /**
     * @brief Default constructor
     */
    LicenseInfo() = default;
    /**
     * @brief Constructor from GRPC LicenseInfoResponse
     */
    LicenseInfo(const robotcontrolapp::LicenseInfoResponse& info);

    /**
     * @brief Checks whether a feature is defined in the features list
     * @return true if the feature is defined
     */
    bool HasFeature(const std::string& featureID) const;
    /**
     * @brief Gets a feature from the features list. Throws std::invalid_argument if the feature is not defined (use HasFeature()!).
     * @brief Feature
     */
    const LicenseDetails& GetFeature(const std::string& featureID) const;
};

} // namespace DataTypes
} // namespace App
