from concurrent import futures
import time
import math
import logging

import grpc
import transport_pb2_grpc

class TransportServicer(transport_pb2_grpc.TransportServicer):
    """Provides methods that implement functionality of route guide server."""

    def __init__(self):
        return

    def Exchange(self, request, context):
        return None

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    transport_pb2_grpc.add_TransportServicer_to_server(
        TransportServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()