# Wilhelm & Kind (2014): natural–enforced syneresis bridge

**Reference:** Wilhelm, S. & Kind, M. (2014). “On the Relation between Natural and Enforced Syneresis of Acidic Precipitated Silica.” *Polymers* 6(12), 2896–2911. DOI [10.3390/polym6122896](https://doi.org/10.3390/polym6122896). Open full text: https://publikationen.bibliothek.kit.edu/1000045599/6501742

**Audit date:** 11 November 2026. Article-page full text, Tables 1–4 and conclusion inspected. Supplementary Table S1 was not separately retrieved in this pass.

## Formulation and geometries
- Acidic precipitated silica made by Y-mixing sodium silicate (40 wt% sodium water glass; 35.5 wt% Na2O·3.3SiO2 in the water glass) and 50 wt% sulfuric acid, volumetric ratio 1:1, Re = 2300.
- Gelation time approximately 12 min at 20 °C; theoretical pH −0.97.
- Natural syneresis: cylindrical samples d = 18 mm, V ≈ 6 mL, individually aged in pycnometer flasks; three replicates per time point, 12 time points, at 20, 40 and 60 °C.
- Enforced syneresis: approx. 20 mL samples, height 16 mm, plunger load 100–1950 N, corresponding to Δp = 0.8–15.5 bar; drainage through porous supports and NF270 membranes.
- The authors argue that the characteristic liquid travel distances are similar between the natural and enforced geometries. This geometric similarity is part of their empirical transfer argument, not proof that the stress fields or boundary conditions are identical.

## Natural syneresis: published empirical fit

The authors fit
[
rac{Delta V}{V_0}(t)=left(rac{Delta V}{V_0}ight)_{max}
left[1-expleft(-left(rac{t}{	au}ight)^night)ight].
]

| T (°C) | Maximum volume decrease | τ (h) | n | R² |
|---:|---:|---:|---:|---:|
| 20 | 0.197 | 21.7 | 1.23 | 0.868 |
| 40 | 0.197 | 11.1 | 1.23 | 0.867 |
| 60 | 0.198 | 5.6 | 1.23 | 0.988 |

The article describes faster early shrinkage up to about 50 h, followed by slower shrinkage as the skeleton stiffens. The fitted maximum volume decrease is effectively constant across these three temperatures, whereas τ falls substantially with temperature.

## Enforced syneresis at 20 °C

| Δp (bar) | Maximum volume decrease | τ (h) | R² |
|---:|---:|---:|---:|
| 0.8 | 0.53 | 13.0 | 0.983 |
| 1.6 | 0.63 | 8.4 | 0.999 |
| 2.4 | 0.69 | 5.9 | 0.997 |
| 3.2 | 0.71 | 4.1 | 0.996 |
| 4.0 | 0.73 | 3.5 | 0.996 |
| 5.0 | 0.77 | 2.3 | 0.998 |
| 6.5 | 0.79 | 2.0 | 0.998 |
| 8.0 | 0.80 | 1.5 | 0.997 |
| 15.5 | 0.87 | 1.1 | 0.994 |

The authors state that increasing temperature to 40 and 60 °C shifts the forced curves to shorter times while leaving the maximum shrinkage nearly unchanged. The temperature-specific forced-fit values are in supplementary Table S1, not transcribed here.

## Empirical transfer model and its limits

For maximum shrinkage the authors fit
[
lnleft[(Delta V/V_0)_{max}ight]=A+rac{B}{C+Delta p}.
]
The tabulated coefficients are:

| T (°C) | A | B (bar) | C (bar) | R² |
|---:|---:|---:|---:|---:|
| 20 | −0.14 | −0.72 | 0.57 | 0.979 |
| 40 | −0.14 | −0.81 | 0.57 | 0.992 |
| 60 | −0.18 | −0.61 | 0.57 | 0.965 |

Setting Δp = 0 extrapolates maximum volume decreases of 0.25, 0.21 and 0.29 at 20, 40 and 60 °C, compared with measured natural values near 0.20. The reported relative errors reach about 25% at 20 °C and 45% at 60 °C. The authors explicitly recommend additional enforced measurements below 0.8 bar.

For the characteristic time they use
[
log(	au)=D-Elog(p^*+Delta p),qquad p^*=1 mathrm{bar}.
]
The fitted D values imply extrapolated natural τ values of 24.0, 13.8 and 7.1 h at 20, 40 and 60 °C, versus measured 21.7, 11.1 and 5.6 h. The maximum relative error is reported as 24%.

## Mechanistic interpretation and relevance
The authors interpret continued silanol condensation as a source of network contraction and stress, with increasing siloxane bonding progressively stiffening the skeleton. They explicitly discuss the need for pore liquid to move through the network and state that polymerisation affects permeability and skeleton compliance. This is a mechanistic hypothesis in the paper; permeability and constrained modulus are not independently measured.

This source is unusually valuable because it supplies, in one target-chemistry study:
1. matched natural and pressure-forced response curves;
2. independent empirical fits for endpoint shrinkage and kinetic rate;
3. a documented failure mode of extrapolation, especially for endpoint shrinkage at low pressure;
4. a physical interpretation involving reaction-driven network stress, hydraulic drainage and skeleton compliance.

It is not a validated Darcy/poroelastic constitutive law. The Δp → 0 mapping is empirical and based on data whose minimum forced pressure is 0.8 bar. Do not identify τ with (L^2mu/(kappa M)), or infer permeability/modulus from these curves alone. Also keep this acidic-only study distinct from the later pH/base comparisons in Wilhelm & Kind (2015).

## Modelling implications
- Treat endpoint shrinkage and rate as separate observables/response functions.
- The data support a rate that changes with temperature while the measured natural endpoint is almost unchanged.
- A model that predicts kinetics but misses the final shrinkage (or vice versa) is not an adequate description of the full response.
- The pressure extrapolation below 0.8 bar is precisely where the model is least constrained; the natural condition Δp = 0 is an extrapolated boundary, not a directly tested enforced-syneresis point.
- This paper is a high-priority benchmark for later coupled structural–transport modelling, but should not be used to calibrate permeability without independent mechanics and hydraulic data.
