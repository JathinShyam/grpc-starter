#!/bin/bash

# Clean up any existing generated files
rm -rf generated/*
touch generated/__init__.py

# Generate gRPC code
python -m grpc_tools.protoc -I./protos --python_out=generated --grpc_python_out=generated ./protos/calculator.proto

# Patch the import in calculator_pb2_grpc.py to be relative
sed -i 's/^import calculator_pb2 as calculator__pb2$/from . import calculator_pb2 as calculator__pb2/' generated/calculator_pb2_grpc.py

# Run tests with coverage
PYTHONPATH=$PYTHONPATH:$(pwd) pytest tests/ -v --cov=. 