# CCFSM v0.2 — two-timescale closure for natural syneresis

**Date:** 14 November 2026  
**Scope:** natural, mechanically unloaded syneresis of precipitated aqueous silica gels only  
**Status:** exact reduced model; analytical properties proved; implementation tested; kinetic coefficients not yet identified from target-system data

## 1. Motivation and scope

CCFSM v0.1 represented an individual natural-syneresis curve by
\[
S(t)=A[1-\exp(-t/\tau)].
\]
This is a useful empirical fit but folds distinct mechanisms into one apparent time constant.

Wilhelm and Kind describe continuing post-gel siloxane-bond formation as a source of network contraction and pressure difference, followed by pore-liquid expulsion; they also report progressive network stiffening. Their paper distinguishes natural syneresis from the additional external pressure used in forced syneresis. Scherer's natural-syneresis theory independently shows that sample size, permeability and viscoelastic response affect the rate and curve shape. The Scherer system is a mechanistic comparator, not a source of numerical coefficients for precipitated sodium-silicate/sulfuric-acid gels. Wu et al. motivate an interface-accessibility term in colloidal gels, but their material is not a silica-specific coefficient source.

CCFSM v0.2 separates:
1. generation of an intrinsic, stress-free network contraction potential; and
2. the hydraulic/poroelastic response by which that potential becomes observed bulk shrinkage.

No oedometer, applied-plunger-pressure, filtration-cake or forced-syneresis coefficient is used. No external compressive load appears in the model.

## 2. State variables and parameters

- \(q(t)\in[0,1)\): intrinsic network contraction potential. It is the volumetric contraction the network would express in the reference limit of free contraction and complete drainage.
- \(S(t)=\Delta V(t)/V_0\in[0,1)\): observed macroscopic relative volume shrinkage.
- \(\eta_a\in(0,1]\): effective natural-interface accessibility factor. It represents the fraction of intrinsic contraction expressible under the actual gel/container interface and natural boundary conditions. It is not an applied load. \(\eta_a=1\) is the fully accessible limit.
- \(q_\infty\in[0,1)\): asymptotic intrinsic contraction potential for a fixed formulation, ageing history and temperature protocol.
- \(k_n>0\) [h\(^{-1}\)]: effective network-contraction generation rate. It lumps post-gel chemistry and structural reorganisation; it is not an elementary Si–O–Si reaction constant.
- \(k_h>0\) [h\(^{-1}\)]: effective hydraulic/poroelastic relaxation rate.

The observation clock must be declared. The network may already have aged between gel point and the beginning of the recorded syneresis experiment, so \(q(0)\) need not be zero.

For a monotone natural-syneresis trajectory, admissible initial data satisfy
\[
0\le S_0\le\eta_aq_0\le\eta_aq_\infty<1,
\qquad k_n,k_h>0. \tag{1}
\]

## 3. Two-timescale constitutive closure

The reduced network-evolution equation is
\[
\boxed{\dot q=k_n(q_\infty-q).} \tag{2}
\]

The observed natural-syneresis response is
\[
\boxed{\dot S=k_h(\eta_a q-S).} \tag{3}
\]

Equation (3) relaxes the observed bulk volume toward the currently accessible contraction potential; it does not impose mechanical compression. Both the driving potential and the observed volume are internal state variables.

The closure is intentionally low order. If matched experiments show a broad relaxation spectrum, non-monotone response, strong ageing of coefficients or multiple drainage domains, it must be replaced by a distributed poro-viscoelastic or finite-strain field model.

### 3.1 Exact solution

Equation (2) gives
\[
q(t)=q_\infty+(q_0-q_\infty)e^{-k_nt}. \tag{4}
\]

For \(k_h\ne k_n\), the exact solution of (3) is
\[
S(t)=\eta_aq_\infty+(S_0-\eta_aq_\infty)e^{-k_ht}
+\frac{\eta_ak_h(q_0-q_\infty)}{k_h-k_n}
(e^{-k_nt}-e^{-k_ht}). \tag{5}
\]

For equal rates \(k_h=k_n=k\), the continuous limiting solution is
\[
S(t)=\eta_aq_\infty+
[S_0-\eta_aq_\infty+\eta_ak(q_0-q_\infty)t]e^{-kt}. \tag{6}
\]

For a fresh zero-state start \(q_0=S_0=0\),
\[
S(t)=\eta_aq_\infty\left[
1-\frac{k_he^{-k_nt}-k_ne^{-k_ht}}{k_h-k_n}
\right]. \tag{7}
\]

A notable consequence of (7) is \(\dot S(0)=0\). A measured nonzero apparent initial slope can be consistent with a network that had already matured before the observation clock started (\(q_0>S_0/\eta_a\)), or with an unresolved fast initial stage. The time origin must be recorded rather than silently adjusted.

## 4. Mathematical propositions

### Proposition 1 — global existence and uniqueness

For constant \(q_\infty,k_n,k_h,\eta_a\) satisfying (1), equations (2)–(3) have a unique solution for every \(t\ge0\).

**Proof.** The vector field
\[
F(q,S)=(k_n(q_\infty-q),\,k_h(\eta_aq-S))
\]
is affine and globally Lipschitz in \((q,S)\). Picard–Lindelöf therefore gives a unique local solution; global Lipschitz continuity and the explicit bounded solution (4)–(6) extend it to all non-negative times. \(\square\)

### Proposition 2 — invariant region, positivity and monotonicity

Under (1), for all \(t\ge0\),
\[
0\le S_0\le S(t)\le\eta_aq(t)\le\eta_aq_\infty<1,
\quad \dot S(t)\ge0,
\quad \lim_{t\to\infty}S(t)=\eta_aq_\infty. \tag{8}
\]

**Proof.** Put \(d(t)=\eta_aq(t)-S(t)\). From (2)–(3),
\[
\dot d=\eta_ak_n(q_\infty-q)-k_hd.
\]
Since \(q(t)\le q_\infty\), variation of constants gives
\[
d(t)=d(0)e^{-k_ht}
+\eta_ak_n\int_0^t e^{-k_h(t-r)}[q_\infty-q(r)]\,dr\ge0.
\]
Thus \(\dot S=k_hd\ge0\) and \(S\le\eta_aq\). Equation (4) gives \(q_0\le q(t)\le q_\infty\), so the upper bound and convergence follow. The lower bound follows from \(S(0)\ge0\) and monotonicity. \(\square\)

### Proposition 3 — non-identifiability of the physical rate labels

For a zero-state start \(q_0=S_0=0\), the Laplace transform of the observed response is
\[
\mathcal L\{S\}(s)=
\frac{\eta_aq_\infty k_nk_h}
{s(s+k_n)(s+k_h)}. \tag{9}
\]
It is invariant under exchanging \(k_n\) and \(k_h\). Therefore, an ideal noise-free \(S(t)\) curve alone cannot tell which recovered rate is the network rate and which is the hydraulic rate.

**Proof.** The transform of \(q(t)\), for \(q_0=0\), is \(Q(s)=q_\infty k_n/[s(s+k_n)]\). The hydraulic response gives \(S(s)=\eta_ak_hQ(s)/(s+k_h)\), yielding (9), which is symmetric in the two rates. \(\square\)

In this ideal case, a curve can at best recover the unordered pair through \(k_n+k_h\) and \(k_nk_h\), alongside the endpoint product \(\eta_aq_\infty\). It cannot separate \(q_\infty\) from \(\eta_a\). Independent structural/chemical or hydraulic measurements are required to assign the physical labels.

### Proposition 4 — relation to the single-exponential empirical law

If \(k_n\gg k_h\), network evolution is fast relative to drainage and, after the initial network transient,
\[
S(t)\approx \eta_aq_\infty(1-e^{-k_ht}).
\]
If \(k_h\gg k_n\), hydraulic relaxation is fast and
\[
S(t)\approx \eta_aq_\infty(1-e^{-k_nt}).
\]
Thus the empirical time constant approximates the slower process only in these separated-timescale limits:
\[
\tau_{\rm app}\approx\frac{1}{\min(k_n,k_h)}. \tag{10}
\]
When \(k_n\) and \(k_h\) are comparable, the response is genuinely two-stage and is not exactly a single exponential.

## 5. Hydraulic interpretation and scale prediction

For a homogeneous, saturated, first-mode poroelastic reduction,
\[
\boxed{k_h\simeq
\frac{C_g\,\kappa_{\rm eff}K_{\rm eff}}
{\mu L_d^2}.} \tag{11}
\]
Here \(\kappa_{\rm eff}\) is intrinsic permeability [m²], \(K_{\rm eff}\) the appropriate effective poroelastic modulus [Pa], \(\mu\) pore-liquid viscosity [Pa·s], \(L_d\) the actual hydraulic drainage length [m], and \(C_g>0\) a dimensionless geometry/eigenvalue factor. The right-hand side has units s\(^{-1}\); multiply by 3600 to obtain h\(^{-1}\).

Equation (11) is a scaling closure, not a way to infer permeability from shrinkage alone. \(K_{\rm eff}\) is not automatically interchangeable with an oscillatory storage modulus \(G'\), and viscoelastic memory may require more than one hydraulic rate.

A decisive size experiment holds formulation, age, temperature history, shape family and natural interface treatment fixed while changing only drainage length. Equation (11) predicts \(k_h\propto L_d^{-2}\), while \(k_n\) has no such geometric scaling in this lumped description. Hence \(\tau_h\propto L_d^2\) is falsifiable. It should not be inferred from the existing cylinder-versus-droplet contrast alone, because geometry, interfaces, protocols and temperature histories differ.

## 6. Chemical/fractal coupling upstream of q

A molecularly interpretable hypothesis introduces \(B(t)\), the density of newly formed load-bearing siloxane bridges [mol m\(^{-3}\)]:
\[
\dot B=r_b(T,\mathrm{pH},I,c_{\rm Si,aq},
c_{\rm acid},c_{\rm base},\ldots), \tag{12}
\]
\[
\chi_{\rm nat}=\Omega_b[B(t)-B_0],
\qquad q=1-e^{-\chi_{\rm nat}}. \tag{13}
\]
\(\Omega_b\) [m³ mol\(^{-1}\)] is an **effective network-level** contraction volume per bridge. It includes topology, elasticity and stress redistribution; it is not the bare molecular volume difference of one bond. Equation (13) is a hypothesis to test, not a fitted law.

The first-order closure (2) is a coarse-grained approximation to the chemistry/structure subsystem. A future model may replace it by coupled evolution of \(B,D_f,z\), for example
\[
\dot D_f=k_D(D_{f,\rm eq}-D_f),\qquad
\dot z=k_z(z_{\rm eq}-z),
\]
with \(r_b,D_{f,\rm eq},z_{\rm eq},\Omega_b\) constrained by matched measurements. No sign or monotone mapping from \(D_f\) alone to bulk contraction is assumed: equal fractal dimensions do not imply equal contact topology, pore connectivity, stiffness or permeability.

Acid- and base-catalysed routes must remain separate chemical branches. Wilhelm and Kind describe different network topologies and strong pH dependence of silicic-acid solubility. pH, recipe concentrations and ionic strength must be handled through a chemically consistent state/recipe model rather than treated as independent redundant regressors.

## 7. Finite-strain kinematics and silicon balance

For isotropic homogeneous intrinsic contraction potential \(q\), define
\[
J_{\rm nat}=1-q,\qquad
\mathbf F_{\rm nat}=(1-q)^{1/3}\mathbf I,\qquad
\det\mathbf F_{\rm nat}=1-q. \tag{14}
\]
This is an exact finite volumetric kinematic relation. The logarithmic contraction is
\[
\chi_{\rm nat}=-\ln(1-q). \tag{15}
\]
The observed volume ratio \(1-S\) equals \(J_{\rm nat}\) only in the fully accessible, fully drained limit (\(\eta_a=1\), \(S\to q\)); it must not be imposed during transient drainage.

A mass-balance caveat is important: the v0.1 relation \(\phi_s=\phi_{s0}/(1-S)\) is valid only when the volume of already condensed silica solid is conserved. During continuing polymerisation, dissolved silicic acid can become network-bound silica. A complete silicon balance must therefore distinguish dissolved silicon, network-bound silicon and silicon expelled in pore liquid; the simple solid-fraction identity is not universal during ongoing reaction.

## 8. Empirical status and parameter identifiability

The current repository contains twelve source-reported natural-syneresis \((A,\tau)\) pairs from Wilhelm and Kind (2015), Tables 1–2, and seven provenance-labelled figure-derived exploratory refits. These remain separate from the conflicting basic-droplet values reported in Wilhelm's 2017 dissertation. The digitized values are not author-supplied raw data and have not been pixel-calibrated or independently marker-verified.

For v0.2,
\[
A_{\rm obs}=\eta_aq_\infty
\]
is an endpoint combination and \(\tau_{\rm app}\) is a one-rate summary in the separated-timescale limit. Current data do **not** independently identify numerical values of \(q_\infty,\eta_a,k_n,k_h,\Omega_b\), nor the chemistry/fractal constitutive coefficients. No new two-rate fit is made from approximate digitization: doing so would create false precision and would not resolve the rate-label symmetry in (9).

## 9. Minimum experiment to identify the two processes

For the same precipitation batch and declared post-gel observation clock, measure:

1. freely deforming \(S(t)\) and expelled-liquid volume/mass, with actual drainage surfaces and natural container interface documented;
2. a structural contraction proxy \(q(t)\), or a calibrated bridge-formation proxy \(B(t)\), on matched specimens;
3. intrinsic permeability \(\kappa(t)\), using a sufficiently small diagnostic gradient and correcting for external hydraulic resistance;
4. the appropriate wet-gel poroelastic modulus/viscoelastic spectrum and pore-liquid viscosity;
5. pH(t), temperature(t), ionic strength, dissolved and expelled silicon, recipe and ageing history;
6. at least two independently controlled drainage lengths with otherwise matched geometry and interface treatment.

With \(q(t)\) independently measured, equation (2) constrains \(k_n\). With \(\kappa,K_{\rm eff},\mu,L_d\) independently measured, equation (11) constrains \(k_h\). Only then should both rates be tested against \(S(t)\) without re-fitting either rate to that same curve.

## 10. Software verification

- The Python implementation provides the exact two-stage response, stable equal-rate limit, hydraulic-rate scaling, isotropic finite-strain stretch and unordered rate-pair recovery.
- The 12 regression tests cover the zero-state lag, pre-aged initial state, equal/near-equal rates, invariant region, monotonicity, endpoint, rate-swap symmetry, rate recovery, \(L_d^{-2}\) scaling, finite kinematics and invalid inputs.
- Local run on 14 November 2026: **12/12 tests passed** using **python -m unittest -v**.

This is software/analytical verification, not physical validation. The two-timescale model is a reduced hypothesis and a falsifiable bridge to a future finite-strain poro-viscoelastic field model, not a completed universal constitutive law.

## References

- Wilhelm, S.; Kind, M. (2015). “Influence of pH, Temperature and Sample Size on Natural and Enforced Syneresis of Precipitated Silica.” *Polymers* 7(12), 2504–2521. DOI: 10.3390/polym7121528. Especially §§2.1–2.2 and §4.1.
- Scherer, G. W. (1989). “Mechanics of Syneresis I. Theory.” *Journal of Non-Crystalline Solids* 108(1), 18–27. DOI: 10.1016/0022-3093(89)90328-1.
- Scherer, G. W. (1989). “Mechanics of Syneresis II. Experimental Study.” *Journal of Non-Crystalline Solids* 108(1), 28–36. DOI: 10.1016/0022-3093(89)90329-3.
- Wu, Q.; van der Gucht, J.; Kodger, T. E. (2020). “Syneresis of Colloidal Gels: Endogenous Stress and Interfacial Mobility Drive Compaction.” *Physical Review Letters* 125, 208004. DOI: 10.1103/PhysRevLett.125.208004.

**Version boundary:** v0.2 proves and tests the reduced two-timescale equations under stated assumptions. It does not prove that the target precipitated-silica network follows this exact closure or supply fitted kinetic constants that current evidence cannot identify.
