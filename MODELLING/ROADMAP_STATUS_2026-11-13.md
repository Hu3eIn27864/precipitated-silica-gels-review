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
| **AP B — common-displacement DLCA** | Common cumulative-\(Q\) stopping mode, safety cap, stop reason and overshoot accounting are implemented and tested. The recorded N=32, Q=450 screen reached its Q target in all 21 runs, but none completed aggregation. | **No-go** for morphology or fractal-dimension conclusions and for a large production matrix. Diagnose cluster mobility/merge efficiency and pre-register any new pilot before running it. Q and path length are algorithmic progress measures, not physical time. |
| **AP C — transport solver verification** | Radial solver passed analytical-series/refinement checks. Heterogeneous solver tests now include cell-centre interface refinement and integrated outflow/storage-loss balance; the full transport suite passed 62/62 in CI #342. | The two tests are useful regressions but not independent benchmarks: interface location shifts with grid; flux balance reuses solver face fluxes. Still needed: exact fixed-interface two-layer eigenfunction reference, independent boundary-gradient flux integration, and variable-coefficient manufactured solution. |
| **AP D — evidence and parameter identifiability** | Consolidated source comparison is now in `LITERATURE/transport_parameter_comparison_2026-11-13.md`. Direct target-chemistry rheology and oedometer response, plus industrial cake filtration/mesostructure evidence, are available. No matched intrinsic-permeability/constrained-modulus pair for the target gel state has been identified. | Prioritise direct wet-gel permeability and a mechanical measurement that maps to constrained modulus M on matched formulations/ageing states. Keep cake resistance, oedometer t90, rheological E0 and free-syneresis tau as distinct observables. |
| **AP E — manuscript synthesis** | Claim/evidence synthesis and a coupled transport–mechanics–structure framework exist. | Continue only as a claim audit and outline refinement; no final causal or predictive claim until APs A–D clear their gates. |

## Immediate execution order

1. **AP C1 — independent layered benchmark.** Replace the current grid-shifting interface check as the decisive benchmark with a fixed physical interface and the two-layer eigenfunction condition documented in `MODELLING/transport_model/heterogeneous_1d_verification_review_2026-11-13.md`.
2. **AP C2 — independent flux reconstruction.** Reconstruct boundary gradients from numerical pressure profiles, integrate Darcy flux with a stated quadrature rule, and compare with total storage loss; report this separately from the existing discrete balance identity.
3. **AP D1 — targeted data acquisition.** The source comparison is complete as an audit. Search next for direct wet-gel permeability and constrained-modulus measurements on matched sodium-silicate/sulfuric-acid formulations; do not repurpose cake or oedometer observables as those parameters.
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
- AP C review found that the existing interface-location and integrated-outflow tests are useful but weaker than an independent exact benchmark. The remaining requirements are documented in `MODELLING/transport_model/heterogeneous_1d_verification_review_2026-11-13.md`.
- AP D source-by-source parameter comparison is documented in `LITERATURE/transport_parameter_comparison_2026-11-13.md`. The decisive target-system permeability–mechanical-modulus identifiability gap remains open.
