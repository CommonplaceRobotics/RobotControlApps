#!/bin/bash

builddir=~/build_dependencies
mkdir $builddir


# zlib: optional
echo "Building zlib..."
cd $builddir
git clone -b v1.2.13 --depth 1 https://github.com/madler/zlib.git
cd zlib
# RPi
mkdir out_rpi
cd out_rpi
cmake -DCMAKE_TOOLCHAIN_FILE=/opt/toolchains/toolchain-raspberrypi.cmake ..
make -j 8
make install
