cmake_minimum_required(VERSION 3.16)
project(precipitated_silica_mc3d VERSION 0.1.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

add_library(mc3d_core
    src/SimulationBox.cpp
    src/NeighborList.cpp
    src/MonteCarlo.cpp
    src/DLCA.cpp
    src/Observables.cpp
    src/PeriodicCellList.cpp
    src/FractalDimension.cpp
    src/MassRadius.cpp
)
target_include_directories(mc3d_core PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/include)
if(CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")
    target_compile_options(mc3d_core PRIVATE -Wall -Wextra -Wpedantic)
endif()

add_executable(mc3d_geometry_tests tests/test_geometry.cpp)
target_link_libraries(mc3d_geometry_tests PRIVATE mc3d_core)
add_executable(mc3d_interaction_tests tests/test_interactions.cpp)
target_link_libraries(mc3d_interaction_tests PRIVATE mc3d_core)
add_executable(mc3d_metropolis_tests tests/test_metropolis.cpp)
target_link_libraries(mc3d_metropolis_tests PRIVATE mc3d_core)
add_executable(mc3d_network_tests tests/test_network.cpp)
target_link_libraries(mc3d_network_tests PRIVATE mc3d_core)

if(CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")
    target_compile_options(mc3d_geometry_tests PRIVATE -Wall -Wextra -Wpedantic)
    target_compile_options(mc3d_interaction_tests PRIVATE -Wall -Wextra -Wpedantic)
    target_compile_options(mc3d_metropolis_tests PRIVATE -Wall -Wextra -Wpedantic)
    target_compile_options(mc3d_network_tests PRIVATE -Wall -Wextra -Wpedantic)
endif()

enable_testing()
add_test(NAME geometry COMMAND mc3d_geometry_tests)
add_test(NAME interactions COMMAND mc3d_interaction_tests)
add_test(NAME metropolis COMMAND mc3d_metropolis_tests)
add_test(NAME network COMMAND mc3d_network_tests)
