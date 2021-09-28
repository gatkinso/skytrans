from concurrent import futures
from google.protobuf.json_format import MessageToJson

import grpc
import transport_pb2
import transport_pb2_grpc

class TransportServicer(transport_pb2_grpc.TransportServicer):
    """Provides methods that implement functionality of route guide server."""

    def __init__(self):
        self.i = 0
        return

    def Exchange(self, request, context):
        #json_trans = MessageToJson(request)
        #print(json_trans)
        print(request.meta.data.int_values["id"])

        res = transport_pb2.Response()
        self.i = self.i + 1

        res.meta.data.string_values["Company"] = request.meta.data.string_values["Company"] + " responded"
        res.meta.data.int_values["id"] = self.i
        return res

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=15))
    transport_pb2_grpc.add_TransportServicer_to_server(
        TransportServicer(), server)
    server.add_insecure_port('[::]:1967')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()