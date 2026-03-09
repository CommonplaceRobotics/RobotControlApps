import datetime
import sys
from time import sleep
from AppClient import AppClient
from PositionLogger import PositionLogger

# Start the app
print("Starting Position Logger")

# The first command line argument (if given) is the connection target
connectionTarget = "localhost:5000"
if len(sys.argv) > 1:
    connectionTarget = sys.argv[1]

# Create an instance of the app and connect. The name given here must be equal to the name in rcapp.xml.
app = PositionLogger("PositionLogger", connectionTarget)
app.Connect()

# time of the last example run
lastUpdate = datetime.datetime.now()

try:
    # Keep the app running
    while app.IsConnected():
        sleep(0.5)

# Make sure to disconnect on exception
finally:
    app.Disconnect()
    print("PositionLogger stopped")
