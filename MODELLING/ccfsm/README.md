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
