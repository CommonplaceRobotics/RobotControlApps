FROM ubuntu:22.04 AS robotcontrolappcrossenv

LABEL maintainer="support@cpr-robots.com"
LABEL version="0.1"
LABEL description="RobotControl C++ app development environment"

#ENV ROBOTCONTROL_PATH=/RobotControl
#ENV TZ=Europe/Berlin
#RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get -y update && apt-get -y upgrade
RUN apt-get -y install cmake git g++ libz-dev zip xz-utils

# Crossbuild
COPY crossbuild_environment.tar.xz "/"
RUN mkdir -p "/opt"
RUN tar -vxf crossbuild_environment.tar.xz --directory=/opt
RUN rm /crossbuild_environment.tar.xz

# The toolchain file in crossbuild_environment has some incorrect values
COPY toolchain-raspberrypi.cmake /opt/toolchains/toolchain-raspberrypi.cmake

# Build and install dependencies for RPi
COPY dependencies /opt/dependencies
RUN /opt/dependencies/01_zlib.sh
# Uncomment this if you need OpenSSL
#RUN /opt/dependencies/02_openssl.sh
RUN /opt/dependencies/06_protobuf.sh
RUN /opt/dependencies/07_grpc.sh
# Uncomment this if you need OpenCV
#RUN /opt/dependencies/08_opencv.sh
