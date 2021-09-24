#include <grpcpp/grpcpp.h>
#include <grpc++/grpc++.h>
#include "transport.grpc.pb.h"
#include <iostream>

#pragma once

using grpc::Channel;
using grpc::ClientContext;
using grpc::Status;
using namespace skyloupe::skytrans;

class TransportClient
{
public:
    TransportClient(std::shared_ptr<Channel> channel)
      : stub_(Transport::NewStub(channel)) {}

    Status Exchange(const Request& req, Response& res);

private:
    std::unique_ptr<Transport::Stub> stub_;
};
