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
transport test suite. Hosted CI #293–#295 passed the expanded radial suite and complete integrated workflow.

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


## Update after CI run #257 (2026-11-11)

The common-Q screen is no longer pending: [CI #257](https://github.com/Hu3eIn27864/precipitated-silica-gels-review/actions/runs/43018713555) passed the complete workflow, including all three DLCA screens and artifact upload. The latest artifact was inspected. The fixed-attempt size series completed 2/3 N=32 runs, 0/3 N=64 runs and 0/3 N=128 runs. Do not fit a size-dependent Df trend to this pilot.

The common-Q raw data were further reduced to Q/attempt, path-length/attempt and Q/successful-merge diagnostics. These confirm that Q alone does not standardise the algorithmic trajectory. Step-size changes Q/attempt by nearly a factor of eight across the tested 0.10 and 0.28 settings. Q per merge varies across all configurations, but it is an outcome-conditioned descriptor and must not be treated as a universal clock. Keep Q, path length, attempts, successful merges, component count and largest-component fraction together.

### Workstream D update: direct process-history / mesostructure evidence

Added PSG-045 (Manfoumbi, Roger & Meireles, 2024; DOI 10.5802/crchim.347) and a full source assessment. The study combines SAXS and filtration experiments and reports that adding silicate at basic pH changes the silica network from polymer-like q^-2 scattering toward particle-like q^-4 Porod behaviour, with about two orders of magnitude improvement in filtration-cake specific resistance. This directly supports process-history-dependent mesostructure and filtration behaviour in the studied hydrometallurgical systems. It does **not** measure intrinsic gel permeability, syneresis kinetics or mechanical modulus, so it is not a calibration dataset for the radial solver.

### Revised immediate priorities

1. **DLCA observables:** add explicit cluster-selection counts and per-size-class translation statistics (counts, attempted displacement, realised displacement, Q contribution, path-length contribution). This is needed to understand why Q and L differ across step-size and mobility settings.
2. **DLCA comparison protocol:** retain the three-seed CI screen as a smoke/sensitivity check only. Before a larger study, pre-register a higher-Q target based on a pilot stopping-time distribution and require a minimum completion fraction; do not select only successful runs after seeing the data.
3. **Transport validation:** add mass-conservation and long-time equilibrium checks, mesh/time-step convergence over a wider parameter grid, and an independent manufactured-solution check. Keep constant-coefficient ideal geometry separate from evolving-permeability models.
4. **Evidence synthesis:** distinguish three different transport observables in the review: intrinsic gel permeability, consolidation/syneresis time response, and filtration-cake specific resistance. PSG-043/044 and PSG-045 inform different parts of this chain and must not be numerically pooled.
5. **Manuscript:** update the central process-history framework, but defer any universal causal law or fitted pH-dependent permeability relation until target-system measurements exist.

**Roadmap gate:** no full N=32/64/128 DLCA matrix, no Df-vs-size claim, and no parameter calibration from the present CI pilots. The next DLCA code increment should improve trajectory observability, not simply increase the attempt budget.


### Workstream B implementation increment: size-resolved trajectory accounting

Implemented the first observability increment in the DLCA core. For every
attempted cluster move, the selected cluster's particle count immediately
before the move is used as the size class. The result accumulates, by class:
selection count, realized squared translation Q, and realized path length L.
The ensemble driver writes these values to `_mobility_by_size.csv` for every
seed, including incomplete runs. C++ tests verify that size-class counts sum
to attempts, size-class Q/L sum to global Q/L, and repeated seeds reproduce
the same size-class statistics. CLI smoke coverage checks the additional
output file and schema.

The implementation is committed; the next hosted CI run must validate build,
tests and output. These statistics are trajectory diagnostics only. They do
not implement hydrodynamic mobility, cluster rotation, or physical Brownian
time. The next analysis should compare Q and L accumulated in each size class
against selection frequency and merge events, while retaining all incomplete
runs and the attempt-cap status.


### Workstream B result: size-resolved mobility accounting passed CI

The per-size diagnostics were included in hosted CI [#267](https://github.com/Hu3eIn27864/precipitated-silica-gels-review/actions/runs/43019287245), which completed successfully. The uploaded artifact was inspected across 51 seed/configuration records; selection counts, Q and L all sum exactly (within floating-point tolerance) to the run-level attempts/Q/L. This validates the internal bookkeeping and export path.

The common-Q seed-level data show that the selection fraction for clusters of size at least two was 8.87% at baseline, 15.53% for mobility exponent 0.5 and 11.48% for exponent 1.5. This is qualitatively consistent with the code's declared (m^{-\alpha}) selection weighting, but only verifies an algorithmic consequence in a three-seed, incomplete-cluster screen. It is not a physical mobility law.

**Next analysis gate:** use the new file to compute size-class-conditioned selection frequency, Q and L per selection, and merge outcomes after moves selected from each size class. Keep denominator definitions explicit (attempts/selections, not particles or physical time). Preserve seed-level rows and do not aggregate fit exponents for incomplete clusters. After that, decide whether a larger-Q pilot can be predeclared without strong differential censoring.


### Workstream B extension: merge outcomes stratified by selected size

Extended the per-size statistics with successful component merges caused by
moves selected from each pre-move cluster-size class. The ensemble CSV now
exports this count alongside selections, Q and L. A conservation test requires
the sum of size-class merge counts to equal the run-level successful-merge
count, and the reproducibility test includes this new field. This allows
selection/movement exposure to be distinguished from merge outcomes in the
next analysis. Hosted CI validation of this extension is pending.


### Workstream B extension validated: merge outcomes by size class

The per-size `successful_merges` field is now included in the output. Hosted
CI [#274](https://github.com/Hu3eIn27864/precipitated-silica-gels-review/actions/runs/43019534498)
passed the full workflow and CLI smoke test. The artifact was audited across
51 seed/configuration records: per-size selection counts, successful merges,
Q and L each reproduce the corresponding run-level totals in all 51 cases.
The accounting convention attributes the reduction in component count caused
by a move to the selected cluster's size immediately before that move.

The next analysis can now distinguish (i) how often each size class is selected,
(ii) how much Q/L it accumulates, and (iii) how many component mergers are
associated with its selected moves. It still cannot infer a physical collision
kernel or hydrodynamic mobility without an independently justified time and
mobility model.


### First per-size outcome analysis completed

The CI #274 artifact was reduced to total selections, successful component
merges, merges per selection, and fraction of selections involving size >=2.
The pooled three-seed ratios range from 0.00023 (step 0.10) to 0.00163
(step 0.28), with baseline 0.00074. The large spread is strongly confounded
by step-dependent attempt counts at common Q; these ratios are not physical
collision rates. Most selection exposure is still monomeric (about 84.5–91.1%
across baseline and mobility variants). These diagnostics are documented in
TEST_RESULTS.md and do not justify parameter trends or physical interpretation.

**Next modelling action:** before attempting larger Q, instrument merge events
as distinct move-level events (separate from number of components merged),
and consider a stopping design that matches both cumulative Q and a
predeclared attempt/path-length envelope. Avoid conditioning the sample on
only those trajectories that complete.


### Workstream B: merge-event versus absorbed-component distinction

The common-Q artifact was further inspected by selected pre-move cluster-size
class. This exposed an ambiguity in the existing outcome count: a single
moving cluster can contact multiple other components in one attempted move.
The existing `successful_merges` count records the number of absorbed
components (component-count reduction), not the number of move-level
collision/merge events.

The DLCA result and per-size diagnostics now track both quantities separately:
`successful_merge_events` counts a move with one or more contacts once;
`successful_merges` retains the number of absorbed components. The CSV
schema, deterministic reproducibility checks, and conservation tests have
been updated. Hosted CI validation is pending. This distinction will let us
report event probability per selected move separately from component
reduction per move; neither is a physical collision rate without a physical
time/mobility model.


### Workstream D: direct industrial precipitated-silica transport/mechanics evidence

Added PSG-046, Ragueh et al. (2015), *Separation and Purification Technology* 156, 2–11, DOI 10.1016/j.seppur.2015.10.005. The full author manuscript was inspected. It studies three industrial precipitated-silica dispersions sampled directly from a reactor, combining TEM/SAXS/USAXS, pressure filtration (400–600 kPa, five repeats), Darcy-derived cake permeability and osmotic compression. Percolation thresholds are reported at silica volume fractions approximately 0.06, 0.08 and 0.09 for the three systems. It provides unusually direct evidence linking hierarchy, cake transport and compression/yielding.

Important limit: the permeability is inferred for filtration cakes, not measured directly in freely suspended or syneresising gel fragments. Osmotic compression is slow/isotropic and filtration loading varies with cake height; do not equate their pressure thresholds. This source supports the structural-state/Darcy architecture, but is not direct calibration for the radial syneresis solver.

**Updated modelling implication:** keep at least three state descriptors distinct where data permit: (i) local aggregate structure/length scales, (ii) network connectivity/percolation and volume fraction, and (iii) transport permeability and mechanical yielding. A single Df parameter is unlikely to capture all three.


The run-summary CSV now also exports the run-level merge-event count, so
per-size merge events can be audited against the independent run total in
future artifacts. The CLI smoke test checks the expanded schema and row
structure. Hosted CI validation of this final output-contract addition is
pending.


The run-level event count and expanded CSV schema passed hosted CI [#284](https://github.com/Hu3eIn27864/precipitated-silica-gels-review/actions/runs/43020332694). Artifact-level reconciliation across 51 seed/configuration records matched size-class and run-level totals for attempts, merge events, absorbed components, Q and L in every record. In the seven common-Q configurations, merge-event totals equalled absorbed-component totals (25–36 per configuration), i.e. no move absorbed multiple other components in this screen. The distinction remains in the schema for correct general accounting, but the current pilot does not yet demonstrate a multi-contact move. Larger-size event ratios are too sparse for inference.


### Quantitative structure benchmark from PSG-046

Ragueh et al. report dense-aggregate radii of 82, 125 and 175 nm for S1, S2 and S3. Table 3 lists branch mass-fractal dimensions 1.8, 2.2 and 1.8; the prose immediately below lists 1.8, 2.2 and 2.2. The S3 value is therefore internally inconsistent and is flagged rather than silently resolved. The reported cake solid volume fractions are 0.070–0.108 across 400–600 kPa; absolute specific-resistance values are normalised to a withheld reference, so they cannot be converted to absolute permeability from the table alone.

These values provide a useful **external scale benchmark**, not a calibration target: the SAXS-derived branch exponent is measured on industrial aggregates over a selected scattering window, whereas our Monte Carlo mass-radius exponent is calculated from finite simulated clusters and a chosen real-space radius interval. Before comparing numerical Df values, we must establish equivalent scale windows and structural objects. The present DLCA pilot has insufficient completed aggregates at N=64/128 and therefore no valid size-trend comparison.


The complete workflow was rerun successfully in CI [#286](https://github.com/Hu3eIn27864/precipitated-silica-gels-review/actions/runs/43020521613) after the audit documentation updates. Build, C++ tests, Python ensemble-analysis tests, 1-D transport tests, bounded size pilot, fixed-attempt paired sensitivity, common-Q screening and artifact upload all passed. The DLCA event-accounting implementation itself had already been validated in #284; #286 confirms the subsequent integrated repository snapshot.


## Parallel update — transport verification and identifiability (2026-11-11)

### Workstream C1: corrected planar benchmark re-baselined

Following the eigenvalue-exponent correction, added a dimensionless reference
table for (T_v=c_vt/H_d^2=0) through 2.0. The values are computed from the
corrected analytical series (with the short-time asymptotic below 0.01) and
are regression references only; they are not fitted silica data. The transport
README now states the classical identifiability relation
(c_v=k/(m_v\gamma_w)=kM/\gamma_w). A single consolidation curve therefore
cannot identify permeability and skeleton modulus/compressibility separately.
Independent hydraulic and mechanical measurements are required.

### Workstream C2: radial solver convergence expanded

Added convergence tests for both ideal radial geometries at Fourier number
0.1. The test suite now checks monotonic reduction of error against the
independent eigenfunction-series reference under joint grid/time refinement
(30/60/120 cells and decreasing time step), and time-step refinement at fixed
120-cell resolution. A local independent numerical check of the same scheme
gave decreasing errors for cylinder: 0.01905, 0.00480, 0.000964; sphere:
0.02649, 0.00671, 0.00135 across those three joint refinements. These are
diagnostic values at one Fourier number, not global error bounds. Hosted CI
validation of the newly expanded tests is pending.

### Workstream D: model-structure evidence

PSG-044 (Scherer, 1995) remains class-B comparator evidence because only the
abstract is accessible and the precursor/gel chemistry is not verified.
Its qualitative report of pH-dependent permeability and viscoelastic
relaxation supports allowing transport and skeleton mechanics to evolve
together, but its pore radii and trends are not target-material parameters.
PSG-046 (Ragueh et al., 2015) provides direct precipitated-silica cake and
compression evidence, but not syneresis permeability. The model architecture
must therefore keep permeability, mechanical resistance/yielding, and
network connectivity as separate state variables until target-system data
constrain their coupling.


### Workstream C verification result: CI #293–#295

Hosted CI [#293](https://github.com/Hu3eIn27864/precipitated-silica-gels-review/actions/runs/43021684276) passed the expanded cylinder/sphere grid- and time-step-convergence tests. CI [#294](https://github.com/Hu3eIn27864/precipitated-silica-gels-review/actions/runs/43021709035) passed the corrected planar benchmark tests and the integrated DLCA screens. After adding seven regression points to the corrected planar dimensionless reference curve, CI [#295](https://github.com/Hu3eIn27864/precipitated-silica-gels-review/actions/runs/43021757732) passed the complete workflow, including C++ tests, Python analysis, all transport tests, the bounded DLCA screens and artifact upload.

The planar code-verification references now cover (T_v=0.001,0.01,0.05,0.1,0.2,0.5,1,2), with the independent (T_v=0.1) reference retained. The radial suite tests both ideal geometries against the eigenfunction series and checks monotone error reduction under grid/time refinement. These are numerical verification results only. No experimental parameter fitting or silica-specific validation has been performed.


## Parallel implementation update — 2026-11-11

Completed three independent implementation branches:

- **Experimental comparison:** added `LITERATURE/experimental_syneresis_comparison.csv` with 18 records and explicit fields for natural versus centrifugal forced syneresis, gel type, temperature, reported geometry/dimension, fit-parameter status, drainage-boundary knowledge, permitted comparisons and prohibited inferences. Cylinder height is not inferred from the reported sample volume; approximate droplets are not silently promoted to exact spheres. Natural and forced records are not pooled.
- **Finite-cylinder geometry:** extended `geometry_scaling.py` with the separable first-mode time constant for a finite cylinder with a drained curved wall and either two drained ends or sealed ends. The sealed-end limit recovers the infinite-cylinder radial expression. This is a first-mode identity, not yet a transient 2-D solver; actual specimen end conditions remain unverified.
- **Permeability/mechanics separation:** added `poroelastic_coupling.py` implementing only `c_v=k*M/gamma_w` and its inversion. No constitutive evolution law is assumed; `k` and the constrained modulus `M` remain separate independently supplied inputs.

New tests cover the finite-cylinder limiting cases and scaling, plus algebraic coupling and independent sensitivity to permeability and modulus. These tests establish mathematical/code consistency only. The new comparison CSV was parsed and checked for a consistent 17-column schema (18 data records).

**Next gate:** complete hosted CI for these commits; then, if it passes, decide whether a transient axisymmetric finite-volume solver is warranted by recoverable specimen dimensions and drainage boundaries. Do not use the ideal finite-cylinder formula to fit the Wilhelm & Kind cylinder data until those boundary conditions are established.

### Dimensional correction to hydraulic/mechanical coupling

Use hydraulic conductivity (K) [m/s] in (c_v=K M/\gamma_w), or intrinsic permeability (\kappa) [m²] in (c_v=\kappa M/\mu). These are distinct forms connected by Darcy's law; do not use the same symbol or unit for both. The implementation now exposes separate functions for each form and their inverses. This is an explicit dimensional correction to earlier shorthand notation in project notes.

### Follow-up: completed geometry/data/coupling branch — 2026-11-11

The 18-row comparison matrix has now been analysed descriptively in
`SYNTHESIS/experimental_syneresis_comparison_note.md`. For the natural
12-mm-diameter cylinder series, the fitted base/acid time-constant ratio is
2.35, 2.74 and 5.50 at 20/40/60 °C; for the approximately 3-mm droplets it
is 1.68, 0.89 and 1.23. This protocol-dependent reversal rules out a simple
unqualified acid/base rate ordering. These are ratios of empirical fit
parameters, not measured diffusivities.

The finite-cylinder first-mode helper is tested for drained versus sealed
ends and its infinite-cylinder limit. The poroelastic helper now distinguishes
hydraulic conductivity K [m/s] from intrinsic permeability κ [m²], with
separate forms c_v=K M/γ_w and c_v=κ M/μ. The initial transient CI failure
(#304) was an intermediate import/API mismatch in the new coupling test;
the API and tests were reconciled. Full hosted CI #305–#308 passed, including
the 29 transport tests in #308. This confirms implementation/test consistency
only, not material-model validity.

Next scientific gate remains evidence recovery: actual cylinder height and
drainage surfaces, droplet contact geometry, raw syneresis curves, and
independent permeability/conductivity and constrained-modulus measurements.
Only then decide whether a transient finite-cylinder solver and a
state-dependent k–M coupling can be meaningfully identified.


## Workstream D2 — source-verified data and geometry (updated 2026-11-11)

- Added source-verified geometry audit and a reproducible digitisation protocol.
- Transcribed the 14 acid/base pressure-cell fit records from the open 2015 Table 3 into a separate 15-column CSV; parser validation found 14 rows with consistent schema.
- The natural-cylinder source explicitly assumes radial drainage length \(R=6\) mm for its comparison with pressure-cell data. Preserve that as the authors' assumption, while separately testing finite-end drainage sensitivity.
- Conditional on a right-cylinder interpretation of \(d=12\) mm and \(V\\approx3\) mL, the implied height is 26.5 mm. This is calculated, not reported as a measured height.
- Actual digitised marker points remain outstanding. The published Tables 1–3 are fitted parameters, and the paper's plotted markers must be extracted separately from the fitted lines before residual-based model validation can be attempted.
- Priority next: digitise Figure 8 natural cylinder curves and Figure 10 confined-droplet curves first, preserving source/panel and point uncertainty; then pressure-cell Figure 12 / supplementary data. Avoid fitting a common \(c_v\) before boundary conditions and geometry are mapped.
