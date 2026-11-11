# 3-D off-lattice Monte Carlo model — design specification

## Status

Software verification: the current hosted Release build, all five CTest targets, MC3D Python analysis tests, and 1-D transport tests passed in GitHub Actions run #220 (see TEST_RESULTS.md). The bounded DLCA pilot and parameter screen also executed and produced archived artifacts. This is software/algorithmic verification only; it does not establish silica-specific structural validity, calibrated interactions, or physical kinetics. The neighbour list remains independently verified but is not yet wired into Metropolis.

## Scientific purpose

Explore structural reorganisation of a pre-formed three-dimensional fractal-like silica aggregate during a controlled consolidation protocol. The initial question is how coordination-dependent detachment, effective attraction, and persistent contact formation influence aggregate compaction and network connectivity.

This is a microscopic structural model, not a complete syneresis model. It does not calculate liquid drainage, pore pressure, or physical syneresis time.

## Literature basis and limits

- Schlomach & Kind (2007), DOI: 10.1080/02726350701490912: abstract-level evidence for diffusion/reorganisation and coordination-dependent Arrhenius detachment mechanisms. Full text has not been inspected; do not claim algorithmic reproduction.
- Sahabi & Kind (2011), DOI: 10.3390/polym3042156: open full text discusses a 1000-primary-particle fractal aggregate and compares modelling approaches. Its discussion also identifies limitations of a Monte Carlo approach that lacks explicit realistic interaction potentials.

The proposed implementation is an independently specified, modern, transparent model inspired by these mechanisms.

## Version-1 design decisions

- Language: standard C++17 or newer.
- Geometry: three-dimensional, off-lattice particle centres; periodic boundaries.
- Initial size: approximately 1000 particles, followed by finite-size checks.
- Initial structure: connected fractal-like aggregate; generation algorithm and resulting fractal dimension must be recorded.
- Interactions: explicit effective short-range attraction; optional repulsion only with a stated rationale. All parameters marked as measured, literature-derived, fitted, or assumed.
- Moves: local translation, contact rearrangement, coordination-dependent detachment, and reattachment.
- Contact persistence: distinguish reversible contacts from persistent/irreversible contacts with an explicit rule.
- Sampling: Metropolis acceptance for energy-based configurational moves. Any kinetic/rate-based events must be separately defined and must not be silently treated as equilibrium sampling.
- Compression: only after defining the ensemble and protocol. Changing box volume is not equivalent to physical solvent removal.

## Required outputs

CSV time/step series and final summaries for radius of gyration, coordination distribution, contact count, persistent-contact fraction, cluster connectivity, compactness/occupied fraction, and displacement/rearrangement statistics. Fractal dimension must always be accompanied by the fitting interval and estimator.

## Verification plan

1. Unit tests for periodic geometry, distances, neighbour search, energy differences, and acceptance probabilities.
2. Deterministic reproducibility with fixed seeds.
3. Limiting cases: no attraction, no detachment, no compaction.
4. Independent random-seed ensembles and finite-size / move-size / cutoff sensitivity.
5. Compare qualitative structural trends with published silica-aggregate models and compatible experiments; do not overstate validation where original model details or raw data are inaccessible.

## Physical time and syneresis

One MC sweep is not a physical second. Do not report laboratory syneresis times unless a kinetic MC model is independently calibrated against time-resolved data. Pore-liquid transport and poromechanics remain the role of the separate continuum model.

## Planned source layout

- src/: C++ simulation core and executable.
- include/: particle, network, interaction, and RNG interfaces.
- tests/: deterministic unit and limiting-case tests.
- configs/: explicit parameter sets with provenance comments.
- examples/: small smoke-test configurations.
- analysis/: optional plotting / statistical analysis scripts.

The current kernel implementation and its verification record are documented in [TEST_RESULTS.md](TEST_RESULTS.md). Remaining work includes a general Metropolis run driver, improved DLCA completion and equal-displacement sensitivity diagnostics, broader finite-size ensembles, and physical validation against independent structural data.


## Detailed implementation specification

The implementable V1 contract is now defined in [TECHNICAL_SPEC.md](TECHNICAL_SPEC.md). It narrows the first code milestone to reversible Metropolis sampling with an effective pair potential, reproducible geometry/RNG, verified neighbour lists, observables and unit tests. Coordination-dependent kinetic detachment, irreversible contacts and compaction are explicitly deferred to V2; no physical syneresis time or drainage is claimed. The technical specification is authoritative where this overview is less detailed.


## Implemented foundation (initial code milestone)

- `CMakeLists.txt`: C++17 core library and CTest geometry-test target.
- `include/Vec3.hpp`, `Particle.hpp`: minimal vector and particle data types.
- `include/SimulationBox.hpp` and `src/SimulationBox.cpp`: validated cubic box, periodic wrapping, minimum-image displacement and distance.
- `include/Random.hpp`: seeded `std::mt19937_64` wrapper.
- `tests/test_geometry.cpp`: tests for wrapping, minimum-image geometry and invalid box dimensions.
- `include/PairPotential.hpp`: shifted/truncated LJ potential with an explicit hard core; generic reduced-unit test interaction, not a silica force field.
- `include/Energy.hpp`: brute-force total and single-particle local energy calculations.
- `include/NeighborList.hpp` and `src/NeighborList.cpp`: periodic candidate list with cutoff + skin and a conservative skin/2 rebuild criterion.
- `tests/test_interactions.cpp`: cutoff continuity, hard-core, zero-attraction, local-vs-total energy difference, neighbour-list agreement and invalid-box checks.
- `include/MonteCarlo.hpp` and `src/MonteCarlo.cpp`: reversible single-particle Metropolis moves with symmetric uniform displacement, hard-overlap rejection, reduced-unit acceptance, sweep and acceptance diagnostics. Uses brute-force local energies pending neighbour-list integration.
- `tests/test_metropolis.cpp`: seeded reproducibility, sweep-count, empty-system and 1000-sweep hard-core regression checks.
- `examples/README.md`: build/test instructions.

**Verification status:** see [TEST_RESULTS.md](TEST_RESULTS.md) for exact hosted build/test results and pilot outcomes. GitHub Actions run #220 built and tested the current MC3D snapshot and executed the bounded DLCA workflows. These checks verify software behaviour only; they do not validate the model against experimental silica data.


## Aggregation and network-analysis modules (hosted software verification passed)

- `include/DLCA.hpp` / `src/DLCA.cpp`: seeded rigid-cluster Brownian aggregation in a periodic box. Cluster selection follows an explicit mass-mobility law (D\propto M^{-\alpha}); the exponent is configurable and is an algorithmic assumption, not a hydrodynamic result. Initial monomers are placed by random sequential exclusion. Aggregation stops at one cluster or a declared attempt limit; completion status and merge count are returned.
- `include/Observables.hpp` / `src/Observables.cpp`: pair-contact graph, coordination numbers, connected components, largest-component fraction, contact counts, mean coordination, and per-component radius of gyration from graph-unwrapped coordinates. Periodic winding/inconsistency is flagged rather than silently hidden.
- `tests/test_network.cpp`: deterministic-seed, particle-count, non-overlap, component/merge-accounting, periodic-unwrapping and empty-network checks. The network CTest target passed in hosted CI run #220.
- This is a simplified DLCA-style algorithm, not a full hydrodynamic Brownian-dynamics solver. Rigid translation only; no cluster rotation, lubrication, hydrodynamic interaction, long-range electrostatics, reaction-limited sticking, or solvent chemistry. The resulting fractal dimension must be measured across multiple sizes/seeds and is not prescribed.


**Performance boundary:** the first implementation uses direct particle-pair scans for collision detection and random-sequential initial placement. Its cost can approach quadratic scaling in particle count per attempted move. Treat it as a small-system algorithm/verification prototype; do not assume it is practical at N≈1000. A periodic cell-list/spatial-hash broad phase and benchmarks are required before production-scale generation.


## Periodic cell-list broad phase (new; isolated checks passed)

A periodic uniform-cell grid now supplies conservative candidate sets for DLCA swept-contact detection and post-contact cluster identification. The cell width is chosen at least as large as the query radius, so a wrapped 3×3×3 cell neighbourhood is a superset of all possible neighbours within that radius; the caller still applies exact minimum-image/swept-distance tests. If the swept search radius approaches half the box length, DLCA falls back to the brute-force candidate scan. Initial random sequential placement is still brute force, and the cell grid is rebuilt during cluster moves, so this is not yet a fully optimised production implementation.

The new regression case compares cell-list candidates against brute-force minimum-image neighbours, including periodic-face and small-grid cases. An isolated C++17 ASan/UBSan check of the cell-list module passed. The integrated current CMake/CTest verification passed in hosted CI run #220.


## Mass-radius analysis (implementation and isolated checks)

- `include/MassRadius.hpp` / `src/MassRadius.cpp`: mean enclosed particle count as a function of radius, averaged over all particle centres in one graph-unwrapped component. The caller must exclude components whose periodic unwrapping is inconsistent.
- `include/FractalDimension.hpp` / `src/FractalDimension.cpp`: explicit-window log-log OLS fit returning exponent, slope standard error, R² and point count.
- The estimator is a transparent reference implementation with O(N² N_r) cost; it is not yet optimised for large aggregates.
- An isolated sanitizer-compiled straight-chain test returned Df=0.964034 and R²=0.999992 for a finite 1001-particle chain over radii 10–50. The small downward bias from Df=1 is expected from finite-chain boundary effects.
- The complete repository CMake/CTest suite and fit-window tests passed in hosted CI run #220. Generated-aggregate scaling is still not established: the bounded pilot had only two eligible N=32 aggregates, none at N=64 or N=128, and strong fit-window sensitivity. No silica-specific fractal dimension is claimed.


- A diagnostic fit-window scan now enumerates all contiguous windows with at least three points. It reports sensitivity; it does not automatically select a scaling interval or establish fractality.
- Pair distances use `std::hypot` to avoid intermediate squared-distance overflow. Added tests cover exact-power-law window stability, a constructed crossover, and large finite coordinates; these new repository assertions await full CMake/CTest execution.


- Added deterministic compact-cube and three-arm branched reference geometries to the network test source. An isolated sanitizer-compiled C++17 check returned apparent slopes 2.33099 (finite cube) and 1.07112 (branched cross), within the committed regression bounds. These are estimator sanity checks, not evidence of fractal scaling or silica-specific morphology.


## Reproducible DLCA ensemble executable (hosted smoke test passed)

`examples/dlca_ensemble.cpp` and the `mc3d_dlca_ensemble` CMake target provide a command-line driver over consecutive random seeds. It writes separate run-summary, mass-radius-curve and fit-window CSV files. Only completed aggregates with consistent periodic unwrapping are exported to the mass-radius and fit files; incomplete or winding cases remain visible in the run summary. The default radii and mobility settings are algorithmic reduced-unit choices, not calibrated silica parameters. Usage and output schemas are documented in [examples/README.md](examples/README.md). The driver and fit-window scan compiled and passed the integrated CTest smoke test in hosted CI run #220.


- The fit-window scan omits singular plateau-only windows while retaining valid intervals elsewhere; a completely constant mass curve produces no fit rows rather than aborting the ensemble export.
- A command-line DLCA ensemble example is registered as `mc3d_dlca_ensemble`. It exports seed-level run summaries, mass-radius curves and all non-singular fit windows to three CSV files. See [examples/README.md](examples/README.md). Its full-project compilation and smoke run passed in hosted CI run #220.


## Current verification boundary

The current snapshot has now completed a hosted Release CMake build and all five CTest targets, including `dlca_ensemble_smoke`, in [GitHub Actions run #220](https://github.com/Hu3eIn27864/precipitated-silica-gels-review/actions/runs/43015008467). The complete MC3D Python analysis tests and 1-D transport-model tests also passed. The bounded DLCA size pilot and seven-configuration sensitivity screen executed and their artifacts were uploaded. This verifies software execution for the tested workflow, not physical calibration or silica-specific model validity. See [TEST_RESULTS.md](TEST_RESULTS.md).

## DLCA pilot interpretation and fit sensitivity

The pilot workflow now runs `analysis/analyze_dlca_fit_sensitivity.py` after the seed-level ensemble summary and stores its CSV outputs with the other pilot artifacts. The audit reports within-seed exponent ranges across all available valid fit windows; it does not select a scaling interval or convert fit windows into independent replicates. See [DLCA_PILOT_VALIDATION_PROTOCOL.md](DLCA_PILOT_VALIDATION_PROTOCOL.md) for predeclared interpretation gates. The script and its tests passed in hosted CI run #220. The pilot data show strong fit-window sensitivity and insufficient completion at larger sizes; see [TEST_RESULTS.md](TEST_RESULTS.md).

## DLCA parameter sensitivity controls (implemented and executed in bounded CI; physical interpretation pending)

The ensemble executable accepts three optional trailing parameters:
contact distance, maximum component displacement per coordinate, and
mobility exponent. The original six-positional-argument interface remains
valid and uses the original defaults. Each run-summary row records the
parameter values. The size-series runner forwards the same controls, allowing
separate ensembles to be compared at fixed particle-number density and
attempt limits. The CMake smoke test now invokes a non-default parameter set
and checks the expanded run-summary schema.

These controls expose algorithmic assumptions; they do not make the DLCA
generator a hydrodynamic or silica-calibrated model. Sensitivity comparisons
should vary one parameter at a time initially, preserve common system sizes
and analysis intervals, and report completion fractions as well as structural
observables. The updated driver passed hosted build, CTest and bounded workflow execution in runs #220 and #234. The first sensitivity results are diagnostic only; see the plan for the displacement-clock limitation.

## Bounded DLCA parameter-sensitivity screen

The CI workflow now runs a paired-seed one-factor-at-a-time screening matrix
for contact distance, maximum cluster step and mobility exponent using
N = 32, three seeds per variant and a 50,000-attempt cap. It preserves the
raw per-variant CSV files, writes a parameter manifest, and runs both the
fixed-window ensemble summary and fit-window sensitivity audit. The six
non-baseline variants are compared with a baseline generated inside the same
paired seed block. In the first screen the baseline completed 0/3, so no paired
Rg or exponent comparison was valid. The size pilot completed only 2/3 at
N = 32 and 0/3 at N = 64 or 128; its N = 32 fit-window sensitivity was high.
This bounded screen is not the full finite-size study and does not calibrate
the model to silica. See
[DLCA_PARAMETER_SENSITIVITY_PLAN.md](DLCA_PARAMETER_SENSITIVITY_PLAN.md).


## Realized displacement diagnostics (hosted verification passed)

The run-summary CSV now records the cumulative squared realized cluster
translation and cumulative realized cluster-translation path length. These
metrics passed the C++ reproducibility test and extended smoke-test contract
in hosted CI run #234. At the same 50,000-attempt cap, the baseline step 0.2
accumulated mean squared realized translation 2,000.71, while step 0.1
accumulated 500.30. Step 0.28 completed all three runs in a mean 25,665
attempts at mean accumulated squared translation 2,011.66. Fixed attempt
counts therefore do not represent equal algorithmic progress across step
sizes. The next step is a common-displacement stopping criterion; this
diagnostic is not physical time or a calibrated diffusivity.
