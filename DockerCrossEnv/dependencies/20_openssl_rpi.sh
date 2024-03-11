#!/bin/bash

builddir=~/build_dependencies
mkdir $builddir

# Delete pre-installed OpenSSL version
rm -rf /opt/sysroots/raspberrypi/usr/include/arm-linux-gnueabihf/openssl
rm -rf /opt/sysroots/raspberrypi/usr/lib/arm-linux-gnueabihf/*ssl*
rm -rf /opt/sysroots/raspberrypi/usr/lib/arm-linux-gnueabihf/*crypto*

# OpenSSL: required
echo "Building OpenSSL..."
# RPi:
cd $builddir
#opensslver=openssl-1.1.0j
opensslver=openssl-1.1.1w
wget https://www.openssl.org/source/$opensslver.tar.gz
tar zxf $opensslver.tar.gz
cd $opensslver
./Configure linux-armv4 enable-deprecated --cross-compile-prefix=/opt/cross-pi-gcc/bin/arm-linux-gnueabihf- --prefix=/opt/sysroots/raspberrypi/usr
make -j 8
make uninstall -j 8
make install_sw install_ssldirs -j 8
