FROM ubuntu:22.04 AS robotcontrolappcrossenv

LABEL maintainer="support@cpr-robots.com"
LABEL version="0.1"
LABEL description="RobotControl C++ app development environment"

#ENV ROBOTCONTROL_PATH=/RobotControl
#ENV TZ=Europe/Berlin
#RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get -y update && apt-get -y upgrade
RUN apt-get -y install make cmake git g++ libz-dev zip xz-utils wget

# Crossbuild
COPY crossbuild_environment.tar.xz "/"
RUN mkdir -p "/opt"
RUN tar -vxf crossbuild_environment.tar.xz --directory=/opt
RUN rm /crossbuild_environment.tar.xz

# The toolchain file in crossbuild_environment has some incorrect values
COPY toolchain-raspberrypi.cmake /opt/toolchains/toolchain-raspberrypi.cmake

# Build and install dependencies for RPi
COPY dependencies /opt/dependencies
RUN chmod +x /opt/dependencies/*.sh
RUN /opt/dependencies/01_system_fixes.sh
RUN /opt/dependencies/10_zlib_rpi.sh
RUN /opt/dependencies/20_openssl_rpi.sh
RUN /opt/dependencies/60_protobuf_native.sh
RUN /opt/dependencies/60_protobuf_rpi.sh
RUN /opt/dependencies/70_grpc_native.sh
RUN /opt/dependencies/70_grpc_rpi.sh
# Uncomment this if you need OpenCV
#RUN /opt/dependencies/80_opencv.sh
