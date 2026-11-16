# CCFSM P27.37 Lean kernel

This is an isolated Lean 4 project pinned to Lean **v4.35.0**. It does not change the Python implementation or the CCFSM version line.

## What is proved

- A no-root leaf certificate carries a proof that the predicate has no root anywhere on its closed interval.
- A unique-root leaf certificate carries an existence-and-uniqueness proof for exactly one root in the open interval.
- An unresolved leaf carries no root-count claim.
- The subdivision lemmas prove closed-child coverage and explicitly identify a root at the split point as a boundary case, rather than counting it as an interior root of both children.

## What is not proved yet

This first kernel is a proof-carrying interface and a set of logical subdivision lemmas. It does **not** yet prove that P27.34 floating-point operations are outward rounded, that P27.35 Horner evaluation encloses every polynomial value, or that P27.36 derivative/endpoint tests produce the certificates. It also does not prove completeness of the Python search or physical validity of any CCFSM constitutive equation.

Connecting binary floating-point arithmetic to a sound real-number interval semantics is a substantial next step; the current Python one-ULP widening is not assumed to be formally correct by this Lean module.

## Build

From this directory run `lake build`. The dedicated GitHub Actions workflow builds this project independently of the legacy Python test suite.
