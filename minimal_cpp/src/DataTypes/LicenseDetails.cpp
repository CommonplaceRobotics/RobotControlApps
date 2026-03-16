#include "LicenseDetails.h"

namespace App
{
namespace DataTypes
{

/**
 * @brief Constructor from GRPC LicenseDetails
 */
LicenseDetails::LicenseDetails(const robotcontrolapp::LicenseInfoResponse_LicenseDetails& info)
{
    featureID = info.feature_id();
    isLicensed = info.is_licensed();
    if (info.has_expiry_date())
        expiryDate = info.expiry_date();
    else
        expiryDate = "";
}

/**
 * @brief Constructor from GRPC LicenseInfoResponse
 */
LicenseInfo::LicenseInfo(const robotcontrolapp::LicenseInfoResponse& info)
{
    testDurationRemaining = info.test_duration_remaining_seconds();

    for (const auto& feature : info.licensed_features())
    {
        features.try_emplace(feature.feature_id(), LicenseDetails(feature));
    }
}

/**
 * @brief Checks whether a feature is defined in the features list
 * @return true if the feature is defined
 */
bool LicenseInfo::HasFeature(const std::string& featureID) const
{
    return features.find(featureID) != features.end();
}

/**
 * @brief Gets a feature from the features list. Throws std::invalid_argument if the feature is not defined (use HasFeature()!).
 * @brief Feature
 */
const LicenseDetails& LicenseInfo::GetFeature(const std::string& featureID) const
{
    auto featureIt = features.find(featureID);
    if (featureIt != features.end())
        return featureIt->second;
    else
        throw std::invalid_argument("feature not found");
}

} // namespace DataTypes
} // namespace App
