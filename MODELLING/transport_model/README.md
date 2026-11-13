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
quantity. If hydraulic conductivity is denoted by \(K\) [m/s],

\[c_v=\frac{K}{m_v\gamma_w}=\frac{K M}{\gamma_w},\]

where \(m_v\) is the coefficient of volume compressibility,
\(M=1/m_v\) is the appropriate constrained modulus, and
\(\gamma_w=\rho g\) is liquid unit weight. If intrinsic permeability
\(\kappa\) [m²] is used instead, Darcy's law gives

\[c_v=\frac{\kappa M}{\mu},\]

where \(\mu\) is dynamic viscosity. Hydraulic conductivity and intrinsic
permeability are not the same quantity and must not share an ambiguous
symbol or unit. A fit to a single shrinkage/consolidation curve identifies
at most the relevant lumped combination (also subject to drainage length
and boundary assumptions), not the hydraulic and mechanical parameters
separately. Independent permeability/conductivity and mechanical
measurements are needed to separate them. Do not label fitted \(c_v\) as
a measured gel permeability.

### Expanded radial convergence validation

The radial test suite now checks both cylinder and sphere against the
independent eigenfunction series at (Fo=0.1), with joint grid/time
refinement (30, 60 and 120 cells) and time-step refinement at fixed
120-cell resolution. The local diagnostic errors under joint refinement
were 0.01905, 0.00480 and 0.000964 for the cylinder, and 0.02649, 0.00671
and 0.00135 for the sphere. Hosted CI [#293](https://github.com/Hu3eIn27864/precipitated-silica-gels-review/actions/runs/43021684276)
passed the expanded radial suite as part of the complete workflow.


The corrected planar reference table is now enforced by regression tests at
seven nonzero Fourier numbers in addition to the independent (Fo_d=0.1)
reference test. Hosted CI [#295](https://github.com/Hu3eIn27864/precipitated-silica-gels-review/actions/runs/43021757732)
passed the complete integrated workflow, including all updated 1-D and
radial transport tests.

## Finite-cylinder first-mode extension (idealised)

The helper finite_cylinder_first_mode_time_constant adds the first separable
eigenmode for a finite cylinder with a drained curved wall and explicitly
selected end conditions. For a cylinder of radius R and full height H,
constant isotropic diffusivity D, and both flat ends perfectly drained,

    tau_1^-1 = D * [(2.4048256/R)^2 + (pi/H)^2].

With sealed (zero-flux) ends, the axial contribution is zero and the result
reduces to the infinite-cylinder radial first mode. This provides a clean
limiting-case test and demonstrates why an infinite-cylinder conversion can
overestimate the characteristic time when end drainage is active.

This is a first-eigenvalue calculation, not a transient finite-cylinder
solver. It assumes uniform initial excess pressure, constant scalar D,
perfect drainage at the stated surfaces, and separable geometry. No sample
height is inferred from the reported 3 mL volume, and the Wilhelm & Kind
(2015) pyknometer cylinder is not assigned end-drainage conditions without
source evidence. Mixed drainage, external resistance and evolving geometry
remain unresolved. Tests verify the mathematical limit and parameter
monotonicity only.
## Minimal permeability--mechanics coupling identity

`poroelastic_coupling.py` implements the dimensionally distinct classical
identities:

- Using hydraulic conductivity (K) [m/s]:
  (c_v=K M/\gamma_w), where (gamma_w=\rho g) is liquid unit weight.
- Using intrinsic permeability (kappa) [m²]:
  (c_v=\kappa M/\mu), where (mu) is dynamic viscosity.

The appropriate constrained modulus (M) is an independent input in both
forms. The code exposes separate forward and inverse functions; it does not
silently treat intrinsic permeability as hydraulic conductivity. The default
(gamma_w=9810) N/m³ is a water reference, not a measured pore-liquid
property. The inversion is meaningful only if the corresponding modulus and
fluid property are independently known. A fitted (c_v) alone cannot identify
both hydraulic and mechanical parameters. No constitutive evolution law is
imposed. Tests check both identities, inverses, separate sensitivity to
hydraulic and mechanical inputs, and invalid values; these are code/unit
checks, not a calibrated silica-gel model.

## Geometry-resolved experimental comparison

`LITERATURE/experimental_syneresis_comparison.csv` separates natural
syneresis fit parameters from centrifugal forced-syneresis records. It
records the reported geometry without silently inferring cylinder height
from sample volume or exact droplet sphericity. Boundary-condition
uncertainty is explicit. These records are not pooled into a single fit;
they do not identify permeability or a unique diffusivity.

## Published-fit curve reconstruction (not raw-data digitisation)

`reconstruct_published_syneresis_fits.py` generates a derived CSV from the tabulated
`Smax` and `tau_h` values in the two literature comparison tables. It uses the
single-exponential empirical form

\[
S(t)=S_{\max}\left[1-\exp(-t/\tau)\right].
\]

Run from the repository root:

    python3 MODELLING/transport_model/reconstruct_published_syneresis_fits.py

The default output is
`LITERATURE/derived/published_fit_curve_reconstructions.csv`. Each row is
explicitly labelled
`published_empirical_fit_reconstruction_not_digitised_data`. These generated
points merely sample the reported fit equation and parameters; they are not
experimental marker coordinates, replicate measurements, or an independent
validation dataset. The procedure does not recover residuals, uncertainty,
scatter, or deviations of measurements from the empirical fit.

Tests:

    python3 -m unittest discover -s MODELLING/transport_model -p 'test_reconstruct*.py' -v

Actual figure digitisation remains a separate task and must retain figure,
axis-calibration, pixel/marker, and digitisation-uncertainty metadata.

## Prescribed time-dependent hydraulic mobility (one-way prototype)

`time_dependent_1d.py` extends the fixed-coefficient slab solver by accepting
one positive cellwise hydraulic-mobility field per backward-Euler time step.
Storage compliance remains fixed. This isolates the effect of a prescribed
aging permeability/mobility field while preserving conservative pressure
storage and boundary-flux accounting.

The implementation is intentionally not a fully coupled aging model:
there is no time-varying modulus/storage, porosity evolution, moving boundary,
structure-derived permeability law, membrane-resistance boundary condition,
or pressure-to-MC feedback. See
`prescribed_aging_permeability_design.md` for equations, usage and stop rules.

Tests:

    python3 -m unittest discover -s MODELLING/transport_model -p 'test_time_dependent_1d.py' -v

A successful test run establishes numerical consistency only, not physical
validation or silica-specific calibration.


## Finite external drainage resistance

The prescribed-aging solver `time_dependent_1d.py` now accepts independent
left/right area-specific boundary hydraulic resistances
(`left_boundary_resistance_pa_s_m`, `right_boundary_resistance_pa_s_m`,
units Pa s/m). These represent lumped membrane/support/deposit resistance in
series with the half-cell Darcy resistance. Zero recovers perfect drainage;
large resistance approaches a sealed boundary. The default remains zero, so
existing calls are unchanged.

The extension is documented in
`external_drainage_resistance.md`. Tests cover the zero-resistance limit,
slower relaxation with finite resistance, global mass balance with asymmetric
boundaries and invalid inputs. This is a boundary-condition sensitivity
model, not a calibrated membrane model or proof that the reported base-gel
membrane layer explains the full acid/base kinetic reversal.

## Fixed-interface two-layer eigenfunction verification

`layered_reference.py` provides an independent analytical reference for a
double-drained slab with two piecewise-constant layers separated at a fixed
physical coordinate x=a. Pressure and hydraulic flux are continuous at the
interface. For decay rate sigma, ki=sqrt(sigma Si/lambda_i), and the
characteristic equation is

\[
\lambda_1 k_1\cot(k_1 a)+
\lambda_2 k_2\cot(k_2(L-a))=0.
\]

The implementation solves the equivalent determinant equation, avoiding
cotangent poles, then evaluates the storage-weighted modal expansion for a
uniform initial excess pressure. It uses only the Python standard library.

Run the independent tests with:

    python3 -m unittest discover -s MODELLING/transport_model -p 'test_layered_reference.py' -v

The tests check ordered eigenvalues and a first-eigenvalue regression value,
the modal reference limits/monotonicity, finite-volume convergence against
the fixed-interface analytical result under grid refinement, time-step
refinement, and an independent boundary-gradient reconstruction. The latter
uses p=0 at each boundary and the adjacent cell-centre pressure to reconstruct
Darcy flux, then compares its backward-Euler time integral with independently
computed storage loss; it does not consume the solver's reported flux array.

The fixed-interface verification case uses L=1, a=0.375, (S1,lambda1)=(1,1)
and (S2,lambda2)=(2,0.15) in consistent dimensionless verification units.
The interface is exactly a cell face for N=40,80,160. At t=0.005, the
analytical storage-weighted pressure ratio is 0.9240059118. Spatial errors
for those grids are approximately 3.84e-3, 8.33e-4 and 2.05e-4. At N=160,
time-step refinement from 8e-6 to 4e-6 to 2e-6 also decreases the error.
The independently reconstructed integrated boundary flux differs from
storage loss by about 1.3e-13 in the selected regression case.

These checks verify the numerical implementation for a fixed two-layer
linear problem. They do not validate material parameters, constitutive laws,
or the applicability of the model to precipitated-silica syneresis.
