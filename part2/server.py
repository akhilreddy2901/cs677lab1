import grpc
import time
import threading
from concurrent import futures
import toystore_pb2
import toystore_pb2_grpc

# Define the toy store catalog
toys_db = {
    "Tux": {"price": 25.99, "stock": 8},
    "Whale": {"price": 19.99, "stock": 5},
    "Elephant": {"price": 29.99, "stock": 8},
    "Dolphin": {"price": 22.99, "stock": 3}
}

# Lock for synchronizing access to the toy store database
db_lock = threading.Lock()

class toy_store_server(toystore_pb2_grpc.toy_store_server):
    def Query(self, request, context):  # gRPC method to query information about a toy
        item_name = request.name
        with db_lock:
            # print(f"Thread {threading.current_thread().name} processing Query request for {item_name}")
            if item_name in toys_db:
                #Check if the requested toy exists in the database
                time.sleep(0.2) # Simulate processing time
                item_info = toys_db[item_name]

                return toystore_pb2.Item(name=item_name, price=item_info["price"], stock=item_info["stock"])  # Return the toy information as a gRPC response
            else:
                time.sleep(0.2) # Simulate processing time
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT) # Set gRPC status code and details for item not found
                context.set_details("Item not found")
                return toystore_pb2.Item() # Return an empty item as the response

    # gRPC method to buy a toy
    def Buy(self, request, context):
        item_name = request.name
        with db_lock:
            # print(f"Thread {threading.current_thread().name} processing Query request for {item_name}")
            if item_name in toys_db: # Check if the requested toy exists in the database
                if toys_db[item_name]["stock"] > 0:
                    time.sleep(0.2)  # Simulate processing time
                    toys_db[item_name]["stock"] -= 1 # Decrease the stock count of the toy
                    return toystore_pb2.BuyResponse(status=1) # Return a successful status code
                else:
                    time.sleep(0.2)                     # Simulate processing time

                    return toystore_pb2.BuyResponse(status=0) # Return status code indicating item is out of stock
            else:
                time.sleep(0.2) # simulate the processing time
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT) # Set gRPC status code and details for invalid item name
                context.set_details("Invalid item name")
                return toystore_pb2.BuyResponse(status=-1) # Return status code indicating invalid item name

def start_server():
    # Create a gRPC server with a thread pool executor
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    # Add the toy_store_server implementation to the server
    toystore_pb2_grpc.add_toy_store_server_to_server(toy_store_server(), server)
    server.add_insecure_port('[::]:50043')  # Add an insecure port for serving requests
    server.start() # Start the server
    print("Server started")
    try:
        # Keep the server running until interrupted
        while True:
            time.sleep(86400)  # One day in seconds
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    start_server()
