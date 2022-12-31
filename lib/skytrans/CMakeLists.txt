cmake_minimum_required(VERSION 3.15)

set(TARGETNAME skytrans)

set(TARGET_INC_DIR ${PROJECT_SOURCE_DIR}/include/${TARGETNAME})

set(_INC_DIRS ${TARGET_INC_DIR}
#                ${PROJECT_SOURCE_DIR}/include/stencil
                ${PROJECT_BINARY_DIR}/skytransproto
)

include_directories(${TARGETNAME} ${_INC_DIRS})

set(_SOURCES TransportClient.cpp)

set(_HEADERS ${TARGET_INC_DIR}/TransportClient.h)

add_library(${TARGETNAME} ${_SOURCES})

target_link_libraries(${TARGETNAME} skytransproto ${_GRPC_GRPCPP_UNSECURE} ${_PROTOBUF_LIBPROTOBUF})

install(TARGETS ${TARGETNAME} LIBRARY DESTINATION)
install(FILES ${_HEADERS} DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/${TARGETNAME})

install(
    ${TARGETNAME}
    EXPORT ${TARGETNAME}Config
    ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
    RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
)

export(
    EXPORT ${TARGETNAME}
    NAMESPACE skytrans::
    FILE "${CMAKE_CURRENT_BINARY_DIR}/${TARGETNAME}Config.cmake")

install(
    EXPORT ${TARGETNAME}Config
    NAMESPACE syktrans::
    DESTINATION "${CMAKE_INSTALL_DATADIR}/skytrans/cmake")
