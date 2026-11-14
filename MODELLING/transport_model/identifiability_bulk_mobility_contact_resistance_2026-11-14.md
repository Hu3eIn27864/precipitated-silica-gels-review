# Identifiability of bulk mobility and interface contact resistance

**Status (14 November 2026): design and derivation only. No numerical sensitivity
run or parameter fit is reported in this note.** The data-analysis capability is
temporarily unavailable in this work session, so the numerical Jacobian,
singular values and profile-likelihood calculations remain pending.

## 1. Model and parameter distinction

The one-dimensional pressure-relaxation model is

\[
S_i\,\partial_t p=\partial_x(\lambda_i\,\partial_xp)
\]

inside layer \(i\), with drained external boundaries. At an internal interface
with area-specific contact resistance \(R_{c,j}\), use the transfer state
\(q=\lambda\partial_xp\) and impose

\[
q^-_j=q^+_j,\qquad p^+_j-p^-_j=R_{c,j}q_j.
\]

Here \(S_i\) is storage compliance (Pa\(^{-1}\)), \(\lambda_i\) is
hydraulic mobility (m\(^2\)/(Pa s)), and \(R_{c,j}\) is area-specific
contact resistance (Pa s/m). The Darcy flux is \(-q\). A positive
\(R_c\) is a phenomenological interface parameter until measured.

Do not collapse the two resistances into one fitted effective coefficient:
bulk resistance is the spatial integral of \(1/\lambda\), whereas an
interface contributes a discrete jump \(R_c\). They have different geometric
scaling and can, in principle, be separated by a sufficiently informative
experiment.

## 2. Why one relaxation time is insufficient

For a fixed geometry and known storage, a single observed modal decay rate
\(\sigma_1\) is one scalar datum. If both a bulk mobility scale and at least
one contact resistance are unknown, the inverse problem has at least two
unknowns and one scalar constraint. There is generally a continuum of
parameter pairs consistent with that one rate. A fitted single syneresis
time constant therefore cannot independently determine \(\lambda\) and
\(R_c\).

A useful nondimensional group for a uniform reference mobility \(\lambda_*\)
and specimen thickness \(L\) is

\[
\mathrm{Bi}_c=\frac{R_c\lambda_*}{L}.
\]

The bulk diffusion time scales as \(S L^2/\lambda_*\), while the relative
importance of a contact jump changes with \(\mathrm{Bi}_c\). Varying
thickness while keeping interface chemistry and preparation fixed is
therefore a key design lever: bulk and interface contributions do not scale
with specimen length in the same way.

## 3. Local sensitivity and rank test

For a model with \(n_L\) layer mobilities and \(n_I\) strictly positive
contact resistances, define a log-parameter vector

\[
\theta=(\log\lambda_1,\ldots,\log\lambda_{n_L},
         \log R_{c,1},\ldots,\log R_{c,n_I}).
\]

For each specimen geometry / loading condition \(g\), calculate several
eigenvalues \(\sigma_{g,m}\) from the independent multilayer transfer
matrix. Stack the log-sensitivity rows

\[
J_{(g,m),k}=\frac{\partial\log\sigma_{g,m}}
                   {\partial\theta_k}.
\]

Use a central finite difference in log space, with step-size convergence
checks, to estimate each derivative. Scale rows by the uncertainty of the
corresponding measured log-rate before assessing practical identifiability.
Report singular values, numerical rank, condition number and right singular
vectors; a full rank alone does not guarantee useful precision when the
smallest singular value is tiny.

For a zero-contact baseline, do not take \(\log R_c\). Treat zero as a
separate nested model, or use a nonnegative direct parameter with a
one-sided derivative at the boundary. Do not silently replace zero by an
arbitrary epsilon.

The sensitivity matrix is a local diagnostic only. Follow it with profile
likelihood or a multi-start nonlinear fit over physically admissible
parameter ranges, and check whether distinct parameter sets reproduce the
full transient curves within measurement uncertainty.

## 4. Observation sets and experiment design

Rank the evidence sources by how directly they separate the parameters:

1. **Independent bulk constraints:** measure storage/compressibility and
   mechanical response on the same formulation, curing age, temperature and
   stress state. If \(S\) is unknown, eigenvalues primarily constrain
   diffusivity-like ratios \(\lambda/S\), not \(\lambda\) alone.
2. **Multiple relaxation modes:** use spatially resolved pressure profiles
   or sufficiently resolved transients to identify more than one decay mode.
   A single bulk-average curve may conceal higher modes and their amplitudes.
3. **Thickness series:** repeat otherwise matched specimens at multiple
   thicknesses. Keep interface preparation and chemistry fixed; document
   whether the number of interfaces also changes.
4. **Interface-position series:** move a deliberately prepared interface
   while holding layer compositions and total thickness fixed. This changes
   the bulk path lengths on either side and the modal weighting of the jump.
5. **Independent flux information:** if feasible, measure boundary flux as
   well as pressure. Do not use a solver's own face flux as an independent
   experimental observable.

The minimum useful design should have more independent, uncertainty-weighted
observables than free parameters, and its sensitivity matrix should be
well-conditioned. Replicates estimate noise; they do not automatically add
structural information if they repeat an identical geometry and protocol.

## 5. Confounders and stop rules

- Unknown \(S_i\) is a major confounder with \(\lambda_i\). If both are
  freely fitted from pressure relaxation alone, state clearly which
  combinations are identifiable.
- Layer-specific mobilities and multiple contact resistances rapidly increase
  parameter count. Do not fit all of them from one specimen and one averaged
  time series.
- Initial conditions, boundary drainage resistance, sample dimensions,
  swelling/aging, and time-dependent material properties can mimic changes
  in apparent mobility or contact resistance. Measure or constrain them
  independently before expanding the constitutive model.
- A filtration-cake resistance, colloidal-silica oedometer conductivity, or
  free-syneresis time constant is not a direct measurement of the target
  precipitated-silica wet-gel \(\lambda\) or \(R_c\).
- Keep calibration and validation specimens separate. Report uncertainty
  intervals and parameter correlations, not just a best-fit pair.

## 6. Reproducible numerical work still required

The next computational increment is to add a standard-library sensitivity
utility using `multilayer_eigenvalues` and tests for:

- rank deficiency when one scalar modal rate is used for two unknowns;
- sensitivity-matrix rank and conditioning as additional modes and geometries
  are stacked;
- finite-difference step-size stability;
- invariance / scaling checks for the transfer-matrix eigenvalues;
- explicit failure or warning when the data set cannot constrain all
  requested parameters.

Only after those tests pass should synthetic noisy observations be generated
and inverse recovery tested. Synthetic recovery verifies the implementation;
it does not establish physical identifiability in real silica experiments.

## 7. Current implementation boundary

The repository already contains an interface-aware FV solver with paired
one-sided pressure traces and a multilayer transfer-matrix eigenvalue
reference. The solver's contact law and units are numerically verified in
hosted CI. This note does not assign any measured value to silica gel and
does not claim that bulk mobility and contact resistance have yet been
separated from experimental data.

## 8. Implemented local sensitivity diagnostic (14 November 2026)

Added `identifiability.py` and `test_identifiability.py`. The utility
constructs a central finite-difference Jacobian of log eigen-rates with
respect to two log-scale parameters: a common multiplier on all layer
mobilities and a common multiplier on all strictly-positive contact
resistances. It supports uncertainty-weighted rows through
`sigma_log_rates`, and returns singular values, numerical rank and condition
number from the two-column Gram matrix.

The tests are designed to check the one-rate rank-deficiency case, local
rank with multiple modes, finite-difference step stability, uncertainty
weighting and explicit rejection of zero contact resistance rather than
replacing it with an arbitrary epsilon. These tests have been committed, but
**hosted CI has not yet been inspected**; no pass result is claimed here.

Scope limitation: this is a local two-parameter design diagnostic with common
multipliers, not a general inverse solver. Full-rank sensitivity does not
establish global uniqueness or practical precision. Profile likelihood,
synthetic noisy recovery and tests over multiple geometries remain next
steps. No silica parameter values are inferred.
