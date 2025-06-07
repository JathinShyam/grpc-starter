import pytest
import grpc
from concurrent import futures
import sys
import os
import threading
import time

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from generated import calculator_pb2, calculator_pb2_grpc
from server import CalculatorServicer

@pytest.fixture(scope="function")
def server():
    """Create a test server instance."""
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    calculator_pb2_grpc.add_CalculatorServicer_to_server(
        CalculatorServicer(), server
    )
    port = server.add_insecure_port('[::]:50051')  # Use random port
    server.start()
    yield server
    server.stop(0)

@pytest.fixture(scope="function")
def channel(server):
    """Create a test channel."""
    port = server.add_insecure_port('[::]:50051')  # Get the actual port
    return grpc.insecure_channel(f'localhost:{port}')

@pytest.fixture(scope="function")
def stub(channel):
    """Create a test stub."""
    return calculator_pb2_grpc.CalculatorStub(channel)

def test_add(stub):
    """Test the Add RPC."""
    request = calculator_pb2.AddRequest(a=10, b=20)
    response = stub.Add(request)
    assert response.result == 30

def test_divide(stub):
    """Test the Divide RPC."""
    request = calculator_pb2.DivideRequest(dividend=100, divisor=5)
    response = stub.Divide(request)
    assert response.quotient == 20.0

def test_divide_by_zero(stub):
    """Test division by zero error handling."""
    request = calculator_pb2.DivideRequest(dividend=100, divisor=0)
    with pytest.raises(grpc.RpcError) as exc_info:
        stub.Divide(request)
    assert exc_info.value.code() == grpc.StatusCode.INVALID_ARGUMENT

def test_subtract(stub):
    """Test the Subtract RPC."""
    request = calculator_pb2.SubtractRequest(a=20, b=10)
    response = stub.Subtract(request)
    assert response.a == 10.0

def test_multiply(stub):
    """Test the Multiply RPC."""
    request = calculator_pb2.MultiplyRequest(a=6, b=7)
    response = stub.Multiply(request)
    assert response.result == 42