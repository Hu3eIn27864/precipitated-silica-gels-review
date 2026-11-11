# Sahabi & Kind (2011): direct consolidation evidence for precipitated silica

**Audit date:** 11 November 2026

## 1. Consolidation of Inorganic Precipitated Silica Gel

H. Sahabi and M. Kind, *Polymers* 3(3), 1423–1432 (2011), DOI [10.3390/polym3031423](https://doi.org/10.3390/polym3031423). Open full text: https://www.mdpi.com/2073-4360/3/3/1423

### Material and protocol
- Acidic and alkaline silica model gels made by rapid mixing of sodium silicate solution (Na2O·3.3SiO2) and sulfuric acid in a Y-mixing nozzle.
- Acidic formulation: 50 wt% sulfuric acid and 40 wt% sodium silicate, 1:1 mixing ratio, reported pH −0.97.
- Alkaline formulation: 3.2 wt% sulfuric acid and 40 wt% sodium silicate, 1:1 mixing ratio, reported pH approximately 9.
- Both selected gels had gelation times of approximately 12 min.
- Oedometer test with dewatering at both ends, porous filter plates and NF90 membrane; external pressure approximately 15 bar; temperature 20 or 80 °C.
- The authors determine t90 graphically from consolidation ratio U(t), then use a semi-empirical Terzaghi–Shirato expression.

### Published numerical values

| Gel | pH | t90 at 20 °C | t90 at 80 °C |
|---|---:|---:|---:|
| Alkaline | ~9 | 40,401 s (11.22 h) | 11,236 s (3.12 h) |
| Acidic | −0.97 | 31,506 s (8.75 h) | 5,625 s (1.56 h) |

At constant nominal load, the reported t90 is shorter at 80 °C than at 20 °C for both formulations. The acidic gel consolidates faster than the alkaline gel at both temperatures. The paper reports approximately 90% consolidation on the scale of hours and about 75% final compression in one acidic oedometer example, compared with approximately 15 vol% natural syneresis over 70–150 h in two separate acidic aging examples cited from Vysotskii et al.

### Model-relevant caveats
- These are **pressure-forced oedometer consolidation** data, not natural syneresis under zero externally applied load. The load is approximately 15 bar and drainage is double-sided.
- The published t90 is a lumped empirical response parameter. It is not a direct permeability measurement and cannot uniquely identify intrinsic permeability and constrained modulus.
- The authors report that the simple Terzaghi–Shirato curve deviates from the silica-gel measurements in the primary consolidation phase (except the acidic 80 °C case), and also notes deviations in secondary consolidation. They suggest adding a damping element/viscoelastic contribution.
- The authors' proposed structural explanation is that acidic aggregates are dense at nanoscale but open at microscale, while alkaline aggregates show the inverse hierarchy; they suggest the microscale structure is more readily disrupted in the acidic gel. Treat this as the authors' interpretation, not a separately established causal law.
- The natural-syneresis comparison uses different pH values (0.33 and 1.65) and a different protocol from the pH −0.97 oedometer gel. It is qualitative, not a matched direct comparison.

### Use in this review
This is high-value direct evidence for the target chemistry and for pH-/temperature-dependent mechanical consolidation. It supports including a viscoelastic or delayed structural response in the conceptual model. It does **not** provide the independent permeability–modulus pair needed to calibrate a poroelastic syneresis model.

## 2. Companion modelling paper

H. Sahabi and M. Kind, “Experimentally Justified Model-Like Description of Consolidation of Precipitated Silica”, *Polymers* 3(4), 2156–2171 (2011), DOI [10.3390/polym3042156](https://doi.org/10.3390/polym3042156). Open KIT repository full text: https://publikationen.bibliothek.kit.edu/1000033909/3014841

This companion study simulates consolidation of a model gel fragment using molecular dynamics with van der Waals interactions and thermal motion, and compares simulation results with experimental data and a Monte Carlo simulation. Its model fragment is a fractal aggregate of 1,000 primary particles. It is directly relevant to the particle-scale modelling strand, but its assumptions (idealised aggregate, interaction potential, solvent representation, pressure ensemble) must be audited before reusing parameters or treating it as a validated predictive model. It does not replace the missing independent permeability measurement.

## 3. Consequences for the project

1. Promote Sahabi & Kind (2011) to a core target-system source for forced consolidation.
2. Keep natural syneresis, pressure-cell syneresis, and oedometer consolidation as distinct boundary-value problems and evidence classes.
3. Use the reported t90 values as published response observables only; do not invert them to permeability without specimen geometry, independent modulus/storage, and apparatus-resistance analysis.
4. Review the companion MD paper for a defensible link between fractal aggregate structure and consolidation, while explicitly separating its simulated assumptions from experimentally measured properties.
