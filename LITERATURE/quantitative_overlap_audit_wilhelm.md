# Quantitative overlap audit — Wilhelm / Kind syneresis series

**Assessment date:** 11 November 2026  
**Primary document:** Sebastian Maximilian Wilhelm (2017), *Über die Synärese kolloidaler Strukturen am Beispiel von Siliciumdioxid*, full KIT dissertation.  
**Purpose:** distinguish reproduced article results from additional dissertation experiments and extract a traceable subset of quantitative data.

## 1. Directly demonstrated overlap with the journal papers

The dissertation is an expanded record of the same KIT research programme, but the strength of the overlap evidence differs by output:

- **Wilhelm & Kind (2015): direct figure/data attribution.** The dissertation explicitly attributes natural-syneresis plots in §5.1 (e.g. Fig. 5.1) and pressure-cell plots/tables in Appendix D (Figs. D.3–D.5 and Tables D.3–D.5) to Wilhelm & Kind (2015). These are reused/presented again, not independent replications.
- **Wilhelm & Kind (2014) → 2015 acid-cylinder series: explicit source attribution, with a geometry inconsistency.** In the 2015 article, the acid-catalysed panel of Figure 8 is explicitly attributed to reference [5], i.e. Wilhelm & Kind (2014). The fitted values are also very close (2014: A = 0.197, τ = 21.7 h at 20 °C; 2015: A = 0.20, τ = 21.3 h). However, the 2014 article describes d = 18 mm, V ≈ 6 mL natural-syneresis cylinders, whereas the 2015 article describes the Figure 8 cylinder series as d = 12 mm, V ≈ 3 mL. This is a genuine source-level geometry inconsistency. The 2015 Figure 8 acid series should therefore be treated as **likely reused or refitted 2014 evidence, not an independent replication**, while retaining the unresolved geometry discrepancy. The base-catalysed Figure 8 series is not attributed to the 2014 paper and is additional 2015 evidence.
- The 2017 dissertation cites the 2014 article for the pyknometer apparatus/method in §4.2.1, Fig. 4.2; this reinforces method lineage but does not resolve the geometry discrepancy.
- Both articles are listed in the dissertation bibliography (pp. 139–140).

Accordingly, the thesis is not a third independent study for the explicitly attributed 2015 datasets. The 2015 acid-cylinder natural-syneresis series is explicitly sourced to the 2014 article and has near-matching fit parameters, so it should be counted as one likely shared dataset family, not as an independent replication. The reported cylinder geometry differs between the two papers and remains unresolved. Possible overlap of the acidic pressure-cell series also needs point-level checking; the 2015 paper describes its pressure-cell apparatus as already established in the earlier work, but this alone does not prove identical pressure-series observations.

## 2. What is additional in the dissertation?

The thesis extends the published work in at least three substantive ways:

1. **Centrifugation as an alternative forced-syneresis method.** This avoids the membrane between gel and permeate used in the pressure cell. At 20 °C and initial sample height 20 mm, the thesis reports three centrifugal loading conditions, converted to equivalent mean pressure differences of 0.10, 0.26 and 0.39 bar.
2. **Pore-liquid monomer and membrane-interaction analysis.** The thesis measures dissolved Si(OH)4 in permeate/retentate and documents silica deposition on the membrane during tests with alkaline-gel pore liquid. NMR is cited as confirmation of the silica layer. The resulting additional flow resistance can affect measured kinetics, even if the layer's volume effect is small relative to the gel sample.
3. **A more detailed filtration-model treatment.** Internal driving-force terms are fitted to forced-syneresis curves because they are not independently known. Such fitted terms are calibration parameters, not direct measurements of a unique microscopic force.

The centrifugation experiments are additional observations within the same research lineage, not an independent external replication. Their distinct forcing method and absence of a pressure-cell membrane make them valuable complementary observations, but not an independent research-group replication.

## 3. Extracted centrifugal forced-syneresis data

**Condition:** 20 °C; initial sample height (h_0=20) mm; three centrifugal loading conditions. The listed (Delta p_{mathrm{equiv}}) is a height-averaged equivalent pressure difference, not a directly applied uniform pressure.

| Gel type | Equivalent pressure (bar) | Maximum relative volume decrease ((Delta V/V_0)_{max}) | Characteristic time (	au) (h) |
|---|---:|---:|---:|
| Acid-catalysed | 0.10 | 0.27 | 9.7 |
| Acid-catalysed | 0.26 | 0.34 | 3.8 |
| Acid-catalysed | 0.39 | 0.41 | 4.2 |
| Base-catalysed | 0.10 | 0.64 | 12.4 |
| Base-catalysed | 0.26 | 0.68 | 5.3 |
| Base-catalysed | 0.39 | 0.74 | 3.8 |

**Interpretation:** maximum compaction increases with centrifugal driving force for both gel types. At matched equivalent pressure, the base-catalysed gel compacts substantially more than the acid-catalysed gel. The fitted characteristic time decreases overall with increasing force, although the acid-gel values are not strictly monotonic (3.8 h at 0.26 bar versus 4.2 h at 0.39 bar). Do not smooth away this non-monotonicity or imply a perfectly monotonic kinetic response.

The equivalent pressure is an approximation obtained by averaging the centrifugal body force over the initial sample height. It is not strictly interchangeable with a spatially uniform pressure difference in the pressure-cell experiment.

## 4. Mechanistic caution: the membrane can affect kinetics

The thesis reports that the NF270 membrane retains some monomeric silicic acid. The NP010 membrane performs better in the standard-solution test, but experiments with alkaline-gel pore liquid reveal silica deposition on the membrane. NMR confirms the deposited layer. Its thickness is reported as approximately 50–100 µm, small relative to the roughly 15 mm gel sample, so the direct volume bias is considered negligible. However, the deposit adds hydraulic resistance and may affect the rate of forced syneresis.

This is a material methodological qualification: differences in characteristic time between pressure-cell and centrifuge experiments cannot automatically be interpreted as intrinsic gel kinetics alone. Boundary resistance differs between the two methods.

## 5. Implications for article/dissertation evidence counting

| Result or method | Evidence status | Counting rule |
|---|---|---|
| Pyknometer apparatus/method in thesis §4.2.1, Fig. 4.2 | Cited to Wilhelm & Kind (2014) | Method lineage only; does not prove identical raw observations | 
| Natural syneresis in thesis §5.1, 12 mm / ~3 mL cylinders | Figure captions explicitly cite Wilhelm & Kind (2015) | Reproduced/presented again; do not count as a new independent dataset | 
| Natural acid-cylinder series: 2014 article vs 2015 Figure 8a | 2015 Figure 8a explicitly cites 2014; fit parameters are near-identical, but reported cylinder geometries differ (18 mm/~6 mL vs 12 mm/~3 mL) | Likely shared/reused or refitted dataset family; do not count as independent replication; retain geometry discrepancy | 
| Natural base-cylinder series in 2015 Figure 8b | No 2014 source attribution; additional base-catalysed comparison | Count as additional 2015 evidence, subject to within-paper sample/series independence |
| Pressure-cell forced-syneresis curves and fitted parameters in Appendix D | Explicitly attributed to 2015 article | Reproduced published results; do not count twice |
| Centrifugal forced-syneresis curves and Table 5.5 | Additional dissertation experiments | New observations within the same Wilhelm/Kind programme |
| Permeate/retentate monomer measurements and membrane deposition analysis | Additional methodological/mechanistic detail | New supporting evidence, with membrane-induced hydraulic resistance caveat |
| Filtration-model internal driving-force parameters | Fitted model outputs | Model calibration, not independently measured microscopic forces |

## 6. Review-ready conclusion

The Wilhelm/Kind series supports the conclusion that pH-dependent gel structure strongly affects the extent of syneresis and that imposed mechanical driving forces accelerate compaction. It also shows why enforced syneresis is not a simple substitute for natural syneresis: membrane resistance, force geometry, sample dimensions and extrapolation sensitivity matter. The dissertation adds useful centrifugal experiments and pore-liquid/membrane analysis. Its explicitly 2015-attributed plots and tables must not be counted again as independent observations. More importantly, the 2015 acid-cylinder natural-syneresis series explicitly cites the 2014 paper and has near-identical fitted parameters, strongly indicating reuse or refitting rather than an independent replication. The 18-mm/~6-mL versus 12-mm/~3-mL geometry discrepancy remains unresolved. For acid pressure-cell data, the 2015 paper explicitly describes repeated experiments with a different membrane and reports no significant membrane-related difference; count these as within-programme repeatability/membrane-comparison data, not independent external replication. The 2017 dissertation reproduces 2015-attributed plots and tables.

**Source-level confidence:** high for the presence of dataset overlap and the reported centrifugal values; moderate for mechanistic attribution of membrane effects because the membrane layer changes hydraulic resistance and the model parameters are fitted.


## 7. Correction and confidence boundary (11 November 2026)

A closer article-level check adds a key qualification. The 2015 article explicitly captions the acid-catalysed natural-syneresis panel in Figure 8 as “[5]”, which is Wilhelm & Kind (2014). Its fitted values are nearly identical to the 2014 article (at 20 °C, A = 0.197 and τ = 21.7 h in 2014 versus A = 0.20 and τ = 21.3 h in 2015). This is strong evidence that the acid-cylinder result is reused or refitted, not an independent replication. Yet the 2014 article reports cylinders d = 18 mm and V ≈ 6 mL, while the 2015 article describes Figure 8 as d = 12 mm and V ≈ 3 mL. The mismatch must remain explicit; the exact origin of the discrepancy is not established. The 2015 base-cylinder series is not attributed to 2014 and is an additional comparison. The 2017 dissertation reproduces 2015-attributed natural and pressure-cell outputs, and its apparatus/method discussion cites 2014.

**Revised evidence grades:** high for 2015 acid Figure 8's explicit source attribution to 2014 and for thesis-to-2015 figure/table reuse; high for the presence of an unresolved geometry inconsistency; unresolved for exact raw-point overlap and for 2014-to-2015 acid pressure-cell series. Count the 2014/2015 acid-cylinder curve as one likely shared evidence family, not two independent replications. Do not assign independent status to the pressure-cell series until its raw curves/parameters are compared point by point.


## 8. Pressure-cell repeatability link between 2014 and 2015

The 2015 article's Experimental Set-Up (§3.2) states that the pressure-cell design was modified relative to Wilhelm & Kind (2014). More importantly, §4.2 explicitly says that **all earlier acid-catalysed enforced-syneresis experiments were repeated** using the NP010 membrane instead of NF270, and that no significant difference in results between the two membranes was observed for the acid gel. The 2015 acid pressure-cell results therefore constitute a repeat experiment/membrane comparison in the same research programme, rather than independent external replication. This does not imply identical raw observations; it is evidence of repeated measurement under a modified membrane condition. The 2015 base-gel pressure-cell series is an additional chemical-condition comparison.


### Quantitative comparison caveat: the fitted time constants are not directly interchangeable

The 2014 natural-syneresis fit uses a stretched exponential with exponent n = 1.23; the 2015 article uses a simple exponential (n = 1) for its natural and pressure-cell comparisons. Therefore, even when amplitudes and pressure ranges are similar, the fitted τ values are not strictly like-for-like parameters. For example, the 2014 acid pressure-cell point at Δp = 0.8 bar reports a maximum shrinkage of 0.53 and τ = 13.0 h, whereas the 2015 repeated acid series reports 0.52 and τ = 5.9 h over Δp = 0.63–0.77 bar. The endpoint amplitudes are close, but the τ difference cannot be attributed to a membrane effect or a material kinetic change without refitting both raw series with the same response function and checking the original curves. The paper's statement of no significant membrane-related difference should be reported as the authors' conclusion, while the cross-paper fitted τ values remain model-form-confounded.


## 9. Pressure-cell comparison: published parameters versus common refit

A dedicated parameter-level comparison is recorded in `LITERATURE/wilhelm_kind_pressure_cell_crossstudy_comparison.md`. The 2015 paper explicitly states that all earlier acid pressure-cell experiments were repeated with NP010 instead of NF270 and that no significant membrane difference was observed. Yet the published 20 °C fit summaries show close maximum-shrinkage amplitudes but τ values about 2.1–2.6 times shorter in 2015 at approximate matched pressures. The exponent differs (2014 n = 1.23; 2015 n = 1), so this is a diagnostic discrepancy, not a demonstrated physical change or contradiction. Both fitted forms define τ at 63.2% of the asymptote, but the estimated τ can still depend on the fitted curve shape. A common refit cannot be reconstructed from the tabulated fit summaries; original time series or verified digitisation is required. Do not infer permeability from these values.
