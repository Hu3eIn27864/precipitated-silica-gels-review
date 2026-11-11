if(NOT DEFINED MC3D_EXECUTABLE OR NOT DEFINED OUTPUT_PREFIX)
    message(FATAL_ERROR "MC3D_EXECUTABLE and OUTPUT_PREFIX must be provided")
endif()

execute_process(
    COMMAND "${MC3D_EXECUTABLE}" 12 12.0 12345 1 30000 "${OUTPUT_PREFIX}"
    RESULT_VARIABLE run_result
    OUTPUT_VARIABLE run_stdout
    ERROR_VARIABLE run_stderr
)
if(NOT run_result EQUAL 0)
    message(FATAL_ERROR "DLCA ensemble smoke run failed (${run_result}). stdout: ${run_stdout} stderr: ${run_stderr}")
endif()

set(expected_files
    "${OUTPUT_PREFIX}_runs.csv"
    "${OUTPUT_PREFIX}_mass_radius.csv"
    "${OUTPUT_PREFIX}_fit_windows.csv"
)
set(expected_headers
    "seed,completed,attempts,successful_merges,component_count,largest_component_size,largest_component_rg,unwrapping_consistent"
    "seed,particle_count,radius,mean_enclosed_mass"
    "seed,fit_minimum_radius,fit_maximum_radius,exponent,standard_error,r_squared,point_count"
)
list(LENGTH expected_files file_count)
math(EXPR last_index "${file_count} - 1")
foreach(index RANGE 0 ${last_index})
    list(GET expected_files ${index} file_path)
    list(GET expected_headers ${index} expected_header)
    if(NOT EXISTS "${file_path}")
        message(FATAL_ERROR "DLCA ensemble did not create ${file_path}")
    endif()
    file(STRINGS "${file_path}" first_line LIMIT_COUNT 1)
    if(NOT first_line STREQUAL expected_header)
        message(FATAL_ERROR "Unexpected CSV header in ${file_path}: '${first_line}'")
    endif()
endforeach()
