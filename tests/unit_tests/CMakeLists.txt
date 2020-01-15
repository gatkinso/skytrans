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

set(TARGETNAME unit_tests)

include_directories(
    ${PROJECT_SOURCE_DIR}/include
    ${PROJECT_BINARY_DIR}/skytransproto)

set(UNIT_TESTS
    stencil_unit_test.cpp
    transport_unit_test.cpp)

set(UNIT_TEST_JSON stencil_unit_test.json)

add_executable(${TARGETNAME} main.cpp ${UNIT_TESTS})

target_link_libraries(${TARGETNAME} stencil GTest::GTest GTest::Main ${PLATFORM_LINK_LIBS})

gtest_discover_tests(${TARGETNAME} TEST_PREFIX skytrans_unit_test:)

add_dependencies(${TARGETNAME} stencil skytransproto)

add_custom_command(
    TARGET ${TARGETNAME} POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy
        ${PROJECT_SOURCE_DIR}/cfg/${UNIT_TEST_JSON}
        ${CMAKE_CURRENT_BINARY_DIR}/${UNIT_TEST_JSON})

