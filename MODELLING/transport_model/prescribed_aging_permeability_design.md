# Prescribed-aging permeability: first time-dependent 1-D extension

**Status:** numerical prototype; one-way coupling only. No precipitated-silica parameters or constitutive aging law are calibrated.

## 1. Why this is the next minimal step

The fixed-coefficient solver verifies spatially heterogeneous Darcy/storage diffusion. The next identifiable numerical increment is to prescribe a time-dependent hydraulic mobility while keeping storage compliance fixed. This isolates the consequence of a changing permeability (or viscosity ratio) without silently changing the pressure-storage term.

The new `time_dependent_1d.py` solves, on a fixed slab,

\\[
S(x)\\frac{\\partial p}{\\partial t}
=\\frac{\\partial}{\\partial x}
\\left[\\lambda(x,t)\\frac{\\partial p}{\\partial x}\\right],
\\qquad \\lambda=\\frac{\\kappa}{\\mu},
\\]

with double-drained zero excess-pressure boundaries. (S=1/M) is fixed in time and \\(\\lambda\\) is supplied as one positive cellwise field for each backward-Euler step. The mobility at the new time level is used implicitly. Internal face mobility is the harmonic mean, preserving flux continuity across a discontinuity.

## 2. What the extension can test

- Constant mobility schedule recovers the existing fixed-coefficient solver.
- Increasing or decreasing prescribed mobility changes the pressure-relaxation rate in the expected direction.
- Spatially heterogeneous mobility can evolve with time.
- Per-step storage loss is balanced by integrated boundary outflow to numerical precision.

The returned outputs include mean pressure, full pressure profiles, boundary outflow and a discrete mass-balance residual.

## 3. Explicit limitations

This is not yet a fully coupled syneresis model.

- Storage compliance and constrained modulus are fixed.
- The domain and drainage length are fixed.
- Porosity and skeleton deformation do not evolve.
- Mobility is prescribed, not calculated from porosity, pore-throat size, fractal dimension or coordination number.
- There is no feedback from pressure or compaction to a particle/MC state.
- The model does not distinguish intrinsic gel permeability from an external membrane/support resistance unless that resistance is separately represented in the boundary condition.

A time-dependent modulus cannot be inserted by merely changing (S(t)) in this equation. The conservative accumulation term, evolving reference/current volume, deformation kinematics and constitutive stress law must be derived consistently. This is deliberately deferred.

## 4. How to use it

From the repository root, the module can be imported from the transport-model directory. Supply a list of mobility arrays, one per time step:

```python
from time_dependent_1d import solve_1d_time_dependent_mobility

n_cells = 40
n_steps = 100
storage = [1.0e-5] * n_cells
mobility_schedule = [
    [1.0e-12 * (1.0 - 0.3*k/(n_steps-1))] * n_cells
    for k in range(n_steps)
]
result = solve_1d_time_dependent_mobility(
    storage, mobility_schedule, thickness_m=1.0e-3, dt_s=1.0
)
```

The example is dimensionless in intent and illustrative only; its numerical values are not silica-gel properties.

Tests are in `test_time_dependent_1d.py`. They check constant-coefficient recovery, response to increasing mobility, positivity/monotonicity, mass balance and input validation. Hosted CI is required before calling these tests passed.

## 5. Physical interpretation and falsification

If measured permeability decreases during aging at otherwise fixed \\(S\\), the model predicts slower pressure relaxation. If permeability increases, relaxation accelerates. Neither trend alone determines the shrinkage rate in a real gel if modulus, viscoelasticity, sample geometry or membrane resistance also evolve.

A decisive experiment must measure \\(\\kappa(t)\\) independently while monitoring sample deformation and correct for membrane/support resistance. The pressure-decay or expelled-liquid response can then be predicted without fitting a free time constant to that same response.

## References and scope

Scherer (1989) showed that syneresis kinetics depend on sample size, permeability and viscoelastic network properties, and compared shrinkage curves with predictions based on independently measured permeability, modulus and viscosity (DOI 10.1016/0022-3093(89)90329-3). This is an alkoxide-derived silica-gel precedent, not a precipitated-silica calibration dataset. The present solver is a numerical extension motivated by that coupling principle, not a reproduction of Scherer's constitutive model.
