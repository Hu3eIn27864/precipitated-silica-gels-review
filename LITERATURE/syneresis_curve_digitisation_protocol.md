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


## Priority extraction pass: matched pressure-cell curves (added 11 November 2026)

### Original publisher assets confirmed visually

- Wilhelm & Kind (2014), Figure 7, measured (solid) and fitted (dashed) enforced-syneresis curves at 20 °C:
  https://mdpi-res.com/polymers/polymers-06-02896/article_deploy/html/images/polymers-06-02896-g007-1024.png
- Wilhelm & Kind (2015), Figure 12, measured (solid) and modelled (dashed) curves at 20 °C, acid panel (a) and base panel (b):
  https://mdpi-res.com/polymers/polymers-07-01528/article_deploy/html/images/polymers-07-01528-g012-1024.png

Both assets open in the publisher's web interface, but direct download into the current execution environment failed. This is a retrieval limitation, not evidence that the assets are unavailable to a normal browser. The images have been visually inspected; **no pixel-level digitisation has yet been performed**.

### Pressure-cell-specific extraction rules

- Digitise Figure 7 (2014) and Figure 12 (2015) independently. Never treat dashed model traces as observations.
- Figure 7 omits the 3.2 and 6.5 bar curves for graphical simplicity; do not create points for those pressures from the figure. Their published fit parameters may remain in the parameter table.
- Figure 7 authors note small deviations between measurement and fit for 0.8 bar at t < 12 h. Preserve these deviations; do not smooth or force the markers onto the fit.
- Figure 12 includes acid and base panels, seven pressure conditions each. Preserve the pressure intervals printed in the figure and Table 3; do not collapse intervals to a single exact pressure without retaining the original range.
- For Figure 12, distinguish curve colours/labels using the printed pressure labels, not colour alone. Store source figure, panel, curve class, pressure label/range, and point confidence.
- The two studies are related work from the same research group, not independent external replications. The 2015 acid series was repeated using a different membrane and reported no significant difference for acid gels; the authors explicitly caution that this does not hold for the base gel.

The companion files syneresis_pressure_cell_axis_calibration_template.csv and wilhelm_kind_pressure_cell_marker_pixels_template.csv are blank/preliminary digitisation aids. Calibration coordinates must be checked against the downloaded original before any point values are accepted.
