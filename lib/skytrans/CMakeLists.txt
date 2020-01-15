cmake_minimum_required(VERSION 3.15)

set(TARGETNAME skytrans)

set(_SOURCES skytrans.cpp
)

add_library(${TARGETNAME} ${_SOURCES})

target_link_libraries(${TARGETNAME} skytransproto ${_GRPC_GRPCPP_UNSECURE} ${_PROTOBUF_LIBPROTOBUF})
