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
