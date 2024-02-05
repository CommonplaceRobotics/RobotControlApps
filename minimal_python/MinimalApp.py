import sys
from AppClient import AppClient
from DataTypes.Matrix44 import Matrix44
from robotcontrolapp_pb2 import ButtonState, CheckboxState


class MinimalApp(AppClient):
    # Initializes the app. Pass the app name (as defined in rcapp.xml) and socket to connect to (default: "localhost:5000")
    def __init__(self, appName: str, target: str):
        AppClient.__init__(self, appName, target)

        # Gets called on remote app function calls received from the robot control

    def _AppFunctionHandler(self, function):
        # This prints the received function data
        print("Received app function:")
        print(function)

        # Select the app function to call
        if function.name == "pow":
            self.ExampleExponentiation(function)
        else:
            # Example on how to handle app functions (these are called by the program command "App")
            self.ExamplePrintAppFunctionParameters(function)

        # Confirm that the function finished, otherwise the robot program will wait forever.
        # You may send this later if the function call takes some time but it must be sent at some point.
        self.SendFunctionDone(function.call_id)

    # Gets called on remote UI update requests received from the robot control
    def _UiUpdateHandler(self, updates):
        # This prints the received UI updates:
        print("Received UI updates: ")
        print(updates)

        # Example on how to handle UI events (button clicked, value changed etc)
        self.ExamplePrintUIEvents(updates)

        # Example on how to handle UI events (button clicked, value changed etc)
        self.ExampleUIElementClicked(updates)

    # This example prints all app functions contained in an AppFunction request (e.g. coming from the App program command)
    def ExamplePrintAppFunctionParameters(self, function):
        print(
            f"App function '{function.name}' called with call ID {function.call_id}, label = '{function.label}', ui hint = '{function.ui_hint}', number of parameters = {len(function.parameters)}"
        )

        # print all parameters
        for parameter in function.parameters:
            if parameter.HasField("bool_value"):
                # boolean
                print(
                    f"\tparameter '{parameter.name}', type 'bool' {parameter.bool_value}"
                )
            elif parameter.HasField("int64_value"):
                # integer
                print(
                    f"\tparameter '{parameter.name}', type 'int64' {parameter.int64_value}"
                )
            elif parameter.HasField("double_value"):
                # double
                print(
                    f"\tparameter '{parameter.name}', type 'double' {parameter.double_value:.2f}"
                )
            elif parameter.HasField("string_value"):
                # string
                print(
                    f"\tparameter '{parameter.name}', type 'string' {parameter.string_value}"
                )
            elif parameter.HasField("vector3_value"):
                # 3 dimensional vector
                print(
                    f"\tparameter '{parameter.name}', type 'vector3' ({parameter.vector3_value.GetX():.2f} {parameter.vector3_value.GetY():.2f} {parameter.vector3_value.GetZ():.2f})"
                )
            elif parameter.HasField("cartesian_value"):
                # cartesian position and orientation
                matrix = Matrix44(parameter.cartesian_value)
                print(
                    f"\tparameter '{parameter.name}', type 'cartesian' X={matrix.GetX():.2f}, Y={matrix.GetY():.2f}, Z={matrix.GetZ():.2f}, A={matrix.GetA():.2f}, B={matrix.GetB():.2f}, C={matrix.GetC():.2f}"
                )

    # This example exponentiates the value of a number variable by a given exponent and assigns the result to a different number variable
    def ExampleExponentiation(self, function):
        # Get the function parameters by iterating over the list
        for parameter in function.parameters:
            if parameter.name == "base_variable" and parameter.HasField("string_value"):
                baseVariableName = parameter.string_value
            elif parameter.name == "result_variable" and parameter.HasField(
                "string_value"
            ):
                resultVariableName = parameter.string_value
            elif parameter.name == "exponent_number" and parameter.HasField(
                "double_value"
            ):
                exponentValue = parameter.double_value

        try:
            # Now request the value of the base number variable from the robot control
            baseVariable = self.GetNumberVariable(baseVariableName)
            baseValue = baseVariable.GetValue()

            # And calculate the result
            resultValue = pow(baseValue, exponentValue)

            # Write the result to the target variable
            self.SetNumber(resultVariableName, resultValue)

            print(
                f'Calculated {baseValue}^{exponentValue} = {resultValue}, result was written to variable "{resultVariableName}"'
            )
        except Exception as ex:
            print(f'Function call "exponentiation" failed', file=sys.stderr)
            print(ex, file=sys.stderr)

    # This example prints all UI events contained in a UI update
    def ExamplePrintUIEvents(self, updates):
        for update in updates:
            if update.state.HasField("button_state"):
                # button clicked
                isClicked = update.state.button_state == ButtonState.CLICKED
                print(
                    f"Button '{update.element_name}' changed: is clicked = {isClicked}"
                )
            elif update.state.HasField("checkbox_state"):
                # checkbox toggled
                isChecked = update.state.checkbox_state == CheckboxState.CHECKED
                print(
                    f"Checkbox '{update.element_name}' changed: is checked = {isChecked}"
                )
            elif update.state.HasField("dropdown_state"):
                # drop down selected
                selectedOption = update.state.dropdown_state.selected_option
                print(
                    f"Dropdown '{update.element_name}' changed: selected option = {selectedOption}"
                )
            elif update.state.HasField("textfield_state"):
                # text box changed
                text = update.state.textfield_state.current_text
                print(f"Text box '{update.element_name}' changed: text = {text}")
            elif update.state.HasField("numberfield_state"):
                # number box changed
                number = update.state.numberfield_state.current_number
                print(f"Number box '{update.element_name}' changed: value = {number}")
            elif update.state.HasField("image_state"):
                # image clicked
                if update.state.image_state.HasField("clicked_at"):
                    x = update.state.image_state.clicked_at.X()
                    y = update.state.image_state.clicked_at.X()
                    isClicked = update.state.image_state.clicked_at.is_clicked
                    if isClicked:
                        print(
                            f"Image clicked '{update.element_name}': x = {x:.3f}, y = {y:.3f}"
                        )

    # Counting variable for ExampleUIElementClicked()
    _examplePlusMinusValue = 0

    # This example handles the plus/minus buttons to increase a text element in the app UI
    def ExampleUIElementClicked(self, updates):
        for update in updates:
            # The following sample will increase/decrease a value if the plus/minus button is pressed and send it back to the UI.
            if update.element_name == "buttonMinus":  # button minus pressed
                self._examplePlusMinusValue -= 1
                print(f"Decreasing UI number to {self._examplePlusMinusValue:.0f}")
                self.SetNumber("textLeftRight", self._examplePlusMinusValue)
            elif update.element_name == "buttonPlus":  # button plus pressed
                self._examplePlusMinusValue += 1
                print(f"Increasing UI number to {self._examplePlusMinusValue:.0f}")
                self.SetNumber("textLeftRight", self._examplePlusMinusValue)
