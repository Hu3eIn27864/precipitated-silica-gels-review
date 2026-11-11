# 1-D transport benchmark for syneresis

## Model

A homogeneous planar slab drained at both faces, using the classical linear
one-dimensional consolidation solution:

\[
U(t)=1-\frac{8}{\pi^2}\sum_{m=0}^{\infty}\frac{1}{(2m+1)^2}
\exp\left[-\frac{(2m+1)^2\pi^2 c_v t}{4H_d^2}\right]
\]

The predicted relative volume decrease is prescribed as
\(\Delta V/V_0=S_\infty U(t)\). Here \(H_d\) is the maximum drainage path,
\(c_v\) an effective consolidation diffusivity, and \(S_\infty\) ultimate
shrinkage.

## Run

Python 3.9+; standard library only:

    python3 syneresis_1d.py --cv 1e-10 --drainage-length 0.006 \
      --ultimate-shrinkage 0.20 --t-end-hours 72 --npoints 201 \
      --output trial.csv

These numerical values are illustrative placeholders, NOT measured
precipitated-silica parameters.

## Assumptions and limitations

- Planar slab; both faces perfectly drained.
- Homogeneous material and constant effective diffusivity.
- Linear small-strain consolidation; no evolving permeability or modulus.
- No explicit particle network, chemistry, pH, ionic strength, or reaction.
- Ultimate shrinkage is an independent input, not predicted.
- Cylinders and droplets require geometry-specific radial/spherical solutions.
- Fitted cv is a lumped parameter; it cannot independently identify
  permeability and modulus.

## Tests

Run the analytical-limit and dimensionless-scaling checks with:

    python3 -m unittest test_syneresis_1d.py

These are code-level checks, not validation against experimental silica data.

## Verification checks

1. At t=0, U=0; at long times, U approaches 1.
2. Increasing cv or decreasing Hd accelerates consolidation.
3. Curves collapse against cv*t/Hd^2.
4. Compare numerical output against the series formula before fitting data.

Extend to nonlinear permeability, viscoelastic relaxation, or other geometry
only when published data can constrain those terms.

The test suite additionally checks rejection of NaN/infinite inputs and convergence of the 1000-term default series against a 5000-term reference at a representative dimensionless time. The convergence test is specific to that test point; very early-time cases can require more terms. The function rejects non-finite inputs rather than silently returning a bounded but meaningless result.


## Geometry-specific first-mode scaling utility

`geometry_scaling.py` provides the ideal radial first-mode relations
`tau_1 = R^2/(alpha_01^2 D_app)` for an infinite cylinder with radial
drainage and `tau_1 = R^2/(pi^2 D_app)` for a sphere. It can convert in either
direction and rejects non-finite or non-positive inputs. The associated tests
check the inverse relations and the expected radius-squared scaling.

This is a **first-mode dimensional translation**, not a full transient
cylindrical/spherical consolidation solver. It assumes an ideal drained
surface and omits finite-cylinder end drainage, evolving sample shape,
nonuniform boundary conditions, and coupled changes in permeability and
skeleton stiffness. The resulting `D_app` remains a diagnostic apparent
diffusivity, not a directly measured material property. Do not use it to claim
that acid/base gels share a common transport coefficient without independent
validation.
