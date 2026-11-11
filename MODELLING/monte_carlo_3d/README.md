# 3-D off-lattice Monte Carlo model — design specification

## Status

Design only. No C++ implementation, simulation, calibration, or validation has yet been completed in this directory.

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

No source files are added until the energy function, aggregate-generation method, and move/acceptance rules are specified precisely enough to test.
