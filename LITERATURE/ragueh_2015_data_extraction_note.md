# Ragueh et al. (2015): structured extraction and source-inconsistency audit

**Source:** D. M. Ragueh et al., “Filtration of precipitated silica aggregates: Length scales, percolation threshold and yielding behaviour,” *Separation and Purification Technology* 156 (2015), 2–11. DOI: [10.1016/j.seppur.2015.10.005](https://doi.org/10.1016/j.seppur.2015.10.005). Open author PDF: https://www.lcmd.espci.fr/docs/Rageh-Separation-Purification-2015.pdf

## Extracted quantitative observations

A structured transcription is provided in `LITERATURE/ragueh_2015_structural_filtration_data.csv`. Values are transcribed from the article tables, retaining units and source labels. The source PDF screenshots were inspected for Tables 2–4.

### Structural length scales

- Primary-particle diameters in Table 2: S1 17 nm; the middle row is printed as S3 (25 nm) although the paper elsewhere consistently has three materials S1/S2/S3; final S3 10 nm. The middle sample is therefore **probably S2**, but the table label is not silently corrected in the data file.
- Dense aggregate sizes in Table 3: S1 82 nm; S2 125 nm; S3 175 nm.
- Branch mass-fractal dimensions in Table 3: S1 1.8; S2 2.2; S3 1.8. The prose immediately below instead states 1.8, 2.2, **2.2** for S1/S2/S3. This is a genuine unresolved table–text discrepancy for S3. Neither value should be used as a unique S3 calibration target until the authors or a corrigendum clarify it.

### Filtration-cake properties

Table 4 reports specific resistance as multiples of a confidential reference (R), not as absolute SI values. At 400/500/600 kPa, respectively:

- S1: 2.50 / 2.82 / 3.63 (the 600 kPa entry omits the (R) symbol in the printed table; retained as ambiguous)
- S2: 1.50 / 1.74 / 2.40
- S3: 0.77 / 1.10 / 1.20

Gravimetric silica volume fractions at 400/500/600 kPa:
- S1: 0.082 / 0.088 / 0.096
- S2: 0.084 / 0.086 / 0.108
- S3: 0.070 / 0.074 / 0.078

SAXS-derived bead volume fractions at the same pressures:
- S1: 0.092 / 0.108 / 0.112
- S2: 0.125 / 0.128 / 0.150
- S3: 0.071 / 0.076 / 0.077

Reported uncertainties on specific resistance are 4.5–6.8%; the article gives ±0.2% alongside gravimetric cake volume fractions. Do not infer more precision than the printed reporting supports.

## Mechanistic observations relevant to the model

1. The three slurries are industrial precipitated silica dispersions taken directly from a precipitation reactor; the synthesis routes differ. This is strong material relevance for process-history effects.
2. The paper finds a percolation threshold at silica volume fractions about 0.06 (S3), 0.08 (S1), and 0.09 (S2). In the percolation regime, volume fraction changes little while osmotic pressure increases by more than an order of magnitude. The network behaves as a soft solid.
3. In the yielding regime, volume fraction increases and large dense lumps form through interpenetration of rigid clusters. At low ionic strength, the network becomes more fragile; the authors propose dissolution of silicate deposited at particle necks as a plausible explanation.
4. During pressure filtration from 400 to 600 kPa, local primary-particle and dense-aggregate structure is largely retained. The largest-scale network morphology is more sensitive; S1 shows an increase in low-q scattering at 600 kPa, and S3 shows a high-pressure discrepancy attributed to reorganisation/denser lumps.
5. The effective-medium/Brinkman–Darcy expression is evaluated against filtration cake data using aggregate-scale size and bead volume fraction. It is a cake-scale constitutive comparator, not a direct permeability law for a free-standing syneresing gel.

## Transferability limits

- The experiments concern filtration cakes and osmotic compression of dispersions, not natural syneresis of a macroscopic gel cylinder or confined droplets.
- The specific-resistance reference (R) is undisclosed, so absolute cake permeability cannot be reconstructed from Table 4 alone without additional calibration/geometry/filtration metadata.
- Table 4's relative specific resistance must not be relabelled as intrinsic permeability.
- The paper assumes negligible filter-cloth hydraulic resistance in its filtration reduction; this is a distinct apparatus assumption from the membrane/filter-plate resistance issue in Wilhelm & Kind's pressure-cell experiments.
- The reported structural variables provide useful priors and qualitative constitutive constraints for a future model, but not a matched (k(phi))-(M(phi)) pair for the syneresis target gels.

## Modelling consequences

- Represent process history through material-specific initial structural state (primary-particle size, dense aggregate size, branch structure, and ionic-strength/bond state), not through a single universal fractal dimension.
- A percolation/rigidity transition near the reported cake-system thresholds is a candidate hypothesis for sensitivity studies only; it must not be imported as a universal gel threshold.
- Permit large-scale network reorganisation and yielding while allowing primary-particle and dense-aggregate length scales to remain approximately stable over some pressure window.
- Keep filtration-cake transport calibration separate from natural-syneresis calibration. Any transfer requires a state and boundary-condition mapping.

## Figure-digitisation status

The publisher's HTML exposes image assets and captions for Wilhelm & Kind Figures 8 and 10. This confirms that the original plot artwork is available as separate figure resources, but no experimental marker coordinates have yet been digitised in this phase. Digitisation remains pending until image files can be retrieved at sufficient resolution and axis/marker uncertainty can be recorded.


## Additional source audit and derived comparison (2026-11-11)

A further inspection of the original PDF shows that the S1/S3/S3 sample-label pattern occurs in **Table 1 as well as Table 2**. The likely intended middle label is S2, consistent with the prose and the other sample labels, but the source has not been author-confirmed. The CSV continues to preserve the printed Table 2 label.

A derived comparison of the Table 4 values is available in `LITERATURE/ragueh_2015_relative_resistance_analysis.csv` and `LITERATURE/ragueh_2015_relative_resistance_analysis_note.md`. It calculates pressure trends and grade-to-grade ratios on the printed relative-resistance scale only. It does not infer absolute cake permeability. The reported 400→600 kPa increases are 45.2% (S1), 60.0% (S2) and 55.8% (S3), with the S1 600 kPa calculation flagged because the table omits the reference symbol R.

Table 1 initial slurry composition is now separately transcribed in `LITERATURE/ragueh_2015_initial_slurry_data.csv` with a companion note. It reports dry silica mass fractions 0.053, 0.053 and 0.034 g/g solution and initial silica volume fractions 0.020, 0.018 and 0.011 for printed labels S1, S3 and S3, respectively. The middle row is probably S2 but remains unconfirmed.
