# Examples

## Reproducible DLCA ensemble and mass-radius export

Build from the Monte Carlo module directory:

```bash
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build --target mc3d_dlca_ensemble
```

Run a small ensemble:

```bash
./build/mc3d_dlca_ensemble 32 15.0 1000 5 200000 dlca_example
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


## Automated smoke test

CTest includes a deterministic end-to-end smoke test of the ensemble executable. It verifies successful execution and the three CSV headers, but does not require a completed aggregate or non-empty mass-radius output. The current five-test suite has not yet been executed; see [../TEST_RESULTS.md](../TEST_RESULTS.md) for the verification boundary.


The smoke test additionally requires exactly one run-summary data row for the requested seed and checks the row's basic field structure. This is a CLI/output-contract check, not a stochastic aggregation-success criterion.

## Seed-level ensemble statistics

After running independent ensembles at two or more particle counts, analyse them with one **predeclared common fit interval**. For example, if the driver outputs are `results/n32_*` and `results/n64_*`:

```bash
python3 analysis/analyze_dlca_ensembles.py \
  --system 32:results/n32 \
  --system 64:results/n64 \
  --fit-min 2 --fit-max 5 \
  --output results/size_comparison
```

The script writes `size_comparison_per_run.csv` and `size_comparison_summary.csv`. It reports completion and unwrapping fractions, largest-component fraction, and per-seed fractal-fit statistics (mean, sample standard deviation, median, minimum and maximum) for the exact requested fit interval. A fit is counted only for a completed aggregate with consistent periodic unwrapping. Overlapping fit windows are **not** pooled as independent observations.

The particle count is supplied explicitly because it is not stored in the current run-summary CSV. Keep seed ranges distinct across systems where practical, and preserve the original CSVs, command line, and source revision. The summary reports descriptive sample statistics only; it does not provide a confidence interval or establish convergence. Use enough independent seeds and repeat the analysis with a scientifically justified common fit interval before drawing conclusions. If the requested interval is absent for a run, that run contributes to completion statistics but not to the fitted-exponent statistics.

Run the standard-library unit tests with:

```bash
python3 -m unittest discover -s analysis -p 'test_*.py' -v
```
