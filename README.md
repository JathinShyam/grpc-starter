# gRPC Foundations Project

A complete implementation covering Phase 1 learning objectives:

- gRPC architecture fundamentals
- Protocol Buffer definitions
- Unary RPC implementation
- Error handling patterns

## Prerequisites

- Python 3.7 or higher
- pip (Python package installer)
- Protocol Buffers compiler (protoc)
- Git (optional, for version control)

## Installation

1. Clone the repository (if using Git):

```bash
git clone git@github.com:JathinShyam/grpc-starter.git
cd grpc
```

2. Create and activate virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Install required dependencies:

```bash
pip install -r requirements.txt
```

4. Install Protocol Buffers compiler:

- **Linux**:

```bash
sudo apt-get install protobuf-compiler  # Ubuntu/Debian
sudo yum install protobuf-compiler      # CentOS/RHEL
```

- **macOS**:

```bash
brew install protobuf
```

- **Windows**: Download from [Protocol Buffers releases](https://github.com/protocolbuffers/protobuf/releases)

## Project Structure

```
.
├── protos/                  # Protocol Buffer definitions
│   └── calculator.proto     # Service and message definitions
├── generated/              # Generated gRPC code
│   ├── calculator_pb2.py   # Generated message classes
│   └── calculator_pb2_grpc.py  # Generated service classes
├── server.py              # gRPC server implementation
├── client.py             # gRPC client implementation
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## Key Concepts Covered

### 1. gRPC Architecture

- Client-server communication model
- Protocol Buffers as IDL (Interface Definition Language)
- HTTP/2 transport benefits
- Bi-directional streaming capabilities
- Service definition and implementation

### 2. Protocol Buffers

- Message definitions
- Service declarations
- Scalar data types
- `oneof` field usage
- Package namespacing
- Field numbering and versioning
- Nested message types

### 3. Code Generation

- `protoc` compiler workflow
- Python class generation
- Serialization/deserialization
- Service stub generation
- Message type definitions

### 4. Unary RPC Implementation

- Service implementation inheritance
- Request/response handling
- Context manipulation
- Error handling
- Request validation
- Response formatting

### 5. Error Handling

- Status codes (INVALID_ARGUMENT)
- Error details propagation
- Client-side exception handling
- Timeout management
- Graceful error recovery
- Custom error types

### 6. Best Practices

- Thread pool management
- Proper channel handling
- Input validation
- Clean resource termination
- Connection pooling
- Load balancing
- Security considerations

## Running the Project

1. Start the gRPC server:

```bash
python server.py
```

The server will start on port 50051 by default.

2. Run the client in a separate terminal:

```bash
python client.py
```

3. Example client usage:

```python
import grpc
from generated import calculator_pb2, calculator_pb2_grpc

def run():
    # Create a gRPC channel
    with grpc.insecure_channel('localhost:50051') as channel:
        # Create a stub (client)
        stub = calculator_pb2_grpc.CalculatorStub(channel)

        # Make Add request
        add_request = calculator_pb2.AddRequest(a=10, b=20)
        add_response = stub.Add(add_request)
        print(f"Add result: {add_response.result}")

        # Make Divide request
        divide_request = calculator_pb2.DivideRequest(dividend=100, divisor=5)
        divide_response = stub.Divide(divide_request)
        print(f"Divide result: {divide_response.quotient}")

if __name__ == '__main__':
    run()
```

## Testing

1. Unit Tests:

```bash
# Run tests with coverage
./run_tests.sh

# Or run tests directly with pytest
python -m pytest tests/
```

2. Manual Testing:

- Use the provided client to test different operations
- Test error cases (e.g., division by zero)
- Verify response times and performance

## Troubleshooting

Common issues and solutions:

1. **ImportError: No module named 'grpc'**

   - Solution: Ensure you're in the virtual environment and run `pip install -r requirements.txt`

2. **Connection refused errors**

   - Solution: Verify the server is running and check the port number

3. **Protocol Buffer compilation errors**
   - Solution: Ensure protoc is installed and in your PATH

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request
