# Quantitative extraction note — Wilhelm & Kind (2015), natural syneresis

**Source:** S. Wilhelm and M. Kind, “Influence of pH, Temperature and Sample Size on Natural and Enforced Syneresis of Precipitated Silica,” *Polymers* 7(12) (2015), 2504–2521, DOI 10.3390/polym7121528.

**Access:** Open full article inspected on the publisher site. Tables 1 and 2 provide fitted parameters for natural syneresis. The article models each shrinkage curve empirically as

\[
\frac{\Delta V}{V_0}=\left(\frac{\Delta V}{V_0}\right)_{max}
\left[1-\exp(-t/\tau)\right].
\]

The authors explicitly state that a physically based model remained to be developed. Accordingly, the table entries are fit parameters, not direct measurements of permeability, modulus, diffusivity, or raw pointwise shrinkage.

## Extracted natural-syneresis parameters

| Geometry | Gel | Temperature (°C) | Maximum relative volume decrease | tau (h) |
|---|---|---:|---:|---:|
| Cylinder, 12 mm diameter, ~3 mL | Acid | 20 | 0.20 | 21.3 |
| Cylinder, 12 mm diameter, ~3 mL | Acid | 40 | 0.20 | 11.7 |
| Cylinder, 12 mm diameter, ~3 mL | Acid | 60 | 0.20 | 5.0 |
| Cylinder, 12 mm diameter, ~3 mL | Base | 20 | 0.30 | 50.1 |
| Cylinder, 12 mm diameter, ~3 mL | Base | 40 | 0.39 | 32.0 |
| Cylinder, 12 mm diameter, ~3 mL | Base | 60 | 0.51 | 27.5 |
| Droplet, ~3 mm diameter | Acid | 20 | 0.37 | 0.40 |
| Droplet, ~3 mm diameter | Acid | 40 | 0.41 | 0.64 |
| Droplet, ~3 mm diameter | Acid | 60 | 0.48 | 0.77 |
| Droplet, ~3 mm diameter | Base | 20 | 0.30 | 0.67 |
| Droplet, ~3 mm diameter | Base | 40 | 0.39 | 0.57 |
| Droplet, ~3 mm diameter | Base | 60 | 0.51 | 0.95 |

These 12 entries are now recorded in `LITERATURE/quantitative_extraction_syneresis.csv` with source, experiment type, geometry, data status and interpretive notes.

## Experimental context and caveats

- Both gels were prepared by 1:1 volumetric mixing in a Y-mixer of a 40 wt% sodium-silicate solution and sulfuric acid solution. Acid gel: 50 wt% H2SO4, final pH below 0; base gel: 3.2 wt% H2SO4, final pH approximately 10.
- Cylinders: 12 mm diameter and approximately 3 mL; pycnometric volume measurement; three samples averaged per measurement point.
- Droplets: approximately 3 mm; optical measurement from top and side views. Samples were held at 20 °C during the initial preparation period and then brought to the target temperature. The authors note that this thermal history may explain similar early-time courses at 40 and 60 °C.
- The paper describes smaller samples as shrinking faster and, for these droplet experiments, reaching larger maximum shrinkages. The droplet/cylinder comparison is not a pure length-scale experiment: geometry, measurement method, thermal history and potentially drainage boundaries differ.
- The authors report that the maximum shrinkage of the acid-catalysed cylinders remains near 0.20 over 20–60 °C, whereas the base-catalysed cylinder values rise from 0.30 to 0.51.
- The fitted `tau` values do not themselves identify a unique transport coefficient. A first-mode diffusion mapping is documented separately as a sensitivity diagnostic only.

## Implication for the review

The data directly support strong dependencies of apparent syneresis kinetics and final shrinkage on gel type, temperature and sample size. They do **not** by themselves establish a universal (L^2) drainage law or prove that the fitted time constant is a pore-pressure relaxation time. A geometry-aware physical model must first establish its boundary conditions and distinguish transport from network ageing/stiffening.
