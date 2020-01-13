#include <grpcpp/grpcpp.h>
#include <grpc++/grpc++.h>
#include "transport.grpc.pb.h"
//#include "stencil.pb.h"
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

    Status Exchange(const Request& req, Response& res)
    {
        ClientContext context;

        Status status = stub_->Exchange(&context, req, &res);

        if (!status.ok())
        {
            std::cout << status.error_code() << ": " << status.error_message()
                        << std::endl;
        }

        return Status::OK;
    }

private:
    std::unique_ptr<Transport::Stub> stub_;
};
