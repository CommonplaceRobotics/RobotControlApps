# This class contains information about the features that are licensed by the robot control's license
from dataclasses import dataclass

import robotcontrolapp_pb2


@dataclass
class LicenseDetails:
    """Contains licensing information about a specific feature"""

    featureID: str = ""
    """Feature ID"""
    isLicensed: bool = False
    """True if the feature is licensed and not expired"""
    expiryDate: str = ""
    """Expiry date and time or empty string if the feature does not expire"""


def LicenseDetailsFromGrpc(
    grpc: robotcontrolapp_pb2.LicenseInfoResponse.LicenseDetails,
) -> LicenseDetails:
    """Creates an object from a GRPC LicenseDetails object"""
    details = LicenseDetails()
    details.featureID = grpc.feature_id
    details.isLicensed = grpc.is_licensed
    if grpc.HasField("expiry_date"):
        details.expiryDate = grpc.expiry_date

    return details


@dataclass
class LicenseInfo:
    """This class contains information about the features that are licensed by the robot control's license"""

    def __init__(self):
        self.testDurationRemaining: int = 0
        """
        Number of remaining seconds in the feature test duration or 0 if expired. Within this duration some features can
        be tested without a license.
        """
        self.features = dict()
        """Licensed features and their validity. Key is the feature ID, value an instance of LicenseInfo"""


def LicenseInfoFromGrpc(grpc: robotcontrolapp_pb2.LicenseInfoResponse) -> LicenseInfo:
    """Creates an object from a GRPC LicenseInfo object"""
    info = LicenseInfo()
    info.testDurationRemaining = grpc.test_duration_remaining_seconds

    for f in grpc.licensed_features:
        info.features[f.feature_id] = LicenseDetailsFromGrpc(f)

    return info
