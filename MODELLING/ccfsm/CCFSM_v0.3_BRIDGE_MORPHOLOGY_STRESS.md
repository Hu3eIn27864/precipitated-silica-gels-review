# CCFSM v0.3 — bridge, morphology, eigenstress and natural drainage

**Scope:** natural, mechanically unloaded syneresis of precipitated silica only.  
**Status:** implemented reduced research hypothesis; coefficients uncalibrated; software regression-tested, not physically validated.

## Governing closure

For one fixed recipe and thermal protocol:

\[
\dot B=k_b(B_\infty-B),\quad 0\le B\le B_\infty.
\]
Here B is effective load-bearing siloxane bridge density [mol m^-3]. It is a coarse-grained state, not an elementary reaction coordinate.

Morphology is represented independently:
\[
D_{f,eq}=D_{f,0}+\Delta D_f B/B_\infty,\quad
\dot D_f=k_m(D_{f,eq}-D_f),
\]
\[
z_{eq}=z_0+\Delta z B/B_\infty,\quad
\dot z=k_m(z_{eq}-z).
\]
These are falsifiable first-order hypotheses. No direct mapping from Df or z alone to permeability or modulus is assumed.

Bridge formation generates a network-scale logarithmic contraction increment:
\[
\dot\chi_b=\Omega_b\dot B.
\]
Residual eigenstress-contraction sigma relaxes into accommodated contraction epsilon:
\[
\dot\sigma=\Omega_b\dot B-k_r\sigma,\qquad
\dot\epsilon=k_r\sigma.
\]
Therefore sigma+epsilon is the accumulated bridge contraction inventory (for consistent initial states); stress relaxation redistributes contraction rather than deleting it. Define q=1-exp[-(sigma+epsilon)].

Observed natural shrinkage follows
\[
\dot S=k_h(\eta_aq-S),\quad 0<\eta_a\le1,
\]
with the independently constrained natural hydraulic first-mode rate
\[
k_h=3600 C_g\kappa_{eff}K_{eff}/(\mu L_d^2)\quad [h^{-1}].
\]

## Mathematical and empirical limits

Positive rates and admissible initial states give bounded bridge density, positive contraction inventory, q in [0,1), and monotone natural shrinkage while q increases. The code uses RK4, so step refinement is required; the continuous-time invariant properties do not make arbitrary large RK4 steps safe.

All coefficients are inputs, not fitted constants. Omega_b is an effective network-scale contraction volume, not molecular bond volume. Df and z are parallel measured/identified states, not assumed permeability predictors. Permeability and modulus remain independent measurements. Acid and base routes require separate calibration, actual gel-temperature histories, and a silicon balance separating dissolved, network-bound and expelled silicon.

A shrinkage curve alone cannot identify bridge inventory, Omega_b, morphology rates, stress relaxation, interface accessibility, permeability and modulus. No oedometer or forced-syneresis coefficient is used.

## Identification experiment

Synchronize gel-core temperature, pH, dissolved/network-bound silicon, a declared-scale fractal measurement, contact/coordination proxy, stress relaxation/rheology, expelled-liquid mass, external volume, viscosity, permeability, modulus, drainage length and vessel/interface treatment. This is the minimum route to identifying the separate state processes rather than overfitting S(t).
