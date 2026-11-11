# Protocol for digitising published syneresis curves

## Target figures

1. Wilhelm & Kind (2015), Figure 8: natural syneresis, 12 mm diameter / approximately 3 mL cylindrical samples, 20/40/60 °C, acid/base gel.
2. Wilhelm & Kind (2015), Figure 10: natural syneresis of approximately 3 mm droplets, 20/40/60 °C, acid/base gel.
3. Wilhelm & Kind (2015), Figure 12 and supplementary Figures S3–S6: enforced syneresis in the pressure cell, where boundary resistance and applied pressure must be retained as metadata.
4. Wilhelm (2017), Figure 5.12: centrifugal forced syneresis at 20 °C and initial sample height 20 mm. Treat as additional dissertation observations, not an independent research-family replication.

## Extraction rules

- Save the original figure, its URL/DOI, retrieval date and figure/panel identifier before extracting points.
- Calibrate each panel independently using the printed axis ticks; do not reuse pixel transforms between panels.
- Record only visible experimental markers as digitised observations. Keep fitted lines in a separate curve_type='model_fit' class; never mix model curves and measured markers.
- Record units, axis calibration points, digitiser/software version, estimated pixel/line-width uncertainty and any overlapping markers.
- Preserve the published fitted \(\tau\) and maximum shrinkage in the parameter table. Do not re-fit and replace the reported values without documenting the objective function and residuals.
- Store raw digitised coordinates and transformed values. Keep a stable point ID, panel ID, sample class, temperature, catalyst class, replicate/mean status if known, and extraction confidence.
- The 2015 article states that three samples were averaged for each cylindrical measurement point. Do not treat plotted means as independent replicate observations.
- For droplets, mark the 20 °C initial hold and subsequent heating explicitly. Do not treat the nominal 3 mm size as proof of a free sphere.
- For pressure-cell data, preserve applied pressure, initial height, membrane type, temperature and whether the data came from the article or dissertation.
- Use part of a curve for fitting and retain a separate curve/condition for validation wherever possible. If there are too few independent conditions, label the exercise a consistency check, not validation.

## Suggested point-table schema

study_id,source_doi,figure_panel,point_id,curve_type,gel_type,temperature_C,time_h,relative_volume_decrease,pressure_bar,initial_height_mm,geometry_label,replicate_status,x_pixel_uncertainty,y_pixel_uncertainty,extraction_confidence,notes

No raw curve points are added by this protocol alone. The dataset remains unpopulated until the source figure has actually been digitised and quality-checked.
