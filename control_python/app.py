import datetime
import sys
from time import sleep
from ControlApp import ControlApp

# Start the app
print("Starting control app example")

# The first command line argument (if given) is the connection target
connectionTarget = "localhost:5000"
if len(sys.argv) > 1:
    connectionTarget = sys.argv[1]

# Create an instance of the app and connect. The name given here must be equal to the name in rcapp.xml.
app = ControlApp("ControlApp-Python", connectionTarget)
app.Connect()

# time of the last example run
lastUpdate = datetime.datetime.now()

try:
    # Keep the app running
    while app.IsConnected():
        sleep(0.5)

        # Run some examples every few seconds
        now = datetime.datetime.now()
        if now - lastUpdate > datetime.timedelta(seconds=10):
            lastUpdate = now

            app.UpdateUI()

# Make sure to disconnect on exception
finally:
    app.Disconnect()
    print("Control app example stopped")
