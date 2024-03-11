#!/bin/bash

fileDir="/opt/cross-pi-gcc/arm-linux-gnueabihf/include/c++/9.2.0"
file="$fileDir/climits"
limitsFixed=`fgrep -c "linux/limits.h" $file`
if [ $limitsFixed -eq 0 ]
then
	echo "Adding linux/limits.h to $file..."
	echo "#include <linux/limits.h>" >> $file
fi
