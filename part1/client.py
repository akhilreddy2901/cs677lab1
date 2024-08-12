import socket
import multiprocessing
import time

class Client:
    def __init__(self):
        pass
    
    def send_message(self,toy_name,latencies):
        # Create a new socket  
        s = socket.socket()
        # host = socket.gethostname()  # Get local machine name
        host = "128.119.243.168" # remote machine
        port = 56732 # Specify the port to connect to
        
        # print("Connectig to:",host)
        s.connect((host, port))

        print("Sending message-",toy_name)
        # s.send(toy_name.encode())
        #record the start time
        start_time = time.time()
        #send the toy name to the server
        s.send(toy_name.encode())
        # receive response from the server
        response= s.recv(1024).decode('utf-8')
        #record end time
        end_time = time.time()
        print("response:",response," , latency:",end_time-start_time)
        latencies.append(end_time-start_time) # appending latency to the list of latencies
       
        s.close()  # Close the socket when done

def single_client_process(latencies):
    
    client = Client() #instantiate client object
   
    toys = ["Tux","Whale","Whale","Tux","Whale","Whale","Whale","Whale","Tux","Whale"]
    for toy in toys:
        stringified_pair = '{}: {}'.format("query", toy) # Formatting the toy name as a string with the method name query
        client.send_message(stringified_pair,latencies) # send the message to the server and record latency



if __name__ == "__main__":
    processes= []
    manager = multiprocessing.Manager() # create a manager to handle shared data between processes
    latencies = manager.list() # Create a list to store latencies, which will be shared between processes
    
    n = 3 # number of client processes
    for _ in range(n):
        #Create a new process that executes the single_process function
        process = multiprocessing.Process(target=single_client_process,args=(latencies,))
        processes.append(process)  #Add the process to the list of processes
        process.start() #Start the process

    #wait for all processes to complete
    for process in processes:
        process.join()
    
    # Calculate and print the average latency across all processes
    print("No of client processess = ",n)
    print("Average latency = ",sum(latencies)/len(latencies))
    

