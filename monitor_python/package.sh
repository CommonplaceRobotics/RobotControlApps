#!/bin/bash
# This script packages the app

# Enter the name of the app here. Must not contain spaces.
APP_NAME="monitor_app_python"
TEMPDIR="package_tmp"
CWD=`pwd`

# Delete any earlier package
rm $APP_NAME.zip
# Create temporary directory
mkdir -p $TEMPDIR/$APP_NAME
# Copy Python source code
cp -R src $TEMPDIR/$APP_NAME
# Copy additional files
cp rcapp.xml ui.xml pyproject.toml Licenses*.pdf $TEMPDIR/$APP_NAME
# Clean files
cd $TEMPDIR
find -name "__pycache__" -exec rm -r "{}" \;
# Create package
zip -r ../$APP_NAME.zip $APP_NAME
cd $CWD
# Remove temporary directory
rm -rf $TEMPDIR