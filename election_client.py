import grpc
import election_pb2
import election_pb2_grpc

def run():
    # Establish connection with the gRPC server
    with grpc.insecure_channel('localhost:50000') as channel:
        stub = election_pb2_grpc.ElectionServiceStub(channel)
    
        election_data = [
            election_pb2.PartyVotes(name="FPÖ", votes=900),
            election_pb2.PartyVotes(name="ÖVP", votes=900),
            election_pb2.PartyVotes(name="SPÖ", votes=900)
        ]

        preference_data = [
            election_pb2.PreferenceVotes(name="Andrea Müller", votes=400),
            election_pb2.PreferenceVotes(name="Hermann Mayer", votes=300)
        ]
        
        # Construct the ElectionRequest message with all fields
        election_request = election_pb2.ElectionRequest(
            regionID=101,
            regionName="20., Brigittenau",
            regionAddress="Wexstraße 3",
            regionPostalCodes="1200",
            federalState="Vienna",
            timeStamp="2024-10-08 12:00:00",
            electionData=election_data,
            preferenceData=preference_data
        )
        
        # Send the request and get a response
        response = stub.SubmitElectionData(election_request)
        print("Election client received:", response.confirmation)

if __name__ == '__main__':
    run()
