# Quantitative interpretation: geometry, pH and drainage resistance in Wilhelm & Kind (2015)

**Source:** Wilhelm, S.; Kind, M. (2015), *Polymers* 7, 2504–2521, DOI: 10.3390/polym7121528.  
**Status:** source-level extraction and interpretation; values below are published fitted parameters, not raw time-series data.

## 1. Natural syneresis: cylindrical samples

For cylinders with diameter 12 mm and gel volume approximately 3 mL, the published single-exponential fit parameters are:

| Temperature (°C) | Catalyst | Maximum shrinkage | Characteristic time τ (h) |
|---:|---|---:|---:|
| 20 | acid | 0.20 | 21.3 |
| 20 | base | 0.30 | 50.1 |
| 40 | acid | 0.20 | 11.7 |
| 40 | base | 0.39 | 32.0 |
| 60 | acid | 0.20 | 5.0 |
| 60 | base | 0.51 | 27.5 |

The base-catalysed cylinder has a larger fitted τ at each temperature, while its fitted maximum shrinkage is also larger. The paper proposes that the acid gel has compact primary particles connected relatively loosely, permitting easier drainage, whereas the base gel has a denser network and slower pore-liquid drainage. These are the authors' structural interpretation, not direct permeability measurements.

## 2. Natural syneresis: droplets

For droplets of approximately 3 mm diameter:

| Temperature (°C) | Catalyst | Maximum shrinkage | Characteristic time τ (h) |
|---:|---|---:|---:|
| 20 | acid | 0.37 | 0.40 |
| 20 | base | 0.30 | 0.67 |
| 40 | acid | 0.41 | 0.64 |
| 40 | base | 0.39 | 0.57 |
| 60 | acid | 0.48 | 0.77 |
| 60 | base | 0.51 | 0.95 |

The droplet times are much shorter than cylinder times. At 20 °C, for example, τ falls from 21.3 to 0.40 h for acid and from 50.1 to 0.67 h for base. This is consistent with a strong geometry/drainage-length effect, but it is not a clean measurement of a Darcy L² law: geometry, boundary conditions, measurement method and thermal history differ. The authors also note that the first 30 min of droplet measurements occur at 20 °C before the sample is brought to the target temperature.

## 3. Enforced syneresis: pressure-cell results at 20 °C

For initial sample height 16 mm, the reported fit parameters are:

| Δp (bar) | τ acid (h) | τ base (h) | Maximum shrinkage acid | Maximum shrinkage base |
|---:|---:|---:|---:|---:|
| 0.23–0.29 | 13.1 | 6.5 | 0.38 | 0.69 |
| 0.63–0.77 | 5.9 | 3.2 | 0.52 | 0.76 |
| 1.50–1.54 | 3.8 | 2.1 | 0.63 | 0.81 |
| 2.24 | 2.3 | 1.7 | 0.67 | 0.83 |
| 3.80–3.92 | 1.7 | 1.1 | 0.72 | 0.85 |
| 6.15–6.46 | 1.1 | 1.0 | 0.77 | 0.87 |
| 7.41–7.76 | 1.0 | 0.9 | 0.80 | 0.88 |

This reverses the natural-cylinder ordering: under external compression the base-gel fitted τ is smaller. It must not be read as evidence that base gel has intrinsically higher permeability. The authors identify a thin layer formed on the membrane only in the base-gel tests; it adds hydraulic resistance and affects kinetics, although its small thickness has negligible effect on the maximum shrinkage. The article explicitly says this kinetic influence could not be eliminated.

## 4. Chemistry and structural mechanism: what is actually measured

The article reports very different monomeric silicic-acid concentrations in expelled pore liquid: approximately 0.2–0.4 mmol/L for acid-catalysed natural syneresis and 100–200 mmol/L for base-catalysed natural syneresis. The authors relate this to the strong increase in silicic-acid solubility above pH 8. They also report that the separated pore liquid can become turbid on storage, suggesting additional solid formation after separation; the mechanism is not unambiguously resolved.

The paper's mechanistic account distinguishes:
- acid catalysis: preferentially linear or weakly branched structures, then loosely connected agglomerates;
- base catalysis: highly branched clusters;
- ongoing siloxane-bond formation: contractile stress on the skeleton;
- network stiffening during aging: slower subsequent shrinkage;
- pore-liquid drainage: necessary for macroscopic volume contraction.

These mechanisms are plausible and tied to the authors' interpretation, but the paper does not independently measure age-resolved intrinsic permeability and constrained modulus on the same specimens.

## 5. Implications for the review and model

1. **Do not compare acid/base τ without matching geometry and driving condition.** Natural cylinders, droplets and externally compressed samples are separate experimental classes.
2. **Keep τ distinct from hydraulic consolidation time.** The empirical single-exponential τ is a curve parameter, not automatically (L_d^2mu/(kappa M)).
3. **Include an external resistance term for the pressure-cell boundary.** A membrane/cake resistance in series with gel resistance is a necessary candidate explanation for the base-gel anomaly.
4. **Use the natural-cylinder/droplet contrast as qualitative evidence for size dependence, not as a permeability fit.**
5. **The pore-liquid concentration contrast motivates reactive transport / dissolution–reprecipitation as a separate mechanism**, not a scalar pH correction to permeability.
6. **A matched discriminating experiment should vary drainage length and membrane/support independently**, while measuring expelled-liquid chemistry, sample deformation, permeability and mechanical response.

## Provenance and limits

All numerical entries above are transcribed from the published Tables 1–3. They are published model-fit parameters, not newly fitted values and not digitised raw measurements. The article itself states that a physically based model remains to be developed. The empirical exponential is therefore retained as a descriptive correlation only.
