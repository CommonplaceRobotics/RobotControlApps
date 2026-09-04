import unittest

from irc_app.AppClient import AppClient


class AppClientTest(unittest.TestCase):
    def test_init(self):
        appClient = AppClient("TestAppName", "localhost:5000")

        self.assertLessEqual(14, appClient.VERSION_MAJOR_MIN)
        self.assertLessEqual(0, appClient.VERSION_MINOR_MIN)
        self.assertLessEqual(0, appClient.VERSION_PATCH_MIN)

        self.assertFalse(appClient.logDebug)

        self.assertEqual("TestAppName", appClient.GetAppName())


if __name__ == "__main__":
    unittest.main()

# TODO: Write tests for other functions, but this requires simulating the server side.
# The AppIntegrationTest (in RobotControl repository) tests this with the real robot control.
