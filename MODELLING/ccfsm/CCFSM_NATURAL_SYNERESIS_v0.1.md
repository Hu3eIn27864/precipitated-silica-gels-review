# Chemically Coupled Fractal Syneresis Model (CCFSM)
## Version 0.1 — natural syneresis only
**Date:** 14 November 2026  
**Status:** mathematically specified reduced model; partial empirical parameterisation; full chemical–structural identification pending

## 1. Scope and scientific claim

CCFSM describes the **natural, mechanically unloaded syneresis of precipitated aqueous silica gels**. The system is allowed to contract under its own evolving network stresses and to expel pore liquid subject to the actual hydraulic boundary conditions.

The following are outside the calibration set and must not be used as natural-syneresis observations:

- oedometer compression, externally applied plunger pressure, or any mechanically enforced consolidation;
- forced syneresis and pressure-assisted drainage;
- consolidation parameters fitted under an imposed external load;
- filtration-cake permeability unless transfer to the same wet-gel state is independently demonstrated.

The model has two distinct levels:

1. a chemical–structural state model for post-gel network maturation;
2. a natural poromechanical/hydraulic response model for free shrinkage and pore-liquid transport.

The current data support sample-specific effective shrinkage amplitudes and time constants. They do **not** yet identify all chemical, fractal, elastic, or hydraulic coefficients separately. CCFSM v0.1 therefore reports fitted coefficients where available and explicitly marks the remaining parameters as unidentified. It is not presented as a fully predictive, experimentally validated constitutive law.

## 2. State variables and process inputs

For a spatial point \(x\) and time \(t\), define

\[
\mathbf y(x,t)=
\left(\alpha,D_f,z,\chi,p,\mathbf u\right).
\]

- \(\alpha\in[0,1]\): dimensionless post-gel chemical/network maturation variable. It is a coarse-grained progress variable, not a claim that one elementary reaction controls the whole process.
- \(D_f\in[1,3]\): mass-fractal dimension estimated over a declared length-scale interval.
- \(z>0\): mean number of load-bearing particle contacts per primary particle or structural unit. The counting convention must be held fixed.
- \(\chi\geq0\): natural contractile eigenstrain potential; in the small-strain formulation its trace is the stress-free volumetric contraction.
- \(p\): pore-liquid pressure relative to the external liquid/reservoir pressure.
- \(\mathbf u\): displacement field.

The process input is

\[
\mathbf q(t)=
\big(T,\mathrm{pH},I,c_{\rm Si},c_{\rm acid},c_{\rm base},
\text{mixing/ageing history}\big).
\]

Temperature in Arrhenius laws is in kelvin. pH and acid/base concentrations are not independent arbitrary regressors: pH follows from the recipe, neutralisation, buffering and time. In a fitted model, either measured pH(t) is used together with a chemically consistent recipe description, or a speciation/material-balance model predicts pH(t). The same chemical information must not be counted twice.

The clock origin must be declared for every experiment: mixing start, gel point, or start of the natural-syneresis observation. CCFSM uses the **start of the natural-syneresis observation after gel formation** for the empirical shrinkage law. A separate gelation model may predict the preceding induction/gel time.

## 3. Chemical and structural evolution

### 3.1 Chemical maturation

A candidate reduced kinetic law is

\[
\dot\alpha =
k_{\alpha,0}
\exp\!\left(-\frac{E_\alpha}{RT}\right)
f_{\rm pH}^{\rm branch}(\mathrm{pH},\mathrm{pH}_{\rm iso})
f_I(I)
f_c(c_{\rm Si},c_{\rm acid},c_{\rm base})
(1-\alpha)^m ,
\tag{1}
\]

with \(k_{\alpha,0}>0\), \(E_\alpha\geq0\), \(m>0\), and non-negative dimensionless modifier functions. The pH response is branch-specific: acid-catalysed and base-catalysed condensation are not constrained to share one symmetric function. Wilhelm and Kind report an isoelectric point near pH 1.7–2, acid-catalysed conditions below it (their experiment pH < 0) and base-catalysed conditions above it (their experiment pH approximately 10); their mechanistic discussion distinguishes the resulting network structures. This supports separate functions \(f_{\rm pH}^{\rm acid}\) and \(f_{\rm pH}^{\rm base}\), but does not numerically identify their exponents or amplitudes. This is a model class, not an empirically established post-gel reaction law. Its coefficient values are **not identified** by the present shrinkage curves.

If temperature or pH changes during the experiment, equation (1) must use their measured time histories. A constant-temperature fit must not be silently applied through a temperature ramp.

### 3.2 Fractal and contact-network evolution

A minimal relaxation closure is

\[
\dot D_f =
k_D(\mathbf q,\alpha)\,[D_{f,\mathrm{eq}}(\alpha,\mathbf q)-D_f],
\tag{2}
\]

\[
\dot z =
k_z(\mathbf q,\alpha,D_f)\,[z_{\mathrm{eq}}(\alpha,D_f,\mathbf q)-z].
\tag{3}
\]

Here \(k_D,k_z>0\), \(D_{f,\mathrm{eq}}\in[1,3]\), and \(z_{\mathrm{eq}}>0\). The target functions may be replaced by a population-balance or particle-level model if direct structural data justify it.

For a declared scale interval, the mass-fractal fit is

\[
N(r)=k_f\left(\frac r a\right)^{D_f},
\qquad
D_f=\frac{d\ln N}{d\ln(r/a)}.
\tag{4}
\]

The primary-particle scale \(a\), prefactor \(k_f\), fitting interval, and whether the measured object is an aggregate or the spanning gel network must be reported. A single value of \(D_f\) is not sufficient to specify contact topology, pore connectivity, elastic stiffness, or permeability.

**Important non-equivalence:** a change in the radius of gyration of one simulated cluster is not, by itself, a measurement of bulk gel-volume shrinkage. A structural-to-bulk mapping must be established on matched states.

### 3.3 Network-generated natural contraction

The coupling to mechanics is represented by a constitutive map

\[
\chi=\mathcal X_\theta(\alpha,D_f,z,\mathbf q),
\qquad
\dot\chi\geq0
\quad\text{along a natural-syneresis trajectory}.
\tag{5}
\]

The parameter vector \(\theta\) is to be identified from **matched chemical, structural and free-shrinkage measurements**. Equation (5) deliberately does not assign positive coefficients to \(D_f\) or \(z\) in advance: the direction and strength of each contribution must be measured. In particular, the model does not assume that increasing \(D_f\) uniquely or monotonically determines macroscopic contraction.

For small-strain poromechanics the corresponding isotropic eigenstrain is

\[
\boldsymbol\epsilon^{\rm nat}
=-\frac{\chi}{3}\mathbf I.
\tag{6}
\]

This is a local linearized constitutive representation. The observed relative volume decreases can reach several tenths, so this small-strain PDE is a mechanistic verification level, not yet a quantitatively adequate finite-deformation model for the largest-shrinkage experiments. A finite-strain implementation should replace (6) by a multiplicative natural deformation, for example
\(\mathbf F_{\rm nat}=\exp(-\chi/3)\mathbf I\), with a finite-strain fluid-content law derived consistently from the chosen free energy.

## 4. Natural poromechanical and hydraulic subsystem

For the linearized, quasi-static verification problem, let

\[
\boldsymbol\epsilon(\mathbf u)
=\tfrac12(\nabla\mathbf u+\nabla\mathbf u^{T}),
\]

\[
\boldsymbol\sigma
=\mathbb C:
  \big(\boldsymbol\epsilon(\mathbf u)
       -\boldsymbol\epsilon^{\rm nat}\big)
  -b\,p\,\mathbf I ,
\tag{7}
\]

\[
\nabla\cdot\boldsymbol\sigma=0,
\tag{8}
\]

\[
\zeta=b\,\nabla\cdot\mathbf u+\frac pM,
\qquad
\partial_t\zeta+\nabla\cdot\mathbf q=0,
\tag{9}
\]

\[
\mathbf q=-\frac{k}{\mu(T,\mathbf q_{\rm chem})}\nabla p.
\tag{10}
\]

Here \(\mathbb C\) is a positive-definite drained skeleton elasticity tensor, \(b\) is the Biot coupling coefficient, \(M>0\) is the storage modulus, \(k>0\) is intrinsic permeability in m², and \(\mu>0\) is pore-liquid dynamic viscosity in Pa·s. The symbol \(\zeta\) denotes fluid-content change per reference volume. Coefficients may depend on \((\alpha,D_f,z,\phi,T)\), but evolving or discontinuous coefficients should be introduced only after constant-coefficient verification and matched-state evidence.

### 4.1 Boundary conditions: no imposed syneresis load

Mechanical boundary condition for a freely deforming surface:

\[
\boldsymbol\sigma\mathbf n=\mathbf 0.
\tag{11}
\]

This is a zero-applied-traction condition, not an oedometer condition. If a sample touches a wall, the actual wall-contact constraint must be specified; it must not be replaced by an invented axial load.

Hydraulic conditions depend on the experiment:

- drained gel/liquid interface: \(p=p_{\rm ext}\), with gauge pressure \(p=0\);
- impermeable wall: \(\mathbf q\cdot\mathbf n=0\);
- closed collection cell with finite external liquid volume: couple the boundary flux to an external reservoir balance rather than assuming an infinite-pressure sink.

The boundary condition is part of the model. It cannot be inferred from sample diameter alone.

### 4.2 Reduced hydraulic time scale

For a homogeneous linear poroelastic body, a first-mode reduction gives the characteristic scale

\[
\tau_h \simeq
\frac{\mu L_c^2}{C_g\,k_{\rm eff}K_{\rm eff}},
\tag{12}
\]

where \(L_c\) is the actual drainage length, \(C_g>0\) is a dimensionless geometry/eigenvalue factor under the chosen definition of \(L_c\), and \(K_{\rm eff}\) is the relevant constrained/drained skeleton modulus for that reduction. The units are seconds:
\((\mathrm{Pa\,s})\,\mathrm m^2/(\mathrm m^2\,\mathrm{Pa})=\mathrm s\).

Equation (12) is a reduced scaling relation, not a parameter fit. One measured \(\tau\) identifies at most the combination \(C_g k_{\rm eff}K_{\rm eff}/(\mu L_c^2)\). It does not separately identify permeability, modulus, or geometry factor. Nor may \(\tau\) be equated directly with an intrinsic permeability or with an oedometer \(t_{90}\).

## 5. Empirical natural-syneresis closure

For one fixed formulation, sample geometry, boundary condition and temperature history, the presently supported reduced observation law is

\[
S(t)=\frac{\Delta V(t)}{V_0}
=A\left[1-\exp\left(-\frac t\tau\right)\right],
\tag{13}
\]

equivalently,

\[
\dot S=\frac{A-S}{\tau},
\qquad S(0)=0.
\tag{14}
\]

The empirical coefficients have unambiguous units:

- \(A\): dimensionless final relative volume shrinkage;
- \(\tau\): hours in the tabulated fits;
- \(\lambda_{\rm app}=1/\tau\): h\(^{-1}\), apparent relaxation rate;
- \(v_0=A/\tau\): h\(^{-1}\), initial relative-shrinkage rate.

The CCFSM interpretation is that \(A\) is an effective measure of the total contractile response accessible under the specified natural boundary conditions, while \(\tau\) is an effective coupled network/poroelastic relaxation time. Neither parameter is a fundamental material constant independent of geometry and history.

For a state-dependent extension,

\[
\dot S=\lambda_h(\alpha,D_f,z,\phi,T,L_c)
       \,[A_{\rm eq}(\chi,\phi_0,\text{geometry, BC})-S],
\tag{15}
\]

where \(\lambda_h>0\), \(0\leq A_{\rm eq}\leq A_{\max}<1\), and \(A_{\rm eq}\) maps the natural contractile potential to the accessible bulk shrinkage under the specified geometry and hydraulic boundary condition. The reduced hydraulic rate is constrained by \(\lambda_h\simeq C_g k_{\rm eff}K_{\rm eff}/(\mu L_c^2)\). Equation (13) follows exactly when \(A_{\rm eq}=A\) and \(\lambda_h=1/\tau\) are constant from the defined observation start. If chemistry or structure continues to evolve appreciably, a single exponential is only an effective approximation and equation (15), or the spatial system (7)–(10), must be fitted to richer measurements.

## 6. Empirical coefficients recovered from the repository

There are two separate empirical layers. First, the article reports fitted natural-syneresis coefficients in Tables 1 and 2. These are reproduced below as source-reported values, not refitted raw data. The formulation used sodium silicate solution with mass fraction 0.40 and sulfuric acid mass fractions 0.50 (acidic condition, pH < 0) or 0.032 (basic condition, pH approximately 10). The paper gives pH categories relative to its isoelectric point (approximately 1.7–2), not a continuous pH-response data set.

### 6.1. Source-reported natural-syneresis coefficients

| Geometry | Catalyst | T (°C) | A (source table) | τ (h) | 1/τ (h⁻¹) | A/τ (h⁻¹) |
|---|---|---:|---:|---:|---:|---:|
| cylinder | acidic | 20 | 0.20 | 21.3 | 0.04695 | 0.00939 |
| cylinder | acidic | 40 | 0.20 | 11.7 | 0.08547 | 0.01709 |
| cylinder | acidic | 60 | 0.20 | 5.0 | 0.20000 | 0.04000 |
| cylinder | basic | 20 | 0.30 | 50.1 | 0.01996 | 0.00599 |
| cylinder | basic | 40 | 0.39 | 32.0 | 0.03125 | 0.01219 |
| cylinder | basic | 60 | 0.51 | 27.5 | 0.03636 | 0.01855 |
| droplet | acidic | 20 | 0.37 | 0.40 | 2.50000 | 0.92500 |
| droplet | acidic | 40 | 0.41 | 0.64 | 1.56250 | 0.64063 |
| droplet | acidic | 60 | 0.48 | 0.77 | 1.29870 | 0.62338 |
| droplet | basic | 20 | 0.30 | 0.67 | 1.49254 | 0.44776 |
| droplet | basic | 40 | 0.39 | 0.57 | 1.75439 | 0.68421 |
| droplet | basic | 60 | 0.51 | 0.95 | 1.05263 | 0.53684 |

These are natural-syneresis conditions only. No imposed pressure or oedometer coefficients enter this table. The basic-droplet row set is retained as **source-reported Table 2 evidence**, but not used as a primary digitized calibration because the 2017 dissertation gives a conflicting basic-droplet parameter set. Figure/table and dissertation conflict remain an explicit audit item. The droplet protocol also holds the samples at 20 °C initially, then applies the target temperature; the thermal history is therefore not equivalent to an instantaneous isothermal start.

The table shows that temperature responses depend on both catalyst branch and geometry. For the acid-catalysed cylinder, the reported amplitude A = 0.20 remains constant while tau falls from 21.3 to 5.0 h. The acid-catalysed droplet instead has increasing amplitude and increasing reported tau. A single Arrhenius coefficient fitted across these unlike geometries would be scientifically unjustified.

### 6.2. Project's digitized primary re-fits

The next table reproduces the current curated primary fits in
LITERATURE/wilhelm_kind_curated_primary_fits_2026-11-14.csv.
The fits use 98 AI-assisted approximate chart readings in seven series, from Figures 8a, 8b and 10a of Wilhelm & Kind (2015). They are not author-supplied raw data, were not pixel-calibrated, and have no pointwise uncertainty estimates. No inferential confidence intervals or significance tests are justified.

| Series | Geometry | Catalyst | T (°C) | n | A (fit) | A (paper) | τ (fit, h) | τ (paper, h) | RMSE | 1/τ (h⁻¹) | A/τ (h⁻¹) |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Fig. 8a | cylinder | acidic | 20 | 13 | 0.186976 | 0.20 | 11.116871 | 21.3 | 0.010370 | 0.08995 | 0.01682 |
| Fig. 8b | cylinder | basic | 20 | 11 | 0.284690 | 0.30 | 41.279528 | 50.1 | 0.021322 | 0.02423 | 0.00690 |
| Fig. 8b | cylinder | basic | 40 | 9 | 0.358679 | 0.39 | 24.827435 | 32.0 | 0.010835 | 0.04028 | 0.01445 |
| Fig. 8b | cylinder | basic | 60 | 10 | 0.491525 | 0.51 | 24.904800 | 27.5 | 0.029766 | 0.04015 | 0.01974 |
| Fig. 10a | droplet | acidic | 20 | 15 | 0.369139 | 0.37 | 0.523974 | 0.40 | 0.013396 | 1.90849 | 0.70450 |
| Fig. 10a | droplet | acidic | 40 | 19 | 0.426341 | 0.41 | 0.696416 | 0.64 | 0.031990 | 1.43592 | 0.61219 |
| Fig. 10a | droplet | acidic | 60 | 21 | 0.471044 | 0.48 | 0.620095 | 0.77 | 0.025905 | 1.61266 | 0.75963 |

The distinction between 4 cylinder series and 3 acidic-droplet series is intentional. The two omitted acidic-cylinder series at 40/60 °C remain sensitivity-only. The 3 basic-droplet series from Figure 10b remain excluded from the primary calibration because the figure/table and dissertation evidence require a separately audited conflict branch.

### 6.3 What these numbers do and do not show

1. The amplitudes are broadly close to the published table values, but this is an internal digitization cross-check, not independent experimental validation.
2. Time constants differ noticeably between digitized refits and published table entries. Figure 8a acidic cylinder at 20 °C is the largest discrepancy in this primary set.
3. Figure 10a droplet residuals show positive lag-1 structure (approximately 0.45–0.78 in the existing diagnostics). A one-exponential fit therefore does not fully describe all visible temporal structure.
4. Geometry changes the observed time scale dramatically. Cylinder and droplet time constants must never be pooled into one universal coefficient.
5. These primary data provide only one acidic-cylinder temperature, three basic-cylinder temperatures and three acidic-droplet temperatures. No continuous pH series, ionic-strength series, or matched \(D_f,z,k,K\) measurements exist in this fit table.

### 6.4 Parameter identification status

| Parameter | Meaning | Current status |
|---|---|---|
| \(A\) | sample-specific limiting relative shrinkage | empirically fitted per listed series; approximate digitized evidence |
| \(\tau\) | sample-specific effective time constant | empirically fitted per listed series; approximate digitized evidence |
| \(1/\tau\), \(A/\tau\) | apparent rate and initial slope | derived exactly from the two fitted coefficients |
| \(k_{\alpha,0},E_\alpha,m,f_{\rm pH},f_I,f_c\) | chemical maturation kinetics | not identified by shrinkage-only curves |
| \(k_D,D_{f,\rm eq},k_z,z_{\rm eq}\) | fractal/contact-network kinetics | not identified; matched structural time series required |
| \(\theta\) in \(\mathcal X_\theta\) | structural-to-contractile eigenstrain map | not identified |
| \(k_{\rm eff},K_{\rm eff},C_g\) | transport/mechanical factors in (12) | not separately identifiable from one \(\tau\); matched independent observations required |
| \(b,M,\mathbb C\) | poroelastic storage/coupling/stiffness | require independent mechanical/fluid-content measurements on matched unloaded gel states |

No numerical values are assigned to the unidentified parameters. Doing so would create false precision.

## 7. Mathematical results

### Proposition 1 — invariant chemical and structural state ranges

Assume \(k_\alpha(t)\geq0\), \(m\geq1\), and \(\alpha(0)\in[0,1]\) in (1), with the kinetic factor interpreted as the saturated extension \((1-\alpha)_+^m\) outside the physical interval. Then \(\alpha(t)\in[0,1]\) for all later times for which the solution exists.

If \(k_D>0\), \(D_{f,\rm eq}(t)\in[1,3]\), and \(D_f(0)\in[1,3]\), then (2) preserves \(D_f(t)\in[1,3]\). If \(k_z>0\), \(z_{\rm eq}(t)>0\), and \(z(0)>0\), then (3) preserves \(z(t)>0\).

**Proof.** At \(\alpha=0\), the vector field in (1) is non-negative; at \(\alpha=1\), the saturated vector field is zero. Since \(m\geq1\), the extended scalar vector field is locally Lipschitz at \(\alpha=1\); uniqueness prevents a solution starting in the interval from crossing its endpoints. For (2), the variation-of-constants solution is a convexly weighted combination of the initial value and past equilibrium values:
\[
D_f(t)=e^{-\int_0^t k_D}\,D_f(0)
+\int_0^t e^{-\int_s^t k_D}\,k_D(s)D_{f,\rm eq}(s)\,ds.
\]
The weights are non-negative and sum to one. Positivity of \(z\) follows from the same representation. \(\square\)

### Proposition 2 — exact reduced response, positivity and upper bound

Let \(A\geq0\), \(\tau>0\), and \(S(0)=0\). Equation (14) has the unique solution (13). For every \(t\geq0\),

\[
0\leq S(t)<A,\qquad
\dot S(t)=\frac A\tau e^{-t/\tau}\geq0,
\qquad
\lim_{t\to\infty}S(t)=A.
\]

**Proof.** The linear ODE has integrating factor \(e^{t/\tau}\). Integration gives (13). Since \(e^{-t/\tau}\in(0,1]\), the bounds follow; differentiation gives the non-negative rate and the limit. \(\square\)

A stronger bound holds for the state-dependent reduced equation (15): if \(\lambda_h(t)>0\), \(A_{\rm eq}(t)\in[0,A_{\max}]\), and \(S(0)\in[0,A_{\max}]\), then \(S(t)\in[0,A_{\max}]\). Its variation-of-constants formula is a non-negative weighted average of \(S(0)\) and values of \(A_{\rm eq}\). If \(A_{\rm eq}\) is non-decreasing and \(S(0)\leq A_{\rm eq}(0)\), then \(S\) is non-decreasing as well.

### Proposition 3 — solid-volume balance under homogeneous shrinkage

If the silica solid volume is conserved, there is no solid mass loss, and the whole specimen contracts homogeneously with \(V(t)=V_0[1-S(t)]\), then the solid volume fraction obeys

\[
\phi(t)=\frac{\phi_0}{1-S(t)}.
\tag{16}
\]

**Proof.** Conservation of solid volume gives \(\phi(t)V(t)=\phi_0V_0\). Substituting \(V(t)=V_0[1-S(t)]\) yields (16). The assumptions are essential: spatially heterogeneous deformation, dissolution, solid loss, or a changing solid partial volume require a more complete balance. \(\square\)

### Theorem 4 — fluid balance and energy identity for the linearized natural subsystem

Assume a fixed Lipschitz domain; time-independent \(\mathbb C(x)\) symmetric and uniformly positive definite, time-independent \(M(x)>0\), time-independent Biot coefficient \(b(x)\), and time-independent hydraulic mobility \(k(x)/\mu(x)\geq\kappa_{\min}>0\); sufficiently regular fields; zero applied traction \(\boldsymbol\sigma\mathbf n=0\), and either \(p=0\) on the drained boundary or \(\mathbf q\cdot\mathbf n=0\) on an impermeable boundary. Then equations (7)–(10) satisfy:

**Global fluid balance**
\[
\frac{d}{dt}\int_\Omega\zeta\,dV
=-\int_{\partial\Omega}\mathbf q\cdot\mathbf n\,dA.
\tag{17}
\]

**Energy identity**
\[
\frac{d}{dt}
\int_\Omega
\left[
\frac12(\boldsymbol\epsilon-\boldsymbol\epsilon^{\rm nat})
:\mathbb C:
(\boldsymbol\epsilon-\boldsymbol\epsilon^{\rm nat})
+\frac{p^2}{2M}
\right]dV
+
\int_\Omega\frac{k}{\mu}|\nabla p|^2dV
=
-\int_\Omega
\mathbb C:(\boldsymbol\epsilon-\boldsymbol\epsilon^{\rm nat})
:\dot{\boldsymbol\epsilon}^{\rm nat}\,dV .
\tag{18}
\]

**Proof.** Integrate (9) over \(\Omega\) and apply the divergence theorem to obtain (17). For (18), multiply mechanical equilibrium (8) by \(\dot{\mathbf u}\), integrate by parts, and use zero boundary traction:
\[
\int_\Omega
\mathbb C:(\boldsymbol\epsilon-\boldsymbol\epsilon^{\rm nat})
:\dot{\boldsymbol\epsilon}\,dV
=
\int_\Omega b\,p\,\partial_t(\nabla\cdot\mathbf u)\,dV.
\]
Next multiply the fluid equation in (9) by \(p\), integrate by parts, and use either of the stated hydraulic boundary conditions:
\[
\int_\Omega b\,p\,\partial_t(\nabla\cdot\mathbf u)\,dV
+\frac d{dt}\int_\Omega\frac{p^2}{2M}\,dV
+\int_\Omega\frac{k}{\mu}|\nabla p|^2\,dV=0.
\]
Finally use
\(\dot{\boldsymbol\epsilon}
=\partial_t(\boldsymbol\epsilon-\boldsymbol\epsilon^{\rm nat})
+\dot{\boldsymbol\epsilon}^{\rm nat}\)
and combine the two identities. This gives (18). \(\square\)

If \(\dot{\boldsymbol\epsilon}^{\rm nat}=0\), the stored elastic-plus-fluid energy cannot increase; dissipation is non-negative. During natural syneresis, chemical/network evolution supplies the eigenstrain work on the right-hand side. Equation (17) makes the expelled-liquid balance explicit. Neither identity introduces an externally imposed mechanical load.

For the linearized subsystem with the time-independent coefficients just stated, the energy estimate also gives uniqueness of the weak solution modulo rigid-body motions under the stated coercivity and boundary assumptions. To see this, subtract two solutions with identical data and identical natural eigenstrain. The difference problem has zero eigenstrain forcing; the right-hand side in (18) vanishes, so zero initial energy and non-negative dissipation force zero pressure and zero elastic strain. Existence follows under the standard weak-solution assumptions for linear quasi-static Biot poroelasticity, with the displacement gauge fixed. If coefficients evolve with \(\alpha,D_f,z,\phi\), their time derivatives add terms to the energy balance and (18) must be re-derived; it must not be reused unchanged. This is a mathematical result for the stated linearized subsystem, not proof that the constitutive coefficients represent silica correctly.

## 8. What has actually been established

- The reduced empirical law has an exact mathematical solution and rigorous positivity/boundedness properties.
- The linearized natural poroelastic subsystem obeys global fluid balance and the energy identity above.
- Seven sample-specific empirical pairs \((A,\tau)\) are available from the existing curated digitization.
- The present data do not identify chemical kinetics, fractal/contact kinetics, eigenstrain mapping, permeability and modulus separately.
- No oedometer or forced-syneresis parameter has been used in the natural-syneresis fit table.

What has **not** been established:

- a universal predictive map from pH/concentrations to \(A\) and \(\tau\);
- a measured causal coefficient from \(D_f\) or contact number to free volume shrinkage;
- independently calibrated \(k_{\rm eff}\) and \(K_{\rm eff}\) at matched natural-gel states;
- quantitative finite-strain validation at relative volume shrinkages near 0.3–0.5;
- independent validation on a withheld formulation or specimen geometry.

## 9. Required experiments for full empirical identification

The minimal discriminating dataset should measure, on the same formulation and ageing clock:

1. the full pH(t), temperature(t), recipe and ionic-strength history;
2. free, mechanically unloaded \(S(t)\), including sample geometry and external liquid boundary condition;
3. time-resolved \(D_f(t)\), with declared scattering/imaging length window, and a contact/topology descriptor \(z(t)\);
4. pore-liquid outflow or mass balance, rather than shrinkage alone;
5. independent wet-gel permeability and an appropriate small-strain or finite-strain mechanical modulus on matched states.

At least two specimen drainage lengths are needed to test the \(L_c^2\) scaling; geometry must otherwise be held constant. Calibration and validation formulations/geometries must be separated. A single shrinkage curve cannot independently identify chemical kinetics, structural kinetics, permeability and stiffness.

## 10. Validation and implementation sequence

1. Reproduce the seven current empirical fits from the curated fit CSV; preserve their figure-digitization provenance.
2. Keep basic-droplet Figure 10b and acidic-cylinder 40/60 °C in explicit sensitivity/conflict branches until figure-level review is complete.
3. Verify the scalar solver's exact update, positivity, bounds, semigroup property and solid-volume balance with unit tests.
4. Verify the constant-coefficient poroelastic system against analytical one-dimensional drained/undrained limits and a manufactured solution before evolving coefficients are enabled.
5. Add matched-state structural laws only after \(D_f(t)\) and \(z(t)\) data exist.
6. Move to finite strain before claiming quantitative predictions for large observed shrinkage.
7. Only then perform joint estimation, parameter identifiability analysis, withheld-data validation and uncertainty quantification.

## References and provenance

- Wilhelm, S.; Kind, M. (2015). “Influence of pH, Temperature and Sample Size on Natural and Enforced Syneresis of Precipitated Silica.” *Polymers* 7(12), 2504–2521. DOI: https://doi.org/10.3390/polym7121528. Natural-syneresis Figures 8 and 10, Tables 1 and 2.
- Wilhelm, S. (2017). *Über die Synärese kolloidaler Strukturen am Beispiel von Siliciumdioxid*. KIT dissertation. DOI: https://doi.org/10.5445/KSP/1000073100. Relevant as a source cross-check; Figure 10b basic-droplet/table differences remain a separate source-assessment issue.
- Sahabi, H.; Kind, M. (2011). “Experimentally Justified Model-Like Description of Consolidation of Precipitated Silica.” *Polymers* 3, 2156–2171. DOI: https://doi.org/10.3390/polym3042156. Used as consolidation/particle-model context, not as a direct natural-syneresis calibration.
- Project fit audit: LITERATURE/wilhelm_kind_curated_primary_fit_residual_analysis_2026-11-14.md.
- Project coefficients: LITERATURE/wilhelm_kind_curated_primary_fits_2026-11-14.csv.
- Project fit implementation: MODELLING/transport_model/fit_curated_wilhelm_kind_curves.py.

**Version note:** CCFSM v0.1 is a transparent model specification with a mathematically analysed reduced and linearized core. It is not a claim that the full chemistry–fractal–poroelastic parameter set has already been empirically determined.
