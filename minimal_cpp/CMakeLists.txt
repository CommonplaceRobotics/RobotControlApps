###############################################################################
# This is a sample CMakeLists.txt. Replace all instances of "minimalapp" with
# the name of your app.
# If necessary add your source files and libraries in the Target Definition
# section. Define files to copy to the output in the Copy Data section.
###############################################################################
project(minimalapp
    LANGUAGES C CXX
)

cmake_minimum_required (VERSION 3.16)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(THREADS_PREFER_PTHREAD_FLAG ON)
find_package(Threads REQUIRED)

option(BUILD_TESTS "Compile tests" ON)

###############################################################################
# Generating gRPC C++-Sources
###############################################################################

include(cmake/gRPC.cmake)
file(GLOB PROTOS
    "${CMAKE_CURRENT_SOURCE_DIR}/protos/*.proto"
)

set(PROTO_SRC_DIR "${CMAKE_CURRENT_BINARY_DIR}/generated_protos")

protobuf_generate_cpp(PROTO_SRCS PROTO_HDRS ${PROTO_SRC_DIR} ${PROTOS})
grpc_generate_cpp(GRPC_SRCS GRPC_HDRS ${PROTO_SRC_DIR} ${PROTOS})

list(APPEND INCLUDE_DIRS
    ${PROTO_SRC_DIR})

list(APPEND GRPC_SOURCES
    ${GRPC_SRCS}
    ${PROTO_SRCS})

list(APPEND GRPC_LIBS
    ${_REFLECTION}
    ${_GRPC_GRPCPP}
    ${_PROTOBUF_LIBPROTOBUF})

###############################################################################
# Target definition - define the app source and dependencies here!
###############################################################################

file(GLOB APP_SOURCES src/*.cpp)
file(GLOB APP_SOURCES_DATATYPES src/DataTypes/*.cpp)
file(GLOB SOURCES_tests_DataTypes tests/DataTypes/*.cpp)

add_executable(minimalapp
    ${GRPC_SOURCES}
    ${APP_SOURCES}
    ${APP_SOURCES_DATATYPES})

target_include_directories(minimalapp
    PUBLIC
    ${INCLUDE_DIRS})

target_link_libraries(minimalapp
    PUBLIC
    Threads::Threads
    ${GRPC_LIBS})

###############################################################################
# Copy data to binary output folder
###############################################################################

list(APPEND APP_DATA
    "${CMAKE_CURRENT_SOURCE_DIR}/rcapp.xml"
    "${CMAKE_CURRENT_SOURCE_DIR}/ui.xml")

# copy to <target-build-dir>/Data/Apps
add_custom_command(TARGET minimalapp POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy_if_different
    ${APP_DATA} ${PROJECT_BINARY_DIR}/)

###############################################################################
# Unit Tests
###############################################################################

# Avoid warning about DOWNLOAD_EXTRACT_TIMESTAMP in CMake 3.24:
if (CMAKE_VERSION VERSION_GREATER_EQUAL "3.24.0")
	cmake_policy(SET CMP0135 NEW)
endif()

if (BUILD_TESTS)
    include(FetchContent)
    # googletest is downloaded and compiled automatically
    FetchContent_Declare(
        googletest
        # Specify the commit you depend on and update it regularly.
        URL https://github.com/google/googletest/archive/refs/tags/v1.13.0.zip
    )

    enable_testing()
    include(GoogleTest)

    # For Windows: Prevent overriding the parent project's compiler/linker settings
    set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)
    FetchContent_MakeAvailable(googletest)

    file(GLOB APP_SOURCES_without_main src/AppClient.cpp src/MinimalClient.cpp) # include all *.cpp files except main.cpp for the unit tests

    add_executable(minimalapp_Tests
        ${GRPC_SOURCES}
        ${APP_SOURCES_without_main}
        ${APP_SOURCES_DATATYPES}

        ${SOURCES_tests_DataTypes}
    )

    target_include_directories(minimalapp_Tests PUBLIC
        ${INCLUDE_DIRS})

    target_link_libraries(minimalapp_Tests PUBLIC
        GTest::gtest_main
        GTest::gmock
        Threads::Threads
        ${GRPC_LIBS})

    if(CMAKE_CROSSCOMPILING) # not when cross compiling, this command tries to execute the binary!
        gtest_discover_tests(minimalapp_Tests)
    endif()
endif()
