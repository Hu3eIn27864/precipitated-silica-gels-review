# PSG-049 — Wilhelm (2017): Dissertation source assessment

## Bibliography and access

Sebastian Wilhelm, *Über die Synärese kolloidaler Strukturen am Beispiel von Siliciumdioxid*, doctoral dissertation, Karlsruhe Institute of Technology, oral examination 6 July 2017. KIT Scientific Publishing, DOI: 10.5445/KSP/1000073100.

Full text: https://publikationen.bibliothek.kit.edu/1000073100/4718247

The dissertation front matter states that the document, excluding cover, pictures and graphs, is licensed CC BY-SA 4.0. The cover has a separate CC BY-ND 4.0 license. The figure images are therefore not assumed to be reusable under the text license.

## Directly relevant result

Chapter 5.1, particularly Table 5.3, reports model parameters for natural syneresis of small gel droplets:

| Temperature | Maximum relative shrinkage A | Characteristic time τ (h) |
|---:|---:|---:|
| 20 °C | 0.40 | 0.671 |
| 40 °C | 0.63 | 0.640 |
| 60 °C | 0.82 | 1.055 |

The surrounding text identifies these as the model values for natural syneresis of gel droplets. The adjacent discussion states that maximum shrinkage and rate increase with temperature for the basic-catalyzed droplets.

## Critical comparison with Wilhelm & Kind (2015)

The journal article's Table 2 reports for the basic-catalyzed droplets:

| Temperature | Journal Table 2 A | Journal Table 2 τ (h) |
|---:|---:|---:|
| 20 °C | 0.30 | 0.67 |
| 40 °C | 0.39 | 0.57 |
| 60 °C | 0.51 | 0.95 |

The 2017 dissertation's Table 5.3 therefore differs materially in A, while τ is comparatively similar. The chart-derived free fits to the approximate Figure 10b points are A=0.4195/0.6432/0.8253 and τ=0.726/0.683/1.118 h. These are much closer to the dissertation's A values than to the journal Table 2 A values.

This three-way agreement (Figure 10b chart, 2017 dissertation Table 5.3, free fits to chart readings) is strong evidence that the journal Table 2 amplitude column for the basic-catalyzed droplets is inconsistent with the later dissertation account. It does **not** prove the reason. Possibilities include a correction between manuscript versions, a journal table transcription/layout error, or a change in analysis/data selection between the 2015 article and 2017 dissertation. The current evidence does not distinguish these.

## Independence and evidential status

The dissertation is by the same first author and belongs to the same research lineage as the 2015 article. It is a valuable additional primary-source record, but it is **not an independent replication**. Do not count the article and dissertation as two independent experiments.

For the review:
- Preserve the 2015 journal Table 2 exactly as published.
- Preserve the dissertation Table 5.3 separately as a later same-author source.
- Keep Figure 10b approximate points in their separate conflict/triangulation branch.
- Do not overwrite the journal parameter database with dissertation values.
- When quoting droplet shrinkage maxima, identify the source table and version explicitly.

## Reproducible crosswalk

See `wilhelm_kind_figure10b_source_triangulation_2026-11-14.csv` and the separate fit/residual CSVs from 14 November 2026.

## Source

Wilhelm, S. (2017). *Über die Synärese kolloidaler Strukturen am Beispiel von Siliciumdioxid*. KIT Scientific Publishing. DOI: 10.5445/KSP/1000073100.


## Quantitative fixed-parameter comparison against Figure 10b

Using the curated approximate chart points, we evaluated both source tables *without refitting* their published A and tau parameters. The RMSE values are:

| Temperature | 2015 Table 2 parameters | 2017 Table 5.3 parameters |
|---:|---:|---:|
| 20 °C | 0.0960 | 0.0354 |
| 40 °C | 0.1954 | 0.0262 |
| 60 °C | 0.1944 | 0.0489 |

The dissertation parameters reduce chart-point RMSE by factors of approximately 2.7, 7.4 and 4.0, respectively. Their errors are close to the freely fitted RMSE values (0.0333, 0.0248 and 0.0480). This strengthens the conclusion that the 2017 dissertation parameter set is consistent with the plotted basic-droplet curves. Because the chart points remain approximate and uncalibrated, these RMSE values are diagnostic comparisons only, not formal measurement-error statistics.
