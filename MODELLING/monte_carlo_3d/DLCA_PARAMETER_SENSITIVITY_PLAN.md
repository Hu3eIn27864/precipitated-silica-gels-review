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
attempts per seed. It runs the baseline (1.0, 0.2, 1.0) and all six non-baseline variants
using the same three seeds and attempt limit. The baseline is generated in
the same screening block, not borrowed from the separate size-series pilot,
so all seven configurations share common random-number seeds. This is a
software/integration screen, not a substitute for the full matrix.
The script writes `parameter_manifest.csv` and keeps each variant in a
separate directory. CI then runs the fixed 2–5 contact-distance-unit ensemble
summary and fit-window sensitivity audit for the baseline and every variant.

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

## Paired seed-level comparison

After all seven configurations (baseline plus six variants) have been run and
analysed, `compare_dlca_parameter_sensitivity.py` compares each variant
against the baseline using identical seed IDs. It writes
`*_paired_per_seed.csv` and `*_paired_summary.csv`. The per-seed file retains
every seed, including incomplete or unwrapping-invalid runs. Largest-component
fraction differences are reported for every paired seed; radius-of-gyration
and fixed-window exponent differences are calculated only when the observable
is available for both members of the pair. The summary reports valid-pair
counts and paired completion counts. A strict seed-set check prevents
accidental unpaired comparisons. Positive deltas mean the variant exceeds
the baseline.

These are descriptive paired differences, not inferential tests. With only
three seeds in CI, standard deviations are unstable and no significance or
physical robustness claim should be made. The larger preplanned matrix and
more independent seeds are required before scientific interpretation.


## First hosted screening result (2026-11-11)

GitHub Actions run [#220](https://github.com/Hu3eIn27864/precipitated-silica-gels-review/actions/runs/43015008467) completed the seven-configuration N = 32 screen with three paired seeds and 50,000 attempts per run. The baseline completed 0/3; completion counts were 1/3 at contact distance 0.9, 2/3 at 1.1, 0/3 at step 0.10, 3/3 at step 0.28, 0/3 at mobility exponent 0.5, and 1/3 at 1.5.

There were no pairs in which both baseline and variant runs completed, so the number of valid paired Rg and fixed-window exponent comparisons was zero for every variant. The per-seed largest-component-fraction deltas remain available, but they mix incomplete outcomes and should be read only as finite-attempt progress descriptors. They do not support conclusions about equilibrium morphology, fractal dimension, or physical kinetics. The high completion sensitivity to the maximum cluster step is a reason to investigate algorithmic time stepping and collision-detection robustness before expanding the physical interpretation.

The separate size-series pilot in the same CI run completed 2/3 runs at N = 32 and 0/3 at N = 64 or 128. Its two eligible N = 32 exponents had mean 1.199 (sample SD 0.057), but the mean within-run exponent range across fit windows was 0.394 (maximum 0.587). Thus even the eligible N = 32 fit is strongly window-dependent. No finite-size scaling result is available. These observations reinforce the predeclared decision gate: do not launch or interpret the larger matrix as a scientific scaling study until completion and fit-window stability are improved.


## Important: step size also changes the algorithmic clock

A fixed number of attempts is not a common elapsed-time basis when
`maximum_component_step` changes. Each proposed displacement has independent
Cartesian components uniform on [-s, s], so its mean squared vector length is
E[|Δr_proposed|²] = s². Before collision clipping and state-dependent cluster
selection, changing s from 0.2 to 0.1 reduces this proposal mean-square
displacement per attempt by a factor of four; changing it to 0.28 increases
it by a factor of 1.96. The first CI screen deliberately held attempt count
fixed and therefore mixes step-size effects with different algorithmic
progress per attempt.

The observed completion counts (0/3 at s = 0.2, 0/3 at s = 0.1, and 3/3 at
s = 0.28) must not be interpreted as evidence that the larger step produces
a more physical or more robust aggregate. They are completion outcomes under
different proposal-displacement budgets. The realized displacement is further
reduced by first-contact clipping, and cluster masses/selection probabilities
change during aggregation.

Before a step-size robustness claim, extend the run output to record at least
the cumulative realized squared cluster translations
Σ |Δr_cluster,realized|² and cumulative realized path length. Then compare
configurations at a common, predeclared cumulative translation budget (with
the maximum-attempt limit retained as a safety cap), or use stored trajectory
snapshots at common values of that budget. This is an algorithmic
displacement clock only; it is not physical time and does not by itself
calibrate Brownian diffusivity. The present fixed-attempt screen is useful
for diagnosing runtime/completion sensitivity, not for isolating a
step-independent structural effect.


The follow-up instrumentation was validated in hosted CI run #234. At 50,000 attempts, the three baseline seeds (s = 0.2) accumulated mean Σ|Δr|² = 2,000.71; the s = 0.1 runs accumulated 500.30, close to the expected quarter ratio. The s = 0.28 runs completed in a mean 25,665 attempts and accumulated mean Σ|Δr|² = 2,011.66 at completion. This confirms that fixed attempt count substantially changes the displacement budget across step sizes. It motivates the next implementation step: stop at a common cumulative realized squared-translation budget, with an independent maximum-attempt safety cap, and compare seed-matched structures at that common algorithmic progress coordinate.


## Common-displacement follow-up screen (introduced 2026-11-11)

The DLCA core now supports an optional cumulative squared realized-translation
target (Q=\sum_k |\Delta\mathbf R_k|^2). A run completes each proposed move
and then checks the target; no move is truncated. The maximum-attempt limit
remains an independent hard safety cap. Run metadata reports target Q,
whether the target was reached, whether the cap was reached, and target
overshoot. Target Q = 0 preserves the legacy fixed-attempt mode.

The runner accepts `--target-q`; the CI workflow adds a paired N=32 screen
for the baseline and six one-factor variants using three common seeds,
50,000 maximum attempts, and provisional Q target 450 reduced-length-units
squared. This target is deliberately below the smallest-step pilot's
observed Q values (approximately 499–502 at 50,000 attempts), so all
step-size seeds should be able to reach it without raising the safety cap.
The value is a screening coordinate only, not physical time or calibrated
Brownian motion.

The common-Q screen must report both Q and path length L, attempt count,
target overshoot and completion. Equal Q does not imply equal L or equal
trajectory history. Incomplete clusters remain progress descriptors; no
fractal exponent is valid unless a complete, consistently unwrapped
aggregate exists. This follow-up is intended to test algorithmic sensitivity
at a common displacement coordinate, not to prove physical robustness.
Hosted validation of the core/CLI/tests is tracked in CI run #254; common-Q
screen results are pending artifact inspection.
