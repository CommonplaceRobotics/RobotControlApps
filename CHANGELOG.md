# App Interface Features Changelog

This changelog gives a summary of which features are available with which version of the robot control. We generally recommend using the newest robot control. The API should be backwards compatible but calling unsupported functions may cause no response or unexpected behavior.

## iRC V14-001
Initial release of the app interface
* iRC UI integration
* Robot program integration
* Reading / writing variables

## iRC V14-002
Support for Python apps

## iRC V14-004
* Static information
  * Software version
  * Robot and project type and filename
  * Device ID
  * Axis / module count
  * Main loop cycle statistics
* Robot state
  * Joint angles, cartesian position
  * Error codes
  * Referencing state
  * Temperatures, currents
  * Program states
  * Position interface state
* Control
  * Enabling / disabling motors
  * Referencing
  * Moving to target positions
  * Speed override
  * Programs
    * Starting, pausing, stopping, loading, unloading
    * Replay mode (single, repeat, step)
  * Files (within the Data directory only)
    * Up-/download (to/from file or memory)
    * Listing files