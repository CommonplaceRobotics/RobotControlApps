import datetime
import sys
from time import sleep
from AppClient import AppClient
from MinimalApp import MinimalApp

# Below you will find examples for sending requests from the app to the robot control.
# Also check MinimalApp.py for examples on how to handle requests from the robot control (e.g. user interface and program commands)


def ExamplePrintTCP(app: AppClient):
    """Example: Requests and prints the tool center point (cartesian) position."""
    tcp = app.GetTCP()
    print(
        f"TCP: X={tcp.GetX():.2f} Y={tcp.GetY():.2f} Z={tcp.GetZ():.2f} A={tcp.GetA():.2f} B={tcp.GetB():.2f} C={tcp.GetC():.2f}"
    )


def ExamplePrintNumberVariable(app: AppClient, variableName: str) -> float:
    """Example: Requests and prints a number variable. This variable must be defined in a m_running robot program."""
    try:
        numberVariable = app.GetNumberVariable(variableName)

        print(f'Program variable "{variableName}": {numberVariable.GetValue():.4f}')
        return numberVariable.GetValue()
    except RuntimeError as ex:
        print(f'Could not get number variable "{variableName}":', file=sys.stderr)
        print(
            "for this example please start the a program that defines this variable",
            file=sys.stderr,
        )
        print(ex, file=sys.stderr)
        return 0


def ExampleSetNumberVariable(app: AppClient, variableName: str, value: float):
    """Example: Sets a number variable. The value increases with each call."""
    try:
        app.SetNumberVariable(variableName, value)
    except RuntimeError as ex:
        print(f'Could not set number variable "{variableName}":', file=sys.stderr)
        print(
            "for this example please start the a program that defines this variable",
            file=sys.stderr,
        )
        print(ex, file=sys.stderr)


def ExamplePrintPositionVariable(app: AppClient, variableName: str):
    """Example: Requests and prints a position variable. This variable must be defined in a m_running robot program."""
    try:
        positionVariable = app.GetPositionVariable(variableName)

        print(
            f'Position variable "{variableName}" cart: '
            + f"X={positionVariable.GetCartesian().GetX():.2f} "
            + f"Y={positionVariable.GetCartesian().GetY():.2f} "
            + f"Z={positionVariable.GetCartesian().GetZ():.2f} "
            + f"A={positionVariable.GetCartesian().GetA():.2f} "
            + f"B={positionVariable.GetCartesian().GetB():.2f} "
            + f"C={positionVariable.GetCartesian().GetC():.2f}"
        )
        print(
            f'Position variable "{variableName}" joint: '
            + f"A1={positionVariable.GetRobotAxes()[0]:.2f} "
            + f"A2={positionVariable.GetRobotAxes()[1]:.2f} "
            + f"A3={positionVariable.GetRobotAxes()[2]:.2f} "
            + f"A4={positionVariable.GetRobotAxes()[3]:.2f} "
            + f"A5={positionVariable.GetRobotAxes()[4]:.2f} "
            + f"A6={positionVariable.GetRobotAxes()[5]:.2f} "
            + f"E1={positionVariable.GetExternalAxes()[0]:.2f} "
            + f"E2={positionVariable.GetExternalAxes()[1]:.2f} "
            + f"E3={positionVariable.GetExternalAxes()[2]:.2f}"
        )
    except RuntimeError as ex:
        print(f'Could not get position variable "{variableName}":', file=sys.stderr)
        print(
            "for this example please start the a program that defines this variable",
            file=sys.stderr,
        )
        print(ex, file=sys.stderr)

def ExampleReadWritePositionVariable(app: AppClient):
    """This example reads the current position from variable #position and writes it back to variable "mycurrentposition"""
    try:
        # Read the current position from the system variable "#position"
        positionVariable = app.GetPositionVariable("#position")

        # Send the cartesian position back to position variable "mycurrentposition"
        app.SetPositionVariableBoth("mycurrentposition", positionVariable.GetCartesian(), positionVariable.GetRobotAxes()[0], positionVariable.GetRobotAxes()[1], positionVariable.GetRobotAxes()[2], positionVariable.GetRobotAxes()[3], positionVariable.GetRobotAxes()[4], positionVariable.GetRobotAxes()[5], positionVariable.GetExternalAxes()[0], positionVariable.GetExternalAxes()[1], positionVariable.GetExternalAxes()[2])

    except RuntimeError as ex:
        print(f'Could not get position variable "#position" or set "mycurrentposition":', file=sys.stderr)
        print(ex, file=sys.stderr)

# Start the app
print("Starting minimal app example")

# The first command line argument (if given) is the connection target
connectionTarget = "localhost:5000"
if len(sys.argv) > 1:
    connectionTarget = sys.argv[1]

# Create an instance of the app and connect. The name given here must be equal to the name in rcapp.xml.
app = MinimalApp("MinimalApp-Python", connectionTarget)
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

            try:
                ExamplePrintTCP(app)
                ExamplePrintPositionVariable(app, "apppos")
                value = ExamplePrintNumberVariable(app, "appnum")
                ExampleSetNumberVariable(app, "appnum", value + 1)
                ExampleReadWritePositionVariable(app)
            except RuntimeError:
                pass

# Make sure to disconnect on exception
finally:
    app.Disconnect()
    print("Minimal app example stopped")
