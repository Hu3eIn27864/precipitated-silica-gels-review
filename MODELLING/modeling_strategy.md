# Modelling and simulation strategy

## Purpose and status

This is an optional, hypothesis-driven workstream alongside the evidence-led review. No simulation is committed to the manuscript until a specific question, measurable output, and validation target have been identified. The purpose is not to add computational complexity for its own sake.

The review remains scientifically complete if no new simulation is justified. Any eventual computational study should be reported as a separate, reproducible contribution with its own methods, parameter provenance, sensitivity analysis, and limitations.

## Candidate multiscale questions

1. **Network rearrangement under consolidation** — Under what combinations of attraction strength, repulsive barrier, bond persistence, and applied compression does a pre-aggregated silica network undergo reversible rearrangement versus irreversible contact formation?
2. **Transport-limited syneresis** — How do permeability, sample geometry, drainage boundary conditions, and viscoelastic resistance jointly control the rate and extent of liquid expulsion?
3. **Fragmentation and process history** — How do aggregate connectivity and bond-strength distributions influence breakage under defined shear or extensional flow, and does a finite post-gelation interval exist in which fragments are especially susceptible to breakup?
4. **Chemistry-dependent interactions** — Which measured or literature-supported changes in pH, ionic strength, and surface state can be represented by defensible effective interaction parameters, and which require explicit chemical modelling?

These questions are related but not interchangeable. In particular, a particle-network model without pore-fluid transport cannot predict syneresis kinetics; a CFD–DEM fragmentation model does not automatically represent gel ageing or siloxane-bond formation.

## Method selection hierarchy

### Level 0 — Analytical and data-driven baselines

Before numerical simulation, extract reported time series and endpoint data, harmonise definitions, and test simple kinetic or poroelastic descriptions. Use Scherer's coupled permeability–viscoelasticity framework as a mechanistic baseline for syneresis, while respecting its material-system transferability limits. Fit only identifiable parameters and report uncertainty/covariance where possible.

### Level 1 — Coarse-grained particle/network model (LAMMPS)

**Best first computational candidate:** a deliberately minimal coarse-grained model of a pre-aggregated network under controlled compression.

Possible ingredients:
- particles or beads representing effective primary particles / small clusters;
- short-range attraction and a tunable repulsive barrier;
- reversible contacts plus a separately controlled irreversible-bond or contact-persistence rule;
- a prescribed compression protocol, with unloading/recovery tests;
- optional explicit solvent only if the question requires hydrodynamic coupling.

Candidate observables:
- coordination number and contact persistence;
- radius of gyration and structure factor / pair-correlation function;
- cluster-size distribution and fractal scaling over a stated fitting window;
- void fraction and network anisotropy;
- stress–strain curve, residual strain, and recovery after unloading.

**What it could establish:** qualitative regime maps and sensitivity of network rearrangement to effective interaction and bond-persistence parameters.

**What it cannot establish without additional physics and validation:** real pH-dependent silicate speciation, quantitative silanol condensation rates, industrial syneresis times, pore-liquid drainage, or predictive powder properties. Generic Lennard-Jones or bead-spring parameters must not be presented as chemically specific silica parameters.

### Level 2 — Pore-fluid transport / poromechanics (analytical model or OpenFOAM)

Use a continuum poroelastic or Darcy-type model if the target is drainage, sample-size dependence, or syneresis kinetics. Begin with the simplest geometry and boundary conditions supported by experiments.

OpenFOAM becomes justified if spatially resolved fluid flow, non-trivial geometry, evolving permeability, or coupled flow/solid deformation is essential and the required constitutive laws can be constrained. A CFD result with guessed permeability or modulus is not evidence; it is a sensitivity calculation and must be labelled as such.

### Level 3 — CFD–DEM (OpenFOAM + LIGGGHTS or another maintained DEM implementation)

Consider only for a well-defined particulate-flow question such as aggregate transport, collision, or fragmentation in a specified reactor or shear field.

Requirements:
- a defensible particle/aggregate representation and size distribution;
- calibrated contact, cohesion, and breakage laws;
- independently specified fluid properties and hydrodynamic coupling;
- mesh/time-step and coupling sensitivity checks;
- validation against published reactor, shear, or fragment-size data.

LIGGGHTS is a specialised and comparatively legacy DEM code; before choosing it, check current maintenance, compatibility, licensing, and coupling support. Do not assume an OpenFOAM–LIGGGHTS workflow is turnkey. CFD–DEM is not the first choice for nanoscale primary-particle chemistry or molecular syneresis.

### Level 4 — Atomistic MD or Monte Carlo (MC)

Use atomistic MD only if the review identifies a molecular-scale question that cannot be addressed with effective interactions, for example hydration-dependent silica surface interactions or ion-specific adsorption. This requires a validated silica/water/ion force field, chemically appropriate surface termination, and careful treatment of protonation and pH. Reactive force fields may be computationally costly and are not automatically reliable for all silicate reactions.

MC may be useful for equilibrium sampling, adsorption/speciation or configurational questions, but ordinary equilibrium MC does not provide physical syneresis kinetics. Kinetic MC would require a defensible transition model and rate constants.

Do not begin with atomistic MD/MC merely because these methods are available. First demonstrate that a molecular parameter materially controls a macroscopic claim in the evidence synthesis.

## Minimum validation and reporting requirements

Every simulation proposal must specify:
1. one falsifiable question and the claim it could strengthen, qualify, or challenge;
2. the exact material system and the boundary of transferability;
3. governing equations / interaction law and parameter provenance;
4. which parameters are measured, literature-derived, fitted, or assumed;
5. a baseline analytical or limiting-case check;
6. numerical convergence and sensitivity tests;
7. at least one comparison with independent published data not used solely to tune the model;
8. uncertainty and non-identifiability limitations;
9. reproducible input files, code version, and post-processing workflow.

A visually plausible trajectory or a single fitted curve is not validation.

## Initial go/no-go decision

**Do not launch LAMMPS, CFD–DEM, OpenFOAM, atomistic MD, or MC production runs yet.** The literature synthesis has not finished defining the dominant unresolved mechanism, and several key historical syneresis sources remain full-text inaccessible.

The preferred sequence is:
1. finish the source and claim–evidence audit;
2. decide whether the strongest unresolved question concerns network rearrangement, pore-fluid transport, or fragmentation;
3. identify data suitable for independent validation;
4. implement the smallest model that addresses that question;
5. expand to coupled or molecular methods only if the simpler model demonstrably fails.

A short, transparent sensitivity study is preferable to an elaborate but under-parameterised multiphysics simulation.


## Level 2 — Three-dimensional off-lattice Monte Carlo (C++): network reorganisation

This is now the preferred microscopic modelling candidate, motivated by the fractal-aggregate reorganisation mechanisms discussed by Schlomach & Kind (2007) and the 1000-primary-particle model system used by Sahabi & Kind (2011). It is a proposed extension, not a reproduction of either published implementation.

### Target question

For a pre-formed, three-dimensional fractal-like silica aggregate, how do contact coordination, effective attraction, and the probability of irreversible contact formation control structural compaction under a clearly specified consolidation protocol?

The initial model addresses **structural reorganisation**, not a complete physical simulation of syneresis. It will not claim to calculate pore-liquid drainage, pore pressure, or laboratory time unless a separate transport model and defensible kinetic calibration are added.

### Initial representation

- Off-lattice 3-D primary-particle centres with periodic boundaries; avoid a simple-cubic lattice as the physical starting structure.
- Generate or import a connected fractal-like aggregate and document its construction method, target fractal dimension, particle count, and radius of gyration.
- Start with a tractable system around 10^3 particles for comparison with the published Sahabi–Kind model scale; perform finite-size checks before drawing general conclusions.
- Use a transparent effective interaction model: a short-range attractive contact term and, only if justified, a repulsive contribution. Parameters are dimensionless or explicitly labelled assumed until independently sourced/calibrated.

### Monte Carlo moves and acceptance

1. Local particle translation / configurational diffusion.
2. Contact rearrangement (including rolling-like changes represented by particle translations; do not imply resolved surface rolling).
3. Detachment attempts with a coordination-dependent probability, following the qualitative mechanism reported by Schlomach & Kind (2007).
4. Reattachment / contact formation, with a separately defined reversible or persistent-contact rule.
5. Optional imposed compaction only after the statistical ensemble and protocol are stated (e.g. reduced accessible volume or an explicit external bias). A box contraction is not equivalent to solvent drainage.

For equilibrium-style moves, use a stated energy function and Metropolis acceptance. For irreversible or rate-based moves, specify transition probabilities separately; do not mix arbitrary kinetic rules into an equilibrium Boltzmann sampler without explaining the resulting ensemble.

### Observables

- Radius of gyration and estimated fractal dimension, with the fitted length-scale interval reported.
- Coordination-number distribution and mean coordination.
- Number of contacts, contact persistence, and fraction of persistent contacts.
- Aggregate compactness / occupied volume fraction and void statistics (with estimator definition).
- Particle displacement and local rearrangement statistics.
- Cluster connectivity and, where meaningful, pair-correlation / structure-factor measures.

### Verification and validation sequence

1. Unit tests for periodic distances, neighbour lists, energy changes, and acceptance probabilities.
2. Limiting-case checks: zero attraction, no detachment, and no compaction should behave as defined by the algorithm.
3. Reproducibility with fixed random seeds and independent-seed ensembles.
4. Finite-size, move-size, and neighbour-cutoff sensitivity.
5. Compare only like-for-like trends with the published Schlomach–Kind and Sahabi–Kind results; the exact original MC implementation and full details are not currently available, so do not claim a faithful reproduction.
6. Compare structural trends with experimental fractal/aggregation evidence only where material route and length scale are compatible.

### Physical-time warning

A Monte Carlo sweep is an algorithmic sampling unit, not automatically a second, minute, or laboratory ageing time. Mapping MC steps to physical time requires a kinetic formulation and calibration against independent time-resolved measurements. Until then, report step number and structural observables, not predicted syneresis times.

### Language and implementation

Implement the first version in standard C++ (C++17 or newer), with a small dependency-free core, deterministic seed option, text/CSV output, and separate configuration file. Keep the model and analysis scripts independent. Python may be used for plotting and statistical post-processing, but not as a required runtime dependency for the simulation core.

### Explicit exclusions in version 1

No explicit water molecules, ionic speciation, pH-dependent surface charge, silanol condensation chemistry, hydrodynamic interactions, Darcy flow, or pore-pressure field. Those require additional evidence and a separate model layer. The existing 1-D transport benchmark remains a complementary continuum reference; it should not be artificially coupled to the MC code in the first implementation.
