# Roadmap status and next work packages — 13 November 2026

This is the current execution snapshot for the parallel work plan in
`MODELLING/NEXT_STEPS_PARALLEL_PLAN.md`. It supersedes older statements there
that describe tasks as still pending when later updates in that file record
their completion. Software verification and physical validation remain
separate.

## Work-package status

| Work package | Current status | Gate / next action |
|---|---|---|
| **AP A — DLCA pilot audit** | Completed for the recorded pilot artifact; seed-level provenance and eligibility audit is in `MODELLING/monte_carlo_3d/TEST_RESULTS.md`. | Do not launch the full finite-size matrix until AP B produces completed, interpretable aggregates. |
| **AP B — common-displacement DLCA** | Common cumulative-\(Q\) stopping mode, safety cap, stop reason and overshoot accounting are implemented and tested. The latest CI #342 artifact confirms all 21 N=32/Q=450 runs reached the target, none hit the cap, and none completed aggregation. Baseline runs produced 5–12 merge events and largest components of only 2–4 particles. | **No-go** for morphology or fractal-dimension conclusions and for a large production matrix. Diagnose cluster mobility/merge efficiency and pre-register any new pilot before running it. Q and path length are algorithmic progress measures, not physical time. |
| **AP C — transport solver verification** | Radial solver passed analytical-series/refinement checks. Heterogeneous solver tests now include cell-centre interface refinement and integrated outflow/storage-loss balance; the full transport suite passed 62/62 in CI #342. | The two tests are useful regressions but not independent benchmarks: interface location shifts with grid; flux balance reuses solver face fluxes. Fixed-interface two-layer eigenfunction reference, independent boundary-gradient flux integration, and smooth variable-coefficient manufactured-solution verification are implemented; hosted CI for the latest manufactured-solution commit is pending. Discontinuous/evolving coefficients and physical validation remain open. |
| **AP D — evidence and parameter identifiability** | Consolidated source comparison is now in `LITERATURE/transport_parameter_comparison_2026-11-13.md`. Direct target-chemistry rheology and oedometer response, plus industrial cake filtration/mesostructure evidence, are available. PSG-047 (Butrón et al. 2009) and PSG-048 (Wong et al. 2018) add pure colloidal-silica comparators. PSG-048 is especially promising because an open CC BY 4.0 workbook accompanies pure-gel oedometer compression and t90-derived hydraulic conductivity (about 10^-9–10^-12 m/s); the workbook has not yet been inspected and matched state pairs are not yet verified. No matched intrinsic-permeability/constrained-modulus pair for the target precipitated-silica gel state has been identified. | Prioritise direct wet-gel permeability and a mechanical measurement that maps to constrained modulus M on matched formulations/ageing states. Keep cake resistance, oedometer t90, rheological E0 and free-syneresis tau as distinct observables. |
| **AP E — manuscript synthesis** | Claim/evidence synthesis and a coupled transport–mechanics–structure framework exist. | Continue only as a claim audit and outline refinement; no final causal or predictive claim until APs A–D clear their gates. |

## Immediate execution order

1. **AP C1 — extend coefficient verification.** The smooth manufactured-solution test is now implemented; next test discontinuous variable coefficients against independent fixed-interface references and quantify coefficient-representation error.
2. **AP C2 — independent flux reconstruction.** Reconstruct boundary gradients from numerical pressure profiles, integrate Darcy flux with a stated quadrature rule, and compare with total storage loss; report this separately from the existing discrete balance identity.
3. **AP D1 — extract adjacent open dataset.** Inspect the Wong et al. (2019) CC BY 4.0 workbook linked to PSG-048. First map sheets, specimen IDs, curing ages, stress steps, void-ratio curves, t90 and reported conductivity; determine whether M-like compressibility and conductivity can be paired at identical states. Keep this as a colloidal-silica comparator. In parallel, continue searching for direct wet-gel measurements on matched sodium-silicate/sulfuric-acid formulations; do not repurpose cake or oedometer observables as target-system intrinsic parameters.
4. **AP D2 — figure-level target data.** Return to Wilhelm & Kind figures only with original images and panel-specific calibration. Store experimental marker centres separately from model curves, error bars and AI-assisted approximations.
5. **AP E1 — evidence-linked manuscript outline.** Update the claim–evidence matrix and mark every central mechanism as direct evidence, comparator evidence, model hypothesis or unresolved.

## Data provenance and reproducibility note

The user-supplied `DATA/Raw/kurvendigitalisierung.csv` contains 21 series and
4,780 data rows. Its trace label identifies the visible curves as combined
measurement/model traces where those cannot be separated. It is therefore
not a verified raw experimental time-series dataset and must not be used as
primary experimental calibration data. Preserve the original file unchanged;
any exploratory analysis must retain this provenance label.

The audit utility `LITERATURE/audit_kurvendigitalisierung.py` has been updated
to read from the case-sensitive path `DATA/Raw/kurvendigitalisierung.csv`.
This path correction has been committed; execution of the utility after the
path change has not yet been independently verified in a clean repository
checkout.

## Scientific stop rules

- Do not equate a fitted syneresis time constant or oedometer (t_{90}) with
  intrinsic permeability or a poroelastic diffusivity.
- Do not transfer filtration-cake permeability directly to free gel fragments.
- Do not use the same observations for calibration and independent validation.
- Do not claim a DLCA fractal dimension from incomplete or periodically
  winding aggregates.
- Do not introduce pH-dependent or time-dependent material laws before
  constant-coefficient recovery, conservation and identifiability checks pass.
- Keep digitised, AI-assisted, fitted, simulated and author-reported data
  explicitly separated.


## Work session update — 13 November 2026

- Hosted CI #342 passed 5/5 CTest targets, 21/21 Python ensemble-analysis tests and 62/62 transport-model tests. Full job log and latest artifact were inspected.
- The Q=450 paired screen reproduced 0/21 completed aggregates. All runs reached Q without hitting the attempt cap. This is a stop/diagnostic result, not a basis for a larger production matrix.
- AP C now has an implemented fixed-physical-interface two-layer eigenfunction reference (`layered_reference.py`) and dedicated tests (`test_layered_reference.py`). Local focused numerical checks show grid convergence (errors 3.84e-3, 8.33e-4, 2.05e-4 for N=40,80,160), monotone time refinement, and independent boundary-gradient flux/storage-loss agreement (residual 1.31e-13). Hosted CI #351 passed on commit `9a8160b3bf909d8f953bc11556957444dacc61b7`; the complete transport suite passed 68/68 tests, including all six new layered-reference tests. Variable-coefficient manufactured-solution testing is now implemented locally (5/5 focused tests pass); hosted CI is pending. Smooth-field spatial convergence is approximately second order, temporal refinement is monotone, and source-inclusive balance residual is 1.18e-16.
- AP D source-by-source parameter comparison is documented in `LITERATURE/transport_parameter_comparison_2026-11-13.md`. The decisive target-system permeability–mechanical-modulus identifiability gap remains open.


## Work session update — PSG-048 literature lead

- Added PSG-048 (Wong et al. 2018) and its 2019 CC BY 4.0 open workbook to the literature database and source assessment.
- The article reports pure commercial colloidal-silica gel oedometer compression and hydraulic conductivity derived from Taylor t90 at each loading step (approximately 10^-9–10^-12 m/s). Curing ages include 1, 2, 4 and 8 weeks.
- The workbook is a high-priority extraction target, but it has not yet been downloaded or inspected. Do not claim paired modulus–conductivity observations until specimen-state alignment is verified.
- Material class remains distinct from sodium-silicate/sulfuric-acid precipitated silica.


## AP C implementation update — fixed-interface layered reference

- Added `MODELLING/transport_model/layered_reference.py`: independent standard-library eigenvalue and storage-weighted modal reference for a two-layer drained slab with a fixed physical interface.
- Added `MODELLING/transport_model/test_layered_reference.py`: eigenvalue regression, reference limits/monotonicity, grid/time refinement, and independently reconstructed boundary-gradient flux balance.
- Added README usage and numerical verification details; full review note updated.
- Focused local numerical cross-check: 4/4 checks passed; the check used a local reproduction of the existing finite-volume update because a clean checkout/runtime execution of the remote repository test suite was not available in this session. Hosted CI #351 is now verified successful: 68/68 transport tests passed, including the six new layered-reference tests. The earlier CI #347 also passed 68 tests on the initial implementation commit.
- Numerical convergence and conservation are code-verification only. No material calibration or physical validation is implied.


## AP C manufactured-solution update — 13 November 2026

- Extended `heterogeneous_1d.py` with optional cell-centred initial profiles and source forcing for \(S(x)p_t=\partial_x(\lambda(x)p_x)+f(x,t)\), preserving the default no-source API.
- Added five manufactured-solution tests with smooth nonconstant storage and mobility. Local run: 5/5 passed.
- L2 errors for N=20,40,80: 3.377e-4, 8.471e-5, 2.119e-5; temporal refinement against a same-grid small-dt reference is monotone; source-inclusive balance residual max 1.18e-16.
- Hosted workflow status is pending; no claim of CI success until the run is inspected. This is numerical code verification, not silica-specific physical validation.


## AP C follow-up — discontinuous-interface eigenmode (13 November 2026)

- Added a full-profile, source-free eigenmode verification across the fixed two-layer interface in test_layered_reference.py.
- The independent eigenvalue and piecewise sinusoidal mode enforce pressure continuity and nonzero hydraulic-flux continuity at x=0.375.
- L2 errors at N=40,80,160 are 1.5534e-4, 3.8877e-5 and 9.7218e-6 (approximately second-order spatial convergence with dt proportional to dx^2).
- Hosted CI for this additional test is pending. This remains code verification for a grid-aligned two-layer jump, not validation of silica parameters or constitutive laws.


## AP C extension — off-grid interface, multilayer reference and time-dependent mobility (13 November 2026)

- Added an off-grid two-layer comparison at x=0.37 and N=40,80,160. The test requires decreasing error against the independent eigenfunction reference. This characterises the current cell-centred sampling approach; it does not establish interface-fitted second-order accuracy. A subcell-aware capacity/conductance formulation remains a future numerical improvement.
- Added multilayer_reference.py, an exact transfer-matrix characteristic equation for piecewise-constant layers. Tests check the homogeneous three-layer limit and heterogeneous three-layer eigenvalue roots. This is an eigenvalue reference, not yet a multilayer transient solver benchmark.
- Added time-varying mobility verification against the exact transformed time for uniform lambda(t)=1+0.5t and fixed storage. The test checks temporal convergence and storage/flux balance. Time-varying storage and coupled aging remain unsupported.
- Hosted 1-D transport test steps passed in CI #360, #362 and #363. All four integrated workflows #360–#363 subsequently completed successfully, including the full 1-D transport suite and downstream workflow stages.
- All of the above is numerical code verification, not silica-specific physical validation.


## AP C — interface-aware finite volumes (13 November 2026)

- Added a separate interface-aware 1-D FV solver accepting explicit physical layer boundaries.
- Cell storage is integrated exactly over layer/cell overlaps, including cut cells.
- Hydraulic conductance is computed from the exact series integral of 1/lambda between adjacent cell centres and between boundary and first/last centre.
- Added tests for homogeneous recovery, off-grid two-layer analytical comparison, cut-cell capacity, interface-crossing resistance, three-layer conservation/positivity and invalid geometry.
- This is a conservative piecewise-constant interface-aware method with cell-centred representative pressures. It is not a moving-interface, nonlinear, or high-order cut-cell solver; silica physical validation remains separate. Hosted CI #374 passed the full integrated workflow.


## AP C follow-up — off-grid interface eigenmode profile (13 November 2026)

- Extended the interface-aware solver to accept a prescribed cell-centred initial pressure profile, retaining the scalar uniform-initial-pressure API.
- Added an off-grid two-layer first-eigenmode transient test at x=0.37. It checks analytical pressure continuity and nonzero Darcy-flux continuity, then compares the complete numerical profile against the exact decaying eigenmode for N=40,80,160.
- Added validation for malformed initial profiles. Hosted CI #376 completed successfully, including the full transport suite and all downstream stages.


## AP C extension — finite contact resistance at internal interfaces (13 November 2026)

- Added optional area-specific contact resistances (Pa s/m), one per internal interface, to the interface-aware finite-volume solver. They are added in series to the exact bulk resistance between adjacent cell centres.
- Added an independent transfer-matrix jump condition using q=lambda dp/dx: q_left=q_right and p_right-p_left=R_c q. The sign was checked against the physical Darcy flux -q; a positive resistance slows modal relaxation.
- Added zero-contact limit, modal-rate shift, validation, three-layer conservation/positivity, and full-profile three-layer eigenmode tests. The latter compares the transient FV pressure with the independent analytical eigenmode for N=40,80,160.
- Extended the FV graph with co-located minus/plus pressure degrees of freedom whenever contact resistance is positive. Adjacent control volumes are split at the physical interface and storage is integrated one-sided; the method supports interfaces both on and off original cell centres. Legacy cell-centre profiles are projected from the augmented state, while full one-sided node values remain available.
- Hosted workflow #388 passed all 92 transport tests and the complete integrated pipeline: https://github.com/Hu3eIn27864/precipitated-silica-gels-review/actions/runs/43511782095.
- Contact resistance remains a phenomenological parameter. No value is assigned to precipitated silica and no physical calibration is claimed.


## AP C extension — two-sided interface degrees of freedom (13 November 2026)

- Added an augmented FV graph with co-located minus/plus pressure unknowns at each positive-contact interface. The interface is an explicit node pair, not a resistance hidden inside a bulk face.
- Control-volume storage is split at the interface and integrated separately on each material side. Bulk links use exact integrated resistance; the contact link uses conductance 1/R_c.
- The new representation handles a contact interface exactly at an original cell centre as well as off-grid interfaces. The full augmented state is exposed through node coordinates, side labels and node profiles; the legacy cell-centre profile is projected for compatibility.
- Added a test at x=0.3625 with N=40, verifying the two one-sided traces, finite pressure jump and exact contact conductance. Existing three-layer full-profile eigenmode and conservation checks remain active.
- Hosted CI for the two-sided DOF extension is pending; no claim of success until the run is inspected. No physical contact resistance has been assigned to silica gel.
