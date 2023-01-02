#
#  Copyright (C) 2017 Skyloupe, LLC
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

set(TARGETNAME skytransproto)

set(PROTO_FILES
    example
    stencil
    transport
)

set(PROTO_DIR "${PROJECT_BINARY_DIR}/${TARGETNAME}")

if(UNIX)
    file(MAKE_DIRECTORY ${PROTO_DIR}) 
endif(UNIX)

foreach(PROTO ${PROTO_FILES})
    #cpp Protobuf
    add_custom_command(
        OUTPUT  ${PROTO_DIR}/${PROTO}.pb.h
                ${PROTO_DIR}/${PROTO}.pb.cc
        DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/${PROTO}.proto
        COMMAND ${PROTOBUF_PROTOC_EXECUTABLE}
        ARGS    ${CMAKE_CURRENT_SOURCE_DIR}/${PROTO}.proto
                --cpp_out=${PROTO_DIR}
                --proto_path=${CMAKE_CURRENT_SOURCE_DIR}
    )
    set(PROTOCPP_HEADER_RESULTS ${PROTOCPP_HEADER_RESULTS}
        ${PROTO_DIR}/${PROTO}.pb.h
    )
    set(PROTOCPP_RESULTS ${PROTOCPP_RESULTS}
        ${PROTO_DIR}/${PROTO}.pb.cc
        ${PROTO_DIR}/${PROTO}.pb.h
    )

    #cpp gRPC
    add_custom_command(
        OUTPUT  ${PROTO_DIR}/${PROTO}.grpc.pb.h
                ${PROTO_DIR}/${PROTO}.grpc.pb.cc
        DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/${PROTO}.proto
        COMMAND ${PROTOBUF_PROTOC_EXECUTABLE}
        ARGS    ${CMAKE_CURRENT_SOURCE_DIR}/${PROTO}.proto
                --grpc_out=${PROTO_DIR}
                --proto_path=${CMAKE_CURRENT_SOURCE_DIR}
                --plugin=protoc-gen-grpc=${_GRPC_CPP_PLUGIN_EXECUTABLE}
    )
    set(PROTOCPPgrpc_HEADER_RESULTS ${PROTOCPPgrpc_HEADER_RESULTS}
        ${PROTO_DIR}/${PROTO}.grpc.pb.h
    )
    set(PROTOCPPgrpc_RESULTS ${PROTOCPPgrpc_RESULTS}
        ${PROTO_DIR}/${PROTO}.grpc.pb.cc
        ${PROTO_DIR}/${PROTO}.grpc.pb.h
    )

    #python
    add_custom_command(
        OUTPUT  ${PROTO_DIR}/${PROTO}_pb2.py
        DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/${PROTO}.proto
        COMMAND ${PROTOBUF_PROTOC_EXECUTABLE}
        ARGS    --python_out=${PROTO_DIR}
                --proto_path=${CMAKE_CURRENT_SOURCE_DIR}
                ${CMAKE_CURRENT_SOURCE_DIR}/${PROTO}.proto
    )
    set(PROTOPY_RESULTS ${PROTOPY_RESULTS}
        ${PROTO_DIR}/${PROTO}_pb2.py
    )

    #python -m grpc.tools.protoc --python_out=$OUT --grpc_python_out=$OUT --proto_path=$PROTO_PATH $PROTO_FILE
    #python gRPC
    add_custom_command(
        OUTPUT  ${PROTO_DIR}/${PROTO}_pb2_grpc.py
        DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/${PROTO}.proto
        #COMMAND ${PROTOBUF_PROTOC_EXECUTABLE}
        COMMAND python
        ARGS    -m grpc.tools.protoc
                --grpc_python_out=${PROTO_DIR}
                --python_out=${PROTO_DIR}
                --proto_path=${CMAKE_CURRENT_SOURCE_DIR}
                --plugin=protoc-gen-grpc=${_GRPC_PY_PLUGIN_EXECUTABLE}
                ${CMAKE_CURRENT_SOURCE_DIR}/${PROTO}.proto
    )
    set(PROTOPY_RESULTS ${PROTOPY_RESULTS}
        ${PROTO_DIR}/${PROTO}_pb2_grpc.py
    )

    #go
    add_custom_command(
        OUTPUT  ${PROTO_DIR}/${PROTO}.pb.go
        DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/${PROTO}.proto
        COMMAND ${PROTOBUF_PROTOC_EXECUTABLE}
        ARGS    --proto_path=${CMAKE_CURRENT_SOURCE_DIR} --go_out=${PROTO_DIR}
                ${CMAKE_CURRENT_SOURCE_DIR}/${PROTO}.proto
    )
    set(PROTOGO_RESULTS ${PROTOGO_RESULTS}
        ${PROTO_DIR}/${PROTO}.pb.go
    )

    #go gRPC
    #protoc --go_out=. --go_opt=paths=source_relative \
    #--go-grpc_out=. --go-grpc_opt=paths=source_relative \
    #routeguide/route_guide.proto
    add_custom_command(
        OUTPUT  ${PROTO_DIR}/${PROTO}.grpc.pb.go
        DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/${PROTO}.proto
        COMMAND ${PROTOBUF_PROTOC_EXECUTABLE}
        ARGS    --proto_path=${CMAKE_CURRENT_SOURCE_DIR} --go_out=${PROTO_DIR} --go-grpc_out=${PROTO_DIR}
                ${CMAKE_CURRENT_SOURCE_DIR}/${PROTO}.proto
    )
    set(PROTOGO_RESULTS ${PROTOGO_RESULTS}
        ${PROTO_DIR}/${PROTO}.grpc.pb.go
    )
endforeach(PROTO)

add_custom_target(runPy ALL DEPENDS ${PROTOPY_RESULTS})
add_custom_target(runGo ALL DEPENDS ${PROTOGO_RESULTS})

add_library(${TARGETNAME} STATIC ${PROTOCPP_RESULTS} ${PROTOCPPgrpc_RESULTS})

foreach(header in PROTOCPP_HEADER_RESULTS)
    set_target_properties(${TARGETNAME} PROPERTIES PUBLIC_HEADER ${header})
endforeach()

foreach(header in PROTOCPPgrpc_HEADER_RESULTS)
    set_target_properties(${TARGETNAME} PROPERTIES PUBLIC_HEADER ${header})
endforeach()

if(MSVC)
    target_compile_options(${TARGETNAME} PRIVATE "/wd4800")
endif(MSVC)

target_link_libraries(${TARGETNAME} ${_GRPC_GRPCPP_UNSECURE} ${PROTOBUF_LIBRARIES})

install(TARGETS
    ${TARGETNAME}
    EXPORT skytransConfig
    ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
    RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
    PUBLIC_HEADER DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/skyproto
)

export(TARGETS
    ${TARGETNAME}
    NAMESPACE skytrans::
    FILE "${CMAKE_CURRENT_BINARY_DIR}/skytransConfig.cmake"
)

