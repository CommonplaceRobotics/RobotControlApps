#!/bin/bash

builddir=~/build_dependencies
mkdir $builddir


# gRPC
echo "Building gRPC..."
cd $builddir
git clone -b v1.52.1 --depth 1 https://github.com/grpc/grpc.git
cd grpc
git submodule update --init
# Reset workarounds
digestfile=${builddir}/grpc/third_party/boringssl-with-bazel/src/tool/digest.cc
protoclifile=${builddir}/grpc/third_party/protobuf/src/google/protobuf/compiler/command_line_interface.cc
symbolizefile=${builddir}/grpc/third_party/abseil-cpp/absl/debugging/symbolize_elf.inc
gethostnamefile=${builddir}/grpc/src/core/lib/iomgr/gethostname_host_name_max.cc
git checkout -- $gethostnamefile
cd $builddir/grpc/third_party/boringssl-with-bazel
git checkout -- $digestfile
cd $builddir/grpc/third_party/protobuf
git checkout -- $protoclifile
cd $builddir/grpc/third_party/abseil-cpp/
git checkout -- $symbolizefile
cd $builddir/grpc
# native
mkdir out_native
cd out_native
cmake -DgRPC_BUILD_TESTS=OFF -DgRPC_BUILD_CSHARP_EXT=OFF -DgRPC_BUILD_GRPC_CSHARP_PLUGIN=OFF -DgRPC_BUILD_GRPC_NODE_PLUGIN=OFF -DgRPC_BUILD_GRPC_OBJECTIVE_C_PLUGIN=OFF -DgRPC_BUILD_GRPC_PHP_PLUGIN=OFF -DgRPC_BUILD_GRPC_RUBY_PLUGIN=OFF ..
make -j 8
make install
cd ..
# RPi
mkdir out_rpi
cd out_rpi
# Workaround: PATH_MAX is not defined
sed "s/#include <limits.h>/#include <linux\/limits.h>/g" $digestfile > ${digestfile}2
mv ${digestfile}2 $digestfile
sed "s/#include <limits.h>/#include <linux\/limits.h>/g" $protoclifile > ${protoclifile}2
mv ${protoclifile}2 $protoclifile
# Workaround: SSIZE_MAX is not defined
sed "s/SSIZE_MAX/(SIZE_MAX>>1)/g" $symbolizefile > ${symbolizefile}2
mv ${symbolizefile}2 $symbolizefile
# Workaround: HOST_NAME_MAX is not defined (something seems wrong in the includes of the toolchain or the build system)
sed "s/HOST_NAME_MAX)/64)/g" $gethostnamefile > ${gethostnamefile}2
mv ${gethostnamefile}2 $gethostnamefile
# compile
cmake -DgRPC_BUILD_TESTS=OFF -DgRPC_BUILD_CSHARP_EXT=OFF -DgRPC_BUILD_GRPC_CSHARP_PLUGIN=OFF -DgRPC_BUILD_GRPC_NODE_PLUGIN=OFF -DgRPC_BUILD_GRPC_OBJECTIVE_C_PLUGIN=OFF -DgRPC_BUILD_GRPC_PHP_PLUGIN=OFF -DgRPC_BUILD_GRPC_RUBY_PLUGIN=OFF -DCMAKE_TOOLCHAIN_FILE=/opt/toolchains/toolchain-raspberrypi.cmake ..
make -j 8
make install
