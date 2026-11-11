# 3-D off-lattice Monte Carlo model — design specification

## Status

Verified software kernel plus committed aggregation, network-observable and mass-radius analysis modules pending complete-project execution. The existing geometry, interaction and Metropolis kernel previously passed 3/3 CTest targets in Release and sanitizer Debug builds (see TEST_RESULTS.md). This update adds a reproducible rigid-cluster Brownian aggregation generator (DLCA-style) and contact-graph observables, including graph-based periodic unwrapping of cluster coordinates for radius of gyration. A fourth CTest target has been registered, but the new modules have not yet been locally compiled or tested; do not extend the earlier 3/3 pass claim to them. The neighbour list remains independently verified but is not yet wired into Metropolis. Configuration parsing, production output/metadata and a production simulation driver remain unimplemented. No physical silica validation or calibrated interaction model is claimed.

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

The current kernel implementation and its verification record are documented in [TEST_RESULTS.md](TEST_RESULTS.md). The remaining V1 work is independent build/test verification of the new DLCA and observables modules, coordinate import/export, a reproducible run configuration/output driver, finite-size and sensitivity checks, and a minimal end-to-end smoke run.


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

**Verification status:** see [TEST_RESULTS.md](TEST_RESULTS.md) for the exact compiler/build commands and recorded results. The tested snapshot was reconstructed from the committed source contents fetched from GitHub and built locally; the repository itself was not cloned. The GitHub Actions workflow is configured, but no completed hosted CI result has been retrieved. These checks verify software behaviour only; they do not validate the model against experimental silica data.


## New aggregation and network-analysis modules (verification pending)

- `include/DLCA.hpp` / `src/DLCA.cpp`: seeded rigid-cluster Brownian aggregation in a periodic box. Cluster selection follows an explicit mass-mobility law (D\propto M^{-\alpha}); the exponent is configurable and is an algorithmic assumption, not a hydrodynamic result. Initial monomers are placed by random sequential exclusion. Aggregation stops at one cluster or a declared attempt limit; completion status and merge count are returned.
- `include/Observables.hpp` / `src/Observables.cpp`: pair-contact graph, coordination numbers, connected components, largest-component fraction, contact counts, mean coordination, and per-component radius of gyration from graph-unwrapped coordinates. Periodic winding/inconsistency is flagged rather than silently hidden.
- `tests/test_network.cpp`: deterministic-seed, particle-count, non-overlap, component/merge-accounting, periodic-unwrapping and empty-network checks. The new CTest target is registered but has not yet been executed locally.
- This is a simplified DLCA-style algorithm, not a full hydrodynamic Brownian-dynamics solver. Rigid translation only; no cluster rotation, lubrication, hydrodynamic interaction, long-range electrostatics, reaction-limited sticking, or solvent chemistry. The resulting fractal dimension must be measured across multiple sizes/seeds and is not prescribed.


**Performance boundary:** the first implementation uses direct particle-pair scans for collision detection and random-sequential initial placement. Its cost can approach quadratic scaling in particle count per attempted move. Treat it as a small-system algorithm/verification prototype; do not assume it is practical at N≈1000. A periodic cell-list/spatial-hash broad phase and benchmarks are required before production-scale generation.


## Periodic cell-list broad phase (new; isolated checks passed)

A periodic uniform-cell grid now supplies conservative candidate sets for DLCA swept-contact detection and post-contact cluster identification. The cell width is chosen at least as large as the query radius, so a wrapped 3×3×3 cell neighbourhood is a superset of all possible neighbours within that radius; the caller still applies exact minimum-image/swept-distance tests. If the swept search radius approaches half the box length, DLCA falls back to the brute-force candidate scan. Initial random sequential placement is still brute force, and the cell grid is rebuilt during cluster moves, so this is not yet a fully optimised production implementation.

The new regression case compares cell-list candidates against brute-force minimum-image neighbours, including periodic-face and small-grid cases. An isolated C++17 ASan/UBSan check of the cell-list module passed. Full CMake verification of the current repository remains pending.


## Mass-radius analysis (implementation and isolated checks)

- `include/MassRadius.hpp` / `src/MassRadius.cpp`: mean enclosed particle count as a function of radius, averaged over all particle centres in one graph-unwrapped component. The caller must exclude components whose periodic unwrapping is inconsistent.
- `include/FractalDimension.hpp` / `src/FractalDimension.cpp`: explicit-window log-log OLS fit returning exponent, slope standard error, R² and point count.
- The estimator is a transparent reference implementation with O(N² N_r) cost; it is not yet optimised for large aggregates.
- An isolated sanitizer-compiled straight-chain test returned Df=0.964034 and R²=0.999992 for a finite 1001-particle chain over radii 10–50. The small downward bias from Df=1 is expected from finite-chain boundary effects.
- The complete repository CMake/CTest suite, generated-aggregate scaling analysis and independent-seed ensemble statistics remain pending. The fit-window scan is implemented and covered by committed test cases, but those new cases have not yet been executed in the complete repository test target. No silica-specific fractal dimension is claimed.


- A diagnostic fit-window scan now enumerates all contiguous windows with at least three points. It reports sensitivity; it does not automatically select a scaling interval or establish fractality.
- Pair distances use `std::hypot` to avoid intermediate squared-distance overflow. Added tests cover exact-power-law window stability, a constructed crossover, and large finite coordinates; these new repository assertions await full CMake/CTest execution.
