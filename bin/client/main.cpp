#include "TransportClient.h"
#include "stencil.h"

using namespace skyloupe::skytrans;

int main(int argc, char** argv)
{
    TransportClient client(
        grpc::CreateChannel("localhost:1967", grpc::InsecureChannelCredentials())
    );

    skyloupe::Stencil s;
    s.set_value_int("id", 1);
    s.set_value_string("Company", "Microsoft");
    Request req;

    auto sss = req.mutable_meta()->mutable_data();
    sss->CopyFrom(s.get_proto());

    Response res;
    auto status = client.Exchange(req, res);

    std::cout << "Response received: " << res.DebugString() << std::endl;

    return 0;
}