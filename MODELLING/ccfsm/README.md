# CCFSM — natural syneresis only

This folder contains version 0.1 of the Chemically Coupled Fractal Syneresis Model for **unloaded natural syneresis of precipitated silica gels**.

- CCFSM_NATURAL_SYNERESIS_v0.1.md — model definition, governing equations, empirical coefficient audit, identifiability limits, and mathematical propositions/energy proof.
- ccfsm_reduced.py — verified scalar natural-syneresis response and dimensionally checked hydraulic time-scale helper.
- test_ccfsm_reduced.py — unit tests for exact solution, bounds, monotonicity, semigroup property, volume balance, and input validation.
- natural_syneresis_empirical_coefficients_2026-11-14.csv — machine-readable copy of the seven current digitized primary fits and derived apparent rates.
- wilhelm_kind_natural_syneresis_source_table_coefficients_2026-11-14.csv — separate machine-readable copy of the 12 source-reported natural-syneresis Table 1/2 parameter combinations; the basic-droplet branch is explicitly flagged as conflicting with the dissertation source.
- wilhelm_2017_dissertation_basic_droplet_conflict_2026-11-14.csv — the separate natural-syneresis coefficient branch from dissertation Table 5.3 (A = 0.40/0.63/0.82; tau = 0.671/0.640/1.055 h at 20/40/60 °C). Do not average it with the journal Table 2 values.

## Reproduction

From this folder:

    python -m unittest -v

The seven parameter rows are sourced from the project's curated primary fit table for digitized Wilhelm & Kind (2015) natural-syneresis curves. These are figure-derived approximations, not author-supplied raw data. Excluded sensitivity/conflict branches remain excluded.

No oedometer, imposed-load, or forced-syneresis coefficient is used for the CCFSM natural-syneresis calibration. Unidentified chemical, fractal, eigenstrain, permeability, and modulus parameters are intentionally left unset.


## CCFSM v0.2 — two-timescale natural-syneresis closure

Added on 14 November 2026:

- CCFSM_v0.2_TWO_TIMESCALE.md — separation of intrinsic network contraction and observed hydraulic shrinkage; closed-form solutions; proofs of existence, invariant region, monotonicity and rate-label non-identifiability; finite-strain kinematics; silicon-balance caveat; natural-only experiment design.
- ccfsm_two_stage.py — exact two-state response, stable equal-rate limit, hydraulic-rate scaling, isotropic natural stretch, and unordered rate-pair recovery.
- test_ccfsm_two_stage.py — 12 regression tests.

The two new rates are not fitted to the current one-exponential tables or approximate digitized traces. The source-reported (A, tau) values from v0.1 remain unchanged. A single zero-start shrinkage curve only identifies an unordered pair of two rates and the endpoint product eta_a*q_infinity; assigning physical labels requires an independent chemical/structural or hydraulic measurement.

Local software verification: 12/12 tests passed with python -m unittest -v. This is not physical validation. The natural-only exclusion remains in force: no oedometer, forced-syneresis or imposed-load coefficient is used.

The dedicated GitHub Actions workflow at .github/workflows/ccfsm-ci.yml runs all CCFSM unit tests on push/pull requests that touch this package.
