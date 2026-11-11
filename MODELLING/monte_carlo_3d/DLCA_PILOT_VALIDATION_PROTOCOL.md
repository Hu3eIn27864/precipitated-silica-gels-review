# DLCA pilot validation protocol

## Purpose and scope

This protocol governs interpretation of the first reduced-unit DLCA size series (nominally N = 32, 64, 128). It is a software and algorithmic diagnostic, not a calibrated model of precipitated silica. No physical time, pH dependence, ionic-strength dependence, or experimental fractal dimension may be inferred from this pilot.

## Frozen pilot design

- Particle contact distance: 1.0 reduced length units.
- Maximum Cartesian component of a rigid-cluster translation: 0.2 reduced length units.
- Mobility exponent: 1.0 in the declared algorithmic cluster-selection law.
- Reference system: N = 32, L = 15.0; larger boxes preserve N/L^3.
- CI pilot: three consecutive seeds per size, maximum 50,000 cluster-move attempts per seed.
- Mass-radius radii: 1.5, 2.0, 2.5, 3.0, 4.0, 5.0, 6.0, 8.0 times the contact distance.
- Common initial diagnostic fit interval: 2.0–5.0 contact-distance units. This is not a pre-validated scaling interval.

The ensemble CLI accepts optional trailing values for contact distance,
maximum component step and mobility exponent; the original defaults remain
available. The run-summary CSV records these values. The mass-radius grid
scales with contact distance so fit intervals remain dimensionless in contact
units. For a non-default contact distance, convert fit bounds accordingly.
Any parameter change must be recorded as a new run configuration; do not
overwrite or silently mix outputs from different configurations.

## Mandatory integrity checks

For every seed and system size:

1. Record whether the aggregation completed before the attempt limit.
2. Check that the largest component contains exactly N particles for a completed one-component result.
3. Reject mass-radius analysis if periodic graph unwrapping is inconsistent or the aggregate winds around the periodic cell.
4. Verify unique seeds, matching particle counts, finite positive radii and enclosed masses, and the common radius grid.
5. Keep all fit-window rows linked to their originating completed and consistently unwrapped run.
6. Preserve raw CSV files, exact command line, source commit, compiler/build type, and workflow run identifier.

Incomplete runs are informative outcomes. Do not silently discard them from completion statistics. Do not assign them a fractal exponent.

## Structural analysis

Report, at minimum:

- completion fraction and attempt counts by N;
- largest-component fraction for incomplete runs;
- Rg distribution for the largest component, clearly distinguishing complete and incomplete cases;
- seed-level mass-radius curves;
- fit-window exponent and R-squared diagnostics;
- within-seed exponent range across available windows;
- between-seed dispersion for any common, explicitly declared fit interval.

Fit windows from one aggregate are strongly dependent because they reuse the same mass-radius curve. They are not independent replicates and must never be pooled to inflate sample size. A high R-squared alone does not establish a fractal scaling regime. Do not select a window solely because it produces a desired exponent or highest R-squared.

## Interpretation gates

### Gate A — software and output integrity

Pass only if the full C++ build, all CTest targets, all Python unit tests, and the end-to-end ensemble smoke test complete successfully. The hosted workflow must be inspected; an empty status response is not a pass.

### Gate B — stochastic completion

Report completion fraction for every N. If many runs hit the attempt cap, increase the attempt budget or revise the pilot design in a separately versioned run. Do not compare fitted exponents from a selectively completed subset without explicitly reporting the selection.

### Gate C — finite-size and fit-window sensitivity

Compare seed-level curves, not just pooled summary values. A proposed scaling interval must be supported by a visible approximately linear region on log–log axes, enough radius points, stability to modest changes in the interval, and consistency across seeds and sizes. The current radius grid is sparse; if no convincing common region exists, report that no robust exponent can be assigned.

### Gate D — parameter sensitivity

Before any physical interpretation, vary one factor at a time: maximum cluster step, mobility exponent, initial number density/box length, and contact distance. Keep seeds and other settings fixed where a paired comparison is intended. Equal attempt counts are not equal elapsed algorithmic progress when the maximum step changes: the proposal mean-square displacement per attempt is s² for Cartesian components uniform on [-s,s]. A step-size comparison must therefore record realized cumulative cluster displacement and compare at a common predeclared displacement budget (or common-budget trajectory snapshots), while retaining an attempt cap. This is an algorithmic clock, not physical time. The initial fixed-attempt screen is only a completion/runtime diagnostic. This separates algorithmic robustness from random-seed variation.

### Gate E — physical calibration and validation

Only after Gates A–D should the model be extended toward silica-specific claims. Required inputs include experimentally defensible primary-particle/contact scales, interaction parameters with provenance, chemistry (at least pH and ionic strength where relevant), and compatible independent structural observations. Validate against data not used to tune parameters. DLCA move attempts are not physical time.

## Reporting template

For each N report: requested seeds, completed seeds, completion fraction, attempt-limit hits, unwrapping-valid seeds, largest-component fractions, Rg mean and sample SD where defined, number of usable mass-radius curves, fit interval, per-seed exponents, median/range and sample SD, fit-window sensitivity, and explicit limitations. Always distinguish missing fits due to incomplete runs from invalid fits due to geometric winding.

## Decision rule

If completion, unwrapping, or fit-window robustness is inadequate, do not proceed to a silica parameter fit. The next task is to diagnose the numerical/algorithmic limitation, not to increase model complexity or claim physical mechanisms.

A predeclared one-factor-at-a-time bracket for contact distance, maximum
component step and mobility exponent is documented in
[DLCA_PARAMETER_SENSITIVITY_PLAN.md](DLCA_PARAMETER_SENSITIVITY_PLAN.md).
