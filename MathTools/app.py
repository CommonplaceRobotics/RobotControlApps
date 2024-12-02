import datetime
import sys
from time import sleep
from AppClient import AppClient
from MathToolsApp import MathToolsApp

# Start the app
print("Starting MathTools")

# The first command line argument (if given) is the connection target
connectionTarget = "localhost:5000"
if len(sys.argv) > 1:
    connectionTarget = sys.argv[1]

# Create an instance of the app and connect. The name given here must be equal to the name in rcapp.xml.
app = MathToolsApp("MathTools", connectionTarget)
app.Connect()

try:
    # Keep the app running
    while app.IsConnected():
        sleep(0.5)

# Make sure to disconnect on exception
finally:
    app.Disconnect()
    print("MathTools stopped")
