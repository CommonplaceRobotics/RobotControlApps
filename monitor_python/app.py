import datetime
import sys
from time import sleep
from MonitorApp import MonitorApp

# Start the app
print("Starting monitor app example")

# The first command line argument (if given) is the connection target
connectionTarget = "localhost:5000"
if len(sys.argv) > 1:
    connectionTarget = sys.argv[1]

# Create an instance of the app and connect. The name given here must be equal to the name in rcapp.xml.
app = MonitorApp("MonitorApp-Python", connectionTarget)
app.Connect()

# time of the last example run
lastUpdate = datetime.datetime(2000, 1, 1)

try:
    # Keep the app running
    while app.IsConnected():
        sleep(0.5)

        app.ReadAndUpdateRobotState()

        # Run some examples every few seconds
        now = datetime.datetime.now()
        if now - lastUpdate > datetime.timedelta(seconds=10):
            lastUpdate = now

            app.UpdateSystemInfo()

# Make sure to disconnect on exception
finally:
    app.Disconnect()
    print("Monitor app example stopped")
