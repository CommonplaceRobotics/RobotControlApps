# Minimal Robot Control App Example

This app is intended as a minimal example and as a base for new app development.

The features shown in this sample are available from iRC V14-001 but the API (```AppClient.h```) will be updated for the newest feature set. Check the other samples for other features.

## Files

### Base directory
* ```rcapp.xml``` - app definition file, this tells RobotControl all it needs to start and integrate your app.
* ```ui.xml``` - the UI definition, this is optional if your app does not need user input
* ```CMakeLists.txt``` - Definition for compiling with CMake
* ```vcpkg.json``` - Dependency definition for [vcpkg](https://vcpkg.io). This is intended for building for Windows but may also work for Linux-native builds.
* The ```protos``` directory contains the gRPC definition file. CMake will use it to automatically generate the C++ interface.

### src directory
In the src directory you will find the following files:
* ```main.cpp``` - this contains the main function, initialize your app here
* ```AppClient.h / .cpp``` - this contains an interface to the robot control. You should not need to change this, simply derive your own class and implement the abstruct methods.
* ```MinimalApp.h / .cpp``` - this contains a sample implementation of AppClient. It shows how to handle commands and UI events coming from the robot control, as well as how to send messages and UI changes back to the robot control.
* ```DataTypes``` - this directory contains helper classes for matrices, program variables etc.


## How to write a new app
Copy the code of the minimal app and derive your own class from ```AppClient```. You will need to override ```AppFunctionHandler()``` (this is called when a robot program calls a function of your app) and ```UiUpdateHandler()``` (this is called on UI events).

The most important functions of the app interface can be used via the methods of ```AppClient``` - read the comments of the public methods in ```AppClient.h``` for more info. Other functions may require you to build GRPC ```AppAction``` messages and send them via ```SendAction()```. Please refer to the ```robotcontrolapp.proto``` file for the message structure. Classes ```MinimalApp``` and ```AppClient``` contain examples on how to create these messages.

Create an instance of your app class in ```main.cpp``` and remove ```MinimalApp``` and the examples there. Delete ```MinimalApp.h / .cpp``` when you don't need the examples anymore.


## Compiling
Read the [Building guide](BUILDING.md) on how to compile C++ apps for Windows, Linux and Raspberry Pi (embedded robot control).
