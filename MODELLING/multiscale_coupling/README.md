# Multiscale coupling architecture: MD / Monte Carlo / porous-medium CFD

## Status and scope

This document specifies a staged, one-way-first multiscale architecture. It is a design proposal, not an implemented or validated coupled solver. The target phenomenon is structural reorganisation and liquid expulsion during consolidation/syneresis of precipitated silica gels.

The key modelling principle is to couple models through **measurable effective quantities**, not by directly exchanging every atomistic coordinate with a macroscopic CFD mesh.

## Physical question

How does the evolution of silica-particle contacts change network stiffness and permeability, and how do those evolving properties feed back on pore-liquid pressure and drainage during syneresis?

Working causal loop:

1. Local particle interactions and contact formation change network topology.
2. Network topology changes effective stiffness and pore-space geometry.
3. Pore-space geometry changes permeability and fluid resistance.
4. Fluid pressure gradients and drainage alter local stress and compaction.
5. Compaction changes particle contacts again.

This is a hypothesis to test, not an established causal sequence in every silica-gel system.

## Model roles and hand-off variables

| Model | Resolved physics | Inputs | Outputs passed onward |
|---|---|---|---|
| Atomistic MD | Hydration, surface interactions, ion effects, local contact energetics (only if force field validated) | Silica surface termination, water, ions, temperature, protonation assumptions | Effective interaction potential / potential of mean force; possibly local adhesion or contact energy |
| 3-D off-lattice MC | Statistical rearrangement of a coarse-grained aggregate; contact creation/loss and topology | Effective interaction law, initial aggregate, protocol | Coordination statistics, contact persistence, (R_g), fractal/compactness measures, structural state variables |
| Porous-medium CFD / poromechanics | Darcy/Brinkman-scale liquid transport, pore pressure, stress and deformation | Permeability law, stiffness/constitutive law, fluid viscosity, geometry, drainage boundaries | Local pressure, fluid flux, strain / compaction field |

MD does not directly provide a macroscopic permeability from a small atomistic box unless a representative porous structure and an appropriate upscaling procedure are defined. MC structural observables likewise need a separate mapping to continuum constitutive quantities.

## Recommended coupling sequence

### Stage A — MD-informed effective interactions (one-way)

Use MD only if a chemically credible silica/water/ion model can be established. Compute a potential of mean force or other clearly defined effective interaction for two silica surface patches/particles under selected conditions. Record surface hydroxylation, protonation, ionic composition, temperature, water model, force field, finite-size effects and sampling uncertainty.

If reliable reactive chemistry or pH control cannot be represented, do not claim that MD predicts pH-dependent siloxane bond formation. In that case, use literature-bounded effective interaction parameters and treat them as uncertain.

### Stage B — MC structural ensemble

Use the effective interaction in a 3-D off-lattice MC network model. The MC model resolves aggregate-scale contact rearrangement and persistent-contact rules. It produces a family of structures across consolidation states, not an automatic physical time trajectory.

For each structural state, estimate:
- coordination-number distribution and persistent-contact fraction;
- radius of gyration and fractal scaling interval;
- solid fraction / void fraction using a stated geometric estimator;
- pore-size distribution and connectivity using a reproducible algorithm;
- structural anisotropy, if loading is directional.

### Stage C — Upscale structure to continuum properties

Generate representative volume elements (RVEs) from MC structures. Estimate permeability by solving a pore-scale Stokes-flow problem on the resolved pore geometry or by a separately verified numerical homogenisation method. Estimate effective stiffness from a mechanical network calculation or small-strain loading test.

Fit relations such as

\[
k = k(\phi, z, f_{\rm persistent}, \ldots), \qquad
G = G(\phi, z, f_{\rm persistent}, \ldots),
\]

where (k) is permeability, (phi) is solid fraction (definition fixed), (z) is mean coordination, and (G) is an effective shear modulus. These are candidate constitutive maps, not assumed universal laws. Include uncertainty and test whether the RVE is large enough to be representative.

### Stage D — Porous-medium CFD / poromechanics

For a gel with unresolved pores, the first continuum model should normally be Darcy flow coupled to a deformable porous skeleton (poroelasticity / poromechanics), not a fully resolved Navier–Stokes CFD calculation over every nanopore.

A minimal saturated formulation may combine fluid mass conservation, Darcy flux, and skeleton force balance. For example:

\[
\mathbf q = -\frac{k(\mathcal S)}{\mu}\nabla p,
\]

where (mathbf q) is Darcy flux, (k(\mathcal S)) is permeability dependent on structural state (mathcal S), (mu) is liquid viscosity, and (p) is pore pressure. A separate constitutive law relates effective stress and deformation to strain and structural state. The precise equations and boundary conditions must be selected for the actual experiment; this expression is only a starting point.

The continuum solver returns pressure, flux and strain fields. These fields can be converted into local compaction or loading conditions for MC in a subsequent coupling stage.

### Stage E — Bidirectional staggered coupling

Only after one-way stages are verified should a staggered coupling be attempted:

1. CFD/poromechanics advances pressure and strain over a continuum time interval.
2. Representative MC domains receive local stress/compaction conditions and update their structural state.
3. MC-derived permeability and stiffness are averaged and returned to the continuum model.
4. Iterate with a controlled coupling interval and convergence criterion.

The MC time mapping must be calibrated before interpreting this as physical time. If MC remains equilibrium/configurational, use it only to generate state-dependent constitutive maps, not to advance a kinetic history.

## What is not recommended initially

- Direct atom-by-atom coupling of MD to a macroscopic CFD domain.
- Fully resolved CFD through every nanoscale pore of a millimetre-scale gel sample.
- Treating MC sweeps as seconds or applying arbitrary detachment probabilities as physical rate constants.
- Using an arbitrary Lennard-Jones silica model as validated surface chemistry.
- Assuming a universal permeability–porosity or modulus–coordination relation without testing it against independent data.
- Calibrating all submodels against the same syneresis curve and then calling that independent validation.

## Minimum validation ladder

1. **MD:** validate bulk water and relevant silica-surface properties; test force-field and surface-chemistry sensitivity.
2. **MC:** unit tests, detailed balance for equilibrium moves, reproducibility, finite-size and move-size sensitivity; compare structural observables with available aggregate evidence.
3. **Upscaling:** mesh convergence for pore-scale flow, mechanical solver checks, RVE-size convergence, and comparison with limiting analytical geometries.
4. **Continuum:** recover the 1-D analytical consolidation benchmark, check mass conservation, mesh/time-step convergence, and test geometry/boundary-condition limits.
5. **Coupled model:** verify conservation across hand-offs, coupling-interval sensitivity, and validation against experimental data not used to determine all parameters.

## Data connection to this project

Potential target-system comparisons include the Wilhelm & Kind natural/enforced syneresis data and the additional centrifugal data described in Wilhelm (2017). These are not yet sufficient by themselves to identify a unique permeability law, modulus law and kinetic contact model. Scherer (1989) provides a useful poromechanical conceptual benchmark, but its accessible evidence is from alkoxide-derived silica gels and should not be treated as direct validation for industrial precipitated silica.

## Practical implementation order

1. Finish and test the independent C++ MC core.
2. Define a simple pore-geometry estimator and export representative structures.
3. Build a separate pore-scale Stokes-flow / permeability estimator for those structures.
4. Build a continuum Darcy–poroelastic solver and verify it against the existing analytical 1-D benchmark.
5. Couple MC-derived (k(\mathcal S)) and stiffness maps to the continuum model one-way.
6. Attempt bidirectional staggered coupling only if data support time-dependent structural feedback.

The initial deliverable should be a verified one-way multiscale workflow. Bidirectional coupling is a later research objective, not a prerequisite for obtaining useful scientific results.
