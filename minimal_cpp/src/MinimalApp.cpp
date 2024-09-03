#include "MinimalApp.h"

#include <math.h>
#include <sstream>

#include "DataTypes/Matrix44.h"

/**
 * Below you will find examples on how to handle requests from the robot control (e.g. user interface and program commands)
 * Also check main.cpp for examples on how to send requests from the app to the robot control.
 */

/**
 * @brief Constructor
 * @param target connection target in the following format: "hostname:port" or "ip:port", e.g. "localhost:5000"
 */
MinimalApp::MinimalApp(const std::string& target) : AppClient(std::string(APP_NAME), target) {}

/**
 * @brief Gets called on remote app function calls received from the robot control
 * @param function app function data
 */
void MinimalApp::AppFunctionHandler(const robotcontrolapp::AppFunction& function)
{
    // Select the app function to call
    if (function.name() == "pow")
    {
        ExampleExponentiation(function);
    }
    else
    {
        // Example on how to handle app functions (these are called by the program command "App")
        ExamplePrintAppFunctionParameters(function);
    }

    // Confirm that the function finished, otherwise the robot program will wait forever.
    // You may send this later if the function call takes some time but it must be sent at some point.
    SendFunctionDone(function.call_id());
	// Or call this in case the function failed. This stops the robot program.
	// SendFunctionFailed(function.call_id(), "failure reason");
}

/**
 * @brief Gets called on remote UI update requests received from the robot control
 * @param updates updated UI elements. Key is the element name, value contains the changes.
 */
void MinimalApp::UiUpdateHandler(const std::map<std::string, const robotcontrolapp::AppUIElement*>& updates)
{
    // Example on how to handle UI events (button clicked, value changed etc)
    ExamplePrintUIEvents(updates);

    // Example on how to handle UI events (button clicked, value changed etc)
    ExampleUIElementClicked(updates);
}

/**
 * @brief This example prints all app functions contained in an AppFunction request (e.g. coming from the App program command)
 * @param function
 */
void MinimalApp::ExamplePrintAppFunctionParameters(const robotcontrolapp::AppFunction& function) const
{
    std::cout << "App function '" << function.name() << "' called with call ID " << function.call_id() << ", label = '" << function.label() << "', ui hint = '"
              << function.ui_hint() << "', number of parameters = " << function.parameters_size() << std::endl;

    // print all parameters
    for (int i = 0; i < function.parameters_size(); i++)
    {
        const robotcontrolapp::AppFunction_Parameter& parameter = function.parameters().Get(i);
        std::ostringstream value;
        std::string typeStr;
        switch (parameter.value_case())
        {
            case robotcontrolapp::AppFunction_Parameter::kBoolValue:
                // boolean
                typeStr = "bool";
                value << (parameter.bool_value() ? "true" : "false");
                break;
            case robotcontrolapp::AppFunction_Parameter::kInt64Value:
                // integer
                typeStr = "int";
                value << parameter.int64_value();
                break;
            case robotcontrolapp::AppFunction_Parameter::kDoubleValue:
                // double
                typeStr = "double";
                value << parameter.double_value();
                break;
            case robotcontrolapp::AppFunction_Parameter::kStringValue:
                // string
                typeStr = "string";
                value << parameter.string_value();
                break;
            case robotcontrolapp::AppFunction_Parameter::kVector3Value:
                // 3 dimensional vector
                typeStr = "vector";
                value << "(" << parameter.vector3_value().x() << ", " << parameter.vector3_value().y() << ", " << parameter.vector3_value().z() << ")";
                break;
            case robotcontrolapp::AppFunction_Parameter::kCartesianValue:
                // cartesian position and orientation
                {
                    typeStr = "cartesian";
                    // read the values into a matrix, this allows easy access to the cartesian position and orientation
                    App::DataTypes::Matrix44 matrix(parameter.cartesian_value());
                    value << "X=" << matrix.GetX() << ", Y=" << matrix.GetY() << ", Z=" << matrix.GetZ() << ", A=" << matrix.GetA() << ", B=" << matrix.GetB()
                          << ", C=" << matrix.GetC();
                }
                break;
            default:
                break;
        }

        std::cout << "\tparameter '" << parameter.name() << "', type '" << typeStr << "', value '" << value.str() << "'" << std::endl;
    }
}

/**
 * @brief This example exponentiates the value of a number variable by a given exponent and assigns the result to a different number variable
 * @param function function parameters
 */
void MinimalApp::ExampleExponentiation(const robotcontrolapp::AppFunction& function)
{
    std::string baseVariableName;
    std::string resultVariableName;
    double exponentValue = 1;

    bool hasBaseVariable = false, hasResultVariable = false, hasExponent = false;

    // Get the function parameters by iterating over the list
    for (int i = 0; i < function.parameters_size(); i++)
    {
        const robotcontrolapp::AppFunction_Parameter& parameter = function.parameters().Get(i);

        // check parameter name and type
        if (parameter.name() == "base_variable" && parameter.value_case() == robotcontrolapp::AppFunction_Parameter::kStringValue)
        {
            baseVariableName = parameter.string_value();
            hasBaseVariable = true;
        }
        else if (parameter.name() == "result_variable" && parameter.value_case() == robotcontrolapp::AppFunction_Parameter::kStringValue)
        {
            resultVariableName = parameter.string_value();
            hasResultVariable = true;
        }
        else if (parameter.name() == "exponent_number" && parameter.value_case() == robotcontrolapp::AppFunction_Parameter::kDoubleValue)
        {
            exponentValue = parameter.double_value();
            hasExponent = true;
        }
    }

    // Check whether all parameters were received
    if (!hasBaseVariable || !hasResultVariable || !hasExponent)
    {
        std::cerr << "Function call \"exponentiation\" failed: incomplete function parameters!" << std::endl;
        return;
    }

    try
    {
        // Now request the value of the base number variable from the robot control
        std::shared_ptr<App::DataTypes::NumberVariable> baseVariable = GetNumberVariable(baseVariableName);
        double baseValue = baseVariable->GetValue();

        // And calculate the result
        double resultValue = pow(baseValue, exponentValue);

        // Write the result to the target variable
        SetNumber(resultVariableName, resultValue);

        // Do some debug output if you like
        std::cout << "Calculated " << baseValue << "^" << exponentValue << " = " << resultValue << ", result was written to variable \"" << resultVariableName
                  << "\"" << std::endl;
    }
    catch (std::exception& ex)
    {
        // Make sure to catch exceptions, e.g. when the variable does not exist!
        std::cerr << "Function call \"exponentiation\" failed: " << ex.what() << std::endl;
    }
}

/**
 * @brief This example prints all UI events contained in a UI update
 * @param updates UI updates
 */
void MinimalApp::ExamplePrintUIEvents(const std::map<std::string, const robotcontrolapp::AppUIElement*>& updates) const
{
    for (auto& update : updates)
    {
        switch (update.second->state().state_case())
        {
            case robotcontrolapp::AppUIElement::AppUIState::kButtonState:
                // button clicked
                {
                    bool isClicked = update.second->state().button_state() == robotcontrolapp::ButtonState::CLICKED;
                    std::cout << "Button '" << update.first << "' changed: is clicked = " << isClicked << std::endl;
                }
                break;
            case robotcontrolapp::AppUIElement::AppUIState::kCheckboxState:
                // checkbox toggled
                {
                    bool isChecked = update.second->state().checkbox_state() == robotcontrolapp::CheckboxState::CHECKED;
                    std::cout << "Checkbox '" << update.first << "' changed: is checked = " << isChecked << std::endl;
                }
                break;
            case robotcontrolapp::AppUIElement::AppUIState::kDropdownState:
                // drop down selected
                {
                    const std::string& selectedOption = update.second->state().dropdown_state().selected_option();
                    std::cout << "Dropdown '" << update.first << "' changed: selected option = " << selectedOption << std::endl;
                }
                break;
            case robotcontrolapp::AppUIElement::AppUIState::kImageState:
                // image clicked
                if (update.second->state().image_state().has_clicked_at())
                {
                    double x = update.second->state().image_state().clicked_at().x();
                    double y = update.second->state().image_state().clicked_at().y();
                    bool isClicked = update.second->state().image_state().clicked_at().is_clicked();
                    if (isClicked)
                    {
                        std::cout << "Image clicked '" << update.first << "': x = " << x << ", y = " << y << std::endl;
                    }
                }
                break;
            case robotcontrolapp::AppUIElement::AppUIState::kNumberfieldState:
                // number box changed
                {
                    double value = update.second->state().numberfield_state().current_number();
                    std::cout << "Number box '" << update.first << "' changed: value = " << value << std::endl;
                }
                break;
            case robotcontrolapp::AppUIElement::AppUIState::kTextfieldState:
                // text box changed
                {
                    const std::string& text = update.second->state().textfield_state().current_text();
                    std::cout << "Text box '" << update.first << "' changed: text = " << text << std::endl;
                }
                break;
            default:
                std::cerr << "Got UI update for UI element '" << update.first << "' with unknown type" << std::endl;
                break;
        }
    }
}

/**
 * @brief This example handles the plus/minus buttons to increase a text element in the app UI
 * @param updates UI updates
 */
void MinimalApp::ExampleUIElementClicked(const std::map<std::string, const robotcontrolapp::AppUIElement*>& updates)
{
    for (auto& update : updates)
    {
        // The following sample will increase/decrease a value if the plus/minus button is pressed and send it back to the UI.
        if (update.second->state().state_case() == robotcontrolapp::AppUIElement::AppUIState::kButtonState)
        {
            if (update.first == "buttonMinus") // button minus pressed
            {
                m_ExamplePlusMinusValue--;
                std::cout << "Decreasing UI number to " << m_ExamplePlusMinusValue << std::endl;
                SetNumber("textLeftRight", m_ExamplePlusMinusValue);
            }
            else if (update.first == "buttonPlus") // button plus pressed
            {
                m_ExamplePlusMinusValue++;
                std::cout << "Increasing UI number to " << m_ExamplePlusMinusValue << std::endl;
                SetNumber("textLeftRight", m_ExamplePlusMinusValue);
            }
        }
    }
}
