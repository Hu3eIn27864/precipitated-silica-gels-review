# 3-D off-lattice Monte Carlo — technical specification (V1)

## Status and scope
**Specification plus partial software scaffold.** Foundational C++17 geometry/build files and geometry tests have been committed. They have not yet been compiled or executed in this environment. No production run, calibration, or experimental validation is claimed. V1 is a structural model of a pre-formed 3-D fractal-like aggregate, not a physical syneresis, pore-drainage, or chemistry-resolved silica model.

### Falsifiable V1 question
At fixed particle number, particle diameter, thermal-energy scale, and initial aggregate, how do dimensionless attraction strength and move amplitude affect reversible compactness, coordination statistics, and aggregate structure? Kinetic detachment and persistent contacts are a separate V2 question.

## 1. Language, build, reproducibility
- ISO C++17; standard library only in the simulation core.
- CMake build; enable -Wall -Wextra -Wpedantic on GCC/Clang.
- CTest with a dependency-free test executable.
- RNG: std::mt19937_64; seed supplied in configuration and written to every output header.
- Double precision for coordinates, distances, energies, and accumulators.
- One sweep = N attempted single-particle moves. This is an algorithmic unit, not seconds.
- Record git commit, compiler/version, build type, configuration, and seed.
- Reproducibility is expected for the same executable/configuration/seed/platform; cross-platform bitwise identity is not promised.

## 2. Units and nondimensionalisation
Use particle diameter d as length scale and thermal energy kBT as energy scale. Position x*=x/d; energy U*=U/(kBT); set kBT=1 in reduced units. V1 reports attempted moves, accepted moves, and sweeps only. Pressure, viscosity, permeability, and physical time are not V1 state variables.

Every parameter must be labelled assumed, literature-derived, measured, or fitted. Initial values are algorithmic test values, not measured silica properties.

## 3. Particles and simulation box
Each particle stores a stable integer ID and 3-D position. Equal diameter d=1 in V1; polydispersity is deferred.

Use a cubic periodic box of side L and minimum-image distances. The aggregate must be dilute enough not to interact with periodic images. Record L, N, L/d, and initial radius of gyration. Flag runs where aggregate extent plus interaction range approaches the periodic self-image distance.

Wrap accepted coordinates into [0,L). Structural analysis of a cluster crossing a periodic boundary must use unwrapped cluster coordinates; never calculate Rg directly from wrapped coordinates. A finite non-periodic mode is deferred.

## 4. Initial aggregate
Do not use a simple-cubic lattice as the physical initial structure.

1. Generate a connected, non-overlapping cluster using a documented stochastic aggregation procedure; preferred first candidate: diffusion-limited cluster-cluster aggregation (DLCA).
2. Relax small overlaps/high-energy contacts using the declared interaction model without silently changing target topology.

Save generation algorithm/parameters, seed, N, d, L, Rg, estimated Df with fitting interval and estimator, connected-component count, and coordination distribution. Do not force a target Df by post-processing; measure the resulting value and report finite-size limitations. If DLCA is deferred, allow import of documented coordinates; a lattice may only be a labelled software test fixture.

## 5. Effective interaction
V1 uses hard-core exclusion and a short-range attractive well. A shifted/truncated Lennard-Jones 12-6 potential is acceptable as a generic coarse-grained test potential if overlap is prevented and energy is continuous at cutoff. Morse or square-well alternatives require separate tests and parameter documentation.

Reject hard overlaps for r/d<1; apply attraction for 1<=r/d<rc/d; zero pair energy beyond cutoff. Functional form, cutoff, and values must be explicit in configuration and output metadata. Default values are smoke-test choices, not a calibrated silica potential. No electrostatics, pH dependence, silanol condensation, explicit water, ions, or hydrodynamics. Do not call this a silica force field.

## 6. V1 algorithm: reversible Metropolis sampling
For each attempted move: select one particle uniformly; propose a translational displacement from a symmetric documented distribution; wrap coordinates; reject hard-core overlap; calculate local total pair-energy difference Delta U*; accept with P=min(1,exp(-Delta U*)); update coordinates and neighbour data only after acceptance.

Move amplitude is an algorithm parameter, not a physical observable. Neighbour lists require a tested skin-distance/rebuild rule. No irreversible bond flag, Arrhenius detachment, coordination-weighted kinetic rate, or imposed consolidation is allowed in V1.

## 7. Kinetic extension V2 — separate
A later kinetic model may implement coordination-dependent detachment inspired qualitatively by Schlomach & Kind (2007), attachment, reversible/persistent contacts, and rates with stated provenance. Use event-driven or rejection-free kinetic MC only if transition rates are defensible.

If irreversible contacts are introduced, the model is non-equilibrium and must not be described as ordinary equilibrium Metropolis sampling. Physical-time mapping requires independent calibration against time-resolved observations. The accessible Schlomach & Kind abstract is insufficient to claim reproduction of their numerical algorithm or parameterisation.

## 8. Consolidation — deferred
Do not implement box contraction as a surrogate for syneresis in V1. A later compaction study must choose one explicit protocol: external mechanical compression with defined ensemble; prescribed accessible-volume reduction explicitly labelled numerical compaction; or a kinetic model with a physically motivated driving term. Report work/energy input and boundary conditions. Imposed volume change is not pore-liquid drainage. Darcy/poroelastic coupling belongs to a separately verified continuum workstream.

## 9. Required observables
Write per-run CSV summaries and selected step-resolved outputs:
- Rg from unwrapped coordinates.
- Df from a declared mass-radius or structure-factor fit, with fitting window, estimator, and goodness-of-fit diagnostics.
- Coordination histogram and mean, using a declared contact cutoff.
- Unique contact count and contact-graph connected components/largest-cluster fraction.
- Occupied fraction from a stated excluded-volume estimator; do not equate it with total gel solid fraction without mapping.
- Displacement statistics with periodic unwrapping.
- Attempted/accepted moves as algorithm diagnostics.
- Total reduced potential energy.

Void fraction and pore-size distribution are deferred until a reproducible estimator is specified. Distinguish particle-scale void statistics from experimentally measured mesoporosity.

## 10. Software architecture
Proposed layout under MODELLING/monte_carlo_3d:
- CMakeLists.txt; configs/smoke_test.toml
- include/: Vec3, Particle, SimulationBox, PairPotential, NeighborList, Network, MonteCarlo, Observables, Random interfaces
- src/: main and corresponding implementation units
- tests/: geometry, potential, Metropolis, and network tests
- examples/README.md

Responsibilities: SimulationBox handles wrapping/minimum-image displacement; PairPotential evaluates pair energy; NeighborList manages candidate neighbours; Network stores particles/contact graph; MonteCarlo handles proposals, overlap, energy differences, acceptance and RNG; Observables performs read-only calculations; main parses configuration and writes metadata/results.

Use a dependency-free documented key-value configuration parser initially. Do not silently add external dependencies. Large generated trajectories remain local and are not committed.

### Implemented V1 kernel and interaction-layer contract

The current scaffold implements a reversible single-particle Metropolis kernel: each sweep makes N attempted moves, selects a particle uniformly, proposes a symmetric component-wise uniform translation, rejects hard-core overlap, and applies the reduced-unit Boltzmann acceptance rule with kBT=1. The kernel currently evaluates local energies by brute force to provide a transparent correctness baseline. A shifted/truncated 12-6 Lennard-Jones potential with a hard-core overlap sentinel (+infinity), brute-force total/local energy functions, and a periodic neighbour candidate list. The list stores pairs within `cutoff + skin`; it is considered valid only while every particle has moved no more than `skin/2` from its reference position (minimum-image displacement). The list radius must be smaller than half the cubic box length. The interaction tests compare neighbour-list local energy against brute force and compare local energy differences with full-system energy differences. Seeded reproducibility and sweep-count tests are also included. These tests are committed but have not yet been compiled or executed.

## 11. Required tests
1. Periodic wrapping below zero and above L. (implemented; execution pending)
2. Minimum-image distance across opposite faces.
3. Unwrapped-cluster Rg invariant to translating a cluster across a periodic face.
4. Hard-core overlap proposals rejected.
5. Potential gives expected values and zero beyond cutoff; shifted cutoff is continuous. (implemented; execution pending)
6. Local Delta U equals full-system energy difference in a small system. (implemented for brute-force local energy; execution pending)
7. Metropolis accepts Delta U<=0 and gives the correct probability for positive Delta U in a seeded statistical test.
8. Neighbour list agrees with brute-force enumeration for random small systems. (basic deterministic configuration implemented; randomized coverage pending)
9. Connectivity and coordination match known test graphs.
10. Same seed/configuration reproduces identical output on the same build.
11. Zero-attraction limit has no attraction-driven compaction; algorithm check only, not material prediction.

## 12. Verification and acceptance
Before interpreting results: compare neighbour-list energy with brute force; test at least three system sizes including ~1000 particles when feasible; test move amplitude and cutoff sensitivity; use independent seeds and report ensemble spread; establish equilibration/autocorrelation or justify kinetic interpretation; check periodic-image artefacts; report parameter provenance.

V1 is a verified software baseline only after all tests pass, a smoke test is reproducible, and observables are independently cross-checked on small configurations. This is code verification, not validation against real precipitated silica. Scientific validation requires independent compatible benchmarks matching material route and length scale. Schlomach & Kind (2007) and Sahabi & Kind (2011) motivate mechanisms/scale but do not validate this implementation.

## 13. Explicit non-goals
V1 does not predict natural/forced syneresis curves, pore-liquid pressure or drainage, absolute permeability or modulus, industrial precipitation chemistry or nucleation, pH-/ion-specific silica chemistry, laboratory ageing time, or catalyst/toothpaste/coating properties. These require separately parameterised and validated layers.

## 14. Implementation order and go/no-go
1. Geometry and deterministic RNG.
2. Particle container and coordinate import/export.
3. Pair potential and brute-force energy.
4. Neighbour list verified against brute force.
5. Single-particle Metropolis moves and diagnostics.
6. Observables and reproducible output.
7. DLCA generator/imported fractal cluster and structural characterisation.
8. Smoke tests, independent seeds, finite-size and parameter sensitivity.
9. Only after V1 review: specify V2 kinetic contact dynamics and compaction.

**Go/no-go:** do not start V2 irreversible kinetics, MD parameter transfer, or MC–continuum coupling until V1 passes code verification and the relevant parameter/validation gap is identified.
