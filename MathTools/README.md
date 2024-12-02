# Math Tools

This app contains a collection of useful math, logic and kinematic operations. It is intended to extend the feature set of the robot control software by infrequently used functions and to evaluate functions that may be added in future.

Consider adding your own functions if you need any, it should be relatively simple, just follow the examples!

# Features
Currently the following features are included:
* Scalar math
  * Square root
  * Exponentiation
  * Minimum
  * Maximum
* Positions
  * XYZ distance between variables
  * Check whether two position variables are near each other (XYZ only)
  * Partial copy of a position variable (specify which components to copy)
* Kinematics
  * Convert joint position to cartesian position
  * Convert cartesian position to joint position

# Adding your own functions
* Add the function and its parameters in rcapp.xml
* Add the function definition in MathToolsApp.py
  * Add a method that does the logic
  * In _AppFunctionHandler() check if the function is called (by its ID), if so call your method