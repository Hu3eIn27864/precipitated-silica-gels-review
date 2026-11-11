# Examples

## Reproducible DLCA ensemble and mass-radius export

Build from the Monte Carlo module directory:

```bash
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build --target mc3d_dlca_ensemble
```

Run a small ensemble:

```bash
./build/mc3d_dlca_ensemble 32 15.0 1000 5 200000 results/dlca
```

Arguments are:

1. particle count
2. cubic periodic box side length (same reduced length units as contact distance)
3. first random seed
4. number of consecutive seeds
5. maximum attempted cluster moves per run
6. output prefix

The driver uses contact distance 1.0, maximum component displacement 0.2, mobility exponent 1.0, and radii 1.5, 2, 2.5, 3, 4, 5, 6 and 8. These are explicit algorithmic defaults, not calibrated silica parameters. Ensure the box side length is greater than twice the contact distance. The example is intended for small verification systems; DLCA performance and feasibility at larger particle counts have not yet been benchmarked.

Three CSV files are written:

- `<prefix>_runs.csv`: seed, completion, attempts, merge count, component count, largest component size, radius of gyration and periodic-unwrapping flag.
- `<prefix>_mass_radius.csv`: all-centre mean enclosed mass for completed aggregates whose largest component unwraps consistently.
- `<prefix>_fit_windows.csv`: all non-singular contiguous log-log fit windows with exponent, standard error, R² and point count.

Incomplete runs and aggregates with inconsistent periodic unwrapping are excluded from the whole-aggregate mass-radius and fit-window files, but remain represented in the run summary. Singular plateau windows are omitted by the fit-window scan. The scan does not select a preferred scaling interval. Inspect raw curves and fit-window dependence before interpreting an exponent.

Output files are overwritten if the same prefix is reused. Preserve the command line and source revision alongside any results intended for analysis.

## Build and tests

```bash
cmake -S . -B build
cmake --build build
ctest --test-dir build --output-on-failure
```

The complete CMake/CTest suite for the current repository snapshot has not yet been verified. See [../TEST_RESULTS.md](../TEST_RESULTS.md) for the exact validation boundary.
