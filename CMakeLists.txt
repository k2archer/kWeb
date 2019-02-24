cmake_minimum_required(VERSION 3.10)
project(kWeb)

# 指定 C++ 标准版本
set(CMAKE_CXX_STANDARD 11)

# 指定输出目录
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ./build/)

include_directories(include)

add_executable(kWeb
        include/k_socket.h
        include/k_unit_test.h
        include/k_web.h
        include/socklib.h

        src/kWeb.cc)

TARGET_LINK_LIBRARIES(kWeb pthread)