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

        if (ret != google::protobuf::util::Status::OK)
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

        if (ret != google::protobuf::util::Status::OK)
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

    bool done = false;
    for (auto iter = stencil_proto_.mutable_string_values()->begin(); iter != stencil_proto_.mutable_string_values()->end(); iter++)
    {
        auto val = iter->first;
        if (val == key)
        {
            iter->second = value;
            done = true;
        }
    }

    if (done == false)
    {
        google::protobuf::MapPair < std::string, std::string > pair(key, value);
        stencil_proto_.mutable_string_values()->insert(pair);
    }

    return true;
}

bool Stencil::set_value_int(const::std::string& key, int value)
{
    if (key.empty() || stencil_proto_.IsInitialized() == false)
    {
        return false;
    }

    auto map = *stencil_proto_.mutable_int_values();
    map[key] = value;

    return true;
}

bool Stencil::set_value_bool(const::std::string& key, bool value)
{
    if (key.empty() || stencil_proto_.IsInitialized() == false)
    {
        return false;
    }

    bool done = false;
    for (auto iter = stencil_proto_.mutable_bool_values()->begin(); iter != stencil_proto_.mutable_bool_values()->end(); iter++)
    {
        auto val = iter->first;
        if (val == key)
        {
            iter->second = value;
            done = true;
        }
    }

    if (done == false)
    {
        google::protobuf::MapPair < std::string, bool > pair(key, value);
        stencil_proto_.mutable_bool_values()->insert(pair);
    }

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

// bool Stencil::set_value_member(uint32_t key, const std::string& type, const std::string& name, uint32_t endian)
// {
//     if (stencil_proto_.IsInitialized() == false)
//     {
//         return false;
//     }

//     auto iter = stencil_proto_.mutable_members()->find(key);
//     if (iter == stencil_proto_.members().end())
//     {
//         (*stencil_proto_.mutable_members())[key].set_type(type);
//         (*stencil_proto_.mutable_members())[key].set_name(name);
//         (*stencil_proto_.mutable_members())[key].set_endian(endian);
//     }
//     else
//     {
//         iter->second.set_type(type);
//         iter->second.set_name(name);
//         iter->second.set_endian(endian);
//     }

//     return true;
// }

// bool Stencil::get_value_member(uint32_t key, std::string& type_val, std::string& name_val, uint32_t& endian_val)
// {
//     if (stencil_proto_.IsInitialized() == false)
//     {
//         return false;
//     }

//     auto iter = stencil_proto_.mutable_members()->find(key);
//     if (iter == stencil_proto_.members().end())
//     {
//         return false;
//     }
//     else
//     {
//         type_val = iter->second.type();
//         name_val = iter->second.name();
//         endian_val = iter->second.endian();
//     }

//     return true;
// }

// bool Stencil::clear_key_member(uint32_t key)
// {
//     size_t ret = stencil_proto_.mutable_members()->erase(key);
//     if (ret == 0)
//         return false;
//     return true;
// }

}

