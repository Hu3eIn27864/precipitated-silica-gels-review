# Parallel next-step plan

**Status date:** 2026-11-11  
**Scope:** numerical robustness, transport verification, and evidence readiness. This plan deliberately separates software verification from physical validation.

## Current verified baseline

- Hosted workflow run [#237](https://github.com/Hu3eIn27864/precipitated-silica-gels-review/actions/runs/43015804303), commit `9717046c349af3ca2ce246ad739d57ba4aa8198d`, completed successfully. The Release build, C++ tests, Python ensemble-analysis tests, 1-D transport tests, bounded DLCA size pilot, paired-seed parameter screen, and artifact upload all passed.
- Run [#234](https://github.com/Hu3eIn27864/precipitated-silica-gels-review/actions/runs/43015552646) validated the realized-displacement diagnostics.
- The first sensitivity screen is not a valid structural robustness comparison: the baseline completed 0/3, so there were no completed baseline/variant pairs for Rg or fixed-window Df.
- The current first-mode cylinder/sphere utility is a dimensional scaling relation, not a transient radial solver.
- No silica-specific interaction parameter, physical time scale, or fractal dimension is established.

## Workstream A — Pilot artifact audit (analysis gate)

**Objective:** produce a reproducible, seed-level report from the latest artifact of run #237.

1. Retrieve and unpack artifact `mc3d-dlca-pilot-and-sensitivity` (artifact ID `13851749184`).
2. Verify artifact provenance against commit, workflow run, manifest, exact seeds, parameter values, and attempt caps.
3. Recompute completion, attempt-cap hits, unwrapping validity, largest-component fractions, Rg eligibility, and fixed-window fit eligibility from raw CSVs.
4. Reconcile all derived summaries with the stored analysis outputs; retain incomplete runs in denominators.
5. Report each seed and each variant, not just pooled means. Distinguish missing fits due to incomplete aggregation from invalid fits due to periodic winding.
6. For each fit-capable aggregate, report fixed-window Df and the full within-seed fit-window range. Do not treat windows from one curve as independent replicates.
7. Do not launch the full finite-size matrix until the numerical decision gates in Workstream B are met.

**Deliverable:** `TEST_RESULTS.md` update with raw-data provenance, a seed-level table, explicit missingness, and a go/no-go decision. A successful CI run is not a physical validation result.

## Workstream B — DLCA common-displacement protocol (numerical robustness gate)

**Objective:** remove the known confounding between maximum component step and fixed attempt count.

1. Add an optional cumulative realized squared-translation target, (Q_\mathrm{target}=\sum_k |\Delta\mathbf R_k|^2), where each `Delta R` is the actual accepted rigid-cluster translation after collision clipping.
2. Retain the maximum-attempt limit as a hard safety cap. Record whether a run stopped by reaching the target or by the cap.
3. Record both cumulative squared translation (Q) and cumulative path length (L=\sum_k |\Delta\mathbf R_k|). These are algorithmic progress coordinates, not physical time or Brownian diffusivity.
4. Stop only after a completed move; record target overshoot explicitly. Never silently truncate a move to hit the budget, since that would alter the collision/aggregation algorithm.
5. Preserve the legacy fixed-attempt mode. Add tests for zero movement, target reached, safety-cap reached, deterministic reproducibility, and overshoot accounting.
6. First compare paired seeds at N=32 with a common, predeclared Q target anchored to the observed pilot displacement scale (approximately 2,000 reduced length-units squared), plus an independent attempt cap. Treat this value as a pilot diagnostic choice, not a calibrated parameter.
7. Report completion and structural outcomes at common Q, and also show the distribution of L and attempts. If the same Q yields materially different L or completion, report that; Q alone may not fully parameterise algorithmic progress.
8. Only after the N=32 common-budget screen is understood should the same protocol be extended to N=64 and 128 and additional seeds.

**Decision gate:** no claim of step-size-independent morphology unless paired seed-level completion, unwrapping, and fit-window stability are adequate across the tested step bracket.

## Workstream C — Radial transport solver (independent mathematical verification)

**Objective:** replace the current first-mode conversion utility with a verifiable transient benchmark before coupling it to a changing network.

1. Implement radial diffusion/consolidation in one spatial coordinate for an ideal infinite cylinder and sphere:
   `du/dt = c_v * r^(1-d) * d/dr(r^(d-1) * du/dr)`, with (d=2) for cylinder and (d=3) for sphere.
2. Use symmetry at the centre (`du/dr = 0`) and a perfectly drained outer boundary (`u(R,t)=0`). State the initial condition explicitly.
3. Compute the volume-weighted average excess pressure and degree of consolidation; use the correct radial volume weights.
4. Verify against an independently coded analytical eigenfunction-series solution, including early-, intermediate-, and long-time cases.
5. Add grid-refinement and time-step-refinement studies; demonstrate convergence of average consolidation and characteristic time.
6. Verify radius-squared scaling at fixed (c_v), and the cylinder/sphere eigenvalue limits. Check mass/volume weighting and boundary treatment separately.
7. Keep (c_v) an effective lumped coefficient. Do not identify it with permeability alone; in poroelastic consolidation it depends on permeability and skeleton compressibility/stiffness.
8. Do not fit Wilhelm & Kind curves until solver verification and boundary-condition mapping are documented. Empirical fitted time constants are not automatically eigen-times.

**Deliverable:** solver, independent reference implementation, tests, convergence note, and explicit assumptions. No pH-dependent material law in this stage.

## Workstream D — Literature and validation evidence (parallel evidence stream)

**Objective:** close the parameter-identifiability and independent-validation gaps.

1. Prioritise direct precipitated-silica sources for syneresis, pH, temperature, sample geometry, and forced-pressure conditions.
2. Treat Wilhelm & Kind (2015) fitted shrinkage parameters as fitted observables, not raw time-series or direct permeability measurements.
3. Keep Scherer (1989) as a transferability-limited mechanistic comparator until full numerical permeability, modulus, viscosity, and shrinkage data are recovered.
4. Inspect the open Pedrotti colloidal-silica transport dataset only as an adjacent software/transport benchmark; do not label it precipitated-silica syneresis validation.
5. Audit research-family overlap (articles, dissertations, companion papers) before counting data as independent.
6. Record source access level, exact figure/table, material identity, protocol, uncertainty, and whether a dataset has already been used for calibration.
7. Build a parameter-identifiability table: measured directly / reported as fitted / inferred / unavailable. Prioritise permeability and modulus as the main missing independent target-system inputs.

**Deliverable:** updated validation-data roadmap and claim-evidence matrix with explicit evidence grades and data lineage.

## Workstream E — Manuscript synthesis (parallel, but no premature claims)

1. Refine the review narrative around the chain precipitation → aggregation/gelation → fragmentation → consolidation/reorganisation → syneresis.
2. Keep direct precipitated-silica evidence separate from generic silica-gel and colloidal-silica comparators.
3. Frame the central gap as the feedback between evolving network structure, permeability, mechanical resistance, and syneresis kinetics.
4. Draft figures only from sourced data or clearly labelled conceptual schematics. No fitted or simulated result should be presented as experimental.
5. Delay strong mechanistic conclusions until Workstreams A–D provide adequate support.

## Parallel execution and dependencies

- A (artifact audit) and D (literature evidence) can proceed independently.
- C (radial solver verification) can proceed independently of A and D, but data fitting must wait for C's verification gate.
- B (common-displacement implementation) can begin from the existing instrumentation, but its parameter choice and interpretation must be informed by A; no large production matrix before B's tests pass.
- E (manuscript synthesis) can progress as a claim/evidence audit, but final conclusions wait for A–D.

## Stop rules

- No physical-time interpretation of DLCA attempts, path length, or squared displacement.
- No fractal exponent for incomplete or winding aggregates.
- No pooled fit windows as independent samples.
- No parameter fitting and validation against the same observations.
- No promotion of mechanistic comparator data to direct precipitated-silica validation.
- Any failure of reproducibility, convergence, or provenance pauses interpretation and triggers diagnosis rather than parameter tuning to obtain a preferred result.


## Literature verification update — 2026-11-11

A targeted source check strengthens the transport-validation workstream, while also clarifying its transferability limits:

- Scherer, G. W. (1989), “Mechanics of syneresis II. Experimental study,” *Journal of Non-Crystalline Solids* 108(1), 28–36, DOI: 10.1016/0022-3093(89)90329-3. The accessible abstract reports that shrinkage-rate dependence on sample size and contraction-curve shape are predicted from network permeability and viscoelastic properties, and that calculated curves agreed reasonably with shrinkage measurements using independently measured permeability, modulus, and viscosity. This is a strong mechanistic/validation comparator for silica-gel syneresis, but it must not be silently treated as a direct validation dataset for industrial precipitated silica.
- Scherer, G. W. (1996), “Influence of Viscoelasticity and Permeability on the Stress Response of Silica Gel,” *Langmuir* 12(5), 1109–1116, DOI: 10.1021/la9503111. The publisher abstract explicitly links response rates to both permeability and network modulus and describes syneresis in chemically aggressive liquid environments. Treat as a review/mechanistic synthesis, not independent experimental replication of the 1989 study.
- A radial infinite-cylinder consolidation formulation has been treated with finite differences and compared with a semi-analytical solution in the literature (DOI: 10.1016/S0266-352X(98)00018-4). This is a useful numerical-method comparator for Workstream C; its poroelastic assumptions and boundary conditions must be checked before adapting it.
- The governing radial diffusion/consolidation equation is not sufficient by itself to specify the physical model. Workstream C must state initial conditions, drained boundary conditions, volume-weighted averaging, and whether the effective consolidation coefficient is constant. The coefficient must not be equated with permeability alone; it also contains skeleton/fluid storage and stiffness terms.

**Consequence for the work plan:** keep Workstream C's analytical-series cross-check independent from the finite-difference implementation; use Scherer (1989) as a mechanistic benchmark only after the sample geometry and boundary conditions are mapped. No parameter fitting is authorised by this literature check alone.


## Analytical benchmark for the radial solver

For the restricted benchmark problem of constant \(c_v\), initially uniform excess pressure \(u(r,0)=u_0\), centre symmetry, and a perfectly drained outer boundary \(u(R,t)=0\), the volume-averaged excess-pressure ratio has the following eigenfunction-series references. Let \(T=c_vt/R^2\).

- Infinite cylinder (radial dimension 2):
  \[
  \frac{\bar u(t)}{u_0}=\sum_{n=1}^{\infty}\frac{4}{\alpha_n^2}\exp(-\alpha_n^2T),
  \qquad J_0(\alpha_n)=0.
  \]
  The first root is \(\alpha_1\approx2.4048255577\), giving first-mode time \(\tau_1=R^2/(\alpha_1^2c_v)\).
- Sphere (radial dimension 3):
  \[
  \frac{\bar u(t)}{u_0}=\sum_{n=1}^{\infty}\frac{6}{n^2\pi^2}\exp(-n^2\pi^2T),
  \]
  giving first-mode time \(\tau_1=R^2/(\pi^2c_v)\).

In both cases the volume-average weights sum to one at \(t=0\). The degree of consolidation for this benchmark is \(U(t)=1-\bar u(t)/u_0\). These expressions are benchmark references for the stated idealised boundary-value problem only; they do not model evolving permeability, nonlinear skeleton mechanics, finite-cylinder end drainage, or chemical ageing. The finite-difference implementation should be tested against the full series, not only the first-mode time constant.


## Progress update — 2026-11-11

### Workstream A: latest artifact audit completed

The raw artifact from run #237 (ID 13851749184) was downloaded and audited seed by seed. The detailed tables and recomputed eligibility counts are recorded in `MODELLING/monte_carlo_3d/TEST_RESULTS.md`. Decision: no-go for the full finite-size matrix until common-displacement stopping and fit-window stability are addressed. There were zero completed baseline/variant pairs, so no paired Rg or Df comparisons exist.

### Workstream C: first transient radial solver implementation

Added `MODELLING/transport_model/radial_consolidation.py` and
`test_radial_consolidation.py`. The solver uses conservative cell-centred
finite volumes, backward Euler, a symmetry condition at the centre, and a
perfectly drained outer boundary. It reports volume-weighted mean excess
pressure versus Fourier number for an ideal infinite cylinder or sphere.
Independent eigenfunction-series references are included (first ten J0
roots for the cylinder; ten spherical modes).

Five local standard-library unittest cases passed in the isolated Python
environment, including agreement with the series at Fourier numbers 0.02,
0.1 and 0.5, monotonicity/bounds, and a grid/time refinement comparison.
This local run is not a hosted CI result. The workflow path filter was
extended so changes under `MODELLING/transport_model/**` trigger the existing
transport test suite. Hosted CI validation is pending.

The radial solver remains an ideal constant-coefficient benchmark. It is not
yet experimentally validated, does not include finite-cylinder end drainage,
and is not coupled to permeability evolution or network mechanics.

### Immediate next tasks

- Verify the new radial solver and its tests in hosted CI; inspect the complete
  job logs rather than relying only on the run-level success badge.
- Continue Workstream B by implementing a common cumulative-Q stopping mode
  with a hard attempt cap, explicit stop reason and overshoot accounting;
  retain the legacy fixed-attempt mode and add deterministic tests.
- Keep the full DLCA size matrix gated until the common-Q comparison has
  adequate completion, unwrapping and fit-window stability.


### Workstream B: common-Q stopping mode implemented

Added an optional cumulative squared realized-translation target to the DLCA
core and CLI. The legacy fixed-attempt mode remains the default when target
Q is zero. In common-Q mode, the simulation finishes the current rigid-cluster
move and then stops; it never truncates a move to hit the target. The result
records whether Q was reached, whether the hard attempt cap stopped the run,
and the nonnegative Q overshoot. The size-series and paired-sensitivity
runners accept and record `--target-q`.

A deterministic C++ test covers target reached, attempt-cap reached, and
legacy mode. The end-to-end CLI smoke test now exercises a positive Q target
and checks the expanded run-summary schema. Hosted CI run #254 has passed
build, all five CTest targets, Python analysis tests, and transport tests;
the bounded fixed-attempt screen has completed. The common-Q paired screen
(Q target 450, N=32, three paired seeds, 50,000-attempt safety cap) is still
running at the time of this update. Its raw outputs and paired summaries are
retained in the same workflow artifact.

Q=450 is a provisional numerical screening target selected because all three
step-0.10 seeds in the preceding fixed-attempt pilot reached approximately
Q=499–502 by the 50,000-attempt cap. It is not a physical time, Brownian
diffusivity, or material parameter. The screen must also report path length
L, attempts, overshoot, and stop reason; equal Q is not assumed to imply
identical trajectory history or morphology.

### Workstream D: additional permeability comparator

Added PSG-044, Scherer (1995), on pH-dependent permeability and viscoelastic
relaxation of silica gels, to the literature database and source assessments
(batch 18). The accessible abstract reports increasing permeability and
relaxation rate with pH, pore radii around 14–20 nm, and a slight decrease in
shear modulus. This remains class B comparator evidence: exact precursor and
formulation are unverified, full text has not been inspected, and no values
are transferred to industrial precipitated silica. It is grouped with the
related Scherer silica-gel mechanics/permeability research family, not counted
as an independent external replication.


### Workstream B result: common-Q screen completed

Hosted CI run [#254](https://github.com/Hu3eIn27864/precipitated-silica-gels-review/actions/runs/43018481413) passed the common-Q C++/CLI tests and completed the seven-configuration N=32 paired screen at Q=450. All 21 runs reached the target, none hit the 50,000-attempt cap, and none completed aggregation. There are therefore no valid Df fits or completed-pair Rg comparisons.

The screen shows that equal Q does not equalise path length L: step 0.10 produced mean L≈4,321, baseline L≈2,159, and step 0.28 L≈1,542. Largest-component fractions were similar in scale but remain incomplete-cluster descriptors with only three seeds. Thus Q is a useful common algorithmic progress coordinate, but not a complete trajectory descriptor and certainly not physical time. Full seed-level summary is recorded in MODELLING/monte_carlo_3d/TEST_RESULTS.md.

**Next decision:** do not yet increase Q or system size. First inspect whether Q and L together, plus cluster-selection/mobility history, provide a defensible algorithmic comparison. Any higher-Q target must be predeclared and must retain the hard attempt cap and explicit target/cap outcomes.

### Workstream C result: hosted verification

The radial finite-volume cylinder/sphere solver passed the integrated transport test stage in hosted CI runs #239 and #254. This verifies the implementation against the analytical eigenfunction series and numerical refinement tests. It remains a constant-coefficient ideal-geometry benchmark; experimental validation and coupling to evolving permeability/mechanics are still pending.
