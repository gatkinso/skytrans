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

set(TARGETNAME stencil)

add_library(${TARGETNAME} STATIC)

set(TARGET_INC_DIR ${PROJECT_SOURCE_DIR}/include/${TARGETNAME})
set(_INC_DIRS ${TARGET_INC_DIR}
              ${PROJECT_SOURCE_DIR}/include/${TARGETNAME}
              ${PROJECT_BINARY_DIR}/skytransproto)

include_directories(${TARGETNAME} ${_INC_DIRS})

set(_SOURCES stencil.cpp)
set(_HEADERS ${TARGET_INC_DIR}/stencil.h)

target_sources(${TARGETNAME}
    PRIVATE ${_SOURCES}
    PUBLIC FILE_SET HEADERS
    BASE_DIRS ${TARGET_INC_DIR}
    FILES ${_HEADERS}
)

add_dependencies(${TARGETNAME} skytransproto)

target_link_libraries(${TARGETNAME} skytransproto)

install(TARGETS
    ${TARGETNAME}
    EXPORT skytransConfig
    ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
    RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
    FILE_SET HEADERS DESTINATION  ${CMAKE_INSTALL_INCLUDEDIR}/${TARGETNAME}
)

export(TARGETS
    ${TARGETNAME}
    NAMESPACE skytrans::
    FILE "${CMAKE_CURRENT_BINARY_DIR}/skytransConfig.cmake"
)
