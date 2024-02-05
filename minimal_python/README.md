# MinimalApp Python
This is the minimal example and simple API for Python.

# Structure
* ```rcapp.xml``` - app definition file, this tells RobotControl all it needs to start and integrate your app.
* ```ui.xml``` - the UI definition, this is optional if your app does not need user input
* ```app.py``` - the main file, starts the app and runs some examples.
* ```AppClient.py``` - the basic app client class. Derive this for your own application.
* ```MinimalApp.py``` - the example application class. It contains some examples of functions to be called by the robot program and UI event handlers.
* ```robotcontrolapp_pb2...``` - these files are generated from the ```protos/robotcontrolapp.proto``` definition. Do not change these! You can regenerate / update them by calling
    ```
    python3 -m grpc_tools.protoc -Iprotos --python_out=. --pyi_out=. --grpc_python_out=. protos/robotcontrolapp.proto
    ```

* DataTypes - this contains data classes used by ```AppClient```

# System setup
To run Python apps you need to install Python 3.7 or newer and GRPC as explained in the [GRPC documentation](https://grpc.io/docs/languages/python/quickstart/).

Depending on your system you may need to adapt the following commands.

## PC
[Download Python 3](https://www.python.org/downloads/) and install it. Then run the following commands in a command line to install gRPC for Python:

```
python3 -m pip install --upgrade pip
python3 -m pip install grpcio
python3 -m pip install grpcio-tools
```

## Embedded Robot Control (Raspberry Pi)
Python is already installed on the embedded robot control. You still need to install gRPC for Python. To do this (temporarily) connect the robot control to the internet (e.g. connect it to a WiFi hotspot), then run the following commands:

```
sudo apt update
sudo mount -o remount,rw /boot/
sudo apt upgrade
sudo apt install python3-pip
python3 -m pip install --upgrade pip
python3 -m pip install grpcio
python3 -m pip install grpcio-tools
```

# Packaging and running the app
See [Packaging documentation](../documentation/Packaging.md).

# App definition file
See [rcapp.xml documentation](../documentation/rcapp.xml.md).

# UI definition file
See [ui.xml documentation](../documentation/ui.xml.md).
