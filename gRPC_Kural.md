# gRPC Development Protocol

## Project Overview

This project implements a gRPC server in Python to handle election data and clients in both Python and C# that send this data. The communication relies on gRPC and Protocol Buffers for serialization and cross-language compatibility.

---

## Part 1: Python gRPC Server

### Step 1: Setup

**Creating the Project**:

- A new directory was created for the project.
- ```bash
  mkdir ElectionServer
  cd ElectionServer
  
  ```
  
  Install grpc libraries and protocol buffers:
  
  `pip install grpcio grpcio-tools` 

## Step 2: Define the proto file

The proto file included definitions for the election service, request messages, and response messages:

```python
message ElectionRequest {
    int32 regionID = 1;
    string regionName = 2;
    repeated Party electionData = 3;
    repeated Preference preferenceData = 4;
}
```

### Step 3: Generate Python Code from Proto

- Using the `grpc_tools.protoc` compiler, I generated the Python classes required for the gRPC server and client:
  
  `python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. protos/election.proto`
  
  Be careful to not use the variable I. like I.=

### Step 4: Implementing the Server Logic

1. **Server Implementation**:
   - In the `election_server.py` file, I implemented the gRPC server logic by creating a service class that inherits from the generated service base class from proto. This class contains the logic for handling incoming requests.
   - The server listens on a specified port (50000) and responds with a confirmation message:
   - ```python
     import grpc
     from concurrent import futures
     import election_pb2
     import election_pb2_grpc
     
     class ElectionService(election_pb2_grpc.ElectionServiceServicer):
         def SubmitElectionData(self, request, context):
             print(f"Received data: {request}")
             return election_pb2.ElectionReply(confirmation="Election data received successfully")
     
     def serve():
         server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
         election_pb2_grpc.add_ElectionServiceServicer_to_server(ElectionService(), server)
         server.add_insecure_port('[::]:50052')  # Binding to port 50052
         server.start()
         print("Server is running on port 50052...")
         server.wait_for_termination()
     
     if __name__ == '__main__':
         serve()
     
     ```
   
   ### Problems Encountered
   
   - **Proto File Issues**: Initially, I faced issues with syntax in the proto file. I resolved it by closely following the Protocol Buffers documentation and examples.
   - **Port Binding Conflicts**: The server failed to start due to port conflicts. I resolved this by changing the port number and ensuring no other application was using it. 

## Part 2: Python Client Development

### Step 1: Setting Up the Client

1. **Creating the Client**:
   - I created a separate directory for the client and installed the same dependencies: `pip install grpcio grpcio-tools`

### Step 2: Implementing the Client Logic

1. **Client Implementation**:
   - The client was implemented to send election data to the server:

```python
import grpc
import election_pb2
import election_pb2_grpc

def run():
    with grpc.insecure_channel('localhost:50052') as channel:
        client = election_pb2_grpc.ElectionServiceStub(channel)
        request = election_pb2.ElectionRequest(
            regionID=1,
            regionName="Central District",
            electionData=[election_pb2.Party(name="Party A", votes=1500)],
            preferenceData=[
                election_pb2.Preference(name="Mail-in", votes="300"),
                election_pb2.Preference(name="In-person", votes="1200")
            ]
        )
        response = client.SubmitElectionData(request)
        print("Client received:", response.confirmation)

if __name__ == '__main__':
    run()

```

### Problems Encountered

- **Connection Issues**: The client had issues connecting to the server. This was resolved by checking the server's running state and ensuring both were using the same port.
- **Data Serialization Errors**: I encountered data serialization issues when sending complex objects. I addressed this by ensuring the request message was constructed correctly according to the proto definitions.

## Part 3: C# Client Development

### Step 1: Creating a C# Client

1. **Creating the Project**:
   
   - A new Console App project was created in Visual Studio, and the necessary NuGet packages were added:

```bash
Install-Package Google.Protobuf
Install-Package Grpc.Net.Client
Install-Package Grpc.Tools
```

2. **Adding the Proto File**:
- The same `election.proto` file was used, ensuring the correct namespace for the C# classes. This allows for the same data structure definitions to be utilized across languages.

### Step 2: Implementing the C# Client Logic

1. **C# Client Implementation**:
   - Implemented the client to interact with the Python server:

```cs
using Grpc.Net.Client;
using ElectionClient;  // Adjust this according to your namespace

class Program
{
    static async Task Main(string[] args)
    {
        using var channel = GrpcChannel.ForAddress("http://localhost:50052");
        var client = new ElectionService.ElectionServiceClient(channel);
        
        var request = new ElectionRequest
        {
            RegionID = 1,
            RegionName = "Central District",
            ElectionData =
            {
                new Party { Name = "Party A", Votes = 1500 }
            },
            PreferenceData =
            {
                new Preference { Name = "Timon Bla", Votes = 300 },
                new Preference { Name = "Vincent", Votes = 300 }
            }
        };

        var response = await client.SubmitElectionDataAsync(request);
        Console.WriteLine("C# Client received: " + response.Confirmation);
    }
}


```

### Problems Encountered

- **NuGet Package Issues**: Initially, I had trouble resolving the gRPC packages in Visual Studio. This was resolved by clearing the local NuGet cache and ensuring all dependencies were correctly installed.
- **Serialization Problems**: The structure of the request object needed to match the proto definition exactly.

# Part 4: Output

Python client:

![](C:\Users\JamesDean\AppData\Roaming\marktext\images\2024-10-08-16-13-59-image.png)

.NET Client:
![](C:\Users\JamesDean\AppData\Roaming\marktext\images\2024-10-08-16-14-50-image.png)

# Part 5: Questions

1. **What is gRPC and why does it work across languages and platforms?**
   
   - **gRPC** is a framework for remote procedure calls (RPC) that allows services in different programming languages to communicate. It uses Protocol Buffers for defining services and messages, which makes it compatible across languages.

2. **Describe the RPC life cycle starting with the RPC client.**
   
   - The client calls a method on a stub, sends a serialized message to the server, which processes it and sends back a response. The client then deserializes the response.

3. **Describe the workflow of Protocol Buffers.**
   
   - Write definitions in a `.proto` file, use the `protoc` compiler to generate code, and then serialize/deserialize messages in your application to send over the network.

4. **What are the benefits of using Protocol Buffers?**
   
   - Benefits include efficient data size, cross-language compatibility, and the ability to change data structures without breaking existing services.

5. **When is the use of Protocol Buffers not recommended?**
   
   - Not recommended for simple applications, when human readability is important, or when dynamic message structures are needed.

6. **List 3 different data types that can be used with Protocol Buffers.**
   
   - Basic types: `int32`, `int64`, `float`, `double`, `bool`, `string`, and complex types such as `message`.
