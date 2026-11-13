# Common-form kinetic analysis plan for digitised syneresis curves

**Working protocol; 13 November 2026**  
**Status:** analysis specification only. No new fits are reported in this file.

## 1. Data hierarchy

Every curve record must preserve: source DOI, figure/panel, gel chemistry, temperature, pressure label and range, initial specimen height, geometry, membrane/support, source trace type, digitisation method, axis calibration, point uncertainty and any curve-tracing confidence.

Keep three data classes separate:
- **PUBLISHED_FIT:** parameter values transcribed from the article's tables.
- **AI_DIGITISED_COMBINED_TRACE:** points extracted by ChatGPT where solid measured and dashed fitted traces may overlap or be inseparable.
- **VERIFIED_MEASURED_TRACE:** only a trace independently checked against the original high-resolution figure and identified as the measured curve.

Do not merge these classes in a fit without an explicit sensitivity analysis.

## 2. Candidate response functions

Primary common form:

\\[
S(t)=A\\left[1-\\exp\\left(-\\left(t/\\tau\\right)^n\\right)\\right],
\\]

where (A) is the asymptotic shrinkage, \\(\\tau\\) is the 63.2%-of-asymptote time, and (n) controls curve shape.

Pre-register these fit cases:
- **F1:** shared fixed (n=1.23), estimate (A,\\tau) separately for each curve.
- **F2:** shared fixed (n=1.00), estimate (A,\\tau) separately.
- **F3:** fit (n) per curve only if the time series has enough independent curvature information; report parameter covariance/profile likelihood and boundary sensitivity.
- **F4:** optional global/shared (n) across a chemically and geometrically comparable subset, with curve-specific (A,\\tau). Do not force acid and base series into one (n) without evidence.

The published 2014 and 2015 parameter tables used different fixed curve shapes (2014 (n=1.23); 2015 (n=1)). Their \\(\\tau\\) values therefore should not be treated as strict like-for-like estimates.

## 3. Time-zero and endpoint handling

- Preserve all original digitised points, including apparent deviations at early time.
- Do not force (S(0)=0) unless the source plot and measurement definition support that baseline; if a baseline offset is needed, document and fit it as a separate sensitivity model.
- Do not infer an asymptote from the last plotted point alone. Compare fitted (A) with the published table and visible plateau.
- Do not remove non-monotone points automatically. Flag them and retain a trace-level audit trail.
- If a trace is combined measurement/model or its curve identity is uncertain, fit only as an explicitly labelled exploratory sensitivity case.

## 4. Digitisation uncertainty and robust sensitivity

At minimum, perturb each point within its recorded pixel-to-data uncertainty and repeat the fit (Monte Carlo or parametric bootstrap). Also perform:
- full-curve versus early-time-excluded sensitivity (early exclusion only as a labelled sensitivity, never the primary fit by default);
- fit window sensitivity;
- leave-one-segment-out sensitivity for visually ambiguous or overplotted sections;
- F1 versus F2 model-form sensitivity;
- point-weighted versus time-uniform weighting if digitisation density is nonuniform.

Report confidence intervals and parameter correlations, not only (R^2). A high (R^2) is not evidence of physical validity.

## 5. Quality gate before fitting

A curve is eligible for primary fitting only if:
1. axis calibration is documented and independently checked;
2. the measured trace can be distinguished from model/dashed traces;
3. pressure and panel identity are unambiguous;
4. no unresolved line-switching or gross discontinuity remains;
5. the extracted trace covers enough of the rise and plateau to constrain (A) and \\(\\tau\\);
6. point density and uncertainty are adequate for the intended parameter precision.

Otherwise label it exploratory or exclude it from quantitative comparison while preserving it in the audit.

## 6. Cross-study and chemistry comparison

- Match pressure by interval and preserve the original interval; do not silently replace a range by its midpoint.
- Keep 2014 versus 2015 acid comparison separate from acid versus base comparison.
- Record geometry, drainage length, sample age, temperature and membrane/support before comparing \\(\\tau\\).
- Calculate the half-response time (t_{50}=\\tau(\\ln2)^{1/n}) only as a derived quantile of the fitted function; it does not remove confounding or harmonise model error.
- Use published parameter tables as an external consistency check, not as fitting targets.

## 7. Reporting language

Preferred: “AI-assisted digitisation of published plotted traces; points are approximate and were subjected to curve-level quality screening.”

Avoid: “raw experimental data”, “measured time series” or “validated kinetics” unless original machine-readable observations or independently verified measurement-only traces are obtained.

A curve that passes the internal smoothness screen is not thereby experimentally validated.
