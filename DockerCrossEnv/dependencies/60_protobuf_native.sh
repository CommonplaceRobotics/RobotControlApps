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

# nativ
mkdir out_native
cd out_native
cmake -DBUILD_TESTING=OFF -Dprotobuf_BUILD_TESTS=OFF ..
make -j 8
make install
cd ..
