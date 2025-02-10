#include <exception>
#include <iostream>

#include "MonitorApp.h"

/**
 * @brief Main function
 * @param argc argument count
 * @param argv argument vector
 * @return
 */
int main(int argc, char* argv[])
{
    std::cout << "Starting monitor app example" << std::endl;

    // the first command line argument (if given) is the connection target
    std::string connectionTarget = "localhost:5000";
    if (argc > 1) connectionTarget = argv[1];

    // initialize the app
    MonitorApp app(connectionTarget);

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

            // Request robot state updates manually (remove app.StartRobotStateStream() above!)
            app.UpdateRobotState();

            // Run some examples every few seconds
            auto now = std::chrono::steady_clock::now();
            if (now - lastUpdate > std::chrono::seconds(5))
            {
                lastUpdate = now;

                app.UpdateSystemInfo();
            }
        }
    }
    catch (std::exception& ex)
    {
        std::cerr << "Exception: " << ex.what() << std::endl;
        return -1;
    }

    std::cout << "Monitor app example stopped" << std::endl;
    return 0;
}
