import socket
import threading
import time

# toy store database
toys_db = {
    "Tux": {"price": 25.99, "stock": 8},
    "Whale": {"price": 19.99, "stock": 3}
}

# Define the number of threads in the thread pool
N = 5

class CustomQueue:
    def __init__(self):
        #inititalize the queue, lock and condition 
        self.queue = []
        self.lock = threading.Lock()
        self.condition = threading.Condition(lock=self.lock)

    def put(self, request):
        # add an item to the queue
        with self.condition:
            self.queue.append(request)
            self.condition.notify()

    def get(self):
        # get an item from the queue
        with self.condition:
            while not self.queue:
                self.condition.wait()
            return self.queue.pop(0)

class ThreadPool:
    def __init__(self, N):
        # initialize the thread pool with the specified number of threads
        self.N = N
        self.request_queue = CustomQueue()
        self.threads = []
        self.create_threads()
        
    def create_threads(self):
        # create worker threads
        print("Creating threads")
        for i in range(self.N):
            thread = threading.Thread(target=self.wait_for_request_and_handle)
            thread.start()
            self.threads.append(thread)

    def wait_for_request_and_handle(self):
        # worker function for processing requests
        print("inside wait_for_request_and_handle")
        while True:
            request = self.request_queue.get()
            print("Received request")
            self.handle_request(request)
    
    def handle_request(self,client_socket):
        # processing the client request
        print("inside handle_request")
        try:
            while True:
                # recieve and process requests from the client
                t1 = time.time()

                request = client_socket.recv(1024)
                if not request:
                    break
                #decode and parse the request
                stringified_message = request.decode('utf-8').strip()
                method, toy_name = stringified_message.split(': ')
                
                print("toy_name:",toy_name)
                if method == "query":
                    #query the toy price
                    t2 = time.time()
                    price = self.query_toy(toy_name)
                    t3 = time.time()
                    # print("query time = ",t3-t2)
                
                # send the price to the client
                print("price:",price)
                time.sleep(0.2)
                
                client_socket.send(str(price).encode('utf-8'))

                t4 = time.time()
                print("time taken by handle request = ",t4-t1)
        except ConnectionResetError:
            print("Connection reset by peer")
        finally:
            print("client_socket closed")
            client_socket.close()


    def query_toy(self,toy_name):
        # query the toy price from the toy store database
        if toy_name in toys_db:
            if toys_db[toy_name]["stock"] > 0:
                return toys_db[toy_name]["price"]
            else:
                return 0  # Item found but not in stock
        else:
            return -1

class Server:
    def __init__(self,N):
        # inititalize the server with a thread pool
        self.threadpool = ThreadPool(N)

    def add_request(self,request):
        # add a request to the thread pool's request queue 
        self.threadpool.request_queue.put(request)

    def start_connection(self):
        #start the server and listen for incoming connections
        s = socket.socket()
        host = socket.gethostname()  # Get local machine name
        port = 56732  # Reserve a port for your service

        dns_resolved_addr = socket.gethostbyname(host)
        print(dns_resolved_addr)

        s.bind((host, port))  # Bind to the port

        s.listen(5)  # Now wait for client connection

        while True:
            # accept the  incoming connections and add them to the thread pool
            c, addr = s.accept()  # Establish connection with client
            self.add_request(c)
            print("Recieved ",c)

if __name__ == "__main__":
    # Create a server instance with the specified number of threads
    server = Server(5)
    #Start the server and handle incoming connections
    server.start_connection()
