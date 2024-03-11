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
cmake -DgRPC_BUILD_CSHARP_EXT=OFF -DgRPC_BUILD_GRPC_CSHARP_PLUGIN=OFF -DgRPC_BUILD_GRPC_NODE_PLUGIN=OFF -DgRPC_BUILD_GRPC_OBJECTIVE_C_PLUGIN=OFF -DgRPC_BUILD_GRPC_PHP_PLUGIN=OFF -DgRPC_BUILD_GRPC_RUBY_PLUGIN=OFF -DgRPC_ZLIB_PROVIDER=package -DgRPC_PROTOBUF_PROVIDER=package ..
make -j 8
make install
