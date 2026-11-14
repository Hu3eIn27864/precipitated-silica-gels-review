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
Hosted CI [#351](https://github.com/Hu3eIn27864/precipitated-silica-gels-review/actions/runs/43506021553) passed after the layered reference and tests were committed; the complete 1-D transport suite reported **68/68 tests passing**, including all six fixed-interface tests. This is numerical code verification only.


## Manufactured-solution verification with spatially variable coefficients

`heterogeneous_1d.py` now accepts an optional cell-centred initial pressure profile and a source callback
`source_term_s_inv(x, t)`. The solver advances

\[
S(x)\,\partial_t p = \partial_x\!\left(\lambda(x)\,\partial_x p\right)+f(x,t)
\]

with backward Euler; the source is evaluated at cell centres and the new time
level. The source has units s⁻¹ when S is in Pa⁻¹, p in Pa, and λ in
m²/(Pa s). The default path (uniform initial pressure, no source) is unchanged.

`test_manufactured_solution.py` prescribes
\(p(x,t)=e^{-t}\sin(\pi x/L)\), with smooth nonconstant
\(S(x)=1+0.4x\) and \(\lambda(x)=1+0.3x\) on \(L=1\). The source is
derived independently as \(f=S p_t-\partial_x(\lambda p_x)\). Tests cover
spatial refinement, temporal refinement against a small-time-step reference
on the same grid, source-inclusive global storage/flux balance, initial
profile handling, finite/nonnegative pressure and invalid inputs.

Run:

    python3 -m unittest discover -s MODELLING/transport_model -p 'test_manufactured_solution.py' -v

Local focused results: five tests pass. At N=20,40,80 the discrete L2
errors are approximately 3.377e-4, 8.471e-5 and 2.119e-5 (about second-order
spatial convergence with dt proportional to dx²). At N=40, temporal
differences against dt=1e-5 are 2.388e-6, 1.165e-6 and 5.519e-7 for
dt=4e-4,2e-4,1e-4. The maximum source-inclusive discrete balance residual
in the selected run is 1.18e-16.

These results verify the discretisation for a smooth manufactured problem
with variable storage and mobility. They do not verify discontinuous
coefficients, evolving coefficients, silica material parameters, or
physical constitutive validity.

### Discontinuous-interface eigenmode verification

The fixed-interface suite additionally tests a nonzero-flux eigenmode of the two-layer operator. The mode is assembled from phi1=sin(k1*x) and phi2=A*sin(k2*(L-x)), with A chosen for pressure continuity. The independent two-layer characteristic equation enforces continuity of lambda*dp/dx. Unlike the earlier uniform-initial-pressure mean-response check, this test directly evolves a spatial eigenfunction with nonzero interface flux and compares the full cell-centred profile with exp(-sigma*t)*phi(x).

For N=40,80,160 and dt=0.05*dx^2, the discrete L2 errors at t=0.05 are approximately 1.5534e-4, 3.8877e-5 and 9.7218e-6, respectively, consistent with second-order spatial convergence. The test also asserts pressure and flux continuity at the interface and explicitly rejects the trivial zero-interface-flux case. Run with the existing test_layered_reference.py command above.

This verifies the piecewise-constant discontinuity at a grid-aligned fixed interface for a nonzero-flux eigenmode. It does not yet test a moving or off-grid interface, more than two layers, or nonlinear constitutive jumps.

### Off-grid interface, multilayer reference and time-varying mobility — 13 November 2026

Three additional verification branches were added after the grid-aligned two-layer eigenmode test.

**Off-grid two-layer interface.** The layered-reference test now places the material jump at x=0.37 for N=40,80,160, so the interface is not a cell face. It compares the cell-centred-coefficient solver with the independent two-layer eigenfunction reference and requires the mean-pressure error to decrease under refinement. This is deliberately a convergence/limitation test: the present solver does not receive the exact subcell interface coordinate, and its cell-centre sampling does not provide a general interface-fitted second-order guarantee. A future interface-aware finite-volume representation should integrate storage over each cut cell and use exact series resistance for faces crossed by a material boundary.

**Three-layer analytical eigenvalue reference.** multilayer_reference.py propagates pressure and flux (lambda*p_x) exactly through each piecewise-constant layer with a transfer matrix. Tests check the homogeneous limit when all three layers are identical, ordered eigenvalues for a heterogeneous three-layer stack, and the characteristic residual at each computed root. This is an independent eigenvalue reference; it is not yet a multilayer transient finite-volume convergence benchmark.

**Time-varying mobility.** A new test uses the time transformation theta(t)=integral(lambda/S dt) to compare the existing prescribed-mobility schedule solver with an independent analytical reference for spatially uniform lambda(t)=1+0.5t and fixed S=1. It checks time-step convergence of mean pressure, stepwise storage/flux balance and nonnegative pressure. The solver still keeps storage compliance fixed and accepts mobility as a per-step schedule; this is not a coupled aging/poroelastic model.

Hosted CI transport-test steps passed for workflow #360 (off-grid interface), #362 (three-layer tests), and #363 (time-dependent mobility reference). All four integrated workflows #360–#363 completed successfully, including build, C++ tests, Python ensemble analysis, the full 1-D transport suite and the downstream syneresis/DLCA pilot stages. See:
- https://github.com/Hu3eIn27864/precipitated-silica-gels-review/actions/runs/43509969646
- https://github.com/Hu3eIn27864/precipitated-silica-gels-review/actions/runs/43509979674
- https://github.com/Hu3eIn27864/precipitated-silica-gels-review/actions/runs/43509984528

These are numerical verification results only. They do not validate precipitated-silica material parameters, constitutive laws, or physical predictions of syneresis.


## Interface-aware finite-volume discretisation

Added interface_aware_1d.py as a separate solver so the established cell-centred-array API remains backward compatible. Unlike the prior off-grid test, this solver receives the exact physical layer boundaries.

For piecewise-constant layers it computes:
- exact storage capacity in each finite volume, C_i = integral_cell S(x) dx, including cells cut by a material interface;
- exact centre-to-centre hydraulic resistance, R_(i+1/2) = integral_between_centres 1/lambda(x) dx, then conductance G=1/R;
- exact boundary half-cell resistance from each drained boundary to its adjacent pressure centre.

The resulting backward-Euler system is conservative. Its global residual is the storage change plus time-integrated boundary outflow. Tests cover the homogeneous-material limit, a non-grid-aligned two-layer comparison against the independent eigenfunction series, exact cut-cell capacity and crossed-face resistance, a three-layer conservation/positivity case, and invalid layer partitions.

Usage:
    from interface_aware_1d import solve_interface_aware
    result = solve_interface_aware(
        layer_boundaries_m=[0.0, 0.37, 1.0],
        storage_compliance_pa_inv=[1.0, 2.0],
        mobility_m2_pa_s=[1.0, 0.15],
        n_cells=80, thickness_m=1.0, dt_s=1e-5, n_steps=100)

This is an interface-aware, piecewise-constant 1-D method with cell-centred representative pressures and mass-lumped storage. With finite contact resistance, it augments the grid by a co-located pair of minus/plus interface pressure degrees of freedom; the associated control volumes are split exactly at the interface. It is not a high-order method for smoothly varying coefficients inside layers, moving interfaces, or nonlinear mobility. It does not validate silica constitutive parameters.


### Off-grid interface eigenmode verification

The interface-aware solver also accepts an explicit cell-centred initial pressure profile. This enables a full-profile eigenmode test for a two-layer jump located inside a cell. The test compares the transient numerical profile with the independent analytical first eigenmode, whose pressure and nonzero Darcy flux are continuous at the physical interface, over three grid resolutions. This is a stronger check than comparing only the spatial mean. The augmented two-sided implementation passed all 92 transport tests in hosted CI #399; the full integrated workflow also completed successfully. No formal spatial convergence order is claimed.


## Finite contact resistance at internal material interfaces

`interface_aware_1d.py` accepts an optional area-specific contact resistance for each internal material interface, in Pa s/m. It is added in series to the exact bulk resistance between adjacent cell centres. For the transfer state q=lambda dp/dx, the interface law is q_left=q_right and p_right-p_left=R_c q. The physical Darcy flux is -q; this sign convention makes a positive resistance increase the pressure jump in the direction of increasing x for positive q.

`multilayer_reference.py` now applies the same jump law as an independent transfer-matrix eigenvalue reference. Zero contact resistance recovers the perfectly bonded interface; positive resistance slows modal relaxation. Tests cover this zero limit, nonnegative-input validation, slower drainage in a three-layer FV stack, and conservation. A nonzero contact resistance is represented by separate minus/plus interface degrees of freedom, including when the interface coincides with an original cell centre. The ordinary cell-centred profile returned for compatibility averages the two traces at a coincident centre; the complete `node_profiles_pa`, `node_coordinates_m`, and `node_sides` arrays preserve the one-sided values.

The contact resistance is an optional phenomenological parameter, not a measured silica-gel property. It must not be fitted independently from bulk mobility without additional measurements or identifiability analysis.


## Two-sided interface degrees of freedom

When any contact resistance is positive, the solver augments the one-dimensional FV graph with a pair of co-located `minus` and `plus` pressure unknowns at each such interface. The two adjacent control volumes are split at the physical interface, so their storage is integrated on the correct material side. The link between the traces has conductance `1/R_c`; bulk links on either side use the exact integrated resistance. This works both for off-grid interfaces and when the interface exactly coincides with an original cell centre. The solver returns the augmented `node_profiles_pa`, `node_coordinates_m`, and `node_sides`; the legacy `profiles_pa` remains an original-cell-centre projection and averages the two traces if the interface coincides with a centre.

The new test checks the coincident-centre case explicitly, including the finite jump and exact contact conductance. The three-layer eigenmode test continues to compare the transient FV solution with the independent transfer-matrix spectrum. The current scheme remains mass-lumped and first-order in time (backward Euler); no higher-order spatial claim is made. Contact resistance remains phenomenological and uncalibrated for silica gels.

## Local identifiability sensitivity utility

`identifiability.py` builds an uncertainty-weighted finite-difference Jacobian
of log modal decay rates against two log parameters: a common multiplier on
all layer mobilities and a common multiplier on all strictly-positive contact
resistances. It calls the independent `multilayer_eigenvalues` transfer-matrix
reference. The returned diagnostics include the Jacobian, two singular values,
numerical rank and condition number. The optional `sigma_log_rates` field
weights each log-rate observation by its stated standard uncertainty.

Example design (dimensionless verification values only):

    design = {
        "storage": [1.0, 1.0],
        "mobility": [1.0, 1.0],
        "widths": [0.4, 0.6],
        "contact_resistances": [0.08],
    }
    result = log_rate_sensitivity([design], n_modes=3)

Run its tests with:

    python3 -m unittest discover -s MODELLING/transport_model -p 'test_identifiability.py' -v

One modal rate produces at most rank one for these two unknown scales. A
rank-two local Jacobian is necessary but not sufficient for practical
identifiability; inspect the condition number, uncertainty weights, parameter
profiles and model discrepancy. This utility uses common multipliers only,
requires strictly-positive contact resistances for log differentiation, and
does not estimate layer-specific parameters. Its synthetic verification is
not a measurement or calibration of precipitated-silica gel.



## Synthetic inverse recovery of bulk mobility and contact resistance

`synthetic_inverse.py` adds a small deterministic weighted Gauss--Newton
inverse demonstrator. It estimates only two global positive multipliers:
one on every layer mobility and one on every strictly-positive interface
contact resistance. Input observations are log modal decay rates from one or
more specimen designs; optional `sigma_log_rates` values weight the residuals.
The implementation rejects locally rank-deficient or severely ill-conditioned
designs and uses a backtracking line search.

Run the focused checks with:

    python3 -m unittest discover -s MODELLING/transport_model -p 'test_synthetic_inverse.py' -v

The tests generate exact synthetic modal observations from known parameter
multipliers, recover them from multiple heterogeneous designs and a displaced
initial guess, and check rejection of a one-mode underdetermined design and
invalid uncertainties. These are algorithmic verification tests only. They
do not use experimental observations, establish practical identifiability
under model discrepancy, estimate layer-specific parameters, or calibrate
precipitated-silica gels. Before applying the inverse method to experiments,
the mode assignment, geometry, storage compliance, uncertainty model and
contact-resistance interpretation must be independently justified.
