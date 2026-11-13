# Finite external drainage resistance for 1-D syneresis transport

**Status:** first numerical implementation, one-way hydraulic boundary model. Not calibrated to the Wilhelm–Kind pressure cell.

## 1. Why a boundary resistance is needed

The pressure-cell experiments on base-catalysed precipitated silica report a thin layer at the membrane that adds hydraulic resistance. A model that imposes zero excess pressure directly at the gel boundary silently assumes a perfectly drained support and cannot represent this effect.

A resistance-in-series boundary is the minimal extension. It separates the internal gel resistance from an external membrane/support/cake resistance without pretending that the latter is part of intrinsic gel permeability.

## 2. Boundary law and units

Let the outward superficial liquid flux be q [m/s], the excess pressure at the gel-side boundary be p_b [Pa], and the lumped area-specific external hydraulic resistance be R_b [Pa s/m]. Then

\[
q=\frac{p_b}{R_b}.
\]

For a cell-centred finite volume, the Darcy resistance between the cell centre and its boundary is Δx/(2λ), where λ=κ/μ [m²/(Pa s)]. The combined face conductance is therefore

\[
g_b=\left[\frac{\Delta x}{2\lambda_1}+R_b\right]^{-1},
\qquad q=g_b p_1.
\]

The same expression applies at the right boundary. R_b=0 recovers a perfectly drained Dirichlet boundary. As R_b→∞, the boundary approaches a sealed/no-flux limit. The external resistance can be decomposed into membrane, support and deposited-layer contributions in series if independent measurements justify that decomposition.

This is consistent with resistance-in-series Darcy formulations in membrane filtration, where clean membrane, fouling and gel-layer resistances add. That literature supports the boundary representation as a generic hydraulic modelling construct; it does not supply a numerical resistance for the precipitated-silica pressure cell.

## 3. Implementation

The time_dependent_1d.py solver now accepts:
- left_boundary_resistance_pa_s_m
- right_boundary_resistance_pa_s_m

Both default to zero, preserving the previous perfectly drained behaviour. The boundary conductance is evaluated using the mobility at the current implicit time level. Storage remains fixed and mobility remains prescribed externally; no pressure-to-network feedback is implied.

The solver reports outward boundary flux and a discrete global storage/outflow balance residual. The new tests cover:
1. zero resistance reproduces the previous perfect-drainage solution;
2. finite external resistance slows pressure relaxation;
3. global mass balance remains satisfied with asymmetric boundary resistances;
4. negative and non-finite resistance inputs are rejected.

## 4. Identifiability and experimental calibration

A shrinkage curve alone cannot identify gel permeability and membrane resistance separately. At minimum, measure:
- clean membrane/support water permeance before gel contact;
- post-run permeance after a controlled rinse, to estimate irreversible deposited-layer resistance;
- pressure drop across the gel and across the support separately if possible;
- sample height/volume and expelled-liquid flux during the same run;
- at least two gel drainage lengths or thicknesses.

A useful diagnostic is to compare total hydraulic resistance at matched age and viscosity across sample thicknesses. If the external resistance is constant while gel resistance scales with gel thickness, a thickness series can separate the intercept (external) from the slope (gel contribution), provided deformation and material state are controlled. This is a proposed measurement strategy, not an assumption that resistance is constant during the experiment.

## 5. Limits and next model steps

- The current model is 1-D, saturated, small-strain and fixed-domain.
- Boundary resistances are constant in time. A time-dependent membrane/cake resistance would require independently justified kinetics or direct measurement.
- No osmotic-pressure term, chemical species transport, silica dissolution/reprecipitation, or moving boundary is included.
- No constitutive relation links permeability to porosity, fractal dimension or contact number.
- No constrained-modulus aging or pressure feedback to MC is included.
- The current implementation is a numerical sensitivity tool, not a fit or validation of the published curves.

Next: add an independent static resistance-calibration utility only if source data provide measured permeance; then consider age-dependent external resistance as a separate hypothesis. Do not fit R_b(t), κ(t) and M(t) simultaneously to a single shrinkage curve.
