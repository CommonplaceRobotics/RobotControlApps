import unittest

from DataTypes.LicenseInfo import LicenseInfo, LicenseDetails
import robotcontrolapp_pb2


class LicenseInfoTest(unittest.TestCase):
    def test_init(self):
        licenseInfo = LicenseInfo()
        self.assertEqual(0, licenseInfo.testDurationRemaining)
        self.assertEqual(0, len(licenseInfo.features))

        licenseDetails = LicenseDetails()
        self.assertEqual("", licenseDetails.featureID)
        self.assertEqual(False, licenseDetails.isLicensed)
        self.assertEqual("", licenseDetails.expiryDate)

    def test_FromGrpc(self):
        grpc1 = robotcontrolapp_pb2.LicenseInfoResponse()
        grpc1.test_duration_remaining_seconds = 42

        result1 = LicenseInfo.FromGrpc(grpc1)
        self.assertEqual(42, result1.testDurationRemaining)
        self.assertEqual(0, len(result1.features))

        grpc2 = robotcontrolapp_pb2.LicenseInfoResponse()
        grpc2.test_duration_remaining_seconds = 123

        ld1 = grpc2.licensed_features.add()
        ld1.feature_id = "MyFeature"
        ld1.is_licensed = True

        ld2 = grpc2.licensed_features.add()
        ld2.feature_id = "SecondFeature"
        ld2.is_licensed = True
        ld2.expiry_date = "2026-03-13T12:13:14Z"

        ld3 = grpc2.licensed_features.add()
        ld3.feature_id = "ThirdFeature"
        ld3.is_licensed = False

        result2 = LicenseInfo.FromGrpc(grpc2)
        self.assertEqual(123, result2.testDurationRemaining)
        self.assertEqual(3, len(result2.features))

        self.assertEqual(True, "MyFeature" in result2.features)
        self.assertEqual(True, "SecondFeature" in result2.features)
        self.assertEqual(True, "ThirdFeature" in result2.features)
        self.assertEqual(False, "MyFeature2" in result2.features)

        self.assertEqual("MyFeature", result2.features["MyFeature"].featureID)
        self.assertEqual(True, result2.features["MyFeature"].isLicensed)
        self.assertEqual("", result2.features["MyFeature"].expiryDate)

        self.assertEqual("SecondFeature", result2.features["SecondFeature"].featureID)
        self.assertEqual(True, result2.features["SecondFeature"].isLicensed)
        self.assertEqual(
            "2026-03-13T12:13:14Z", result2.features["SecondFeature"].expiryDate
        )

        self.assertEqual("ThirdFeature", result2.features["ThirdFeature"].featureID)
        self.assertEqual(False, result2.features["ThirdFeature"].isLicensed)
        self.assertEqual("", result2.features["ThirdFeature"].expiryDate)


if __name__ == "__main__":
    unittest.main()
