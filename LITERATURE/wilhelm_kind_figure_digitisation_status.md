# Marker digitisation workflow — Wilhelm & Kind (2015), Figures 8 and 10

## Source access and verified metadata

The full article is available through the KIT repository record:
https://publikationen.bibliothek.kit.edu/1000052536/3796774

- Figure 8: natural syneresis of 12 mm diameter, approximately 3 mL cylinders; acid-catalysed panel (a), base-catalysed panel (b); temperatures 20, 40 and 60 °C.
- Figure 10: natural syneresis of approximately 3 mm droplets; acid-catalysed panel (a), base-catalysed panel (b); temperatures 20, 40 and 60 °C.
- The cylinder protocol averages three samples per plotted measurement point. Do not treat these plotted means as individual replicates.
- Droplets are held at 20 °C for the first 20 minutes after gelation before being placed in the thermostated measurement cell. The article later discusses similarity of courses during the first 30 minutes; this is not the same as the actual preconditioning duration.
- The source states that multiple droplet series were averaged. It does not provide per-replicate raw values in the figure.

## Current extraction status

The PDF text and figure locations are verified, but the figure PNG/PDF page images could not be retrieved into the execution environment in this pass (the 13 MB repository PDF exceeds the image-render/screenshot retrieval limit, and direct PNG download fails). **No marker pixels or calibrated data points have been generated.** The CSV files in this directory are empty templates, not observations.

Original publisher figure assets:
- Figure 8: https://mdpi-res.com/polymers/polymers-07-01528/article_deploy/html/images/polymers-07-01528-g008-1024.png
- Figure 10: https://mdpi-res.com/polymers/polymers-07-01528/article_deploy/html/images/polymers-07-01528-g010-1024.png

## Reproducible workflow

1. Download the original PNGs at the URLs above and preserve the unmodified originals.
2. Assign a unique panel ID to each plot panel (8a, 8b, 10a, 10b). Calibrate each panel independently using at least two x-axis and two y-axis tick marks; use three or more where possible to detect skew/nonlinearity.
3. Record each visible experimental marker centre in pixel coordinates. Do not digitise the fitted solid curves as measured points. Record overlap/occlusion and uncertainty in locating the marker centre.
4. Fill `syneresis_figure_axis_calibration_template.csv` with one row per calibration tick and `syneresis_figure_marker_pixels_template.csv` with one row per marker. Axis `scale` is `linear` or `log10`.
5. Run:
   `python digitise_syneresis_markers.py --calibration syneresis_figure_axis_calibration_template.csv --pixels syneresis_figure_marker_pixels_template.csv --output syneresis_figure_digitised_points.csv`
6. Review calibrated outputs against the plot, check monotonicity only where physically/source justified, and compare digitised trends to Table 1/2 empirical fit parameters. Do not force markers onto the fit curve.

## Uncertainty convention

Pixel uncertainties are propagated locally through the fitted axis calibration. They represent marker-centre and axis-reading uncertainty only; they do not include the paper's between-sample variation, plotting/printing distortion, or uncertainty in the experimental method. Calibration uses ordinary least squares across supplied tick marks. If residuals show curvature or perspective distortion, correct the image or use a more appropriate calibration rather than increasing uncertainty to conceal systematic error.

## Interpretation safeguards

- Keep `curve_type=experimental_marker` and `curve_type=model_fit` in separate files or classes.
- Figure 8 measurement points are means of three samples.
- Figure 10 uses a 20-minute 20 °C preconditioning period; preserve absolute time from the authors' plotted origin unless the axis definition requires otherwise.
- The article's empirical single-exponential fit is not a physical permeability or diffusivity model.


## Update: original figure assets received (11 November 2026)

Both original 1536-pixel-wide publisher PNGs were supplied in the working conversation and visually inspected:
- Figure 8: two panels, 0–250 h and relative shrinkage 0–0.6.
- Figure 10: two panels, 0–8 h and relative shrinkage 0–1.0.

The axis-calibration CSV now contains initial pixel/value correspondences for all four panels, using multiple major ticks per axis. These coordinates are an initial image-coordinate calibration, not yet a final calibration certificate: the digitisation pass must inspect residuals against the tick marks and refine any pixel positions before accepting the calibrated marker data.

No experimental marker coordinates have yet been committed. This is deliberate: the marker symbols overlap one another and, in several regions, the fitted curves; automatic colour-component detection alone merges markers with lines and would create false precision. The next extraction step must therefore use manually reviewed marker centres (with image-coordinate overlays or equivalent review) and keep error-bar extents in Figure 8/10 separate from centre-location uncertainty.
