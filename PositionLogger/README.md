# PositionLogger
This is a simple position logger. When triggered via the motion or logic program it adds the current TCP or a position variable to a CSV file.

The code should be easy to extend with some basic Python skills. See PositionLogger.py, rcapp.xml and the documentation in [MinimalApp](../minimal_python/README.md).

The log file "positionlog.csv" is created in the app directory on the robot control (Data/Apps/PositionLogger/positionlog.csv). It can be accessed via SFTP or by downloading a backup of the app via iRC.

# Commands
The position logger adds the following app commands:
* Clear log: Deletes the log file, should be called before logging is started to reset the log file
* Add TCP to log: Adds the current tool center point position
* Add position variable to log: Adds a position from a variable
