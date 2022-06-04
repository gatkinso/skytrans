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

#include <fstream>
#include "stencil.h"
#include "google/protobuf/util/json_util.h"
#include "google/protobuf/reflection.h"

namespace skyloupe
{

bool Stencil::read_file(const std::string& pathname)
{
    if (pathname.length() == 0)
    {
        return false;
    }

    try
    {
        std::ifstream file(pathname.c_str(), std::ios::in | std::ios::ate);

        if (file.fail()) 
        {
            return false;
        }

        size_t size = (size_t)file.tellg();

        char* memblock = new char[size+1];
        memset(memblock, 0, size+1);

        file.seekg(0, std::ios::beg);
        file.read(memblock, size);
        file.close();

        std::string str(memblock);

        auto ret = read_string(str);

        delete[] memblock;
        
        if (ret == false)
        {
            stencil_proto_.Clear();
            return false;
        }
    }
    catch (std::ifstream::failure e)
    {
        return false;
    }

    return true;
}

bool Stencil::write_file(const std::string& pathname) const
{
    if (pathname.length() == 0 || stencil_proto_.IsInitialized() == false)
    {
        return false;
    }

    try
    {
        std::string json_str;
        auto ret = write_string(json_str);

        if (ret == false)
        {
            return false;
        }

        std::ofstream file(pathname, std::ios::out | std::ios::trunc);

        if (file.fail())
        {
            return false;
        }

        file.write(json_str.c_str(), json_str.size());

        file.close();
    }
    catch (std::ofstream::failure e)
    {
        return false;
    }

    return true;
}

bool Stencil::read_string(const std::string& json_str)
{
    if (json_str.length() == 0)
    {
        return false;
    }

    try
    {
        auto ret = google::protobuf::util::JsonStringToMessage(json_str, &stencil_proto_);

        if (false == ret.ok())
        {
            stencil_proto_.Clear();
            return false;
        }
    }
    catch (std::ifstream::failure e)
    {
        return false;
    }

    return true;
}

bool Stencil::write_string(std::string& json_str) const
{
    if (stencil_proto_.IsInitialized() == false)
    {
        return false;
    }

    try
    {
        auto ret = google::protobuf::util::MessageToJsonString(stencil_proto_, &json_str);

        if (false == ret.ok())
        {
            return false;
        }
    }
    catch (std::ofstream::failure e)
    {
        return false;
    }

    return true;
}

std::vector<std::string> Stencil::get_value(const::std::string& key, const std::string nomatch)
{
    std::vector<std::string> values;

    if (key.empty() || stencil_proto_.IsInitialized() == false)
    {
        values.push_back(nomatch);
        return values;
    }

    const google::protobuf::Message* pMessage = &stencil_proto_;
    const google::protobuf::Descriptor* pDescriptor = pMessage->GetDescriptor();

    if (pDescriptor == nullptr)
    {
        values.push_back(nomatch);
        return values;
    }

    const google::protobuf::FieldDescriptor* pFieldDescriptor = pDescriptor->FindFieldByName(key);

    if (pFieldDescriptor != nullptr)
    {
        const google::protobuf::Reflection* pReflection = pMessage->GetReflection();
        if (pReflection == nullptr)
        {
            values.push_back(nomatch);
            return values;
        }

        if (true == pFieldDescriptor->is_repeated())
        {
            google::protobuf::RepeatedFieldRef<std::string> ref =
                pReflection->GetRepeatedFieldRef<std::string>(*pMessage, pFieldDescriptor);

            for (int i = 0; i < ref.size(); i++)
            {
                values.push_back(pReflection->GetRepeatedString(*pMessage, pFieldDescriptor, i));
            }
        }
        else
        {
            if (false == pReflection->HasField(*pMessage, pFieldDescriptor))
            {
                values.push_back(nomatch);
                return values;
            }

            values.push_back(pReflection->GetString(*pMessage, pFieldDescriptor));
        }
    }
    else
    {
        values.push_back(nomatch);
    }

    if (values.size() == 0)
    {
        values.push_back(nomatch);
    }

    return values;
}

std::string Stencil::get_value_string(const::std::string& key, const std::string nomatch)
{
    std::string value(nomatch);

    if (key.empty() || stencil_proto_.IsInitialized() == false)
    {
        return nomatch;
    }
    
    for (auto val : stencil_proto_.string_values())
    {
        if (val.first == key)
        {
            value = val.second;
            break;
        }
    }

    return value;
}

bool Stencil::get_value_int(const::std::string& key, int& value, int nomatch)
{
    value = nomatch;

    if (key.empty() || stencil_proto_.IsInitialized() == false)
    {
        return false;
    }

    for (auto val : stencil_proto_.int_values())
    {
        if (val.first == key)
        {
            value = val.second;
            break;
        }
    }

    return true;
}

bool Stencil::get_value_bool(const::std::string& key, bool& value, bool nomatch)
{
    value = nomatch;

    if (key.empty() || stencil_proto_.IsInitialized() == false)
    {
        return false;
    }

    for (auto val : stencil_proto_.bool_values())
    {
        if (val.first == key)
        {
            value = val.second;
            break;
        }
    }

    return true;
}

bool Stencil::get_value_uint(const::std::string& key, uint32_t& value, uint32_t nomatch)
{
    value = nomatch;

    if (key.empty() || stencil_proto_.IsInitialized() == false)
    {
        return false;
    }

    for (auto val : stencil_proto_.uint_values())
    {
        if (val.first == key)
        {
            value = val.second;
            break;
        }
    }

    return true;
}

bool Stencil::get_value_int64(const::std::string& key, int64_t& value, int64_t nomatch)
{
    value = nomatch;

    if (key.empty() || stencil_proto_.IsInitialized() == false)
    {
        return false;
    }

    for (auto val : stencil_proto_.int64_values())
    {
        if (val.first == key)
        {
            value = val.second;
            break;
        }
    }

    return true;
}

bool Stencil::get_value_uint64(const::std::string& key, uint64_t& value, uint64_t nomatch)
{
    value = nomatch;

    if (key.empty() || stencil_proto_.IsInitialized() == false)
    {
        return false;
    }

    for (auto val : stencil_proto_.uint64_values())
    {
        if (val.first == key)
        {
            value = val.second;
            break;
        }
    }

    return true;
}


bool Stencil::set_value(const::std::string& key, const std::string& value)
{
    if (key.empty() || stencil_proto_.IsInitialized() == false)
    {
        return false;
    }

    google::protobuf::Message* pMessage = &stencil_proto_;
    const google::protobuf::Descriptor* pDescriptor = pMessage->GetDescriptor();

    if (pDescriptor == nullptr)
    {
        return false;
    }

    const google::protobuf::FieldDescriptor* pFieldDescriptor = pDescriptor->FindFieldByName(key);

    if (pFieldDescriptor != nullptr)
    {
        const google::protobuf::Reflection* pReflection = pMessage->GetReflection();
        if (pReflection == nullptr)
        {
            return false;
        }

        if (true == pFieldDescriptor->is_repeated())
        {
            pReflection->AddString(pMessage, pFieldDescriptor, value);
        }
        else
        {
            pReflection->SetString(pMessage, pFieldDescriptor, value);
        }
    }

    return true;
}

bool Stencil::set_value_string(const::std::string& key, const std::string& value)
{
    if (key.empty() || stencil_proto_.IsInitialized() == false)
    {
        return false;
    }

    ::google::protobuf::Map<std::string, std::string>& mappy = *stencil_proto_.mutable_string_values();
    mappy[key] = value;

    return true;
}

bool Stencil::set_value_int(const::std::string& key, int value)
{
    if (key.empty() || stencil_proto_.IsInitialized() == false)
    {
        return false;
    }

    ::google::protobuf::Map<std::string, int>& mappy = *stencil_proto_.mutable_int_values();
    mappy[key] = value;

    return true;
}

bool Stencil::set_value_uint(const::std::string& key, uint32_t value)
{
    if (key.empty() || stencil_proto_.IsInitialized() == false)
    {
        return false;
    }

    ::google::protobuf::Map<std::string, uint32_t>& mappy = *stencil_proto_.mutable_uint_values();
    mappy[key] = value;

    return true;
}

bool Stencil::set_value_int64(const::std::string& key, int64_t value)
{
    if (key.empty() || stencil_proto_.IsInitialized() == false)
    {
        return false;
    }

    ::google::protobuf::Map<std::string, int64_t>& mappy = *stencil_proto_.mutable_int64_values();
    mappy[key] = value;

    return true;
}

bool Stencil::set_value_uint64(const::std::string& key, uint64_t value)
{
    if (key.empty() || stencil_proto_.IsInitialized() == false)
    {
        return false;
    }

    ::google::protobuf::Map<std::string, uint64_t>& mappy = *stencil_proto_.mutable_uint64_values();
    mappy[key] = value;

    return true;
}

bool Stencil::set_value_bool(const::std::string& key, bool value)
{
    if (key.empty() || stencil_proto_.IsInitialized() == false)
    {
        return false;
    }
    
    ::google::protobuf::Map<std::string, bool>& mappy = *stencil_proto_.mutable_bool_values();
    mappy[key] = value;

    return true;
}

bool Stencil::clear()
{
    stencil_proto_.Clear();

    return true;
}

bool Stencil::clear_key(const::std::string& key)
{
    if (key.empty() || stencil_proto_.IsInitialized() == false)
    {
        return false;
    }

    google::protobuf::Message* pMessage = &stencil_proto_;
    const google::protobuf::Descriptor* pDescriptor = pMessage->GetDescriptor();

    if (pDescriptor == nullptr)
    {
        return false;
    }

    const google::protobuf::FieldDescriptor* pFieldDescriptor = pDescriptor->FindFieldByName(key);

    if (pFieldDescriptor != nullptr)
    {
        const google::protobuf::Reflection* pReflection = pMessage->GetReflection();
        if (pReflection == nullptr)
        {
            return false;
        }

        pReflection->ClearField(pMessage, pFieldDescriptor);
    }

    return true;
}

bool Stencil::clear_key_string(const::std::string& key)
{
    if (key.empty() || stencil_proto_.IsInitialized() == false)
    {
        return false;
    }

    stencil_proto_.mutable_string_values()->erase(key);

    return true;
}

bool Stencil::clear_key_int(const::std::string& key)
{
    if (key.empty() || stencil_proto_.IsInitialized() == false)
    {
        return false;
    }

    stencil_proto_.mutable_int_values()->erase(key);

    return true;
}

bool Stencil::clear_key_bool(const::std::string& key)
{
    if (key.empty() || stencil_proto_.IsInitialized() == false)
    {
        return false;
    }

    stencil_proto_.mutable_bool_values()->erase(key);

    return true;
}

}


