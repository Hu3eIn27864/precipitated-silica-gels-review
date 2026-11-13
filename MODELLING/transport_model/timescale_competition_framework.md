# Timescale competition between hydraulic drainage and network evolution

## Purpose

This note defines a falsifiable way to distinguish hydraulic-transport limitation from chemistry/mechanics-limited syneresis. It is a scaling framework, not a fitted constitutive law and not evidence that either regime has been observed in a particular precipitated-silica sample.

## Hydraulic relaxation scale

For the one-dimensional linear saturated poroelastic approximation,

\[
S\,\partial_t p=\partial_x\!\left(\lambda\,\partial_xp\right),
\qquad S\simeq M^{-1},\quad \lambda=\kappa/\mu,
\]

the characteristic hydraulic relaxation time over drainage length \(L_d\) is

\[
\tau_h\sim\frac{S L_d^2}{\lambda}
=\frac{\mu L_d^2}{\kappa M}.
\]

The omitted numerical prefactor depends on geometry, boundary conditions, and the definition of the characteristic time. This estimate assumes a saturated continuum, small deformation, and coefficients that can be treated as locally constant over the relaxation interval.

## Structural-evolution scale and regime indicator

Let \(\tau_r\) denote a measured or independently estimated characteristic time for network evolution. It must be operationally defined (for example, a characteristic time from a rheological modulus-growth curve or a structural observable), not chosen by fitting the same syneresis curve.

Define

\[
\Pi=\frac{\tau_h}{\tau_r}.
\]

Interpretation:

- \(\Pi\ll1\): pressure can relax hydraulically faster than the network evolves. The rate/extent of shrinkage may then be controlled primarily by the rate of stress generation, bond formation, or skeleton rearrangement. This is a candidate reaction/mechanics-limited regime.
- \(\Pi\gg1\): network evolution is faster than pressure can equilibrate by drainage. Persistent pore pressure and sample-size/drainage-length effects are expected; this is a candidate transport-limited regime.
- \(\Pi\sim1\): coupled evolution is expected; neither process can safely be treated as instantaneous relative to the other.

These are asymptotic hypotheses, not sharp phase boundaries. A distributed pore network has a spectrum of drainage times, and a viscoelastic skeleton has a spectrum of relaxation times.

## Important distinction: permeability and modulus do not have interchangeable effects

The scaling \(\tau_h\propto(\kappa M)^{-1}\) is the pressure-diffusion timescale in the simplified linear equation. Decreasing permeability lengthens pressure relaxation. Increasing constrained modulus shortens this pressure-diffusion timescale in that equation, but a stiffer skeleton can simultaneously reduce the magnitude of shrinkage produced by a given chemical eigenstrain or internal contractile stress. Therefore, the observed syneresis rate cannot be inferred from \(\tau_h\) alone.

For an aging gel, both \(\kappa(t)\) and \(M(t)\) may evolve, while the chemical driving term and the network's stress-free reference configuration may also change. A physically complete model must specify all of these separately. Do not simply substitute time-varying values into the constant-coefficient equation and interpret the result as a fully coupled poroelastic model.

## Experimental discrimination

A minimal matched experiment should measure, on the same formulation and aging history:

1. Syneresis or expelled-liquid volume versus time, with sample dimensions and drainage boundaries documented.
2. Permeability versus age, using a sufficiently small pressure gradient and monitoring deformation during the measurement.
3. Mechanical response versus age (confined compression or creep/recovery); oscillatory \(G'\) and \(G''\) are useful but are not automatically the constrained modulus \(M\).
4. A structural indicator versus age (porosity/pore-size distribution, scattering, microscopy, or another justified observable).
5. Liquid viscosity, temperature, pH, ionic strength, and dissolved-silica chemistry.

Use independent measurements to estimate \(\tau_h\) and \(\tau_r\), then predict which sample sizes or boundary conditions should show transport sensitivity. Do not infer both \(\kappa\) and \(M\) from a single syneresis curve.

## Falsifiable predictions

- At fixed chemistry and age, increasing drainage length should increase the hydraulic relaxation time approximately as \(L_d^2\) in the continuum regime.
- If transport limitation dominates, changing drainage length or boundary drainage resistance should systematically shift the time course, not merely its final shrinkage.
- If network-evolution limitation dominates, syneresis kinetics should correlate more strongly with independently measured structural/mechanical aging than with drainage length, once the samples are sufficiently small and well drained.
- If permeability falls strongly with age, late-time syneresis can become progressively more transport-limited even if the initial stage was not.
- If modulus rises while permeability falls, their opposing contributions to \(\tau_h\) must be evaluated separately; a net timescale trend cannot be assumed.

## pH comparison

Acidic and alkaline formulations must be compared at matched silica concentration, ionic strength/counterion as far as feasible, temperature, and sample geometry. pH can affect condensation, dissolution/reprecipitation, surface charge, and particle interactions. It is therefore not a single-variable switch for a universal kinetic mechanism. In particular, dissolution/reprecipitation may alter pore geometry and connectivity in ways not captured by a scalar porosity.

## Scope and exclusions

This framework does not yet include unsaturated flow, moving boundaries, membrane resistance, spatially evolving porosity, nonlinear permeability, anisotropy, chemical mass transport, or pressure feedback on microscopic Monte Carlo moves. It does not establish a Kozeny–Carman closure for fractal or heterogeneous precipitated-silica gels. Those additions require independent evidence and separate validation.

## Provenance note

The scaling follows from the stated linear diffusion equation. Regime labels are proposed diagnostics. They are not experimental conclusions for the digitised Wilhelm–Kind curves, whose AI-assisted trace readings remain unverified and must not be treated as raw data.
