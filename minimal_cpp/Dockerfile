# TODOs for creating your own app:
# - Change the installation directory name in line "ENV APP_DIR_NAME=..."
# - Change all instances of "minimalapp" to the name of your apps binary
# - Add any additional files to both "RUN cp..." lines
#
# Run the following command to build the app and export the zip file
# docker build . --output type=local,dest=output

FROM ubuntu:26.04 AS base

LABEL maintainer="support@cpr-robots.com"
LABEL version="0.1"
LABEL description="RobotControl Minimal C++ app build environment"

ARG DEBIAN_FRONTEND=noninteractive

# Enter the name of the directory that the app will be installed to. This must be a unique name (e.g. the apps name) and must not contain spaces, slashes or any other characters that are invalid for paths.
ENV APP_DIR_NAME=minimalapp

RUN apt-get -y update && apt-get -y upgrade
RUN apt-get -y install make cmake git g++ zip xz-utils wget python3 python3-venv

# Set up Conan in Python venv
RUN python3 -m venv ~/.conan_venv
RUN source ~/.conan_venv/bin/activate && python3 -m pip install conan

# Prepare Crossbuild
RUN mkdir -p /opt/gcc
RUN cd /opt/gcc && wget --quiet https://downloads.cpr-robots.com/Software/CI/gcc_armv8-rpi4-linux-gnueabihf.tar.gz
RUN cd /opt/gcc && tar -xf gcc_armv8-rpi4-linux-gnueabihf.tar.gz


###############################################################################
# Building for Raspberry Pi
###############################################################################
FROM base AS rpi_build

# Copy app code to Docker image
COPY . /app

# Build dependencies
WORKDIR /app
RUN source ~/.conan_venv/bin/activate && conan install . --lockfile-partial --build=missing --profile:host=cpr_linux_rpi4_gcc10_release --profile:build=cpr_linux_x86_64_release -c tools.cmake.cmake_layout:build_folder_vars="['settings.os', 'settings.arch']"

# Clearing unused dependencies
RUN source ~/.conan_venv/bin/activate && conan remove --lru=12w "*"

# Build for Raspberry Pi
WORKDIR /app/out_rpi
RUN cmake -DBUILD_TESTS=OFF -DCMAKE_TOOLCHAIN_FILE=/opt/toolchains/toolchain-raspberrypi.cmake ..
RUN cmake --build .

RUN rm -f CMakePresets.json
RUN echo "{\"version\": 4,\"include\":[\"out/conan/Linux/armv8_32/Release/generators/CMakePresets.json\"]}" >> CMakePresets.json
RUN cmake --preset conan-linux-armv8_32-release .

WORKDIR minimal_cpp/out/build/Linux/armv8_32/Release
RUN cmake --build . --target minimalapp

# Create zip package
WORKDIR /app/package
RUN mkdir $APP_DIR_NAME
# Copy files. Add any additional files your app needs.
RUN cp ../Licenses_SampleApps.pdf ../rcapp.xml ../ui.xml ../out_rpi/minimalapp $APP_DIR_NAME
RUN zip -r package.zip $APP_DIR_NAME


###############################################################################
# Copy results to export stage. These files are copied to the output directory.
###############################################################################
FROM scratch AS export
COPY --from=rpi_build /app/package/package.zip /minimalapp_rpi.zip
