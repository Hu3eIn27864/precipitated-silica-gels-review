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


## Transient radial finite-volume benchmark

`radial_consolidation.py` adds a cell-centred, conservative finite-volume
solver for the dimensionless radial equation in an ideal infinite cylinder
or sphere. It uses backward Euler, symmetry (zero flux) at the centre, and a
perfectly drained Dirichlet boundary at the outer surface. The solver returns
the volume-weighted mean excess-pressure ratio at requested Fourier numbers
(Fo=c_v t/R^2); degree of consolidation is one minus that ratio.

The module also provides independent eigenfunction-series references:
`4/alpha_n^2 * exp(-alpha_n^2 Fo)` for the cylinder (alpha_n are J0 zeros)
and `6/(n^2 pi^2) * exp(-n^2 pi^2 Fo)` for the sphere. The cylindrical
reference currently tabulates the first ten J0 roots. The tests check
initial/long-time limits, monotonicity, finite-volume agreement with the
series at several times, and improvement under grid/time refinement.

Run all transport tests with:

    python3 -m unittest discover -s MODELLING/transport_model -p 'test_*.py' -v

This is a numerical benchmark under constant-coefficient ideal boundary
conditions. It does not yet model finite-cylinder end drainage, nonlinear
permeability, viscoelasticity, changing geometry, pH effects, or coupled
network reorganisation. Agreement with the series is code verification, not
experimental validation of precipitated-silica syneresis.


### Early-time numerical stability of the planar solution

The direct odd-eigenvalue series converges slowly as (Fo_d=c_v t/H_d^2\to0).
For (Fo_d<0.01), the implementation now uses the Poisson-transformed
short-time asymptotic (U\simeq2\sqrt{Fo_d/\pi}), whose omitted corrections
are exponentially small in (1/Fo_d). This avoids a spurious dependence on
the arbitrary number of retained eigenmodes at very early times. Tests check
term-count independence in the short-time branch, square-root scaling and
continuity at the branch threshold. This is a numerical evaluation improvement,
not a change to the physical assumptions of the linear slab model.


### Regression correction: planar eigenvalue exponent

The branch-transition regression test exposed an implementation error in the
planar series exponent. The correct exponent is
\((2m+1)^2\pi^2 c_v t/(4H_d^2)\); the previous code had inverted the
\(\pi^2/4\) factor. The implementation is corrected and a reference-value
test at \(c_v t/H_d^2=0.1\) is now included. The short-time asymptotic branch
and the corrected eigenfunction series agree continuously at the chosen
threshold. Hosted CI #290 and #291 passed the full transport test suite and
the integrated workflow. This correction changes prior numerical outputs
from the 1-D benchmark; any previous illustrative curves generated by the
old implementation should be regenerated before reuse.


## Corrected planar reference values

The corrected analytical implementation was independently evaluated at the
following dimensionless times (T_v=c_v t/H_d^2). These values are
dimensionless code-verification references, not fitted silica-gel data.

| (T_v) | Average degree of consolidation (U) |
|---:|---:|
| 0 | 0 |
| 0.001 | 0.0356824823 |
| 0.01 | 0.1128379167 |
| 0.05 | 0.2523132522 |
| 0.1 | 0.3568234005 |
| 0.2 | 0.5040878202 |
| 0.5 | 0.7639503307 |
| 1.0 | 0.9312596785 |
| 2.0 | 0.9941704789 |

The short-time approximation and full series agree to exponentially small
corrections at the switch (T_v=0.01). Any earlier curves produced before the
eigenvalue-exponent correction must be regenerated.

## Parameter identifiability

In classical linear consolidation, the effective coefficient is a lumped
quantity, conventionally (c_v=k/(m_v\gamma_w)), where (k) is hydraulic
permeability, (m_v) is the coefficient of volume compressibility and
\(\gamma_w\) is the liquid unit weight. Equivalently, if an appropriate
constrained modulus (M=1/m_v) is used, (c_v=kM/\gamma_w). A fit to a
single shrinkage/consolidation curve therefore identifies at most this
combination (subject also to drainage length and boundary assumptions), not
(k) and (M) separately. Independent permeability and mechanical
measurements are needed to separate them. This is a central reason not to
label a fitted (c_v) as a measured gel permeability.
