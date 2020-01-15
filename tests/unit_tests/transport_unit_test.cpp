//
//   Copyright (C) 2019 Skyloupe, LLC
//   
//   Licensed under the Apache License, Version 2.0 (the "License").
//   You may not use this file except in compliance with the License.
//   A copy of the License is located at
//   
//   https://www.apache.org/licenses/LICENSE-2.0.html
//   
//   or in the "license" file accompanying this file. This file is distributed
//   on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
//   express or implied. See the License for the specific language governing
//   permissions and limitations under the License.
//

#include <gmock/gmock.h>
#include <gtest/gtest.h>
#include "google/protobuf/reflection.h"
#include <google/protobuf/util/json_util.h>
#include "google/protobuf/util/message_differencer.h"
#include <string>
#pragma warning(disable:4800)
#include "transport.pb.h"
#include "example.pb.h"
#pragma warning(default:4800)

class TransportUnitTest : public ::testing::Test
{
protected:
    TransportUnitTest() {}

    skyloupe::skytrans::Request req_;
    skyloupe::skytrans::Response res_;
};

TEST_F(TransportUnitTest, SerDes_Json)
{
    google::protobuf::MapPair < std::string, std::string > pair("key", "value");
    req_.mutable_payload()->mutable_string_values()->insert(pair);

    skyloupe::skytrans::Example ex;
    ex.set_count(111);
    ex.set_precision(222.2);
    *ex.add_names() = "John Doe";

    req_.add_impl()->PackFrom(ex);

    std::string json_str;
    auto ret = google::protobuf::util::MessageToJsonString(req_, &json_str);

    ASSERT_EQ(google::protobuf::util::Status::OK, ret);

    skyloupe::skytrans::Request req_out;
    ret = google::protobuf::util::JsonStringToMessage(json_str, &req_out);

    ASSERT_EQ(google::protobuf::util::Status::OK, ret);
    ASSERT_TRUE(google::protobuf::util::MessageDifferencer::Equivalent(req_out, req_));
}
