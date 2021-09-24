#include "TransportClient.h"


Status TransportClient::Exchange(const Request& req, Response& res)
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
