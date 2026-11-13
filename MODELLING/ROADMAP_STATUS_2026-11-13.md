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
| **AP C — transport solver verification** | Ideal radial cylinder/sphere solver passed analytical-series and refinement checks. Fixed-coefficient heterogeneous 1-D solver passed the recorded hosted test suite (CI #328; 51 transport tests). | Add a layered-medium/interface benchmark, interface-location refinement, manufactured-solution check for variable coefficients, and integrated boundary-flux versus stored-pressure-loss balance. Only then consider time-varying constitutive coefficients. |
| **AP D — evidence and parameter identifiability** | Direct precipitated-silica syneresis, oedometer, rheology and structure sources are assembled. PSG-045 and PSG-046 add filtration/mesostructure evidence, but cake resistance is not the intrinsic permeability of a free syneresing gel. The matched target-system permeability–constrained-modulus pair remains unavailable. | Build a source-by-source parameter table (directly measured / fitted / inferred / unavailable); prioritise matched-state permeability and constrained/viscoelastic modulus, and preserve material, pressure path and geometry distinctions. |
| **AP E — manuscript synthesis** | Claim/evidence synthesis and a coupled transport–mechanics–structure framework exist. | Continue only as a claim audit and outline refinement; no final causal or predictive claim until APs A–D clear their gates. |

## Immediate execution order

1. **AP C1 — numerical interface benchmark.** Construct a two-layer 1-D case with piecewise constant mobility/storage and known interface location. Verify the discrete solution against an independent reference or manufactured solution; check convergence as the interface moves relative to cell faces.
2. **AP C2 — global conservation.** Integrate boundary flux over time and compare it with the change in volume-weighted stored pressure. Report discretisation error over grid and time-step refinement.
3. **AP D1 — permeability evidence matrix.** Compare the existing target-system and comparator sources, especially Sahabi & Kind (2011), Ragueh et al. (2015), Manfoumbi et al. (2024; PSG-045), and Ragueh et al. (2015; PSG-046). Keep cake-specific resistance/permeability, oedometer consolidation response, and free-gel intrinsic permeability as distinct observables.
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
