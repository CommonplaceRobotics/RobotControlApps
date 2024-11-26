# rcapp.xml documentation

The ```rcapp.xml``` file is used to register the features of your app at the robot control.

The following example shows the file structure:
```xml
<App name="MinimalApp" label="Minimal App Sample" vendor="My Company" version="1.0.0">
    <!-- Define the executable(s) to call -->
	<executable path="minimalapp"/>

    <!-- Example: Calculate <base_number_variable> to the power of <exponent_number> and assign the result to <result_variable> -->
	<function name="pow" label="Exponentiation">
		<parameter name="base_variable" type="string" ui-hint="text" label="Base (number variable)"></parameter>
		<parameter name="exponent_number" type="double" ui-hint="number" label="Exponent"></parameter>
		<parameter name="result_variable" type="string" ui-hint="text" label="Result (number variable)"></parameter>
	</function>
</App>
```

# App name, label, vendor and version
The first line, starting with ```<App...``` defines the name and label of the app. The name is used internally for identifying your app and should not contain spaces. The label is the human readable name that is shown to the user in iRC / CPRog.

Vendor and version are optional infos. These are shown when the user opens the app info dialog via the ribbon above the app UI. The app version is also logged by the RobotControl Core so that different versions of an app can be distinguished.

# Executables
The line ```<executable path="minimalapp"/>``` defines an executable to start. You may enter 0 or more of these lines. If your executable runs on a different device do not enter any executable entry.

**Binaries:** Do not give a file extension. The robot control will automatically add .exe on Windows (this way you can create multi-platform apps, simply add both RPi and Windows binaries to the zip file).

**Python:** If a file ending with .py is given the robot control will call python3 to run it.

# Functions
To integrate your app into the program editor you can define functions and parameters.

## Tag function
The line ```<function...``` defines the name and label of the function (see app name and label).

## Tag parameter
Add 0 or more ```<parameter...``` lines to let the robot program send parameters to your app whenever the app function is called. It is up to you how to use these parameters.

Each parameter must have a name (no spaces), label (human readable), type and ui-hint.

The type is currently not used. For future compatibility use these (more may be added later):
* string
* double
* bool

The UI hint defines what UI element is created (more may be added later):
* text - a text box
* number - a number box
* dropdown - a dropdown box - currently not supported yet, creates a text box instead
* checkbox - a checkbox
