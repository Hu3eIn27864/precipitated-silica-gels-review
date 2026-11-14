# Existing-data reanalysis: first-pass evidence map

**Date:** 14 November 2026  
**Status:** descriptive reanalysis of published fit parameters; not a refit of experimental time series and not physical-model validation.

## 1. Scope and evidence classes

This pass uses only values already transcribed in:

- `LITERATURE/quantitative_extraction_syneresis.csv` (12 natural-syneresis parameter pairs from Wilhelm & Kind 2015 Tables 1–2, plus six centrifugal forced-syneresis fit pairs from Wilhelm 2017);
- `LITERATURE/pressure_cell_syneresis_comparison.csv` (14 pressure-cell fit pairs from Wilhelm & Kind 2015 Table 3);
- `LITERATURE/experimental_geometry_audit_wilhelm.md`;
- `LITERATURE/wilhelm_kind_figure_digitisation_status.md`.

Three evidence classes must remain distinct:

1. **Published fitted parameters:** (S_{max}) and (	au) transcribed from article/dissertation tables. These are empirical fit results, not raw observations.
2. **AI-assisted approximate chart readings:** 164 points supplied previously and retained in `wilhelm_kind_approximate_measurement_points.csv`. They have no source pixel coordinates, axis-calibration residuals, or pointwise uncertainty and have not been independently digitised. Exploratory only; excluded from quantitative conclusions below.
3. **Original marker-level observations:** not yet available in a verified, calibrated project dataset. The figure digitisation templates are not data.

## 2. Natural syneresis: published characteristic times

The published natural-syneresis fit time constants (	au) (hours) are:

| Geometry | Gel | 20 °C | 40 °C | 60 °C |
|---|---|---:|---:|---:|
| Cylinder, nominal diameter 12 mm | Acid | 21.3 | 11.7 | 5.0 |
| Cylinder, nominal diameter 12 mm | Base | 50.1 | 32.0 | 27.5 |
| Droplet, nominal diameter about 3 mm | Acid | 0.40 | 0.64 | 0.77 |
| Droplet, nominal diameter about 3 mm | Base | 0.67 | 0.57 | 0.95 |

These are direct transcriptions of the published empirical fit parameters, not newly estimated values.

### 2.1 Within-geometry acid/base contrast

The ratio (	au_{base}/	au_{acid}), calculated at each temperature, is:

| Geometry | 20 °C | 40 °C | 60 °C |
|---|---:|---:|---:|
| Cylinder | 2.35 | 2.74 | 5.50 |
| Droplet | 1.68 | 0.89 | 1.23 |

The cylinder series has a consistently longer fitted time constant for base gel, with a widening ratio over temperature. The droplet series does not show the same ordering at 40 °C. This contrast is descriptive only: the nominal geometries, boundary conditions, preparation/thermal history, and possibly the table/figure consistency differ. It cannot be interpreted as an intrinsic mobility or permeability ratio.

### 2.2 Temperature trend differs by geometry

The ratios (	au(60,^circ C)/	au(20,^circ C)) are:

| Geometry | Acid | Base |
|---|---:|---:|
| Cylinder | 0.235 | 0.549 |
| Droplet | 1.925 | 1.418 |

Thus, the published cylinder fit parameters become faster with temperature, whereas the droplet fit parameters become slower over the same endpoints. This is a major geometry/protocol-dependent discrepancy, not evidence for a simple universal temperature law. The source notes an initial 20 °C hold for droplets before transfer to the target-temperature cell; this thermal history must be represented before attributing the trend to material transport.

### 2.3 Geometry warning

The paper reports 12 mm cylinder diameter and approximately 3 mL volume; a 26.5 mm height follows only if the specimen is assumed to be a right circular cylinder. The authors' comparison uses radial drainage with (R=6) mm as a modelling assumption. The droplet is described as approximately 3 mm and observed in a cell with cover glasses; a freely drained sphere is not established. Therefore, the cylinder and droplet (	au) values must not be converted into a single shared diffusivity without geometry/boundary sensitivity.

## 3. Pressure-cell forced syneresis

For the seven pressure intervals at 20 °C and initial height 16 mm, the transcribed Table 3 fit parameters show decreasing (	au) with increasing pressure for both gels:

| Pressure interval (bar) | Acid (	au) (h) | Base (	au) (h) |
|---|---:|---:|
| 0.23–0.29 | 13.1 | 6.5 |
| 0.63–0.77 | 5.9 | 3.2 |
| 1.50–1.54 | 3.8 | 2.1 |
| 2.24 | 2.3 | 1.7 |
| 3.80–3.92 | 1.7 | 1.1 |
| 6.15–6.46 | 1.1 | 1.0 |
| 7.41–7.76 | 1.0 | 0.9 |

Within this pressure-cell series, base-gel (	au) is lower than acid-gel (	au) at every reported interval, opposite to the natural-cylinder ordering. This is not an intrinsic permeability comparison: pressure-cell drainage includes the membrane/filter-plate assembly, mechanical loading and potentially evolving gel properties. Pressure ranges are preserved rather than silently replaced by midpoints.

The six centrifugal points from Wilhelm (2017) remain a separate series: 20 mm initial height and height-averaged equivalent centrifugal pressure. They must not be pooled with uniform pressure-cell loading.

## 4. Main findings and what they do not establish

1. The natural-syneresis published fit parameters show a strong geometry-associated change in apparent temperature response.
2. Acid/base ordering changes between natural cylinder, natural droplet, and pressure-cell protocols.
3. A single empirical (	au) is therefore not a direct material transport coefficient. It combines specimen geometry, boundary resistance, mechanical response, thermal history and the authors' empirical fit form.
4. These parameter tables are useful for **cross-condition consistency checks and model-discrepancy tests**, but do not provide the time-resolved residuals, replicate scatter, or point-level uncertainties needed for a statistically defensible refit.
5. The 164 AI-assisted chart readings are not used in the quantitative tables above. In particular, the unresolved Figure 10b figure/table inconsistency must remain explicit; do not “correct” either the published table or the approximate readings by choosing whichever agrees with a model.

## 5. Recommended next analysis sequence

1. **Lock the evidence ledger:** keep published fit parameters, approximate chart readings, and verified marker observations in separate files/status classes.
2. **Resolve the figure/table discrepancy:** retrieve the original Figure 8, Figure 10 and pressure-cell Figure 12 image files into a reproducible working environment; calibrate each panel; manually review marker centres and error bars. Record pixel coordinates and calibration residuals before generating physical values.
3. **Reconstruct only what is actually published:** use the empirical equation stated in the article to generate reference curves from tabulated (S_{max}) and (	au), clearly labelled as fit reconstructions, never as experimental points.
4. **Perform held-out consistency checks:** where sufficient verified marker data become available, fit one condition and predict another geometry/temperature/chemistry condition without retuning all parameters. Treat related Wilhelm/Kind publications as one research lineage, not independent replication.
5. **Only then revisit geometry optimisation:** use the evidence-supported boundary conditions and uncertainty ranges. Do not recommend a laboratory geometry based only on a synthetic two-layer identifiability optimum.

## 6. Decision gate

**Current decision:** proceed with literature-data curation and source-figure verification. Do not yet infer target-gel permeability, modulus, diffusivity, or contact resistance from the published (	au) values. The next quantitative model test should be a geometry-aware prediction with explicitly bounded nuisance parameters, not a free fit of every condition.
