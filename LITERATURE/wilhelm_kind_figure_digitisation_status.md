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


### Panel identity and calibration correction

The supplied assets establish the correct figure/time-axis mapping unambiguously:
- Figure 8 (file ending `g008`): cylinders; 0–250 h; relative shrinkage 0–0.6.
- Figure 10 (file ending `g010`): droplets; 0–8 h; relative shrinkage 0–1.0.

The initial calibration coordinates were refined after inspecting the actual 1536 × 591/594 pixel images. The CSV now records the revised major-tick coordinates for all four panels. These are image-coordinate estimates from the raster and remain subject to residual checks in the calibration script before any point data are released.


## KI-gestützte Näherungsablesung integriert (2026-11-11; Provenienz präzisiert)
164 näherungsweise aus JPEG abgelesene Messpunkte wurden durch einen anderen ChatGPT-Account erstellt und anschließend vom Nutzer als Text übermittelt; sie wurden nicht vom Projektteam pixelkalibriert oder unabhängig am Originalbild geprüft. Die Werte wurden in `wilhelm_kind_approximate_measurement_points.csv` überführt. Struktur- und Plausibilitätsprüfung: `wilhelm_kind_digitisation_quality_audit.md`. Keine Werte wurden an publizierte Fitparameter angepasst. Kritische Auffälligkeiten: Figure 10b bei 20/40/60 °C (digitale Maxima 0.51/0.67/0.86 gegenüber Tabellen-Fitparametern 0.30/0.39/0.51); Figure 10b/60 °C ist besonders dringlich zu prüfen. Auch Figure 8b/40 und 60 °C sowie Figure 10a/60 °C zeigen nichtmonotone Rückgänge. Pixelkoordinaten, Fehlerbalken und Unsicherheiten fehlen weiterhin. Alle Werte bleiben vorläufige Näherungsablesungen.


## Explorative Halbzeitprüfung (2026-11-11)
Ein fitfreies Screening der Zeit bis zur Hälfte der publizierten Fit-Amplitude wurde ergänzt: `wilhelm_kind_t50_screening.csv` und zugehörige Methodennotiz. Die Ergebnisse sind nur Plausibilitätsprüfung mittels linearer Interpolation, keine neue Parameterschätzung. Auffällig sind verzögerte digitale Halbzeiten in Figure 8a bei 40/60 °C; Figure 10b zeigt trotz relativ passender Halbzeiten weiterhin stark überhöhte digitale Endmaxima.


### Provenienz-Korrektur und Evidenzgrenze (2026-11-11)

Die 164 Kurvenpunkte sind **KI-gestützte, ungeprüfte Näherungsablesungen**, keine vom Projektteam selbst digitalisierten Messdaten und keine Originaldaten der Autoren. Die zuvor verwendete Formulierung „Nutzer-Digitalisierung“ war unpräzise und wird zurückgenommen. Bis zur unabhängigen Prüfung am Originalbild bleiben die Werte Evidenzgrad D: ausschließlich exploratives Screening; keine gewichteten Fits, Fehlerstatistik, physikalische Parameteridentifikation oder quantitativen Schlussfolgerungen aus kleinen Kurvenunterschieden. Tabellenwerte (A) und τ aus dem Artikel werden separat als publizierte Literaturwerte behandelt.

### Verifikation der empirischen Fitfunktion

Der Volltext gibt Gleichung (3) als (S(t)=A[1-\exp(-t/\tau)]) an. Für diese Funktion gilt exakt (t_{50}=\tau\ln 2). Die bisherige Umrechnung in `wilhelm_kind_t50_screening.csv` ist daher formal korrekt; die digitale Halbzeit bleibt wegen der ungeprüften Kurvenpunkte unsicher. Quelle: Wilhelm & Kind (2015), Gleichung (3), Abschnitt 4.1.


### Original image review through publisher page (2026-11-11)

The original 1024-pixel publisher PNGs for Figures 8 and 10 were opened directly through the MDPI article page. This is a visual source inspection only; the image files could not be downloaded into the code execution environment, so no new pixel-coordinate digitisation or uncertainty propagation was performed.

For Figure 10b, the visible late experimental markers and plotted model curves are clearly above the base-catalysed Table 2 amplitudes (0.30/0.39/0.51). The previously supplied approximate maxima (about 0.51/0.67/0.86) are qualitatively consistent with the visible marker levels. Notably, the three base-catalysed Table 2 amplitudes repeat the Table 1 base-catalysed cylinder amplitudes exactly. This raises a plausible source-level table transcription/transfer error, but no erratum or author confirmation has been established.

Preserve the table values as printed and the figure as separate evidence. Do not overwrite either. The 164 AI-assisted approximate points remain unverified; this visual check only weakens the hypothesis that the discrepancy must be caused by symbol misassignment. Figure 10b should now be flagged as a **publication-internal figure/table inconsistency candidate**, not simply as a digitisation outlier.
