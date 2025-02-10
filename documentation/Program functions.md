# Program functions

Program functions are a mechanism to extend the robot program's functions with your own functions to be called during robot program execution. This way you add functions that are missing or specific to your task, e.g. for doing calculations, querying data from a camera or other source or for sending telemetry data.

## Defining an app function
To define an app function you must declare it in [```rcapp.xml```](rcapp.xml.md). This makes the function and it's parameters known to the robot control and selectable in the program editor.

Once the robot control reaches your function in a robot program it will call method ```AppFunctionHandler``` of ```AppClient``` with an object containing the call ID and the parameters. Override this function in your app to receive function calls. The robot program will wait until you call ```SendFunctionDone()``` or ```SendFunctionFailed()``` with the call ID. If you send FunctionFailed the program will abort with an error code. Make sure to always call one of either functions (e.g. via try-catch), otherwise the robot program will be stuck until the program is restarted.

## Examples
See the example apps [```MathTools```](../MathTools/) or [```MinimalApp```](../minimal_cpp/) for examples.

```MathTools``` shows how you can integrate multiple different functions. You can easily extend this app.

Example for the definition of an app with two functions in ```rcapp.xml```:
```
<App name="MathTools" label="Math Tools" vendor="" version="1.0.0">
	<executable path="app.py"/>

	<function name="min" label="Minimum">
		<parameter name="value_a" type="string" ui-hint="text" label="Number A"/>
		<parameter name="value_b" type="string" ui-hint="text" label="Number B"/>
		<parameter name="result" type="string" ui-hint="text" label="Result"/>
	</function>
	<function name="max" label="Maximum">
		<parameter name="value_a" type="string" ui-hint="text" label="Number A"/>
		<parameter name="value_b" type="string" ui-hint="text" label="Number B"/>
		<parameter name="result" type="string" ui-hint="text" label="Result"/>
	</function>
</App>
```

Override ```AppFunctionHandler()``` to receive function calls. Select between the different functions here:
```
    def _AppFunctionHandler(self, function: AppFunction):
        """Gets called on remote app function calls received from the robot control"""
        try:
            # Select the app function to call
            if function.name == "min":
                self.Minimum(function)
            elif function.name == "max":
                self.Maximum(function)
            else:
                self.SendFunctionFailed(function.call_id, "unknown function")
        except Exception as ex:
            print("Function call failed: " + ex)
            self.SendFunctionFailed(function.call_id, ex)
```

The implementation of one of the functions:
```
    def Minimum(self, function: AppFunction):
        """Copies the minimum value to the result variable"""
        # Get parameters
        valueAStatement = self.GetParameter(function, "value_a", "string").string_value()
        valueBStatement = self.GetParameter(function, "value_b", "string").string_value()
        resultVar = self.GetParameter(function, "result", "string").string_value()

        # Get values
        valueA = self.GetNumber(valueAStatement)
        valueB = self.GetNumber(valueBStatement)
        result = math.min(valueA, valueB)

        # Set result
        self.SetNumberVariable(resultVar, result)

        self.SendFunctionDone(function.call_id)
```

Use the same approach for C++ apps.