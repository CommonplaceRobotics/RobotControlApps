# Robot Control Apps

Since [version 14](https://wiki.cpr-robots.com/index.php/IgusRobotControl-Release14-EN) the Commonplace Robotics (CPRog) / igus Robot Control (iRC) can be extended by apps. This repository contains guides, APIs and examples for creating your own apps.

## Features
* Simple C++ and Python API
* Add new functions to robot programs
* User interface integration into igus Robot Control / CPRog, e.g. for configuration or monitoring
* Read/write program variables
* Read the robot's state
  * Position
  * Current cartesian velocity
  * Digital IOs and global signals
  * Hardware and kinematic error codes
  * Referencing state
  * Temperatures
  * Program states
  * etc.
* Read the system info
  * Robot software version
  * Robot type and owner
  * Cycle time statistics
  * Axis and IO module count
  * etc.
* Initialize the robot
  * Enable/disable joints
  * Reference joints
* Get/set digital outputs, global signals and digital inputs (including setting digital inputs in simulation)
* Programs
  * Load program files
  * Start/stop/pause motion and logic programs
* Move-To: Move to absolute or relative joint or cartesian positions
* Files
  * Upload/download files
  * List files on the robot control (e.g. list all programs)

This is just a summary, please read [```AppClient.h```](minimal_cpp/src/AppClient.h) or [```AppClient.py```](minimal_python/AppClient.py) for a list of all features.

## Planned features
The following features are planned or considered to be added in future:
* App UI
  * Text styling (font size, bold, italic, etc.)
  * Multi line text
  * Assign icons to the buttons in the ribbon above the 3D view
  * Define images to be loaded by the iRC PC software instead of having to send them by the app
* Control
  * External axis velocity (conveyor)

## Technology overview
The robot control provides a [gRPC](https://grpc.io/) interface that allows calling functions and transmitting data between the robot control and the app. With the gRPC protocol file ```robotcontrolapp.proto``` you can generate the API for [several different programming languages](https://grpc.io/docs/languages/). In this repository you will find classes for C++ and Python that you can use for a quick start.

The app configuration file ```rcapp.xml``` is used to register the app at the robot control. It defines the binaries or scripts to execute and the functions that are available to the program editor. The app can also [run on a different device](documentation/Packaging.md), e.g. if more performance is required.

The UI definition file ```ui.xml``` defines the user interface that integrates into iRC / CPRog using a simple XML structure. UI events are sent to the app and the app can request value and visibility changes.

All files are packed as a zip file that can be installed via iRC / CPRog.

## Security
**Warning:** Apps can run arbitrary code and can cause damage e.g. to the robot control or the network. Only use apps that you trust and do not connect the robot to the internet or your company network if you can avoid it!

## Minimal App
The MinimalApp is our example and API (available in C++ and Python) that you can use as a base for your own app. The class ```AppClient``` provides a simple interface for the most common functions. Create a class derived from ```AppClient``` and override the methods ```AppFunctionHandler()``` and ```UiUpdateHandler()```. The former is called when the robot program calls a function of your app, the latter is called on UI events.

Read ```main.cpp``` or ```app.py``` and class ```MinimalApp``` for examples and replace these to create your own robot control app.

The ```MinimalApp.xml``` file is a sample robot program that calls the pow function of the sample apps and creates some program variables for the apps to read and write. Observe their values in the variables section below the 3D view.

# Monitor App
This app is an example for reading and displaying the robot's state.

# Control App
This app is an example for controlling a robot via an app.

# Math Tools
This app extends the robot control by new math features like calculating the distance between two position variables. With some Python knowledge you should be able to easily extend the robot control's programs with your own functions.

# Documentation
See the README.md files and the source code comments in the example directories.

The [documentation](documentation/README.md) directory contains further explanations.
