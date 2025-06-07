import grpc
from concurrent import futures
import sys
import os
from generated import calculator_pb2, calculator_pb2_grpc

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class CalculatorServicer(calculator_pb2_grpc.CalculatorServicer):
    def Add(self, request, context):
        """Unary RPC implementation for addition"""
        print(f"Received Add request: {request.a} + {request.b}")
        result = request.a + request.b
        return calculator_pb2.AddResponse(result=result)
    
    def Divide(self, request, context):
        """Unary RPC with error handling for division"""
        print(f"Received Divide request: {request.dividend}/{request.divisor}")
        
        # Error handling for division by zero
        if request.divisor == 0:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details("Cannot divide by zero")
            return calculator_pb2.DivideResponse()
        
        # Valid division
        quotient = request.dividend / request.divisor
        return calculator_pb2.DivideResponse(quotient=quotient)
    
    def Subtract(self, request, context):
        """Unary RPC implementation for subtraction"""
        print(f"Received Subtract request: {request.a} - {request.b}")
        result = request.a - request.b
        response = calculator_pb2.SubtractResponse()
        response.a = result  # Set the 'a' field in the oneof
        return response

    def Multiply(self, request, context):
        """Unary RPC implementation for multiplication"""
        print(f"Received Multiply request: {request.a} * {request.b}")
        result = request.a * request.b
        return calculator_pb2.MultiplyResponse(result=result)

def serve():
    # Create gRPC server
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10),
        options=[
            ('grpc.max_send_message_length', 50 * 1024 * 1024),
            ('grpc.max_receive_message_length', 50 * 1024 * 1024)
        ]
    )
    
    # Add service to server
    calculator_pb2_grpc.add_CalculatorServicer_to_server(
        CalculatorServicer(), server
    )
    
    # Start server
    server.add_insecure_port('[::]:50051')
    server.start()
    print("gRPC Server running on port 50051...")
    
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        print("\nServer stopped")

if __name__ == '__main__':
    serve()