from concurrent import futures
import grpc
import election_pb2
import election_pb2_grpc

class ElectionServiceServicer(election_pb2_grpc.ElectionServiceServicer):
    def SubmitElectionData(self, request, context):
        print(f"Received Election Data from Region ID: {request.regionID}")
        print(f"Region Name: {request.regionName}")
        print(f"Address: {request.regionAddress}")
        print(f"Postal Codes: {request.regionPostalCodes}")
        print(f"Federal State: {request.federalState}")
        print(f"Timestamp: {request.timeStamp}")
        
        print("\nElection Data (Parties and Votes):")
        for party in request.electionData:
            print(f"Party: {party.name}, Votes: {party.votes}")
        
        print("\nPreference Data:")
        for preference in request.preferenceData:
            print(f"Type: {preference.name}, Description: {preference.votes}")
        
        return election_pb2.ElectionReply(confirmation="Election data received successfully")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    election_pb2_grpc.add_ElectionServiceServicer_to_server(ElectionServiceServicer(), server)
    server.add_insecure_port('[::]:50000')
    print("Election Server is running on port 50000...")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
