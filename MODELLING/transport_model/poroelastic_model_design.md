# Staged poroelastic model design for precipitated-silica syneresis

**Status:** design specification; no target-system constitutive law calibrated.

## 1. Purpose and boundary

The next transport model must distinguish pore-liquid transport from the mechanical response of the evolving silica network. A constant-coefficient consolidation equation is retained as a verification baseline, not as the final physical description.

The target is a saturated, deformable, particulate gel fragment or specimen undergoing natural syneresis. The first implementation will use a fixed reference domain and small-strain assumptions. Moving boundaries, fragmentation, chemical reaction transport and fully bidirectional MD/MC coupling are deferred until the simpler model is identifiable and verified.

## 2. Minimum governing structure

Pore-liquid flux (intrinsic permeability form):

\[
\mathbf q=-\frac{\kappa(\phi,\mathcal S,t)}{\mu}\nabla p
\]

where κ is intrinsic permeability [m²], μ is dynamic liquid viscosity [Pa s], p is pore pressure [Pa], φ is porosity, and S denotes structural descriptors.

For a linear saturated poroelastic approximation with Biot coefficient near unity and incompressible pore liquid:

\[
c_v\approx\frac{\kappa M}{\mu}
\]

where M is the appropriate constrained skeleton modulus [Pa]. This relation is a scaling closure; exact coefficients depend on the constitutive and drainage conditions. It is not valid to substitute a generic storage modulus G' or instantaneous creep modulus E0 for M without a constitutive conversion.

A first one-way coupled version may prescribe measured/assumed κ(t) and M(t) separately and solve the pore-pressure/consolidation response. This is a sensitivity framework, not a prediction until both functions are independently constrained.

## 3. Candidate constitutive closures — hypotheses, not established laws

### Hydraulic closure

Start with a monotone porosity-only reference (e.g. a Kozeny–Carman-type relation) and compare it with a structure-aware closure involving characteristic pore/aggregate length and contact/network descriptors:

\[
\kappa=\kappa(\phi,\ell_p,D_f,z,\mathcal S)
\]

where ℓp is a pore/structural length, Df a relevant fractal descriptor, and z a contact/coordination measure. The functional form and the appropriate scale of Df must be justified from measurements. A cake-scale filtration relation is not automatically a free-gel relation.

### Mechanical closure

Use measured time-dependent storage/loss moduli and creep/recovery data to decide between:
- quasi-elastic reference: M=M(φ,S);
- aging elastic reference: M=M(φ,S,t);
- linear viscoelastic response with a small number of relaxation modes.

Do not assume a single exponential aging law merely because it is convenient. The logarithmic growth and low-frequency relaxation reported for reactive high-pH silica gels are reasons to test broader descriptions, not proof of one universal law.

## 4. Identifiability

A single shrinkage curve or fitted characteristic time identifies, at best, a lumped combination of permeability, modulus, liquid viscosity, specimen size and boundary conditions. It does not identify κ and M separately.

The utility poroelastic_scaling.py makes the dimensional relation explicit: cv=κM/μ; tc=Ld²/cv. Given any selected M, a fitted time implies a corresponding κ, but that is an inferred pair along a non-unique curve, not two measured parameters.

The model must report parameter families or sensitivity envelopes until independent hydraulic and mechanical measurements exist.

## 5. Required independent evidence

Minimum matched-batch measurements:
1. Permeability under a low pressure gradient, with sample deformation and syneresis monitored during the test.
2. Creep/recovery or confined compression to determine the relevant constrained mechanical response.
3. Oscillatory rheology G'(t,ω), G''(t,ω) to detect aging and relaxation.
4. Porosity and structural descriptors (pore-size distribution, aggregate/cluster size, contact/network descriptors).
5. Liquid viscosity, temperature, pH, ionic strength and dissolved-silica concentration.

A permeability experiment on a deformable gel must correct for pressure-induced deformation and spontaneous syneresis during measurement; otherwise the inferred permeability is coupled to the evolving specimen.

## 6. Numerical implementation sequence

1. Keep the existing constant-coefficient 1-D and radial solvers as independent mathematical benchmarks.
2. Add dimensional scaling/identifiability utilities (implemented in poroelastic_scaling.py) and unit tests.
3. Implement a 1-D variable-coefficient transport solver with prescribed κ(t) and M(t), first in one-way mode.
4. Verify constant-coefficient recovery, grid/time convergence, mass balance, and limiting cases.
5. Add a simple viscoelastic constitutive option only after the quasi-elastic solver is verified.
6. Couple the structural state to κ and M only when independent data support the closures.
7. Add feedback from pressure/compaction to the structural model only after parameter identifiability and numerical stability are demonstrated.

## 7. Falsification and stop rules

- If the model cannot reproduce constant-coefficient analytical limits, do not add material complexity.
- If predicted behaviour depends strongly on an unconstrained closure, report that sensitivity rather than choosing a preferred law.
- If κ and M are only jointly inferred, do not describe either as measured.
- Do not transfer alkoxide-derived silica-gel parameters to precipitated silica without explicit evidence of material equivalence.
- Do not fit and validate on the same Wilhelm & Kind shrinkage curves.
- Do not call a high R² fit to AI-assisted approximate digitisation a physical validation.

## 8. First heterogeneous finite-volume solver (implemented; verification pending)

A new fixed-coefficient 1-D finite-volume implementation is added in heterogeneous_1d.py. It solves

\[
S(x)\,\partial_t p=\partial_x\!\left(\lambda(x)\,\partial_x p\right),\qquad
S=1/M,\quad \lambda=\kappa/\mu,
\]

on a fixed slab with zero excess pressure at both drained faces. Coefficients are cellwise constant and time-independent in this first implementation. Internal face mobility uses a harmonic mean; the implicit backward-Euler system is tridiagonal. The solver returns storage-weighted mean pressure, profiles, boundary outflow and a per-step discrete balance residual.

This is deliberately not yet a time-dependent aging model. If storage changes with time, the conservative accumulation term and any coupling to evolving porosity/deformation must be specified before prescribing arbitrary M(t). The implementation is a mathematical transport benchmark only; no silica-specific law or parameter is supplied. Tests compare the homogeneous limit with the existing analytical slab series, check discrete mass balance, positivity/monotonicity, piecewise coefficients and input validation. Hosted CI must pass before the implementation is considered numerically verified.

### Verification status after hosted CI #325 (11 November 2026)

The fixed-coefficient solver passed hosted workflow #325. The transport-model test discovery executed 51 tests, including homogeneous analytical recovery, discrete per-step mass balance, nonnegative/monotonic pressure response, piecewise coefficient handling, and explicit spatial-grid and time-step refinement checks. This establishes numerical consistency for the implemented fixed-coefficient PDE within the tested cases. It does not validate the PDE as a complete physical model of silica-gel syneresis, nor any silica-specific parameter or closure. A layered-medium/interface benchmark and global integrated-flux/storage-loss check remain next before introducing time-dependent material coefficients.
