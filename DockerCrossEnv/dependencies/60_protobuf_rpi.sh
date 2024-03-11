#!/bin/bash

builddir=~/build_dependencies
mkdir $builddir


# protobuf: required for gRPC
echo "Building protobuf..."
cd $builddir
git clone -b v21.6 --depth 1 https://github.com/protocolbuffers/protobuf
cd protobuf
git submodule update --init
symbolizefile=${builddir}/protobuf/third_party/abseil-cpp/absl/debugging/symbolize_elf.inc
cd $builddir/protobuf/third_party/abseil-cpp/
git checkout -- $symbolizefile
cd $builddir/protobuf

# RPi
mkdir out_rpi
cd out_rpi
# Workaround: SSIZE_MAX is not defined
sed "s/SSIZE_MAX/(SIZE_MAX>>1)/g" $symbolizefile > ${symbolizefile}2
mv ${symbolizefile}2 $symbolizefile
cmake -DBUILD_TESTING=OFF -Dprotobuf_BUILD_PROTOC_BINARIES=OFF -Dprotobuf_BUILD_TESTS=OFF -DCMAKE_TOOLCHAIN_FILE=/opt/toolchains/toolchain-raspberrypi.cmake ..
make -j 8
make install