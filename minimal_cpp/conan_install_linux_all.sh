#!/bin/bash
# Builds the dependencies and toolchain via conan. This must be called before using CMake.

./conan_install_linux_native.sh
./conan_install_linux_rpi.sh