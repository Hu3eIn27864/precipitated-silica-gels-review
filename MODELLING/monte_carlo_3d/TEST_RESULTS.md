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
