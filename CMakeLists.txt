#
#  Copyright (C) 2018 Skyloupe, LLC
#
#  Licensed under the Apache License, Version 2.0 (the "License").
#  You may not use this file except in compliance with the License.
#  A copy of the License is located at
#
#  https://www.apache.org/licenses/LICENSE-2.0.html
#
#  or in the "license" file accompanying this file. This file is distributed
#  on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
#  express or implied. See the License for the specific language governing
#  permissions and limitations under the License.
#
cmake_minimum_required(VERSION 3.15)

project(skytrans)

include (CTest)

#option(SKYTRANS_PREFIX_PATH "Skytrans prefix search path")
set(CMAKE_PREFIX_PATH ${SKYTRANS_PREFIX_PATH})

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

#foreach(path ${CMAKE_PREFIX_PATH})
    message("Prefix Path: " ${SKYTRANS_PREFIX_PATH})
#endforeach(path)

if(MSVC)
    # Set compiler options.
    set(configs
        CMAKE_C_FLAGS_DEBUG
        CMAKE_C_FLAGS_MINSIZEREL
        CMAKE_C_FLAGS_RELEASE
        CMAKE_C_FLAGS_RELWITHDEBINFO
        CMAKE_CXX_FLAGS_DEBUG
        CMAKE_CXX_FLAGS_MINSIZEREL
        CMAKE_CXX_FLAGS_RELEASE
        CMAKE_CXX_FLAGS_RELWITHDEBINFO
    )

    foreach(config ${configs})
        if(${config} MATCHES "/MD")
            string(REGEX REPLACE "/MD" "/MT" ${config} "${${config}}")
        endif()
    endforeach()
endif(MSVC)

find_package(Protobuf REQUIRED)
include_directories(${PROTOBUF_INCLUDE_DIRS})

find_package(gRPC CONFIG REQUIRED)

set(_GRPC_GRPCPP_UNSECURE gRPC::grpc++_unsecure)
set(_GRPC_CPP_PLUGIN_EXECUTABLE $<TARGET_FILE:gRPC::grpc_cpp_plugin>)
set(_GRPC_PY_PLUGIN_EXECUTABLE $<TARGET_FILE:gRPC::grpc_python_plugin>)
set(_GRPC_GO_PLUGIN_EXECUTABLE protoc-gen-go)

enable_testing()
find_package(GTest REQUIRED)

if(UNIX)
    add_definitions(-DAPPLE)
endif(UNIX)

if(UNIX AND NOT APPLE)
    set(LINUX TRUE)
    add_definitions(-DLINUX)
endif(UNIX AND NOT APPLE)

add_subdirectory(lib)
add_subdirectory(bin)
add_subdirectory(tests/unit_tests)
