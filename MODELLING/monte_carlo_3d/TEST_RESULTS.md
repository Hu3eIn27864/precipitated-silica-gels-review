# MC3D V1 — local build and test record

**Status: PASS for the current software kernel; not a physical model validation.**

## Tested source snapshot

The source contents were fetched from the GitHub repository and assembled into a temporary local build tree because a repository clone was unavailable in the execution environment. The CMake configuration used for the Release verification is the committed `MODELLING/monte_carlo_3d/CMakeLists.txt`.

Relevant source revisions:
- Neighbour-list test fixture correction: `df8195842caaa51223b92ad03203224b74a27a7d`
- Extended Metropolis regression test: `69209565c42a545b72e17b2348270710634ba1b2`

## Environment

- Compiler: GNU C++ 14.2.0
- CMake: 3.31.6
- Language standard: C++17
- Platform: Linux x86_64 execution environment
- Build dependency: C++ standard library only

## Release build

Commands:

```bash
cmake -S MODELLING/monte_carlo_3d -B build/mc3d -DCMAKE_BUILD_TYPE=Release
cmake --build build/mc3d --parallel 2
ctest --test-dir build/mc3d --output-on-failure
```

Result:
- CMake configure: PASS
- Compilation and linking: PASS
- CTest: **3/3 passed**
  - `geometry`: PASS
  - `interactions`: PASS
  - `metropolis`: PASS

## Debug sanitizer build

Commands:

```bash
cmake -S MODELLING/monte_carlo_3d -B build/mc3d-sanitize \
  -DCMAKE_BUILD_TYPE=Debug \
  -DCMAKE_CXX_FLAGS="-fsanitize=address,undefined -fno-omit-frame-pointer" \
  -DCMAKE_EXE_LINKER_FLAGS="-fsanitize=address,undefined"
cmake --build build/mc3d-sanitize --parallel 2
ASAN_OPTIONS=detect_leaks=1 ctest --test-dir build/mc3d-sanitize --output-on-failure
```

Result:
- Debug configure: PASS
- Sanitizer-instrumented compilation and linking: PASS
- CTest: **3/3 passed**
- AddressSanitizer / UndefinedBehaviorSanitizer reported no failures in these tests.

## Coverage represented by the passing tests

- Periodic wrapping and minimum-image distances.
- Invalid simulation-box dimensions.
- Hard-core overlap sentinel, zero-attraction limit, and shifted potential continuity at cutoff.
- Local energy difference versus full-system energy difference.
- Neighbour-list energy versus brute-force energy.
- Seeded neighbour-list skin check: bounded particle displacements do not omit pairs that enter the interaction cutoff.
- Reproducibility for equal RNG seeds.
- Exactly N attempted moves per sweep.
- Empty-system and invalid-step handling.
- 1000 Metropolis sweeps (4000 attempted moves) with finite total energy and no hard-core overlap.

## Test-fixture correction

The first local run exposed a flawed test fixture, not an implementation failure: one periodic pair had separation below the hard-core diameter, so both energy calculations correctly returned positive infinity. The test helper compared finite differences only and therefore rejected the matching infinities. The pair was repositioned to a non-overlapping periodic separation, and the comparison helper now treats matching infinities as equal. The subsequent Release and sanitizer suites both passed.

## What this does not establish

- It does not prove hosted GitHub Actions succeeded; no completed hosted run was available when this record was written.
- It does not establish that the neighbour list is used by the Metropolis sampler. The sampler intentionally uses brute-force local energies as the correctness baseline.
- It does not verify a DLCA generator, structural observables, periodic unwrapping for cluster radius of gyration, or production output/metadata.
- It does not calibrate the generic shifted/truncated Lennard-Jones potential to silica chemistry.
- It does not validate structural predictions against precipitated-silica experiments and does not predict physical time, syneresis, pore pressure, or drainage.

**Conclusion:** the current geometry–interaction–Metropolis software kernel has a locally compiled and tested V1 baseline (3/3 CTest targets in Release and sanitizer Debug builds). The broader scientific V1 model is not yet complete.


## New DLCA/network module — preliminary isolated check (2026-11-11)

The new files `DLCA.cpp`, `Observables.cpp`, and `test_network.cpp` have been added to the project and a fourth CTest target is registered. An isolated local C++17 harness was assembled for the new algorithms using interface-compatible minimal geometry/RNG headers. It compiled with GCC using `-Wall -Wextra -Wpedantic` and the test executable passed checks for periodic unwrapping/Rg, deterministic seeded output, particle count, non-overlap, empty-network behaviour, contact counts, and component/merge accounting.

**Verification boundary:** this isolated harness is a preliminary algorithm check, not a full CMake build of the repository's committed source tree. The previous 3/3 Release and sanitizer results still apply only to the original geometry/interaction/Metropolis targets. The new fourth CTest target has not yet been confirmed by a complete repository build or hosted CI run. No claim of physical DLCA fidelity or silica validation is made.

The network regression target was subsequently extended with two further cases: invariance of (R_g) when a connected cluster is translated across a periodic face, and explicit flagging of a component that winds around the periodic box. The equivalent isolated harness passed both checks. The full-project/hosted-CI verification boundary stated above remains unchanged.


## Periodic cell-list broad-phase check (2026-11-11)

The periodic cell-list source was compiled in an isolated C++17 harness with GCC, `-Wall -Wextra -Wpedantic`, AddressSanitizer and UndefinedBehaviorSanitizer. Tests compared candidate sets with brute-force minimum-image distance checks for a periodic-face configuration and a two-cells-per-dimension grid. All tested in-radius neighbours were present in the candidate set; the executable completed successfully. A separate isolated DLCA harness using interface-compatible geometry/RNG headers completed a 12-particle seeded run and verified no overlaps. These are isolated module checks, not a complete build/test of the committed CMake project. The full four-target CTest suite and hosted CI remain unverified.

The cell-list regression source was also extended to cover negative periodic query coordinates and rejection of non-finite query coordinates. These additional assertions are registered in the CTest source but have not been run as part of a full repository build.


## Cell-list allocation guard and randomized regression additions (2026-11-11)

The dense periodic grid now refuses allocations above 1,000,000 cells. DLCA catches this specific grid-size exception and reverts to exact brute-force candidate enumeration for both swept-contact broad phase and final contact identification. This preserves correctness while avoiding an unexpectedly large dense allocation; it may be slower for such geometries.

The network CTest source now includes deterministic pseudo-random candidate-completeness comparisons against brute-force minimum-image distances (240 generated positions) and a test that verifies the dense-grid cap rejects an excessive allocation request. These tests have been added to the committed target but **have not yet been executed in a complete repository CMake build**. Earlier isolated cell-list tests do not cover these latest additions. No performance benchmark or silica validation is claimed.


## Mass-radius power-law regression utility (2026-11-11)

Added a standalone log-log OLS helper with explicit fit interval, slope standard error, R² and fitted-point count. The CTest source includes recovery of a synthetic exponent (1.65) and rejection of non-positive mass input. This checks regression arithmetic only. The utility does not generate mass-radius curves or validate a physical fractal regime. The new source and updated test have **not yet been compiled or executed in a full repository build**.


## Mean enclosed mass-radius estimator — isolated check (2026-11-11)

The committed `MassRadius.cpp` implementation was compiled in an isolated C++17 harness with GCC, `-Wall -Wextra -Wpedantic`, AddressSanitizer and UndefinedBehaviorSanitizer. A three-particle collinear fixture verified the analytically expected mean enclosed masses (5/3 at radius 1 and 3 at radius 3); the executable passed.

**Verification boundary:** this isolated check exercised the committed estimator implementation, but not the full repository CMake target or the newly extended `test_network.cpp`. The complete four-target CTest suite remains unverified. Translation-invariance and invalid-radius assertions have been added to the repository test source but were not included in this isolated executable. No fractal-dimension result or physical validation is claimed.


## Network-to-mass-radius integration test added (2026-11-11)

The component-observables structure now retains graph-unwrapped coordinates, and the network regression source checks that a cluster crossing a periodic face produces the analytically expected mean enclosed mass-radius values when passed to the estimator. This connects the two committed interfaces in the test source. The assertion has **not** yet been executed in the complete repository test target; the full CMake/CTest suite remains pending.


## Known-geometry line-scaling harness (2026-11-11)

A standalone C++17 harness implementing the committed mass-radius counting and log-log regression logic was compiled with GCC using `-Wall -Wextra -Wpedantic -fsanitize=address,undefined`. For a finite straight chain of 1001 equally spaced particles and radii 10, 15, 20, 25, 30 and 40, 50, it returned (D_f=0.964034) and (R^2=0.999992); both satisfy the repository regression thresholds (|Df−1| < 0.05, R² > 0.995). The deviation from exactly one is expected from finite-chain boundary effects. The harness is an isolated executable, not the complete CMake/CTest suite, and does not independently compile the complete committed repository target.


## Fit-window scan and robust distance tests added (2026-11-11)

The test source now checks exhaustive contiguous-window enumeration (28 windows for nine radii with at least three points), exponent invariance for an exact power law, and detection of a deliberately constructed crossover. It also checks the mass-radius estimator at large finite coordinate scales after replacing squared-distance comparison with `std::hypot`. These assertions have been committed but have **not** yet been executed in the full CMake/CTest target. No test pass is claimed for these additions.


## Compact and branched reference-geometry isolated check (2026-11-11)

A standalone C++17 harness using the same all-centre enclosed-mass definition and log-log OLS calculation was compiled with GCC and AddressSanitizer/UndefinedBehaviorSanitizer. It returned an apparent exponent of 2.33099 for the finite 9×9×9 cubic lattice (radii 1–4.5) and 1.07112 for the three-arm, 603-point cross (radii 5–20). Both fall inside the new regression bounds. This isolated geometry harness is not the complete repository test target; the newly committed test functions still await full CMake/CTest execution.


## Fit-window plateau handling (2026-11-11)

A standalone C++17 harness mirroring the committed fit and scan logic was compiled with GCC and AddressSanitizer/UndefinedBehaviorSanitizer. A curve with an initial plateau retained nine non-singular fit windows; a fully constant curve returned zero windows without throwing. This is an isolated logic check, not execution of the complete repository CTest target. The DLCA ensemble executable has not yet been compiled or run against the complete project.


## End-to-end ensemble smoke test registered (2026-11-11)

The CMake project now registers a fifth CTest entry, `dlca_ensemble_smoke`. It invokes the committed ensemble executable for a deterministic 12-particle, one-seed, bounded-attempt run and checks that all three CSV files are created with their expected headers. The test intentionally does not require aggregation to complete or mass-radius rows to be present; it verifies the CLI/output contract without imposing an unverified stochastic completion expectation.

The existing GitHub Actions workflow builds the MC3D directory and runs CTest on relevant pushes and pull requests, so this test will be exercised by the next matching workflow run. **No result is claimed yet:** the complete current CMake build, five-test suite and smoke run remain pending until the hosted workflow reports a result.


## Smoke-test harness logic check (2026-11-11)

The new CMake smoke-test script was exercised locally with a temporary stand-in executable that wrote the three expected CSV headers. CMake 3.31.6 completed the script successfully. This verifies the CMake script's argument handling, file checks and header comparisons only; it does **not** compile or execute the actual DLCA ensemble program. The full repository build and five-test CTest run remain unverified.


## Driver input and output edge-case audit (2026-11-11)

A source-level audit of `dlca_ensemble.cpp` confirms that integer arguments are digit-validated before conversion, positive size arguments are required, box length must be finite and positive, seed-range overflow is rejected, all three output streams are checked before writing, and incomplete/winding aggregates are excluded from mass-radius fitting while retained in the run summary. The smoke test checks the three CSV headers after a real executable invocation. This audit is static inspection, not compilation or execution of the driver.


## Smoke-test run-row assertion (2026-11-11)

The DLCA ensemble smoke script now checks not only that all three CSV files exist with the expected headers, but also that the one-seed invocation writes exactly one run-summary data row with the requested seed and structurally valid integer metadata fields. The strengthened CMake script passed an isolated local harness using a temporary stand-in executable that emitted the expected CSV schema. This validates the script and row assertion only, not the actual C++ ensemble executable or full project build.

 
## Seed-level ensemble analysis utility added (2026-11-11)

Added `analysis/analyze_dlca_ensembles.py` to combine independent DLCA driver outputs across explicitly supplied particle counts. The user specifies one common lower/upper radius bound; the script extracts at most one fit per seed for exactly that interval, and only from completed aggregates with consistent periodic unwrapping. It reports completion, unwrapping and valid-fit fractions, largest-component fraction, and descriptive per-seed exponent/Rg statistics. It deliberately does not pool overlapping fit windows or treat them as independent replicates.

A standard-library `unittest` file covers fixed-window extraction, exclusion of incomplete and winding runs, handling of undefined Rg, and duplicate-seed rejection. The tests are committed but have not yet been executed in this environment. The script is a post-processing tool; it does not alter the DLCA generator or validate its physical assumptions.

 
The GitHub Actions workflow now also runs the Python standard-library unit tests for the ensemble-analysis utility after the C++ CTest suite. This CI step is newly registered; no hosted result is claimed until a workflow run completes.

 
## DLCA size-series runner added (2026-11-11)

Added `analysis/run_dlca_size_series.py` to execute a set of particle counts at constant initial reduced number density by scaling the cubic box as (L propto N^{1/3}). Defaults use the existing 32-particle, side-length-15 reduced-unit reference condition, with five consecutive seeds and 200,000 attempted cluster moves per run. A unit-volume-fraction calculation gives approximately 0.005 for the reference hard-sphere system; this is an algorithmic dilute test condition, not an experimentally calibrated silica concentration.

A companion test checks the box-scaling relation and seed/input parsing. The runner tests were executed against an isolated local copy of the committed runner and test module: 4/4 passed, including the CLI fake-executable test and disjoint-seed allocation. The repository checkout itself and its full CI suite have not been executed locally. The suggested common fit interval 2–5 is only a diagnostic starting point and must not be interpreted as a validated scaling regime.

 
## Ensemble-fit provenance validation (2026-11-11)

The seed-level analyser now reads the underlying mass-radius CSV rather than trusting fit-window summaries alone. It checks particle-count consistency, positive finite radius/mass values, duplicate radii, a common radius grid across seeds, fit-to-observation seed correspondence, and fit point counts for the selected common interval. Unit-test fixtures were extended accordingly. These repository tests are committed and included in CI, but have not yet been run against the repository checkout or confirmed by a GitHub Actions result.

 
A local isolated regression check of the size-series runner logic and its four runner tests passed (4/4), including a fake-executable CLI integration test. This did not compile or execute the repository's C++ DLCA executable and is not a substitute for the committed GitHub Actions suite. The ensemble-analyser tests have been updated for the new mass-radius provenance checks but remain pending execution.

 
The seed-level analyser additionally rejects impossible largest-component counts and any run marked complete whose largest component does not contain all particles. A dedicated regression case was added. The updated analyser test suite remains pending execution in a repository checkout or CI run.

 
The size-series runner now allocates disjoint consecutive seed blocks across particle counts and checks the combined seed range for uint64 overflow. Its CLI regression test verifies that separate system sizes receive non-overlapping seed ranges. This design supports unpaired comparisons across sizes; it does not implement paired-seed statistics.

 
The analyser regression suite now includes an explicit mismatch test for the fit point count versus the source mass-radius grid. Its multi-window fixture also uses the actual number of radii in the broad interval. Local targeted checks of the validation logic (fixed-window extraction, completion-size invariant, and fit-point provenance) passed 3/3; this was a focused reconstructed harness, not execution of the committed repository test module. The full committed Python and C++ suites remain unverified pending CI or a repository checkout.

## Run-manifest provenance checks (2026-11-11)

The ensemble analyzer cross-checks all mass-radius observations and selected fit rows against the run-summary manifest. It rejects observations for unknown seeds, mass-radius data attached to incomplete or periodically ambiguous runs, and selected fit rows without a matching completed and consistently unwrapped run. This prevents derived rows from being silently omitted from seed-level statistics. Regression tests cover orphaned fit seeds and mass-radius data attached to unfinished runs. Full repository CI remains unverified.

## Periodic swept-collision image audit (2026-11-11)

A code review found an edge case in DLCA collision detection: the narrow phase solved the swept-sphere quadratic only for the initial minimum image. For contact distances approaching half the box length, a permitted cluster translation can cross a minimum-image Voronoi face and encounter a neighbouring periodic image; the old calculation could miss that collision. Added a dedicated periodic swept-collision helper that checks the 27 images surrounding the initial minimum image, integrated it into DLCA, and added a deterministic regression test for a collision that occurs only after crossing the image boundary. The change is committed but the C++ build and CTest suite have not yet been executed.

### Isolated periodic swept-collision helper check (2026-11-11)

The new PeriodicSweptCollision.cpp helper was compiled with GCC in C++17 mode using -Wall -Wextra -Wpedantic against a minimal Vec3-compatible test interface and a small deterministic harness. The first isolated harness covered neighbouring-image contact, no-contact motion, and initial overlap, but did not independently check the sign convention for relative motion. A subsequent 500-trajectory sampled comparison exposed that sign error; the helper and regression test were corrected to use relative(t) = relative(0) - displacement*t. The earlier three-case pass must therefore not be treated as validation of the original implementation. An AddressSanitizer/UBSan-linked executable could be built, but the runtime could not start in this environment because the ASan runtime was not first in the process library list. The successful plain build/run is an isolated helper check only; it does not replace the complete CMake build, integrated DLCA tests, or CTest suite.

### Randomized periodic swept-collision comparison (2026-11-11)

Added a deterministic 500-trajectory regression that compares the analytic periodic swept-sphere result with sampled minimum-image trajectories (2,001 time fractions per trajectory). It checks that sampled contacts are not missed, that the analytic first-contact fraction is no later than the first sampled contact, and that every reported contact lies on or inside the contact sphere within tolerance. The test uses the DLCA convention relative(t) = relative(0) - clusterDisplacement*t. An isolated GCC C++17 harness using a minimal Vec3-compatible interface passed all 500 trajectories; two trajectories intersected the contact sphere in this deterministic sample. This is an isolated helper-level test, not a full integrated build or CTest run.

### CI rerun trigger (2026-11-11)

Documentation-only change to trigger the repository's configured MC3D push workflow after the periodic swept-collision regression was added. This note is not a test result; record build and test outcomes only after inspecting the workflow run.

### Parallel validation work added (2026-11-11)

Added `analysis/analyze_dlca_fit_sensitivity.py` and unit tests to quantify within-seed exponent variation across all available fit windows, while rejecting fits attached to incomplete or invalid runs. Added the script to the CI pilot workflow. Added `DLCA_PILOT_VALIDATION_PROTOCOL.md` defining integrity, completion, finite-size, fit-window, parameter-sensitivity, and physical-calibration gates. These are committed additions; no hosted CI or pilot result is claimed until the workflow run is retrieved and inspected.

### Pilot provenance capture (2026-11-11)

The CI pilot step now writes `build/mc3d/pilot/provenance.txt` before running the size series. It records the checked-out Git commit/ref, runner OS, CMake/compiler/Python versions, particle sizes, seed block, attempt cap, reference box/size, and common diagnostic fit interval. This metadata is uploaded with the raw CSV and analysis artifacts. The addition improves traceability but does not itself establish that the workflow executed.

### Parallel 1-D transport benchmark hardening (2026-11-11)

The slab consolidation function now rejects non-finite time, diffusivity, and drainage-length inputs. Added tests for NaN/infinity rejection and for agreement of the default 1000-term series with a 5000-term reference at a representative dimensionless time. The hosted MC3D workflow now also runs the independent `MODELLING/transport_model` Python unit tests. These changes are committed; hosted test results remain unverified.

### Radial scaling and DLCA parameter-control additions (2026-11-11)

Added `MODELLING/transport_model/geometry_scaling.py` with ideal first-mode time-constant and inverse apparent-diffusivity functions for radially drained infinite cylinders and spheres. Added tests for inverse consistency, radius-squared scaling and invalid inputs. This utility does not solve the full transient radial field and does not identify permeability.

The DLCA CLI now accepts optional `contact_distance`, `maximum_component_step` and `mobility_exponent` arguments, while preserving prior calls through the original defaults. The run-summary CSV records all three parameters. The size-series runner forwards the parameters and validates their ranges. The smoke test was updated to check a non-default parameter set and the expanded CSV schema. These changes are committed, but no full-project C++ build, CTest, or repository Python test pass is claimed here.
