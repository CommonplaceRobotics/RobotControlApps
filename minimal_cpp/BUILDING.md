# Building apps
This guide explains how to compile C++ apps for Windows, Ubuntu and Raspberry Pi (embedded robot control).

## Windows
Building apps to run on Windows is mainly intended for simulating and testing.

You will need the vcpkg, it automatically downloads and builds the dependencies (as defined in ```vcpkg.json```). Follow [the guide on the vcpkg website](https://vcpkg.io/en/getting-started) to install it. When building with cmake you will need to pass the vcpkg toolchain file als shown in the guide.

You should be able to use cmake with any supported build system on Windows, however we recommend and only support building with Visual Studio and MSVC since that is what we use.

Open the minimal_cpp folder with Visual Studio. It should recognize it as a CMake project and may ask about installing CMake support. When loading the folder for the first time you will need to set the vcpkg toolchain. To do that open the CMake settings in Visual Studio (configurations drop down box in the tool bar -> "Manage Configurations..."). Set up a configuration for Windows and set the entry for "CMake toolchain file" to ```\<YourPathTo>/vcpkg/scripts/buildsystems/vcpkg.cmake```.

Open the Project menu to configure the CMake cache. When doing this for the first time this will take a while (gRPC takes ~30min, possibly more, to compile). In our experience it occasionally needs to recompile but since the gRPC version is locked this should be rare.

Then compile and run the app.

## Ubuntu 22.04 and Raspberry Pi cross compilation using Docker
We recommend using Docker to build your apps. Docker uses containers to install dependencies and execute commands reproducibly without changes to your system. We prepared a Docker environment with all necessary tools and libraries so that you do not need to install any yourself and so that you are using compatible versions.

### Setup
Before you can build your app you will need to set up the build environment docker image as explained in [DockerCrossEnv/README.md](../DockerCrossEnv/README.md).

### Building your app
5. Open a command line or PowerShell in the minimal_cpp folder and run the following command to build the app:
    ```
    docker build . --tag=minimal --output type=local,dest=output
    ```
    This builds the app for both Raspberry Pi and Ubuntu and creates zip archives with all relevant files. The output files are copied to the ```output``` folder.
    If this step fails with ```ERROR: failed to solve: robotcontrolappcrossenv: pull access denied[...]``` either the previous step failed or Docker does not find the previously built image at the tag ```robotcontrolappcrossenv``` for some reason.
6. Execute the following command to run your app in Docker. This may be useful for quick tests while developing. Alternatively you can install the app zip file at the robot control and run it there.
    ```
    TODO
    ```
    You will need to do the following changes so it is able to connect:
    * Set the IP address of your robot in ```src/main.cpp```. You may keep it at ```localhost``` if you are testing with a simulation.
    * You need to install the app at the robot control or simulation. You likely want to remove the exectutable tag in ```rcapp.xml``` so that the robot control registers the app without trying to start any binary itself.

### Changing the Docker files for your own app
The ```Dockerfile``` in the app directory defines the commands that are called to build and package your app.

The following two build your app. This should be fine for most apps but you may want to extend it for specific cmake setups.
```
# Build for Raspberry Pi
WORKDIR /app/out_rpi
RUN cmake -DCMAKE_TOOLCHAIN_FILE=/opt/toolchains/toolchain-raspberrypi.cmake ..
RUN cmake --build .
```

The next section collects all files that need to be added to the app zip file. You may want to add further files. Change the zip file name to the name of your app.
```
# package
WORKDIR /app/package
RUN cp ../Licenses_MinimalApp.pdf .
RUN cp ../rcapp.xml .
RUN cp ../ui.xml .
RUN cp ../out_rpi/minimalapp .
RUN zip minimalapp *
```

This is followed by another set of the same commands for building for a native linux system. You can commend the entire section from ```FROM build AS native``` to (excluding) ```FROM scratch AS export``` to build roughly twice as fast, however you will not be able to run your app from Docker anymore.

The last section defines the files that are copied to your PC if you build the Docker image with the ```--output``` parameter. Change minimalapp to the name of your app. If you remove the native build section as explained above you will also need to remove or comment the native copy commands here.
```
# Copy results to export stage. These files are copied to the output directory.
FROM scratch AS export
COPY --from=rpi /app/out_rpi/minimalapp /minimalapp_rpi
COPY --from=rpi /app/package/minimalapp.zip /minimalapp_rpi.zip
COPY --from=native /app/out_native/minimalapp /minimalapp_native
COPY --from=native /app/package/minimalapp.zip /minimalapp_native.zip
```

### Working with Visual Studio Code
While we have not tried this much Visual Studio Code seems to have a good integration for building with Docker. If you installed the Docker plugin you can do a right click at the Dockerfile in the files list and click "Build Image..." to build your app. In the default configuration VS Code asks Docker to pull the cross build environment image from the internet which will fail (with the error mentioned above at step 5). To fix this open the settings, copy ```docker.commands.build``` into the settings search bar, it should show ```Docker > Command: Build```. Click ```Edit in settings.json``` and remove ```--pull``` from the build command.
