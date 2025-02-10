#include <exception>
#include <iostream>

#include "MinimalApp.h"

/**
 * Below you will find examples for sending requests from the app to the robot control.
 * Also check MinimalApp.cpp for examples on how to handle requests from the robot control (e.g. user interface and program commands)
 */

/**
 * @brief Example: Requests and prints the tool center point (cartesian) position.
 * @param app reference to the app client
 */
void ExamplePrintTCP(App::AppClient& app)
{
    try
    {
        App::DataTypes::Matrix44 tcp = app.GetTCP();
        std::cout << std::fixed << "TCP: X=" << tcp.GetX() << " Y=" << tcp.GetY() << " Z=" << tcp.GetZ() << " A=" << tcp.GetA() << " B=" << tcp.GetB()
                  << " C=" << tcp.GetC() << std::endl;
    }
    catch (std::exception& ex)
    {
        std::cerr << "TCP: exception occured: " << ex.what() << std::endl;
    }
}

/**
 * @brief Example: Requests and prints a number variable. This variable must be defined in a m_running robot program.
 * @param app reference to the app client
 * @param variableName name of the variable
 * @return value of the variable or 0
 */
double ExamplePrintNumberVariable(App::AppClient& app, const std::string& variableName)
{
    try
    {
        std::shared_ptr<App::DataTypes::NumberVariable> numberVariable = app.GetNumberVariable(variableName);
        std::cout << std::fixed << "Program variable \"" << variableName << "\": " << numberVariable->GetValue() << std::endl;
        return numberVariable->GetValue();
    }
    catch (std::exception& ex)
    {
        std::cerr << "Could not get number variable \"" << variableName << "\": " << ex.what()
                  << " - for this example please start the a program that defines this variable" << std::endl;
    }
    return 0;
}

/**
 * @brief Example: Sets a number variable. The value increases with each call.
 * @param app reference to the app client
 * @param variableName name of the variable
 */
void ExampleSetNumberVariable(App::AppClient& app, const std::string variableName, double value)
{
    try
    {
        app.SetNumberVariable(variableName, value);
    }
    catch (std::exception& ex)
    {
        std::cerr << "Could not set number variable \"" << variableName << "\": " << ex.what()
                  << " - for this example please start the a program that defines this variable" << std::endl;
    }
}

/**
 * @brief Example: Requests and prints a position variable. This variable must be defined in a m_running robot program.
 * @param app reference to the app client
 * @param variableName name of the variable
 */
void ExamplePrintPositionVariable(App::AppClient& app, const std::string& variableName)
{
    try
    {
        std::shared_ptr<App::DataTypes::PositionVariable> positionVariable = app.GetPositionVariable(variableName);
        std::cout << std::fixed << "Position variable \"" << variableName << "\" cart: X=" << positionVariable->GetCartesian().GetX()
                  << " Y=" << positionVariable->GetCartesian().GetY() << " Z=" << positionVariable->GetCartesian().GetZ()
                  << " A=" << positionVariable->GetCartesian().GetA() << " B=" << positionVariable->GetCartesian().GetB()
                  << " C=" << positionVariable->GetCartesian().GetC() << std::endl;
        std::cout << std::fixed << "Position variable \"" << variableName << "\" joint:";
        for (size_t i = 0; i < positionVariable->GetRobotAxes().size(); i++)
        {
            std::cout << " A" << (i + 1) << "=" << positionVariable->GetRobotAxes().at(i);
        }
        for (size_t i = 0; i < positionVariable->GetExternalAxes().size(); i++)
        {
            std::cout << " E" << (i + 1) << "=" << positionVariable->GetExternalAxes().at(i);
        }
        std::cout << std::endl;
    }
    catch (std::exception& ex)
    {
        std::cerr << "Could not get position variable \"" << variableName << "\": " << ex.what()
                  << " - for this example please start the a program that defines this variable" << std::endl;
    }
}

/**
 * @brief This example reads the current position from variable #position and writes it back to variable "mycurrentposition"
 * @param app app reference to the app client
 */
void ExampleReadWritePositionVariable(App::AppClient& app)
{
    try
    {
        std::shared_ptr<App::DataTypes::PositionVariable> positionVariable = app.GetPositionVariable("#position");
        app.SetPositionVariable("mycurrentposition", positionVariable->GetCartesian(), positionVariable->GetRobotAxes()[0], positionVariable->GetRobotAxes()[1],
                            positionVariable->GetRobotAxes()[2], positionVariable->GetRobotAxes()[3], positionVariable->GetRobotAxes()[4],
                            positionVariable->GetRobotAxes()[5], positionVariable->GetExternalAxes()[0], positionVariable->GetExternalAxes()[1],
                            positionVariable->GetExternalAxes()[2]);
    }
    catch (std::exception& ex)
    {
        std::cerr << "Could not get position variable \"#position\" or set \"mycurrentposition\": " << ex.what();
    }
}

/**
 * @brief Main function
 * @param argc argument count
 * @param argv argument vector
 * @return
 */
int main(int argc, char* argv[])
{
    std::cout << "Starting minimal app example" << std::endl;

    // the first command line argument (if given) is the connection target
    std::string connectionTarget = "localhost:5000";
    if (argc > 1) connectionTarget = argv[1];

    // initialize the app
    MinimalApp app(connectionTarget);

    try
    {
        // connect to the robot control
        app.Connect();

        // time of the last example run
        std::chrono::steady_clock::time_point lastUpdate = std::chrono::steady_clock::now() - std::chrono::seconds(60);

        // wait forever or do things
        while (app.IsConnected())
        {
            std::this_thread::sleep_for(std::chrono::milliseconds(500));

            // Run some examples every few seconds
            auto now = std::chrono::steady_clock::now();
            if (now - lastUpdate > std::chrono::seconds(10))
            {
                lastUpdate = now;

                ExamplePrintTCP(app);
                ExamplePrintPositionVariable(app, "apppos");
                double value = ExamplePrintNumberVariable(app, "appnum");
                ExampleSetNumberVariable(app, "appnum", value + 1);
                ExampleReadWritePositionVariable(app);
            }
        }
    }
    catch (std::exception& ex)
    {
        std::cerr << "Exception: " << ex.what() << std::endl;
        return -1;
    }

    std::cout << "Minimal app example stopped" << std::endl;
    return 0;
}
