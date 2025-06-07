import grpc
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from generated import calculator_pb2, calculator_pb2_grpc

def run_operation(stub, operation, a, b):
    """Execute RPC operation with error handling"""
    try:
        if operation == "add":
            response = stub.Add(calculator_pb2.AddRequest(a=a, b=b))
            print(f"Result: {a} + {b} = {response.result}")
        
        elif operation == "divide":
            # Set timeout for division operation
            response = stub.Divide(
                calculator_pb2.DivideRequest(dividend=a, divisor=b),
                timeout=10
            )
            
            # Handle oneof result
            if response.HasField("quotient"):
                print(f"Result: {a} / {b} = {response.quotient:.2f}")
            else:
                print(f"Error: {response.error}")
        
        elif operation == "subtract":
            response = stub.Subtract(calculator_pb2.SubtractRequest(a=a, b=b))
            if response.HasField("result"):
                print(f"Result: {a} - {b} = {response.result}")
            else:
                print(f"Error: {response.error}")
    
    except grpc.RpcError as e:
        print(f"RPC failed: {e.code().name} - {e.details()}")
    except Exception as e:
        print(f"Error: {str(e)}")

def main():
    # Create channel and stub
    channel = grpc.insecure_channel('localhost:50051', options=[
        ('grpc.max_send_message_length', 50 * 1024 * 1024),
        ('grpc.max_receive_message_length', 50 * 1024 * 1024)
    ])
    stub = calculator_pb2_grpc.CalculatorStub(channel)
    
    print("gRPC Calculator Client\n" + "-" * 30)
    
    while True:
        print("\nOperations: add, divide, subtract, exit")
        command = input("Enter operation: ").strip().lower()
        
        if command == "exit":
            break
        
        if command not in ["add", "divide", "subtract"]:
            print("Invalid operation")
            continue
        
        try:
            a = int(input("Enter first number: "))
            b = int(input("Enter second number: "))
            run_operation(stub, command, a, b)
        except ValueError:
            print("Invalid input. Numbers must be integers.")

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

        # Make Subtract request
        subtract_request = calculator_pb2.SubtractRequest(a=20, b=10)
        subtract_response = stub.Subtract(subtract_request)
        print(f"Subtract result: {subtract_response.a}")

        # Make Multiply request
        multiply_request = calculator_pb2.MultiplyRequest(a=6, b=7)
        multiply_response = stub.Multiply(multiply_request)
        print(f"Multiply result: {multiply_response.result}")

if __name__ == '__main__':
    main()