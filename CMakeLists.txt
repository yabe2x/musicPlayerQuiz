cmake_minimum_required(VERSION 3.10)
project(musicPlayerQuiz)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Find required packages
find_package(CURL REQUIRED)
find_package(SDL2 REQUIRED)

# Add quiz executable
add_executable(quiz
    main.cpp
    quiz.cpp
)

# Add server executable
add_executable(server
    server.cpp
    quiz.cpp
)

# Include directories for both executables
target_include_directories(quiz PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}/include
    ${CURL_INCLUDE_DIRS}
    ${SDL2_INCLUDE_DIRS}
)

target_include_directories(server PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}/include
    ${CURL_INCLUDE_DIRS}
    ${SDL2_INCLUDE_DIRS}
)

# Link libraries for both executables
target_link_libraries(quiz PRIVATE
    ${CURL_LIBRARIES}
    ${SDL2_LIBRARIES}
)

target_link_libraries(server PRIVATE
    ${CURL_LIBRARIES}
    ${SDL2_LIBRARIES}
) 