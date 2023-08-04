import grpc
import location_pb2
import location_pb2_grpc

from concurrent import futures

from kafka_location_producer import store_location

class LocationIngesterServicer(location_pb2_grpc.LocationServiceServicer):

    def __init__(self, *args, **kwargs):
        pass

    def StoreLocation(self, request, context):
        payload = {
            "person_id": int(request.person_id),
            "latitude": request.latitude,
            "longitude": request.longitude
        }

        store_location(payload)
        return location_pb2.LocationMessage(**payload)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    location_pb2_grpc.add_LocationServiceServicer_to_server(LocationIngesterServicer(), server)
    #Starting gRPC server on port 5005...")
    server.add_insecure_port('[::]:5005')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()