cmake_minimum_required(VERSION 3.15)

set(TARGETNAME client++)

set(_SOURCES client++.cpp
)

add_library(${TARGETNAME} ${_SOURCES})

target_link_libraries(${TARGETNAME} skyproto ${_GRPC_GRPCPP_UNSECURE} ${_PROTOBUF_LIBPROTOBUF})
