//
//   Copyright (C) 2017 Skyloupe, LLC
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
#include "stencil.pb.h"
#pragma warning(default:4800)
#include "stencil/stencil.h"

#define SKYTRANS_PORT //

class StencilUnitTest : public ::testing::Test
{
protected:
    StencilUnitTest() 
        : includes_{ "\"math.h\"", "<string>", "\"myheader.h\"" }
    {}

    skyloupe::skytrans::Stencil stencil_proto_;

    std::string includes_[3];
};

TEST_F(StencilUnitTest, Serialize_Json)
{
    std::string json_str;
    google::protobuf::util::Status ret = google::protobuf::util::MessageToJsonString(stencil_proto_, &json_str);

    ASSERT_EQ(google::protobuf::util::Status::OK, ret);
}

TEST_F(StencilUnitTest, read_file)
{
    skyloupe::Stencil stencil;

    bool rc = stencil.read_file("stencil_unit_test.json");
    ASSERT_EQ(true, rc);
}

TEST_F(StencilUnitTest, read_string)
{
    std::string json_str = "{\"stringValues\":{\"classname\":\"TestClass\",\"language\":\"C++\",\"namespace\":\"testspace\"}}";
    skyloupe::Stencil stencil;

    bool rc = stencil.read_string(json_str);
    ASSERT_EQ(true, rc);
}

TEST_F(StencilUnitTest, write_string)
{
    std::string json_str_in = "{\"stringValues\":{\"classname\":\"TestClass\",\"language\":\"C++\",\"namespace\":\"testspace\"}}";
    std::string json_str_out;
    skyloupe::Stencil stencil_left, stencil_right;

    bool rc = stencil_left.read_string(json_str_in);
    ASSERT_EQ(true, rc);

    rc = stencil_left.write_string(json_str_out);
    ASSERT_EQ(true, rc);

    stencil_right.read_string(json_str_out);

    ASSERT_TRUE(google::protobuf::util::MessageDifferencer::Equivalent(stencil_left.get_proto(), stencil_right.get_proto()));
}

TEST_F(StencilUnitTest, read_file_Doesnt_Exist)
{
    skyloupe::Stencil stencil;

    bool rc = stencil.read_file("nosuchfile.json");
    ASSERT_EQ(false, rc);
}

TEST_F(StencilUnitTest, get_value_string)
{
    skyloupe::Stencil stencil;

    bool rc = stencil.read_file("stencil_unit_test.json");
    ASSERT_EQ(true, rc);

    std::string json_str;
    google::protobuf::util::Status ret = google::protobuf::util::MessageToJsonString(stencil.get_proto(), &json_str);

    ASSERT_EQ(google::protobuf::util::Status::OK, ret);

    std::string values = stencil.get_value_string("namespace", "NOT FOUND");

    ASSERT_TRUE(values == "testspace");
}

TEST_F(StencilUnitTest, get_value_int_Not_Int)
{
    skyloupe::Stencil stencil;

    bool rc = stencil.read_file("stencil_unit_test.json");
    ASSERT_EQ(true, rc);

    int value = 1234;
    bool ret = stencil.get_value_int("auto_prune_endpoints", value, 999);

    ASSERT_TRUE(ret);
    ASSERT_TRUE(value == 999);
}

TEST_F(StencilUnitTest, get_value_bool)
{
    skyloupe::Stencil stencil;

    bool rc = stencil.read_file("stencil_unit_test.json");
    ASSERT_EQ(true, rc);

    bool value = false;
    bool ret = stencil.get_value_bool("generate", value, true);

    ASSERT_TRUE(ret);
    ASSERT_TRUE(value == true);
}

TEST_F(StencilUnitTest, get_value_bool_Not_Found)
{
    skyloupe::Stencil stencil;

    bool rc = stencil.read_file("stencil_unit_test.json");
    ASSERT_EQ(true, rc);

    bool value = false;
    bool ret = stencil.get_value_bool("what_is_this", value, true);

    ASSERT_TRUE(ret);
    ASSERT_TRUE(value == true);
}

TEST_F(StencilUnitTest, get_value_bool_Not_Bool)
{
    skyloupe::Stencil stencil;

    bool rc = stencil.read_file("stencil_unit_test.json");
    ASSERT_EQ(true, rc);

    bool value = true;
    bool ret = stencil.get_value_bool("beaconIntervalMs", value, false);

    ASSERT_TRUE(ret);
    ASSERT_TRUE(value == false);
}

TEST_F(StencilUnitTest, set_value_string)
{
    skyloupe::Stencil stencil;

    bool rc = stencil.read_file("stencil_unit_test.json");
    ASSERT_EQ(true, rc);

    rc = stencil.set_value_string("namespace", "newnamespace");
    ASSERT_EQ(true, rc);

    std::string values = stencil.get_value_string("namespace", "NOT FOUND");

    ASSERT_TRUE(values == "newnamespace");
}

TEST_F(StencilUnitTest, set_value_int)
{
    skyloupe::Stencil stencil;

    bool rc = stencil.read_file("stencil_unit_test.json");
    ASSERT_EQ(true, rc);

    rc = stencil.set_value_int("a_field", 9876);
    ASSERT_EQ(true, rc);

    int val = 0;
    bool ret = stencil.get_value_int("a_field", val, 4321);

    ASSERT_TRUE(ret);
    ASSERT_TRUE(val == 4321);
}

TEST_F(StencilUnitTest, set_value_bool)
{
    skyloupe::Stencil stencil;

    bool rc = stencil.read_file("stencil_unit_test.json");
    ASSERT_EQ(true, rc);

    rc = stencil.set_value_bool("a_bool", true);
    ASSERT_EQ(true, rc);

    bool val = true;
    bool ret = stencil.get_value_bool("a_bool", val, false);

    ASSERT_TRUE(ret);
    ASSERT_TRUE(val == true);
}

TEST_F(StencilUnitTest, clear_key_string)
{
    skyloupe::Stencil stencil;

    bool rc = stencil.read_file("stencil_unit_test.json");
    ASSERT_EQ(true, rc);

    std::string values = stencil.get_value_string("language", "NOT FOUND");

    ASSERT_TRUE(values == "c++");

    rc = stencil.clear_key_string("c++");
    ASSERT_EQ(true, rc);

    values = stencil.get_value_string("c++", "NOT FOUND");

    ASSERT_TRUE(values == "NOT FOUND");
}

TEST_F(StencilUnitTest, clear_key_int)
{
    skyloupe::Stencil stencil;

    bool rc = stencil.read_file("stencil_unit_test.json");
    ASSERT_EQ(true, rc);

    int values = 0;

    bool ret = stencil.get_value_int("index", values, 999);

    ASSERT_TRUE(values == 2);

    rc = stencil.clear_key_int("index");
    ASSERT_EQ(true, rc);

    ret = stencil.get_value_int("index", values, 999);

    ASSERT_TRUE(values == 999);
}

TEST_F(StencilUnitTest, clear_key_bool)
{
    skyloupe::Stencil stencil;

    bool rc = stencil.read_file("stencil_unit_test.json");
    ASSERT_EQ(true, rc);

    bool values = false;

    bool ret = stencil.get_value_bool("generate", values, false);

    ASSERT_TRUE(values == true);

    rc = stencil.clear_key_bool("generate");
    ASSERT_EQ(true, rc);

    ret = stencil.get_value_bool("generate", values, false);

    ASSERT_TRUE(values == false);
}

TEST_F(StencilUnitTest, get_value_nomatch)
{
    skyloupe::Stencil stencil;

    bool rc = stencil.read_file("stencil_unit_test.json");
    ASSERT_EQ(true, rc);

    std::vector<std::string> values = stencil.get_value("doesntexist", "NOT FOUND");

    ASSERT_TRUE(values.size() == 1);
    ASSERT_TRUE(values[0] == "NOT FOUND");
}

TEST_F(StencilUnitTest, DISABLED_ReflectionByName)
{
    google::protobuf::Message* paMessage = &stencil_proto_;
    const google::protobuf::FieldDescriptor* paFieldDescriptorByName = paMessage->GetDescriptor()->FindFieldByName("includes");
    const google::protobuf::Reflection* pReflection = paMessage->GetReflection();

    google::protobuf::RepeatedFieldRef<std::string> ref =
        pReflection->GetRepeatedFieldRef<std::string>(*paMessage, paFieldDescriptorByName);

    for (int i = 0; i < ref.size(); i++)
    {
        std::string fld = pReflection->GetRepeatedString(*paMessage, paFieldDescriptorByName, i);

        ASSERT_EQ(fld, includes_[i]);
    }
}

TEST_F(StencilUnitTest, DISABLED_ReflectionByNumber)
{
    google::protobuf::Message* paMessage = &stencil_proto_;
    const google::protobuf::FieldDescriptor* paFieldDescriptorByNum = paMessage->GetDescriptor()->FindFieldByNumber(1000);
    const google::protobuf::Reflection* pReflection = paMessage->GetReflection();

    google::protobuf::RepeatedFieldRef<std::string> ref =
        pReflection->GetRepeatedFieldRef<std::string>(*paMessage, paFieldDescriptorByNum);

    for (int i = 0; i < ref.size(); i++)
    {
        std::string fld = pReflection->GetRepeatedString(*paMessage, paFieldDescriptorByNum, i);

        ASSERT_EQ(fld, includes_[i]);
    }
}

TEST_F(StencilUnitTest, clear)
{
    skyloupe::Stencil stencil;

    bool rc = stencil.read_file("stencil_unit_test.json");
    ASSERT_EQ(true, rc);

    rc = stencil.clear();
    ASSERT_EQ(true, rc);

#ifndef SKYTRANS_PORT
    ASSERT_EQ(stencil.get_proto().includes_size(), 0);
#endif
}

#ifndef SKYTRANS_PORT
TEST_F(StencilUnitTest, get_value_repeated)
{
    skyloupe::Stencil stencil;

    bool rc = stencil.read_file("stencil_unit_test.json");
    ASSERT_EQ(true, rc);

    std::vector<std::string> values = stencil.get_value("includes", "NOT FOUND");

    ASSERT_TRUE(values.size() == 3);

    ASSERT_TRUE(values[0] == "<string>");
    ASSERT_TRUE(values[1] == "<list>");
    ASSERT_TRUE(values[2] == "<map>");
}

TEST_F(StencilUnitTest, clear_key)
{
    skyloupe::Stencil stencil;

    bool rc = stencil.read_file("stencil_unit_test.json");
    ASSERT_EQ(true, rc);

    std::vector<std::string> values = stencil.get_value("includes", "NOT FOUND");

    ASSERT_TRUE(values.size() == 3);

    rc = stencil.clear_key("includes");
    ASSERT_EQ(true, rc);

    values = stencil.get_value("includes", "NOT FOUND");

    ASSERT_TRUE(values.size() == 1);
    ASSERT_TRUE(values[0] == "NOT FOUND");
}

TEST_F(StencilUnitTest, set_value_repeated)
{
    skyloupe::Stencil stencil;

    bool rc = stencil.read_file("stencil_unit_test.json");
    ASSERT_EQ(true, rc);

    rc = stencil.set_value("includes", "<new.h>");
    ASSERT_EQ(true, rc);

    std::vector<std::string> values = stencil.get_value("includes", "NOT FOUND");

    ASSERT_TRUE(values.size() == 4);

    ASSERT_TRUE(values[0] == "<string>");
    ASSERT_TRUE(values[1] == "<list>");
    ASSERT_TRUE(values[2] == "<map>");
    ASSERT_TRUE(values[3] == "<new.h>");
}

TEST_F(StencilUnitTest, set_get_value_member)
{
    skyloupe::Stencil stencil;

    bool rc = stencil.read_file("stencil_unit_test.json");
    ASSERT_EQ(true, rc);

    rc = stencil.set_value_member(100, "float", "m_myfloat", SW_BIG_ENDIAN_FLAG);
    ASSERT_EQ(true, rc);

    std::string type;
    std::string name;
    uint32_t endian;
    rc = stencil.get_value_member(100, type, name, endian);

    ASSERT_TRUE(rc);

    ASSERT_EQ(type, "float");
    ASSERT_EQ(name, "m_myfloat");
    ASSERT_EQ(endian, SW_BIG_ENDIAN_FLAG);
}

TEST_F(StencilUnitTest, clear_key_member)
{
    skyloupe::Stencil stencil;

    bool rc = stencil.read_file("stencil_unit_test.json");
    ASSERT_EQ(true, rc);

    rc = stencil.set_value_member(100, "float", "m_myfloat", SW_BIG_ENDIAN_FLAG);
    ASSERT_EQ(true, rc);

    rc = stencil.clear_key_member(100);

    ASSERT_TRUE(rc);

    std::string type;
    std::string name;
    uint32_t endian;
    rc = stencil.get_value_member(100, type, name, endian);

    ASSERT_FALSE(rc);
}
#endif

//TEST_F(StencilUnitTest, GetString)
//{
//    skyloupe::Stencil stencil;
//
//    stencil.set_value_string("language", "C++");
//    stencil.set_value_string("namespace", "testspace");
//    stencil.set_value_string("classname", "TestClass");
//    stencil.set_value("includes", "<header1.h>");
//    stencil.set_value("includes", "<header2.h>");
//    stencil.set_value("includes", "<header3.h>");
//
//    bool rc = stencil.set_value_member(100, "float", "m_myfloat", SW_LITTLE_ENDIAN_FLAG);
//    rc = stencil.set_value_member(200, "int16_t", "m_myint", SW_LITTLE_ENDIAN_FLAG);
//
//    rc = stencil.write_file("stencil_unit_test_out.json");
//    ASSERT_EQ(true, rc);
//}
