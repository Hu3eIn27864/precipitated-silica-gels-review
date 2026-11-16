# CCFSM baseline CI repairs — 2026-11-16

## Scope

These changes repair the nine test failures that were reproduced on the exact
base commit used by the P27.42/P27.43 interval-arithmetic work. The repairs
are isolated from the natural-syneresis constitutive equations. CCFSM remains
v4.2.57.

## P27.37 — test fixtures, not algorithm

The original depth-limit fixture used a globally monotone linear polynomial,
which P27.36 could certify on the parent interval before subdivision. Thus
max_depth=0 did not force an unresolved result. The original split-boundary
fixture likewise used a linear polynomial whose root at x=0.5 was certified
as the unique interior root of [0,1]. Both expected outcomes were inconsistent
with the P27.36 classifier.

The replacement cubic
p(x)=(x-0.5)(x^2-3x+2.26)
has a derivative that changes sign over [0,1]. The parent therefore remains
unresolved; subdivision at x=0.5 leaves two adjacent closed intervals with
unresolved endpoint signs. Neither child counts the shared root as an
interior root. The P27.37 focused test file passes 8/8 locally.

## Remaining baseline failures addressed in this stack

- **P27.10:** isolated coordinate vertices are retained in the separate
  isolated-vertex report but excluded from vertex-link tests because they are
  not vertices of the tetrahedral simplicial complex.
- **P27.13:** duplicate tetrahedra pass the geometry preflight and fail a
  downstream incidence/topology gate; the test now expects the integrated
  audit's correct failure status.
- **P27.17:** mobile species advection was reconstructed from species face
  fluxes, while Darcy fluid continuity was independently audited. Adding the
  Darcy divergence a second time to the M species equation double-counted
  transport. The reconstruction now uses the M advective and diffusive fluxes
  plus their reaction source; Darcy remains a separate fluid balance.
- **P27.18:** the public scalar reconstruction function raises ValueError for
  zero concentration. The old direct-call test incorrectly expected a
  returned status mapping; it now asserts the documented exception.
- **P27.23:** the two-cell fixture integrates elastic energy to 7 J and Biot
  storage to 12 J, for total mechanical energy 19 J, not 20 J.
- **P27.28:** exact integration of the specified polynomial chemical
  potential/flux data gives 18.24 J, not the old expected 18.21 J.

## Verification history

- Before repairs, the isolated baseline branch and P27.42/P27.43 work branch
  reproduced the same nine failing test identifiers.
- After the P27.37 fixture correction, hosted full-package CI no longer reports
  either P27.37 failure.
- This stacked branch includes the P27.37 correction and the other six test /
  implementation fixes. Hosted package CI is the final acceptance gate.

## Scientific and software boundaries

The P27.17 change concerns reconstruction of the discrete finite-volume RHS
from the already supplied species flux decomposition. It does not assert that
the flux constitutive laws are physically complete. The P27.23 and P27.28
changes correct the arithmetic references of synthetic regression fixtures;
they do not calibrate thermodynamic model parameters. The P27.10/P27.13
changes clarify the audited simplicial complex and gate status.

No physical CCFSM law, calibration datum, parameter, or version identifier is
changed. CI success establishes software regression status only, not
experimental validation or physical correctness.
