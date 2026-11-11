if(NOT DEFINED MC3D_EXECUTABLE OR NOT DEFINED OUTPUT_PREFIX)
    message(FATAL_ERROR "MC3D_EXECUTABLE and OUTPUT_PREFIX must be provided")
endif()

execute_process(
    COMMAND "${MC3D_EXECUTABLE}" 12 12.0 12345 1 30000 "${OUTPUT_PREFIX}" 1.0 0.15 0.5 1e-8
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
    "seed,completed,attempts,successful_merges,component_count,largest_component_size,largest_component_rg,unwrapping_consistent,contact_distance,maximum_component_step,mobility_exponent,cumulative_squared_cluster_translation,cumulative_cluster_translation_path_length,target_cumulative_squared_translation,displacement_budget_reached,attempt_limit_reached,displacement_budget_overshoot"
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

# Exactly one run-summary data row must be emitted for the one requested seed.
file(STRINGS "${OUTPUT_PREFIX}_runs.csv" run_lines LIMIT_COUNT 2)
list(LENGTH run_lines run_line_count)
if(NOT run_line_count EQUAL 2)
    message(FATAL_ERROR "Expected one run-summary data row, found ${run_line_count} total lines")
endif()
list(GET run_lines 1 run_row)
if(NOT run_row MATCHES "^12345,[01],[0-9]+,[0-9]+,[0-9]+,[0-9]+,.*,[01],1,0\\.14999999999999999,0\\.5,[0-9.eE+-]+,[0-9.eE+-]+,1e-08,1,0,[0-9.eE+-]+$")
    message(FATAL_ERROR "Malformed run-summary row: '${run_row}'")
endif()
