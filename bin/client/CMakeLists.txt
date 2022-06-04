cmake_minimum_required(VERSION 3.15)

set(TARGETNAME client)

set(_SOURCES main.cpp)

set(_INC_DIRS ${TARGET_INC_DIR}
              ${PROJECT_SOURCE_DIR}/include/skytrans
              ${PROJECT_SOURCE_DIR}/include/stencil
              ${PROJECT_BINARY_DIR}/skytransproto)

include_directories(${TARGETNAME} ${_INC_DIRS})

add_executable(${TARGETNAME} ${_SOURCES})

target_link_libraries(${TARGETNAME} stencil skytransproto skytrans ${_GRPC_GRPCPP_UNSECURE} ${_PROTOBUF_LIBPROTOBUF})
install(TARGETS ${TARGETNAME} RUNTIME DESTINATION)
