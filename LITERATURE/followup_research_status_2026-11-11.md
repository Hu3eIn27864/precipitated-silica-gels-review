# Follow-up source checks — 11 November 2026

## Wilhelm & Kind (2015): published Table 2 and correction search

The full article is available through KITopen under DOI [10.5445/IR/1000052536](https://publikationen.bibliothek.kit.edu/1000052536/3796774), with the original journal DOI [10.3390/polym7121528](https://www.mdpi.com/2073-4360/7/12/2504). The published Table 2 base-catalysed droplet parameters are A = 0.30, 0.39, 0.51 and τ = 0.67, 0.57, 0.95 h at 20, 40, 60 °C. These are adopted as the reference values for this review. Targeted searches for a correction/erratum did not locate a correction notice. This is a negative search result, not proof that no correction exists.

The source article itself distinguishes the 3 mm droplets (Figure 10) from 12 mm, approximately 3 mL cylinders (Figure 8). It also notes that droplets are initially held at 20 °C and then heated, which can influence early-time curve comparisons. The authors describe their exponential shrinkage relation as empirical and explicitly state that a physically based model remains to be developed. Therefore, neither A nor τ should be reinterpreted as a directly measured permeability or consolidation diffusivity.

## Valibeknejad et al. (2026): replication dataset access

The open-access article reports that replication data are deposited in Utrecht University's Dataverse under DOI [10.34894/V9OPAT](https://doi.org/10.34894/V9OPAT). The dataset landing page currently returns an Anubis JavaScript proof-of-work challenge in the available retrieval environment, and the Dataverse API endpoint could not be retrieved through the current web-access route. No dataset files, metadata schema, or raw observations have therefore been inspected in this pass.

The article publisher preview confirms that the study covers four sodium-silicate grouts, including rheology, gelation, mechanical response, syneresis, degradation and leaching. It reports, for example, C-gel syneresis of 16.5% after 7 days and T-gel syneresis below 4%; these are grout-specific values, not direct measurements on industrial precipitated-silica gel fragments. The dataset remains a potentially useful adjacent-system source, not a target-system calibration dataset.

Publisher article: https://www.sciencedirect.com/science/article/pii/S0950061826021422

## Consequences for project use

- Use Wilhelm & Kind Table 2 as the authoritative published parameter table; retain the Figure 10b visual discrepancy separately and unresolved.
- Do not claim an erratum exists or that a typographical error has been established.
- Do not claim the V9OPAT replication data have been inspected or analysed until the actual files are obtained.
- Keep the 2026 sodium-silicate grout study in an adjacent-system evidence class unless transferability to precipitated silica is independently justified.


## Pressure-cell digitisation source-access update (11 November 2026)

The publisher's original image assets have been opened in the web interface for Wilhelm & Kind (2014) Figure 7 and Wilhelm & Kind (2015) Figure 12. Direct image downloads into the execution environment still fail, so no pixel-calibrated points or common raw-data refit are available yet.

Added:
- syneresis_pressure_cell_axis_calibration_template.csv — 36 preliminary axis tick correspondences, each marked as needing verification against the downloaded image.
- wilhelm_kind_pressure_cell_marker_pixels_template.csv — 21 pressure-series metadata rows for measured curves only, preserving 2015 pressure ranges and distinguishing acid/base panels.
- Updated syneresis_curve_digitisation_protocol.md with direct figure URLs and rules separating solid measured traces from dashed model fits.

Next dependency: acquire the two original PNG files locally (or as attachments), then calibrate each panel independently, digitise only measured traces, record uncertainty, and only then run a common-form refit. No digitisation or refit is claimed in this update.
