import faker
import grpc
import location_pb2
import location_pb2_grpc

print("Sending test payload...")

channel = grpc.insecure_channel("127.0.0.1:5005")
stub = location_pb2_grpc.LocationServiceStub(channel)

preloaded_person_ids = [1, 5, 6, 8, 9]
non_existing_person_ids = [987, 56]

fake = faker.Faker()

def random_float_str():
    return str(fake.pyfloat(1))

payloads = [location_pb2.LocationMessage(person_id=y, latitude=random_float_str(), longitude=random_float_str()) for x in [preloaded_person_ids, non_existing_person_ids] for y in x]

for location in payloads:
    response = stub.Create(location)
    print(f"Response from gRPC server: {response}")