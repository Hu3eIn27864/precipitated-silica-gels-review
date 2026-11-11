# Geometry scaling of published natural-syneresis time constants

## Source and extracted parameters

Wilhelm & Kind (2015), *Polymers* 7, 2504–2521, DOI 10.3390/polym7121528, report fitted natural-syneresis curves as

\[ S(t)=S_{\max}\left[1-\exp(-t/\tau)\right]. \]

Tables 1 and 2 give S_max and tau for cylindrical samples (diameter 12 mm) and droplets (approximately 3 mm diameter), for acid- and base-catalysed gels at 20, 40 and 60 °C. The 12 corresponding table entries have been added to LITERATURE/quantitative_extraction_syneresis.csv as fitted parameters, not raw time-series observations.

## Diagnostic first-eigenmode conversion

For a deliberately simplified constant-coefficient diffusion analogy, the slowest decaying mode has

- radially drained infinite cylinder: tau_1 = R^2/(alpha_01^2 D_app), with alpha_01 = 2.4048256, the first zero of J_0;
- radially drained sphere: tau_1 = R^2/(pi^2 D_app).

Using R = 6 mm for the cylindrical samples and treating the 3 mm droplets as spheres with R = 1.5 mm gives the following apparent first-mode diffusivities. These are dimensional translations of empirical fitted time constants under idealised boundary conditions; they are **not measured material diffusivities** and must not be identified with a uniquely determined permeability or poroelastic consolidation coefficient.

| Geometry | Gel | 20 °C (m²/s) | 40 °C (m²/s) | 60 °C (m²/s) |
|---|---|---:|---:|---:|
| Cylinder, radial | Acid | 8.12e-11 | 1.48e-10 | 3.46e-10 |
| Cylinder, radial | Base | 3.45e-11 | 5.40e-11 | 6.29e-11 |
| Sphere, radial | Acid | 1.58e-10 | 9.89e-11 | 8.22e-11 |
| Sphere, radial | Base | 9.45e-11 | 1.11e-10 | 6.67e-11 |

## Interpretation and limitations

1. The apparent diffusivity is not geometry- or temperature-invariant across the two sample classes. For example, the acid-gel estimate rises strongly with temperature in cylinders but falls in droplets under the spherical idealisation.
2. This does **not** prove that the material diffusivity physically changes in the opposite direction. The conversion assumes that the empirical single-exponential shrinkage time constant is the fundamental mode of a linear diffusion problem, which has not been established.
3. The droplets are only described as approximately 3 mm and are measured optically from top and side views; exact sphericity, contact geometry, drainage boundary conditions and evolving shape are not established by the tabulated parameters.
4. The cylindrical specimens are pycnometer samples, and their drainage geometry is idealised as radial in the paper's comparison with the pressure-cell tests. A finite cylinder can have end drainage as well as radial drainage; its exact boundary conditions need to be justified before selecting a cylinder eigenproblem.
5. The paper notes that droplet temperatures are held at 20 °C during initial preparation and then raised to the target temperature. It identifies this thermal transient as a possible reason for similar early-time courses at 40 and 60 °C.
6. The authors explicitly state that their description is empirical and that a physically based model remained future work.

## Consequence for model development

Do not calibrate one universal cv to all cylinder and droplet time constants. The appropriate next model comparison is:

- retain the empirical (S_max, tau) parameters as the directly reported observations;
- formulate geometry-specific radial/finite-cylinder forward solutions with explicit boundary conditions;
- test whether a common material transport parameter can explain both geometries after accounting for sample preparation and temperature history;
- report model discrepancy and parameter identifiability, rather than forcing a common coefficient.

The present 1-D slab code remains a mathematical baseline only. A small
standard-library helper (`geometry_scaling.py`) now implements the ideal
first-mode conversion for infinite-cylinder radial drainage and spherical
radial drainage, with inverse and radius-squared scaling tests. It is not a
full transient radial solution. A geometry-resolved transient solver should
be added only after the drainage geometry and boundary conditions are
sufficiently constrained.