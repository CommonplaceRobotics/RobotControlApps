#!/bin/bash

builddir=~/build_dependencies
mkdir $builddir


# OpenSSL: required
echo "Building OpenSSL..."
# RPi:
cd $builddir
opensslver=openssl-1.1.0j
# Python requires V1.1.1
# V1.1.1 does not run correctly on the RPi, a symbol is missing (MAB)??
#opensslver=openssl-1.1.1t
wget https://www.openssl.org/source/$opensslver.tar.gz
tar zxf $opensslver.tar.gz
cd $opensslver
# Workaround: OSSL_SSIZE_MAX is not found, SSIZE_MAX neither. (SIZE_MAX>>1) is probably better, but bash does not like it
./Configure linux-armv4 enable-deprecated --cross-compile-prefix=/opt/cross-pi-gcc/bin/arm-linux-gnueabihf- --prefix=/opt/sysroots/raspberrypi/usr -DOSSL_SSIZE_MAX=INT_MAX
make -j 8
make install_sw
