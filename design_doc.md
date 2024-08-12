#Design Document: Toy Store Client-Server

**Introduction:**
The Toy Store Client-Server system is a distributed application designed to facilitate online shopping for stuffed animal toys. The system consists of two main components: the server, which hosts the toy store and handles client requests, and the client, which interacts with the server to query toy information and make purchases. We explore socket based and gRPC communication between the client and server.

**Objective:**
The primary objective of the Toy Store Client-Server system is to provide a scalable and efficient platform for users to browse and purchase stuffed animal toys online. The system aims to support concurrent client connections, handle both read and write operations on the product catalog, and ensure data consistency and integrity.

**Solutions Overview/Architecture:**
The system is implemented using two different communication protocols: socket-based communication for Part 1 and gRPC (Remote Procedure Call) for Part 2.

**Socket-Based Communication (Part 1):**
- The server component listens for incoming client connections on a specified network port using a socket.
- Upon connection, each client request is handled by a separate thread in a static thread pool, allowing for concurrent processing of client requests. 
- The server maintains an in-memory product catalog, which stores information about available toys along with their prices and stock levels.
- The client component establishes a socket connection with the server and sends query or buy requests, which are processed by the server.
- Each client sends 10 requests sequentially , where each request sends a message in the form of a buffer specifying the method name (e.g., string "Query") and arguments ("toyName")(e.g., "method_name: toy_name"). Upon receiving these messages, the server decodes and parses the string to extract the relevant information, effectively marshalling and demarshalling data.
- To manage concurrent requests efficiently, a thread pool class is utilized, allowing for the creation of a static number of threads configurable at startup. When the server is instantiated, a thread pool is initialized with the predetermined number of threads.In our implementation, the static thread pool count is fixed to 5 threads. The main server thread then accepts incoming requests over a socket, inserting them into a request queue, and subsequently notifies the thread pool. This mechanism ensures that idle threads are assigned incoming requests for processing.
- The thread pool implementation leverages a custom queue, which is constructed using Python lists. The custom queue comprises two primary functions: "put" for appending client requests to the queue and "get" for retrieving requests. Synchronization is achieved through a combination of locks and conditions within the custom queue, to ensure thread safety when adding or removing requests from the request queue

- To simulate concurrent client activity, the multiprocessing library is employed to facilitate the concurrent transmission of requests from multiple clients. This approach allows for the simulation of 5 client processes making requests simultaneously. Additionally, the multiprocessing manager is utilized to record the latency in query requests across all clients. This ensures accurate latency measurement across different client processes by maintaining separate memory spaces for each client within the multiprocessing environment.

**gRPC Communication (Part 2):**
- The server component exposes two gRPC methods: Query and Buy, which handle client requests to query toy information and make purchases, respectively.
- Each gRPC method invocation corresponds to a remote procedure call, allowing for language-agnostic communication between the client and server.
- The server utilizes a dynamic thread pool provided by the gRPC framework to handle incoming client requests, ensuring efficient resource utilization.
- Similar to Part 1, the server maintains an in-memory product catalog to store toy information.
- Also, we used the same multiprocessing library to simulate concurrent client requests similar to part 1.
- A threading lock is utilized for synchronization purposes. This lock ensures that only one thread can access the critical section (the database in this case) at a time. When a client makes a query or buy request, it uses lock to access the database. If another client is currently holding the lock (e.g., performing a query or buy operation), the requesting client must wait until the lock becomes available. Synchronization mechanisms like locks are needed to prevent potential conflicts. For example, suppose Client A is reading a certain piece of data from the database, and at the same time, Client B is updating that same data. If Client A reads the data while Client B's update is in progress but not yet committed, Client A may see an intermediate state of the data, leading to inconsistency. Thus a lock has been implemented before the Query request and Buy request. While threading locks ensure mutual exclusion and prevent concurrent modifications, they do not distinguish between read and write operations. Introducing read-write locks could potentially improve concurrency by allowing multiple clients to concurrently read the database (as in the case of query requests), while still ensuring exclusive access during write operations (as in the case of buy requests). This finer-grained synchronization can lead to reduced contention and improved performance, particularly in scenarios with a higher proportion of read operations.

Note: In both Part 1 and Part 2, we incorporated a simulated processing time of 200 ms within both the query and buy functions. This choice aimed to emulate the realistic processing time typically encountered when handling read and write requests on an actual database. By introducing this delay, we mimicked the scenario where concurrent client requests contend for server resources, leading to queuing and increased response time.

The inclusion of the sleep time not only provided a more realistic simulation but also underscored the importance of efficient resource utilization and concurrency management in distributed systems. As clients make requests to access or modify the shared database, the server must contend with processing each request sequentially, leading to potential delays and queuing as the load increases.

By incorporating this simulated processing time, our evaluation captured the impact of contention for threads and the queuing phenomenon on response time. This refinement adds a layer of realism to our analysis, highlighting the challenges and considerations involved in designing and optimizing distributed systems for real-world scenarios.
Moreover, without the inclusion of the sleep time, the differences in network speed exert a more pronounced influence on the observed latencies from the client side. This occurs because the actual processing time of the query and buy functions on the server side is significantly shorter in comparison to the time taken to transmit and receive requests over the network. In essence, the absence of a simulated processing time accentuates the impact of network latency on overall response times.


**APIs:**
- Part 1 (Socket-Based):
  - Query(toyName): Takes a toy name as input and returns the price of the toy if it is in stock. Returns -1 if the item is not found and 0 if the item is found but not in stock.
- Part 2 (gRPC):
  - Query: Accepts a request containing a toy name and returns the price of the toy along with its current stock level.
  - Buy: Accepts a request containing a toy name and attempts to purchase the toy. Returns a result code indicating the success or failure of the purchase operation.

**Testing:**
- We used unit testing to verify the functionality of individual components such as the server's query and buy functions, and client-server communication. 
- We used the ‘time’ library in python to systematically measure the latency between the moment a client initiates a query and the time it receives a response from the server. As each client is programmed to execute 10 queries, we compute the average latency across these 10 queries for each individual client. This process is replicated across all five clients to gather comprehensive latency data.
- We also conducted integration tests to validate the communication between the client and server components, ensuring proper handling of query and buy requests.
- We performed load testing to assess system performance under varying levels of client load, measuring response times and scalability. The load testing is done across 10 clients. We observe how the latency varies as we increase the number of clients from 1 to 5 and further to 10 clients.

**List of Known Issues/Alternatives:**
- Efficiency: In part 2 , since we are implementing the same lock in the query and buy requests there is an increase in response time of query as load increases. This can be made more efficient using read - write locks. The use of read-write locks should ideally cause query requests (with read locks) to be faster than buy requests (which need write locks).
-Scalability: While both Part 1 and Part 2 support concurrent client connections, scalability may be limited by factors such as thread pool size, server resources and synchronization overhead. In part 1 the thread pool size is fixed to 5 and in part 2 the maximum number of threads is fixed to 10 in our implementation.
- Network Latency: Both implementations are susceptible to variations in network latency, which can affect response times observed by clients. In our implementation, we added a 0.2s delay using time.sleep in the query and buy function to simulate processing time and make it more practical. This added offset reduces the impact of variations in network latency too.   Implementing caching mechanisms or using content delivery networks (CDNs) could help alleviate this issue. 

**Error Handling:**
- Data Consistency: In part 2, synchronization mechanisms such as locks are crucial to prevent conflicts that may arise from concurrent access to shared resources. For instance, consider a scenario where Client A is reading a particular piece of data from the database while Client B is simultaneously updating the same data. Without proper synchronization, Client A may access an inconsistent or intermediate state of the data, resulting in potential inconsistencies. To address this issue, we have implemented locks before both the Query and Buy requests. These locks ensure mutual exclusion, preventing concurrent modifications and maintaining data integrity. 
- Avoided race conditions : In Part 1, we employed locks to ensure exclusive access to the request queue, preventing multiple threads from concurrently accessing it. This approach helped avoid race conditions by serializing access to shared resources, thereby ensuring safe and sequential processing of client requests.

**Conclusion:**
The Toy Store Client-Server system provides a flexible and efficient platform for online toy shopping, leveraging socket-based and gRPC communication protocols to enable client-server interaction. By maintaining an in-memory product catalog and employing concurrency management techniques, the system ensures reliable and responsive handling of client requests while striving for scalability and data consistency.

**References:**
- Reused code from Lablet1
- Tutorial to gRPC in Python https://grpc.io/docs/languages/python/basics/
- gRPC example in python:https://grpc.io/docs/languages/python/quickstart/
- Tutorials at https://www.tutorialspoint.com/python_network_programming/python_sockets_programming.htm
- Used ChatGPT to understand the multiprocessing module provided by python so that we could simulate concurrent client requests using it. We used  it to see basic examples of custom thread pool implementation and to understand how synchronization is achieved using locks
- We also used gRPC documentation to write the toystore.proto file and to generate the toystore_pb2_grpc.py and toystore_pb2.py files
- We used chatGPT to figure out some issues that we faced like a deadlock situation, private memory spaces for different process while using multiprocessing,etc
- We also used gRPC documentation and chatGPT to figure out how to send and receive messages, error codes, arguments,etc in the gRPC implementation
- Learn about Python's built-in threadpool https://docs.python.org/3/library/concurrent.futures.html#threadpoolexecutor
