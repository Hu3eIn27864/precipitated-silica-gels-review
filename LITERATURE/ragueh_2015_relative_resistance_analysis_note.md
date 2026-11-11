# Ragueh et al. (2015): derived comparison of relative cake resistance

**Purpose.** Provide a transparent comparison of pressure and grade dependence in Table 4 without converting the reported values into absolute permeability.

## Derived quantities

The source reports specific cake resistance as multiples of an undisclosed reference value, R. The companion CSV contains pairwise ratios between silica grades at each pressure, the two reported volume-fraction measures, and their arithmetic difference.

All resistance ratios are dimensionless and derived from the printed multiples of R. They are not permeability ratios unless additional assumptions about cake geometry, porosity and the relation between specific resistance and permeability are made.

## Main descriptive results

- The printed relative resistance rises from 400 to 600 kPa by 45.2% for S1, 60.0% for S2 and 55.8% for S3. The S1 value at 600 kPa is printed without the reference symbol R; its use in this comparison is provisional and explicitly flagged.
- S1/S3 resistance ratios are 3.25, 2.56 and 3.03 at 400, 500 and 600 kPa. S1/S2 ratios are 1.67, 1.62 and 1.51; S2/S3 ratios are 1.95, 1.58 and 2.00.
- The ranking S1 > S2 > S3 is retained at all three pressures in the printed table. This is a grade-dependent cake-resistance result, not a universal ranking for gel permeability or syneresis rate.
- The SAXS-derived bead fraction for S2 exceeds the gravimetric silica fraction by about 0.041–0.042 at all three pressures. Differences for S1 and S3 are much smaller. The two volume-fraction estimates should not be treated as interchangeable: they arise from different measurement/reduction routes and may represent distinct structural definitions or sampled volumes. This systematic offset deserves interpretation before either is mapped onto a single porosity state variable.

## What can and cannot be inferred

The article obtains cake specific resistance from permeate-volume/time data using Darcy's law and neglects filter-cloth resistance because it is estimated to be roughly two orders of magnitude below cake resistance in that apparatus. This is a cake-specific experimental reduction. Table 4 publishes only resistance multiples of a confidential reference, so it does not provide the absolute numerical permeability needed to calibrate a free-gel syneresis model.

The article describes structural retention at primary-particle and dense-aggregate scales alongside greater sensitivity of large-scale network morphology. This supports a multiscale state description, but not a unique constitutive function k(phi, Df, z) for syneresing gels.

## Reproducibility

The CSV is derived from the source Table 4 and the project's audited transcription. Ratios are rounded to six decimal places. No uncertainty propagation was attempted because covariance and the uncertainty structure of the shared reference R are not disclosed. The original printed uncertainties remain in `ragueh_2015_structural_filtration_data.csv`.

## Source and unresolved issues

Ragueh et al., *Separation and Purification Technology* 156 (2015), 2–11, DOI: 10.1016/j.seppur.2015.10.005. Open author PDF: https://www.lcmd.espci.fr/docs/Rageh-Separation-Purification-2015.pdf

Still unresolved: (i) Table 2 prints sample labels S1/S3/S3; (ii) Table 3 gives S3 fractal dimension 1.8 while adjacent prose gives 2.2; (iii) Table 4 omits the R symbol for S1 at 600 kPa. No correction is inferred.
