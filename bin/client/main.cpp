#include "TransportClient.h"
#include "stencil.h"

using namespace skyloupe::skytrans;

void doit(int i)
{
    TransportClient client(
        grpc::CreateChannel("localhost:1967", grpc::InsecureChannelCredentials())
    );

    skyloupe::Stencil s;
    s.set_value_int("id", i);
    s.set_value_string("Company", "Microsoft");
    Request req;

    auto sss = req.mutable_meta()->mutable_data();
    sss->CopyFrom(s.get_proto());

    Response res;
    auto status = client.Exchange(req, res);

    std::cout << "Response received: " << res.DebugString() << std::endl;

    return;
}

int main(int argc, char** argv)
{
    for( int i = 0; i < 10000; i++)
    {
        doit(i);
    }

    return 0;
}