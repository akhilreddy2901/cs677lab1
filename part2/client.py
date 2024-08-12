import grpc
import toystore_pb2
import toystore_pb2_grpc
import multiprocessing
import time

# Function to query a toy from the server
def query_toy(stub, item_name):
    response = stub.Query(toystore_pb2.ItemName(name=item_name))
    if response.name:
        print(f"{response.name}: Price ${response.price}, Stock {response.stock}")
    else:
        print("Item not found")

#Function to buy a toy from the server
def buy_toy(stub, item_name):
    response = stub.Buy(toystore_pb2.ItemName(name=item_name))
    if response.status == 1:
        print("Item purchased successfully")
    elif response.status == 0:
        print("Item out of stock")
    else:
        print("Invalid item name")

# Funtion representing a single client process
def single_client_process(q_latencies,b_latencies):
    #establish a connection to the server
    channel = grpc.insecure_channel('128.119.243.168:50043')
    stub = toystore_pb2_grpc.ToyStoreStub(channel)

    # perform 10 iterations of querting and buying a toy
    for _ in range(10):
        # measure the latency of qquerying a toy
        start_time = time.time()
        query_toy(stub, "Tux")
        end_time = time.time()
        print("Query response time:",end_time-start_time)
        q_latencies.append(end_time-start_time) # record the latency for querying
        
        #meaure the latency of buying a toy 
        start_time = time.time()
        buy_toy(stub, "Tux")
        end_time = time.time()
        print("Buy response time:",end_time-start_time)
        b_latencies.append(end_time-start_time)     # record the latency for buying    

# Main function to generate multiple client processes
def main():
    processes= []  # List to store the client processes
    manager = multiprocessing.Manager() # Manager for sharing data between processes
    q_latencies = manager.list()  # List to store query latencies across processes
    b_latencies = manager.list() #  List to store buy latencies across processes
    n = 6  # Number of client processes to spawn

    # Create and start the client processes

    for _ in range(n):
        process = multiprocessing.Process(target=single_client_process,args=(q_latencies,b_latencies))
        processes.append(process)
        process.start()
    
    # Wait for all client processes to finish
    for process in processes:
        process.join()
    
    print("No of client processess = ",n)
    print("Average query latency = ",sum(q_latencies)/len(q_latencies))
    print("Average buy latency = ",sum(b_latencies)/len(b_latencies))

if __name__ == '__main__':
    main()
