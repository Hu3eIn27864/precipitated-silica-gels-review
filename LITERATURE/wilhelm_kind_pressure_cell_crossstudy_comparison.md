# Wilhelm & Kind (2014/2015): pressure-cell cross-study comparison

**Audit date:** 11 November 2026  
**Scope:** acid-catalysed enforced syneresis at 20 °C, published pressure-series fit summaries. This is a parameter-level comparison, not a re-digitisation or common refit of the plotted time courses.

## 1. Experimental lineage and protocol changes

Wilhelm & Kind (2015) explicitly state that all earlier acid-catalysed enforced-syneresis experiments from Wilhelm & Kind (2014) were repeated using the Microdyn-Nadir NP010 membrane instead of Dow Filmtec NF270. The authors report no significant difference in results between the two membranes for the acid gel. The pressure-cell apparatus was also modified. This is a within-research-programme repeat/membrane comparison, not independent external replication.

The nominal gel chemistry is the same strongly acidic sodium-silicate/sulfuric-acid system. Both studies use a pressure-cell sample height of about 16 mm. However, the pressure ranges represented in the published fit tables differ: 2014 reports 0.8–15.5 bar, whereas the 2015 acid series reports approximately 0.23–7.76 bar. The 2015 table includes pressure intervals rather than single exact values.

## 2. Published 20 °C acid-gel fit summaries

| Study | Δp (bar) | Maximum shrinkage | τ (h) | Empirical exponent |
|---|---:|---:|---:|---:|
| 2014 | 0.8 | 0.53 | 13.0 | 1.23 |
| 2014 | 1.6 | 0.63 | 8.4 | 1.23 |
| 2014 | 2.4 | 0.69 | 5.9 | 1.23 |
| 2014 | 3.2 | 0.71 | 4.1 | 1.23 |
| 2014 | 4.0 | 0.73 | 3.5 | 1.23 |
| 2014 | 5.0 | 0.77 | 2.3 | 1.23 |
| 2014 | 6.5 | 0.79 | 2.0 | 1.23 |
| 2014 | 8.0 | 0.80 | 1.5 | 1.23 |
| 2014 | 15.5 | 0.87 | 1.1 | 1.23 |
| 2015 | 0.23–0.29 | 0.38 | 13.1 | 1.00 |
| 2015 | 0.63–0.77 | 0.52 | 5.9 | 1.00 |
| 2015 | 1.50–1.54 | 0.63 | 3.8 | 1.00 |
| 2015 | 2.24 | 0.67 | 2.3 | 1.00 |
| 2015 | 3.80–3.92 | 0.72 | 1.7 | 1.00 |
| 2015 | 6.15–6.46 | 0.77 | 1.1 | 1.00 |
| 2015 | 7.41–7.76 | 0.80 | 1.0 | 1.00 |

The 2014 table explicitly fixes the stretched-exponential exponent at n = 1.23. The 2015 comparison uses the simple exponential form (n = 1). In both forms, τ is mathematically the time at which the response reaches 1 − exp(−1) ≈ 63.2% of its fitted asymptote. This gives τ a common quantile interpretation, but it does **not** make least-squares estimates obtained from different curve shapes strictly interchangeable: the fitted τ can shift when n is fixed differently.

## 3. Near-pressure comparison

| 2014 pressure (bar) | 2014 max shrinkage | 2014 τ (h) | 2015 pressure interval (bar) | 2015 max shrinkage | 2015 τ (h) | τ2014/τ2015 |
|---:|---:|---:|---:|---:|---:|---:|
| 0.8 | 0.53 | 13.0 | 0.63–0.77 | 0.52 | 5.9 | 2.20 |
| 1.6 | 0.63 | 8.4 | 1.50–1.54 | 0.63 | 3.8 | 2.21 |
| 2.4 | 0.69 | 5.9 | 2.24 | 0.67 | 2.3 | 2.57 |
| 4.0 | 0.73 | 3.5 | 3.80–3.92 | 0.72 | 1.7 | 2.06 |

These are approximate pressure matches, not paired observations at exactly equal pressure. The fitted maximum shrinkages are close (absolute differences 0.01–0.02), while the reported τ values are about 2.1–2.6 times shorter in the 2015 table over these approximate matches. This is a discrepancy worth investigating, but it is not evidence by itself of a membrane effect, changed material kinetics, or an error in either paper.

## 4. Can both studies be refitted with one common empirical function?

**Not from the tabulated summaries alone.** The papers provide fitted parameter tables and plotted time courses, but no machine-readable time-series values were located in the inspected sources. Re-fitting a common model requires the actual time–shrinkage observations (or a carefully calibrated, independently checked digitisation of the figures). Re-fitting the published A and τ values would be circular and would not harmonise the original observations.

The correct common candidate is:

\[
S(t)=S_{\max}\left[1-\exp\left(-\left(t/\tau\right)^n\right)\right].
\]

For a harmonised re-fit, estimate A = Smax and τ from digitised or original time-series points, first using a **shared fixed n = 1.23** across both studies, then perform a sensitivity fit with n free (or with a shared n estimated across the combined series). Preserve each pressure condition as a separate curve. Report digitisation uncertainty and do not treat digitised points as raw measurements. The 2014 authors note that n = 1 can reproduce rates within error bars but with a larger residual sum of squares; that statement supports testing n = 1 as a sensitivity case, not assuming equivalence.

## 5. Interpretation and stop rules

1. Count the 2015 acid pressure-cell series as a repeat/membrane-comparison series within the 2014–2015 research programme, not an independent external replication.
2. Keep the authors' statement of no significant NF270/NP010 difference separate from the numerical comparison of published fitted parameters.
3. Do not interpret the approximately twofold τ difference as a physical rate change until both raw curves have been fitted with the same response function and the pressure matching, geometry and uncertainty are checked.
4. Do not infer permeability or a poroelastic diffusivity from these empirical τ values alone.
5. The 2015 base-catalysed pressure-cell series is a separate chemistry comparison and is not part of this acid-only repeat comparison.

## Sources inspected

- Wilhelm & Kind (2014), *Polymers* 6, 2896–2911, DOI 10.3390/polym6122896: §§3.2–3.3, Figure 7, Table 2 and associated text.
- Wilhelm & Kind (2015), *Polymers* 7, 2504–2521, DOI 10.3390/polym7121528: §§3.2, 4.2–4.3, Figure 12, Table 3 and associated text.

**Status:** published-parameter comparison complete; common raw-curve refit pending source time-series or verified figure digitisation.


## 6. Follow-up figure access check (11 November 2026)

The publisher HTML exposes Figure 12 (2015) as a high-resolution rendered image. Its caption explicitly distinguishes measured curves (solid) from model curves (dashed), and the legend labels pressure levels for acid and base panels. The 2014 HTML confirms Figure 7 shows measured curves with model fits and states that the low-pressure 0.8-bar curve has small deviations for t < 12 h. These source details strengthen the need to digitise measurement curves separately from fitted/model curves, especially at low pressure and early times.

The publisher image can be viewed in the web interface, but the attempt to retrieve the PNG into the local analysis environment failed. Therefore no pixel calibration, point extraction, or common fit has been performed in this follow-up. Do not describe the figures as quantitatively digitised. The next technical route is to use the browser-visible original image in a dedicated digitisation workflow (e.g. WebPlotDigitizer) or obtain the source PNG through a working download route, recording axis calibration, selected curve, point coordinates, and digitisation uncertainty.

Additional direct-source observations:
- 2015 Table 3 reports acid-gel endpoint shrinkage/τ pairs at 20 °C over 0.23–7.76 bar; the 2014 Table 2 spans 0.8–15.5 bar. The lowest-pressure points are not exact matches, and the 2014 curve at 0.8 bar is explicitly the condition with noted early-time fit deviations.
- 2015 explicitly says the acid experiments were repeated with NP010 and reports no significant difference from NF270, but separately warns that this statement does not apply to the base-catalysed gel. The authors attribute a thin layer forming on the membrane in the base-gel case to additional flow resistance that affects kinetics but not the endpoint appreciably.
- Figure 12 (2015) and Figure 7 (2014) are both published as measured curve plus model curve; only measured traces should be used as data in a cross-study re-fit.

Sources: Wilhelm & Kind (2014), publisher full text, §4.2 and Table 2; Wilhelm & Kind (2015), publisher full text, §4.2, Figure 12 and Table 3.


## 7. Derived half-shrinkage time as a common response quantile

To make the different fitted curve shapes easier to compare descriptively, the CSV now also reports the algebraically derived half-shrinkage time

\[
t_{50}=\tau(\ln 2)^{1/n}.
\]

This is a transformation of the published fit parameters, not a refit of the raw observations. For the four approximate pressure matches, the derived values are:

| 2014 / 2015 pressure match (bar) | 2014 t50 (h; n=1.23) | 2015 t50 (h; n=1) | Ratio |
|---|---:|---:|---:|
| 0.8 / 0.63–0.77 | 9.650 | 4.090 | 2.36 |
| 1.6 / 1.50–1.54 | 6.235 | 2.634 | 2.37 |
| 2.4 / 2.24 | 4.380 | 1.594 | 2.75 |
| 4.0 / 3.80–3.92 | 2.598 | 1.178 | 2.20 |

This quantile standardisation does not remove confounding from different fit forms, approximate pressure matching, experimental uncertainty or possible differences in the underlying observations. It shows that the published parameter sets imply slower half-response times in the 2014 fits, but it still does not establish a physical kinetic change or identify a membrane effect. A common refit of measured time-series data remains necessary.
