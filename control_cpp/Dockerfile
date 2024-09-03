FROM robotcontrolappcrossenv AS build

LABEL maintainer="support@cpr-robots.com"
LABEL version="0.1"
LABEL description="RobotControl Control app build environment"

# Copy app code to Docker image
COPY . /app


FROM build AS rpi
# Build for Raspberry Pi
WORKDIR /app/out_rpi
RUN cmake -DBUILD_TESTS=OFF -DCMAKE_TOOLCHAIN_FILE=/opt/toolchains/toolchain-raspberrypi.cmake ..
RUN cmake --build .

# package
WORKDIR /app/package
RUN cp ../Licenses_SampleApps.pdf ../rcapp.xml ../ui.xml ../out_rpi/controlapp ../SampleProgram.xml .
RUN zip controlapp *


FROM build AS native
# Build for Linux x86_64
WORKDIR /app/out_native
RUN cmake ..
# Alternatively you can disable tests for to build faster
#RUN cmake -DBUILD_TESTS=OFF ..
RUN cmake --build .

# Command to run
CMD ./controlapp

# package
WORKDIR /app/package
RUN cp ../Licenses_SampleApps.pdf ../rcapp.xml ../ui.xml ../out_native/controlapp ../SampleProgram.xml .
RUN zip controlapp *


# Copy results to export stage. These files are copied to the output directory.
FROM scratch AS export
COPY --from=rpi /app/out_rpi/controlapp /controlapp_rpi
COPY --from=rpi /app/package/controlapp.zip /controlapp_rpi.zip
COPY --from=native /app/out_native/controlapp /controlapp_native
COPY --from=native /app/package/controlapp.zip /controlapp_native.zip
