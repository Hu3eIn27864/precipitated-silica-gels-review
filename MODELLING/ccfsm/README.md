# CCFSM — natural syneresis only

This folder contains version 0.1 of the Chemically Coupled Fractal Syneresis Model for **unloaded natural syneresis of precipitated silica gels**.

- CCFSM_NATURAL_SYNERESIS_v0.1.md — model definition, governing equations, empirical coefficient audit, identifiability limits, and mathematical propositions/energy proof.
- ccfsm_reduced.py — verified scalar natural-syneresis response and dimensionally checked hydraulic time-scale helper.
- test_ccfsm_reduced.py — unit tests for exact solution, bounds, monotonicity, semigroup property, volume balance, and input validation.
- natural_syneresis_empirical_coefficients_2026-11-14.csv — machine-readable copy of the seven current primary fits and derived apparent rates.

## Reproduction

From this folder:

    python -m unittest -v

The seven parameter rows are sourced from the project's curated primary fit table for digitized Wilhelm & Kind (2015) natural-syneresis curves. These are figure-derived approximations, not author-supplied raw data. Excluded sensitivity/conflict branches remain excluded.

No oedometer, imposed-load, or forced-syneresis coefficient is used for the CCFSM natural-syneresis calibration. Unidentified chemical, fractal, eigenstrain, permeability, and modulus parameters are intentionally left unset.
