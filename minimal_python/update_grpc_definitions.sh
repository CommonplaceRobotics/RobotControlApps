#!/bin/sh
# Regenerates the GRPC Python definition files. Call this after updating protos/robotcontrolapp.proto
../venv/Scripts/activate.bat
py -V:3.9.2 -m grpc_tools.protoc -Iprotos --python_out=. --pyi_out=. --grpc_python_out=. protos/robotcontrolapp.proto
