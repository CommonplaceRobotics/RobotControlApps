#!/bin/bash

builddir=~/build_dependencies
mkdir $builddir

echo "Building OpenCV..."

# OpenCV-Contrib (modules with instable API): for the vision app
cd $builddir
git clone -b 4.7.0 --depth 1 https://github.com/opencv/opencv_contrib.git

# OpenCV: for the vision app
cd $builddir
git clone -b 4.7.0 --depth 1 https://github.com/opencv/opencv.git
cd opencv
git checkout -- 3rdparty modules

# RPi
cd opencv
# Workaround: PATH_MAX is not defined
ittnotifyfile=3rdparty/ittnotify/src/ittnotify/ittnotify_static.c
sed "s/#include <limits.h>/#include <linux\/limits.h>/g" $ittnotifyfile > ${ittnotifyfile}2
mv ${ittnotifyfile}2 $ittnotifyfile
obsensorfile=modules/videoio/src/cap_obsensor/obsensor_stream_channel_v4l2.cpp
sed "s/#include <errno/#include <linux\/limits.h>\n#include <errno/" $obsensorfile > ${obsensorfile}2
mv ${obsensorfile}2 $obsensorfile
mkdir out_rpi
cd out_rpi
cmake -DBUILD_ZLIB=ON -DBUILD_TESTS=OFF -DBUILD_PERF_TESTS=OFF -DBUILD_JPEG=ON -DOPENCV_EXTRA_MODULES_PATH=$builddir/opencv_contrib/modules -DCMAKE_TOOLCHAIN_FILE=/opt/toolchains/toolchain-raspberrypi.cmake ..
make clean
make -j 8
make install