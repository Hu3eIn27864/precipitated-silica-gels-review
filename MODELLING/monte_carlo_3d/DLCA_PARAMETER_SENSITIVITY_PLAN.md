# DLCA algorithmic parameter-sensitivity plan

## Purpose

Test whether the reduced-unit DLCA structural outputs are robust to three
explicit algorithmic choices: contact distance, maximum rigid-cluster
translation step, and the mass-mobility exponent. This is a numerical
robustness study, not physical calibration of precipitated silica.

## Full comparison design

The full proposed study uses the existing size-series runner with:

- particle counts: 32, 64, 128;
- reference box: 15.0 at N = 32, preserving N/L^3 across sizes;
- seed count: 5 per size;
- base seed start: 1000;
- maximum attempts: 200,000 per run;
- default values for all parameters not being varied;
- a separate output directory/prefix for every parameter value.

## Bounded CI screening subset

For CI runtime, `run_dlca_parameter_sensitivity.py` executes a smaller
screening subset: N = 32, three paired seeds starting at 3000, and 50,000
attempts per seed. It runs the six non-baseline variants in the matrix below;
the ordinary CI size-series pilot supplies the baseline at (1.0, 0.2, 1.0).
This is a software/integration screen, not a substitute for the full matrix.
The script writes `parameter_manifest.csv` and keeps each variant in a
separate directory. CI then runs the fixed 2–5 contact-distance-unit ensemble
summary and fit-window sensitivity audit for every variant.

For a paired comparison, reuse the same base seed start for each parameter
variant. The runner then maps the same seed block to each particle count in
every variant. This is deliberate common-random-number pairing across
configurations; do not describe different particle counts as paired to one
another because the runner allocates distinct seed blocks by size.

## One-factor-at-a-time matrix

| Factor | Values | Fixed values |
|---|---|---|
| Contact distance | 0.9, 1.0, 1.1 | step 0.2; mobility exponent 1.0 |
| Maximum component step | 0.10, 0.20, 0.28 | contact distance 1.0; mobility exponent 1.0 |
| Mobility exponent | 0.5, 1.0, 1.5 | contact distance 1.0; step 0.2 |

The maximum step values respect the code's conservative contact-detection
bound sqrt(3) * step <= 0.5 * contact_distance. Values are deliberately
algorithmic brackets, not literature-fitted parameters.

Changing contact distance also changes the initial excluded-volume fraction
at fixed N/L^3 (proportional to contact_distance^3 for equal spheres). Treat
that as part of the tested factor and report it; do not attribute the result
to contact geometry alone.

## Analysis

1. Preserve every raw CSV set and record the exact source commit and command.
2. Report completion fraction, attempt-limit hits, unwrapping-valid fraction,
   largest-component fraction and Rg for each N and parameter value.
3. Run the fit-window sensitivity audit for every configuration.
4. For the fixed-window comparison, use 2–5 contact-distance units. Convert
   these bounds to absolute radii for each contact-distance variant because
   the mass-radius grid is scaled by the configured contact distance.
5. Compare paired seed outcomes where both variants completed and unwrapped,
   but also report unmatched/incomplete cases; do not silently condition away
   failed runs.
6. Do not pool overlapping fit windows as independent observations. Report
   seed-level estimates and between-seed dispersion separately from
   within-seed fit-window ranges.

## Decision criteria

A parameter setting is not preferred merely because it completes more often
or produces a higher R-squared. If completion, unwrapping, or fit-window
stability changes strongly across the bracket, classify the model output as
algorithmically sensitive and defer physical interpretation. No universal
fractal exponent or silica-specific parameter is inferred from this study.
