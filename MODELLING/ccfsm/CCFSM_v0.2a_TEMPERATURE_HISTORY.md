# CCFSM v0.2a — prescribed temperature-history extension

**Date:** 14 November 2026  
**Scope:** natural, mechanically unloaded syneresis of precipitated silica gels only  
**Status:** exact piecewise-constant rate propagator; analytically invariant; regression tested; no new physical rate fit

## 1. Experimental reason for the extension

Wilhelm and Kind's natural 3-mm droplet protocol did not expose each droplet to the target bath temperature from the start. The methods state that the droplets were held at 20 °C for the first 20 min (slightly longer than their reported gelation time of about 12 min), then transferred to the sample areas and subsequently temperature-controlled by immersion. The results state that curves remain similar during roughly the first 30 min because the temperature is initially 20 °C, and that each droplet must heat to its target temperature. This 20-min versus roughly-30-min wording is retained as a source/protocol uncertainty, not silently reconciled.

Consequently, a fit using nominal 40 or 60 °C from t=0 is not a true isothermal kinetic experiment. The early network can mature at 20 °C, while the later sample warms and its chemistry, pore-liquid viscosity and hydraulic response change. The sample's internal temperature T_g(t) need not equal bath set point T_b(t).

The paper also reports temperature-dependent final amplitudes, not only time constants: for its natural cylindrical samples the acid-gel amplitude is approximately unchanged at 0.20 while the basic-gel amplitude rises from 0.30 to 0.51 over 20–60 °C; for droplets both acid- and base-catalysed amplitudes rise across the reported series. Thus, the fixed q_infinity below applies to one specified recipe/geometry/temperature programme. It is not a universal temperature-independent silica constant.

## 2. Non-autonomous CCFSM rates

For one fixed protocol endpoint q_infinity and constant natural-interface accessibility eta_a, retain

\[
\dot q=k_n(t)[q_\infty-q],\qquad
\dot S=k_h(t)[\eta_aq-S]. \tag{1}
\]

Here k_n(t)>0 and k_h(t)>0 are evaluated from the actual gel temperature and current chemistry/structure, not simply from the bath label.

If T_g(t) is measured, one may test a branch-specific Arrhenius form for network maturation:

\[
k_n(T_g)=k_{n,r}
\exp\left[-\frac{E_n}{R}\left(\frac1{T_g}-\frac1{T_r}\right)\right], \tag{2}
\]

with temperatures in kelvin. E_n, k_n,r and reference temperature are inputs to be identified for the particular acid/base branch; the code supplies the functional form only.

The hydraulic rate is preferably calculated from separately measured or constrained material properties:

\[
k_h(t)\simeq
\frac{C_g\kappa_{\rm eff}(t)K_{\rm eff}(t)}
{\mu[T_g(t)]L_d^2}. \tag{3}
\]

A fitted Arrhenius multiplier for k_h would confound changes in viscosity, permeability and modulus, and should not replace their separate measurements.

## 3. Exact piecewise-constant propagator

On a segment of duration Δt with constants k_n,k_h, starting state (q_i,S_i), and fixed q_infinity,eta_a, put

\[
e_n=e^{-k_n\Delta t},\quad e_h=e^{-k_h\Delta t},\quad
\delta=k_h-k_n.
\]

Then

\[
q_{i+1}=q_\infty+(q_i-q_\infty)e_n, \tag{4}
\]

and, for delta not equal to zero,

\[
S_{i+1}=\eta_aq_\infty+(S_i-\eta_aq_\infty)e_h
+\eta_ak_h(q_i-q_\infty)
\frac{e_n-e_h}{\delta}. \tag{5}
\]

For equal rates k_n=k_h=k, the continuous limit is

\[
S_{i+1}=\eta_aq_\infty+
[S_i-\eta_aq_\infty+\eta_ak(q_i-q_\infty)\Delta t]e^{-k\Delta t}. \tag{6}
\]

The implementation evaluates the divided difference with a numerically stable exponential difference near equal rates. Any finite sequence of such segments is composed exactly, up to floating-point arithmetic.

If the initial data satisfy 0≤S_0≤eta_a q_0≤eta_a q_infinity<1, then each positive-rate segment preserves

\[
0\le S(t)\le\eta_aq(t)\le\eta_aq_\infty,\qquad \dot S\ge0.
\]

The proof from v0.2 applies on each segment; continuity of q,S at switches makes the invariant region hold for the complete piecewise history. This also proves monotonicity across switches as long as q_infinity and eta_a remain fixed and both rates remain positive.

## 4. What the implementation does — and does not do

- ccfsm_thermal_history.py provides an Arrhenius rate helper (with user-supplied activation energy), an exact constant-rate segment update, and a piecewise-constant rate-history propagator.
- Rates are inputs evaluated at the gel's actual internal temperature, and can differ on each segment. The module does not assume bath temperature equals gel temperature.
- The module does not estimate activation energy, silica permeability, modulus, sample thermal time constant or the sample's actual temperature trajectory.
- It holds q_infinity and eta_a fixed during one schedule. Different experimental protocols may have different fitted endpoint combinations. An evolving endpoint, reversible stress relaxation, shear accommodation, or a non-monotone response requires an added internal state and matched rheological/structural evidence; it is not smuggled into this exact rate-switch model.

## 5. Verification

Seven new regression tests cover: recovery of the v0.2 exact solution for one segment; semigroup consistency under splitting; distinct response to a staged rate history; invariant-region preservation under 20 successive rate segments; equal-rate limit; Arrhenius reference/temperature direction; zero-duration and invalid-input handling.

Local test run on 14 November 2026: **7/7 tests passed**. The dedicated CCFSM workflow automatically runs all test files in this folder matching test_*.py. Software verification is not physical validation.

## 6. Research implications

1. Refit the droplet curves only after recovering the true time origin, exact 20-min preparation interval and actual sample temperature history.
2. If internal sample temperature was not measured, treat thermal lag as an uncertain nuisance parameter or measure it in a matched non-reactive/representative droplet. Do not assume instantaneous heating.
3. Keep acid and base rate laws separate. The paper reports different chemistry/topology and different temperature response.
4. Do not fit E_n from nominal bath temperature alone while q_infinity, eta_a, k_h, initial age and temperature lag are unresolved.
5. A discriminating natural-syneresis experiment should log gel-core temperature, pH, expelled-fluid mass, free volume and one structural ageing observable simultaneously.

## Source provenance

Wilhelm, S.; Kind, M. (2015). “Influence of pH, Temperature and Sample Size on Natural and Enforced Syneresis of Precipitated Silica.” *Polymers* 7(12), 2504–2521. DOI: https://doi.org/10.3390/polym7121528. Natural droplet protocol §3.2 and discussion of Figure 10 / Table 2; temperature and endpoint discussion §§2.3–2.4 and §4.1.

**Boundary:** this is a protocol-aware mathematical extension for natural syneresis, not evidence that its unknown rates or endpoints have been fitted to the published curves.
