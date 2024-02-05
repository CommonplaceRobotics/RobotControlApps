SET(CMAKE_SYSTEM_NAME Linux)
SET(CMAKE_SYSTEM_VERSION 1)
SET(CMAKE_SYSTEM_PROCESSOR arm)

# Specify the cross compiler
# The compiler from our toolchain
SET(CMAKE_C_COMPILER /opt/cross-pi-gcc/bin/arm-linux-gnueabihf-gcc)
SET(CMAKE_CXX_COMPILER /opt/cross-pi-gcc/bin/arm-linux-gnueabihf-g++)
# The installed compiler: make sure it uses a supported glibc!
#SET(CMAKE_C_COMPILER /usr/bin/arm-linux-gnueabihf-gcc-10)
#SET(CMAKE_CXX_COMPILER /usr/bin/arm-linux-gnueabihf-g++-10)

# Specify the Sysroot folder
SET(CMAKE_SYSROOT /opt/sysroots/raspberrypi)
SET(CMAKE_INSTALL_PREFIX ${CMAKE_SYSROOT} CACHE PATH "")
include_directories(${CMAKE_SYSROOT}/usr/include/arm-linux-gnueabihf)

# Set up pkg_config search to
set(ENV{PKG_CONFIG_DIR} "")
set(ENV{PKG_CONFIG_LIBDIR} "${CMAKE_SYSROOT}/usr/lib/pkgconfig:${CMAKE_SYSROOT}/usr/share/pkgconfig")
set(ENV{PKG_CONFIG_SYSROOT_DIR} ${CMAKE_SYSROOT})

# Search for programs only in the build host directories
SET(CMAKE_FIND_ROOT_PATH_MODE_PROGRAM NEVER)

# Search for libraries and headers only in the target directories
SET(CMAKE_FIND_ROOT_PATH_MODE_LIBRARY ONLY)
SET(CMAKE_FIND_ROOT_PATH_MODE_INCLUDE ONLY)

# legacy, likely for RPi3
#SET(CMAKE_C_FLAGS "-mcpu=cortex-a53 -mfpu=neon-vfpv4 -mfloat-abi=hard ${COMMON_FLAGS}")
# for RPi4
SET(CMAKE_C_FLAGS "-mcpu=cortex-a72 -mfloat-abi=hard -mfpu=neon-fp-armv8 -mtune=cortex-a72 ${COMMON_FLAGS}")
SET(CMAKE_CXX_FLAGS "${CMAKE_C_FLAGS}")

# Workaround (MAB)
SET(_POSIX_PATH_MAX 4096)
