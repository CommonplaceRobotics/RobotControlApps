# TODOs for creating your own app:
# - Change the installation directory name in line "ENV APP_DIR_NAME=..."
# - Change all instances of "minimalapp" to the name of your apps binary
# - Add any additional files to both "RUN cp..." lines
#
# Run the following command to build the app and export the zip file
# docker build . --output type=local,dest=output

FROM robotcontrolappcrossenv AS build

LABEL maintainer="support@cpr-robots.com"
LABEL version="0.1"
LABEL description="RobotControl Minimal C++ app build environment"

# Enter the name of the directory that the app will be installed to. This must be a unique name (e.g. the apps name) and must not contain spaces, slashes or any other characters that are invalid for paths.
ENV APP_DIR_NAME=minimalapp

# Copy app code to Docker image
COPY . /app


###############################################################################
# Building for Raspberry Pi
###############################################################################
FROM build AS rpi
# Build for Raspberry Pi
WORKDIR /app/out_rpi
RUN cmake -DBUILD_TESTS=OFF -DCMAKE_TOOLCHAIN_FILE=/opt/toolchains/toolchain-raspberrypi.cmake ..
RUN cmake --build .

# Create zip package
WORKDIR /app/package
RUN mkdir $APP_DIR_NAME
# Copy files. Add any additional files your app needs.
RUN cp ../Licenses_SampleApps.pdf ../rcapp.xml ../ui.xml ../out_rpi/minimalapp $APP_DIR_NAME
RUN zip -r package.zip $APP_DIR_NAME


###############################################################################
# Building for x86_64 Linux (for testing)
###############################################################################
FROM build AS native
# Build for Linux x86_64
WORKDIR /app/out_native
RUN cmake ..
# Alternatively you can disable tests to build faster
#RUN cmake -DBUILD_TESTS=OFF ..
RUN cmake --build .

# Command to run
CMD ./minimalapp

# Create zip package
WORKDIR /app/package
RUN mkdir $APP_DIR_NAME
# Copy files. Add any additional files your app needs.
RUN cp ../Licenses_SampleApps.pdf ../rcapp.xml ../ui.xml ../out_native/minimalapp $APP_DIR_NAME
RUN zip -r package $APP_DIR_NAME


###############################################################################
# Copy results to export stage. These files are copied to the output directory.
###############################################################################
FROM scratch AS export
COPY --from=rpi /app/package/package.zip /minimalapp_rpi.zip
# Uncomment to build and export for Linux x86_64:
#COPY --from=native /app/package/package.zip /minimalapp_native.zip
