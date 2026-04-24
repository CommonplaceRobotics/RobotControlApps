# MinimalApp Python
This is the minimal example and simple API for Python.

The features shown in this sample are available from iRC V14-001 but the API (```AppClient.h```) will be updated for the newest feature set. Check the other samples for other features.

# Structure
* ```rcapp.xml``` - app definition file, this tells RobotControl all it needs to start and integrate your app.
* ```ui.xml``` - the UI definition, this is optional if your app does not need user input
* ```app.py``` - the main file, starts the app and runs some examples.
* ```AppClient.py``` - the basic app client class. Derive this for your own application.
* ```MinimalApp.py``` - the example application class. It contains some examples of functions to be called by the robot program and UI event handlers.
* ```robotcontrolapp_pb2...``` - Python API for the GRPC interface. ```AppClient.py``` provides a more abstract interface for this.
* DataTypes - this contains data classes used by ```AppClient```

# System setup
To run Python apps you need to install Python 3.7 - 3.12 (tested with 3.9) and GRPC as explained in the [GRPC documentation](https://grpc.io/docs/languages/python/quickstart/).

Depending on your system you may need to adapt the following commands.

## PC
[Download Python 3](https://www.python.org/downloads/) and install it. Then run the following commands in a command line to install gRPC for Python.

### Standalone:
```sh
python3 -m pip install --upgrade pip
python3 -m pip install -r .\requirements.txt
```

### Python install manager:
```sh
py -V:3.9.2 -m venv ../venv
..\venv\Scripts\activate.bat
py -V:3.9.2 -m pip install -r .\requirements.txt
```

## Embedded Robot Control (Raspberry Pi)
Python is already installed on the embedded robot control. You still need to install gRPC for Python. To do this (temporarily) connect the robot control to the internet (e.g. connect it to a WiFi hotspot), then run the following commands:

```sh
sudo apt update
sudo mount -o remount,rw /boot/
sudo apt upgrade
sudo apt install python3-pip
python3 -m pip install --upgrade pip
python3 -m pip install grpcio==1.64.1
python3 -m pip install grpcio-tools==1.64.1
```

# Packaging and running the app
See [Packaging documentation](../documentation/Packaging.md).

# App definition file
See [rcapp.xml documentation](../documentation/rcapp.xml.md).

# UI definition file
See [ui.xml documentation](../documentation/ui.xml.md).

# Updating the GRPC definition
The GRPC python API (```robotcontrolapp_pb2...```) is generated from the ```protos/robotcontrolapp.proto``` definition. You should never need to regenerate these since the API only changes when functions are added to the robot control. Simply use the files provided in this repository.

The files can be regenerated with the following commands:

### Standalone python (see the version requirements above, otherwise the app won't run on the embedded control):
```sh
python3 -m grpc_tools.protoc -Iprotos --python_out=. --pyi_out=. --grpc_python_out=. protos/robotcontrolapp.proto
```

### Python install manager:
```sh
..\venv\Scripts\activate.bat
py -V:3.9.2 -m grpc_tools.protoc -Iprotos --python_out=. --pyi_out=. --grpc_python_out=. protos/robotcontrolapp.proto
```

# Testing
Use the following commands to run the unit tests:

Install pytest for standalone Python:
```sh
python3 -m pip install pytest
```
Or for Python install manager:
```sh
py -V:3.9.2 -m pip install pytest
```

Then run the tests by calling one of the following commands:
```sh
python3 -m pytest
py -V:3.9.2 -m pytest
```
