# Cross Build Environment
Building C++ apps for the embedded robot control requires a cross build environment. The files in this directory can be used to generate a cross building environment for Raspberry Pi and Ubuntu. See the [building C++ apps guide](../minimal_cpp/BUILDING.md) file in minimal_cpp for a guide. Building apps for the simulation on Windows can be done with any compiler, e.g. MSVC (Visual Studio) or MinGW.

Linux apps can be build on Ubuntu (native or in WSL), but to simplify this we prepared a docker environment. The following sections explain how to set it up.

## Building the Docker image

1. Install [Docker Desktop](https://www.docker.com/).
2. Download this repository to your PC via git or as a zip file.
3. Create a Docker image containing the build environment using one of the following sections.

### Using the prebuilt image
We recommend using the prebuilt image to save time and disk space. This contains compiled libraries for Raspberry Pi, only some libraries for the Ubuntu system need to be build. This takes about 18 minutes.

[Download our prebuilt build environment](https://cpr-robots.com/download/embedded-computer/crossbuild_environment_prebuilt.tar.xz) (ca. 650MB, 3.8GB extracted) to this directory.

```
docker build . --tag=robotcontrolappcrossenv --file=Dockerfile_Prebuilt
```

### Building the dependencies
Alternatively you can build all libraries. This will take around 45 minutes and takes more disk space. If you only want to rebuild some libraries consider editing the prebuilt Dockerfile.

[Download our base build environment](https://cpr-robots.com/download/embedded-computer/crossbuild_environment.tar.xz) (ca. 1.9GB, 13GB extracted) to this directory.

```
docker build . --tag=robotcontrolappcrossenv
```

### Building the prebuilt image
The following command builds all libraries and creates the prebuilt image. You should not need this command. Building this takes ca. 90 minutes.

[Download our base build environment](https://cpr-robots.com/download/embedded-computer/crossbuild_environment.tar.xz) (ca. 1.9GB, 13GB extracted) to this directory.

```
docker build . --tag=robotcontrolappcrossenv --file=Dockerfile_Image --output type=local,dest=output
```

## Building in WSL or native Ubuntu

We currently can not provide support for but this approach but it may be useful for debugging. If you do this you should install a Ubuntu 22.04.2 (since this is tested by us). Download the base environment image and and follow the steps in the Dockerfile.

# Adding libraries

If your app needs additional libraries you may want to add them to the build environment image. Rebuilding it may take more time than building the libraries with your app but it may save some time when the build environment image is reused.

The following section calls several scripts that build libraries from source code for Raspberry Pi and Ubuntu (you can install libraries for Ubuntu using apt but Raspberry Pi libraries need to be compiled with our toolchain).
```
# Build and install dependencies for RPi
RUN mkdir -p "/dependencies"
COPY dependencies /dependencies
RUN chmod +x /dependencies/*.sh
RUN /dependencies/01_system_fixes.sh
RUN /dependencies/10_zlib_rpi.sh
RUN /dependencies/20_openssl_rpi.sh
RUN /dependencies/60_protobuf_native.sh
RUN /dependencies/60_protobuf_rpi.sh
RUN /dependencies/70_grpc_native.sh
RUN /dependencies/70_grpc_rpi.sh
# Uncomment this if you need OpenCV
#RUN /dependencies/80_opencv_rpi.sh
```

Take a look at the script files, you should be able to add most libraries in a similar way. Additional non-static libraries must be manually installed to each robot control that runs your app. Copy the ```.so``` files to ```/lib``` and run ```ldconfig``` to install them.