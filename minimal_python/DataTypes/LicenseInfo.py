# This class contains information about the features that are licensed by the robot control's license
import robotcontrolapp_pb2


class LicenseDetails:
    """Contains licensing information about a specific feature"""

    def __init__(self):
        self.featureID = ""
        """Feature ID"""
        self.isLicensed = False
        """True if the feature is licensed and not expired"""
        self.expiryDate = ""
        """Expiry date and time or empty string if the feature does not expire"""

    def FromGrpc(grpc: robotcontrolapp_pb2.LicenseInfoResponse.LicenseDetails):
        """Creates an object from a GRPC LicenseDetails object"""
        self = LicenseDetails()
        self.featureID = grpc.feature_id
        self.isLicensed = grpc.is_licensed
        if grpc.HasField("expiry_date"):
            self.expiryDate = grpc.expiry_date

        return self


class LicenseInfo:
    """This class contains information about the features that are licensed by the robot control's license"""

    def __init__(self):
        self.testDurationRemaining = 0
        """Number of remaining seconds in the feature test duration or 0 if expired. Within this duration some features can be tested without a license."""
        self.features = dict()
        """Licensed features and their validity. Key is the feature ID, value an instance of LicenseInfo"""

    def FromGrpc(grpc: robotcontrolapp_pb2.LicenseInfoResponse):
        """Creates an object from a GRPC LicenseInfo object"""
        self = LicenseInfo()
        self.testDurationRemaining = grpc.test_duration_remaining_seconds

        for f in grpc.licensed_features:
            self.features[f.feature_id] = LicenseDetails.FromGrpc(f)

        return self
