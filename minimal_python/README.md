# MinimalApp Python
This is the minimal example and starting point for an igus Robot Control (iRC) app in Python. It contains the app API code and some samples for the basic functions.

The features shown in this sample are available from iRC V14-001 but the API will be updated for the newest feature set. For other feature examples check the other apps in the parent directory.

## Structure
* [```rcapp.xml```](rcapp.xml) - App definition file. RobotControl uses it to integrate and start the app.
* [```ui.xml```](ui.xml) - UI definition. This is optional if your app does not need user input.
* ```src``` - App source code
    * [```app.py```](src/app.py) - The app's main file. It starts the app and runs some examples.
    * ```minimal_app``` - Additional app files
        * [```MinimalApp.py```](src/minimal_app/MinimalApp.py) - Example app class. It contains some examples of functions to be called by the robot program and UI event handlers.
    * ```irc_app``` - Contains the API code, you should not change it.
        * [```AppClient.py```](src/irc_app/AppClient.py) - App client base class. Derive this for your own application, see ```MinimalApp.py```
        * ```DataTypes``` - Data classes
        * ```rpc``` - gRPC definitions for the iRC App API

For implementing your own app [```app.py```](src/app.py) and [```MinimalApp.py```](src/minimal_app/MinimalApp.py) are the most relevant files, adapt and rename them as you need.

For API reference check the comments in [```AppClient.py```](src/irc_app/AppClient.py)


## Standalone apps

igus Robot Control apps can either run on the robot control (the embedded control module or the simulator on PC) or run separate system as a standalone application. This may be useful if your app requires more system resources, e.g. for high performance image processing. In the first case the robot control starts and stops the app, in the second case you are responsible for running it. For development you may want to run your app like a standalone application from your IDE.

In all situations you must install the app package to the robot control. For standalone operation remove (or comment out) the ```<executable ... />``` line in ```rcapp.xml``` - the robot control will register the app and wait for an incoming connection. Don't forget to enter the robot control's IP (or ```localhost``` if connecting with a simulation on your PC) as the connection target in ```app.py```.


## System Setup
To run Python and develop apps you must set up a Python environment.

### PC / other systems
Follow these steps to run apps in simulation or in standalone mode on PC.

We recommend installing Python via the [Python Install Manager](https://www.python.org/downloads/). This way you can easily install and use different Python versions. For dependency management we use [poetry](https://python-poetry.org/docs/).

```bash
py -V:3.9.2 -m pip install poetry
```

To set up the poetry environment first we need the path to the correct Python binary. Run the following command and copy the path from the first output line.
```bash
py -V:3.9.2 --help
```

Make sure your command line is in the project directory (where this README file is). Then enable the environment using the following command (replace the path with the open you copied).
```bash
py -V:3.9.2 -m poetry env use C:\Users\YourUserName\AppData\Local\Python\pythoncore-3.9-64\python.exe
```

Install the app's dependencies.
```bash
py -V:3.9.2 -m poetry install
```

Now you can run the app locally:
```bash
py -V:3.9.2 ./src/app.py
```

You can run the tests using the following command.
```bash
py -V:3.9.2 -m pytest
```

If you changed the dependencies you may need to update the ```poetry.lock``` file by calling ```poetry lock``` or simply deleting it. Then run ```poetry install``` again.


### Regenerating GRPC files

For compatibility we recommend using Python version 3.9.2. If do not intend to run your app on the robot control you may use a different Python version and update grpc, in this case you will need to regenerate the grpc definitions using the following commands:
```bash
cd src
py -V:3.9.2 -m pip install grpcio-tools==1.64.1
py -V:3.9.2 -m grpc_tools.protoc -I ./irc_app/rpc/ --python_out=./irc_app/rpc --pyi_out=./irc_app/rpc --grpc_python_out=./irc_app/rpc ./irc_app/rpc/robotcontrolapp.proto
```

Then open the generated file ```src/irc_app/rpcrobotcontrolapp_pb2_grpc.py``` and change the import line as follows (the grpc compiler seems unable to detect the correct module path):

```python
from irc_app.rpc import robotcontrolapp_pb2 as robotcontrolapp__pb2
```

### Embedded Robot Control

All new robot controls come with Python 3.9.2 and the gRPC dependencies pre-installed. Unless you add other dependencies you should not need to do anything. If you got an older robot control that predates the introduction of the app interface you will need to install the dependencies manually.

To do this (temporarily) connect the robot control to the internet (e.g. connect it to a WiFi access point or hotspot), then run the following commands:

```bash
sudo apt update
sudo mount -o remount,rw /boot/
sudo apt upgrade
sudo apt install python3-pip
python3 -m pip install --upgrade pip
python3 -m pip install grpcio==1.64.1
python3 -m pip install grpcio-tools==1.64.1
```

## Packaging the app
The app must be packaged before it can be installed to the robot control. If you got Bash (e.g. on Linux or via Cygwin) you can simply call the packaging script, otherwise follow the packaging documentation below.

```bash
package.sh
```

See [Packaging documentation](../documentation/Packaging.md) for the package structure.

## App definition file
The app definition file ```rcapp.xml``` contains any information that the robot control needs to integrate and start the app.

See [rcapp.xml documentation](../documentation/rcapp.xml.md).

## UI definition file
The optional UI definition file defines the app UI elements for integration into the PC software.

See [ui.xml documentation](../documentation/ui.xml.md).
