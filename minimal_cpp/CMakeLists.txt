###############################################################################
# This is a sample CMakeLists.txt. Replace all instances of "minimalapp" with
# the name of your app.
# If necessary add your source files and libraries in the Target Definition
# section. Define files to copy to the output in the Copy Data section.
###############################################################################
cmake_minimum_required (VERSION 3.16)

# Also update the version in rcapp.xml!
project(minimalapp
	VERSION 1.1.0
    LANGUAGES C CXX
)
# Life cycle information for the SBOM
set(RELEASE_DATE "2026-05-08")
set(SUPPORT_PERIOD_END "2000-00-00") # TODO: define support period
set(END_OF_LIFE "2000-00-00") # TODO: define end of life
configure_file(sbomify.json.in sbomify.json)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(THREADS_PREFER_PTHREAD_FLAG ON)
find_package(Threads REQUIRED)

add_subdirectory(../api_cpp ${CMAKE_BINARY_DIR}/api_cpp)

###############################################################################
# Target definition - define the app source and dependencies here!
###############################################################################

file(GLOB APP_SOURCES src/*.cpp)

add_executable(minimalapp
    ${APP_SOURCES}
)

target_include_directories(minimalapp
    PUBLIC
    ${INCLUDE_DIRS}
)

target_link_libraries(minimalapp
    PUBLIC
    Threads::Threads
    iRCApp
)

if(UNIX OR MINGW)
	target_compile_options(minimalapp PRIVATE
		PRIVATE
		# More warnings:
		-Wall -Wextra -pedantic
		# More errors:
		-Werror=parentheses -Werror=return-type
    )
elseif(MSVC)
endif()

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
