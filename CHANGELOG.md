# Changelog

## 2026-11-11 — Project initialisation
- Established the working title and central research question.
- Defined the process-history-centred scope.
- Adopted evidence grades A/B/C/D and verification status V.
- Separated direct precipitated-silica evidence from related model systems.
- Set the approximate 50-source target as a non-binding planning estimate.
- Set *Langmuir* as the target journal for later fit assessment; subscription route preferred, subject to current policy verification.


## 2026-11-11 — Dissertation overlap audit

- Inspected the full KIT dissertations by Jan Schlomach (2006) and Sebastian Wilhelm (2017).
- Added PSG-019 (Schlomach dissertation) and upgraded PSG-008 (Wilhelm dissertation) in the literature database.
- Added `LITERATURE/source_assessments_batch_03.md` with direct-evidence summaries, limitations and a three-family overlap map.
- Identified major dataset overlap within the Schlomach/Quarch and Wilhelm publication families; these outputs must not be counted as independent replications without figure-level verification.
- Validated the CSV structure: 19 records, 18 columns per record.


## 2026-11-11 — Wilhelm quantitative overlap audit

- Re-inspected the full Wilhelm (2017) dissertation and mapped explicit figure/table attributions to Wilhelm & Kind (2014, 2015).
- Confirmed that the natural-syneresis pyknometer method/figure is attributed to the 2014 paper and that Appendix D pressure-cell curves/tables are attributed to the 2015 paper; these are reused outputs, not independent replications.
- Identified additional centrifugal forced-syneresis experiments and membrane/pore-liquid analysis in the dissertation.
- Extracted six centrifugal data points at 20 °C and initial sample height 20 mm into `LITERATURE/quantitative_extraction_syneresis.csv`; preserved the reported non-monotonic acid-gel characteristic time.
- Added `LITERATURE/quantitative_overlap_audit_wilhelm.md` and refined PSG-008 research-family notes.
- CSV validation: 19 records, 18 columns per record; no malformed rows.


## 2026-11-11 — Schlomach / Quarch overlap audit

- Verified in Quarch (2010), §4.2.1, that the standard semi-batch measurements are reproducible repeat experiments of Schlomach (2006).
- Confirmed that Quarch's programme adds distinct rheology, batch-fragmentation, reactor-comparison and ultrasound experiments; it is not wholly duplicative.
- Confirmed that Schlomach (2006) cites Schlomach & Kind (2004); exact figure-level overlap between the journal article and dissertation remains to be checked.
- Added `LITERATURE/research_family_overlap_audit_schlomach_quarch.md` and refined PSG-001, PSG-018 and PSG-019 notes.
- CSV validation: 19 records, 18 columns per record; 0 malformed rows.


## 2026-11-11 — Independent SAXS comparator studies

- Added PSG-020 (Wijnen et al., 1991, *JCIS*) on SAXS/NMR/BET evidence for ageing of water-glass-derived aqueous silica gels.
- Added PSG-021 (Knoblich & Gerber, 2001) on pH-dependent aggregation of sodium-silicate-derived SiO2 sols by SAXS.
- Added LITERATURE/source_assessments_batch_04.md with evidence boundaries, methodological caveats and research-family notes.
- Kept both studies in class B: they provide independent structural/mechanistic comparators, not direct replications of industrial semi-batch precipitated-silica gel fragmentation or syneresis.
- Emphasised that fractal dimensions cannot be compared across studies without harmonising material route, length-scale window and fitting assumptions.
- CSV validation after update: 21 records; 18 columns per record; no malformed rows.


## 2026-11-11 — Commercial precipitated-silica powder ageing

- Added PSG-022 (Chal et al., 2019, *Energy and Buildings*) on hygrothermal ageing of commercial precipitated silica powders alongside fumed, hydrophobized silica and aerogel comparators.
- Added LITERATURE/source_assessments_batch_05.md, explicitly separating wet-gel syneresis, aqueous-gel ageing and post-drying powder ageing.
- Completed volume/pages metadata (183, 626–638) from the publisher record.
- Kept the source in class B: directly relevant to post-manufacture precipitated-silica ageing, but not direct evidence for wet-fragment consolidation or syneresis.
- CSV validation: 22 records; 18 columns per record; no malformed rows.


## 2026-11-11 — Claim–evidence synthesis and historical literature

- Created SYNTHESIS/claim_evidence_matrix_v01.md with 12 bounded claims, source-family dependencies, confidence levels, limitations and priority evidence gaps.
- Added explicit LAMMPS go/no-go criteria: defer implementation until a specific coarse-grained question is justified; distinguish sensitivity modelling from predictive/reactive silica chemistry.
- Added PSG-023 (Sing & Madeley, 1953), PSG-024 (Shapiro & Kolthoff, 1950), PSG-025 (Merrill & Spencer, 1950) and PSG-026 (Madeley & Sing, 1962).
- Added LITERATURE/source_assessments_batch_06.md; paywalled/abstract-unavailable papers remain provisional and no substantive claims are inferred from titles alone.
- Database validation: 26 records; 18 columns per record; no malformed rows.


## 2026-11-11 — Independent wet-process aggregation and silicate-gel syneresis

- Added PSG-027 (Bałdyga et al., 2012): independent batch sodium-silicate/sulfuric-acid precipitation study with pH, temperature, silica and electrolyte variation; abstract indicates DLVO forces alone are insufficient and surface reactions matter.
- Added PSG-028 (Tognonvi et al., 2011): reports ripening-associated syneresis and irreversible consolidation in basic alkali-silicate gels acidified with HCl.
- Added PSG-029 (Tognonvi et al., 2019): abstract-level evidence on chemical species during basic sodium-silicate gel ripening and dissolution/precipitation.
- Added LITERATURE/source_assessments_batch_07.md and SYNTHESIS/claim_evidence_matrix_v02.md. The matrix now contains 15 bounded claims.
- Updated Shapiro & Kolthoff (1950) assessment using an accessible reproduced abstract; still not full-text inspected and strictly limited to high-temperature powder/gel ageing.
- Database validation: 29 records; 18 columns per record; no malformed rows.

## 2026-11-11 — Pilot-scale gelation-to-product-property link

- Added PSG-030 (Quang et al., 2012), a pilot-scale study of staged sulfuric-acid addition to sodium silicate and the effect of gelation history on final powder BET surface area and pore volume.
- Added `LITERATURE/source_assessments_batch_08.md`; the assessment is deliberately abstract-level and does not infer the direction or magnitude of property changes.
- Extended the claim-evidence matrix with C16 as a provisional bridge from process history to final powder properties, not as direct evidence for wet-gel syneresis.
- Database now contains 30 records; CSV row/column validation is pending an independent structural check.

## 2026-11-11 — Expanded publisher-preview appraisal: Quang and Tognonvi

- Reassessed PSG-030 using the expanded ScienceDirect publisher preview. The reported direction of the pilot-scale endpoint trends is now available: BET surface area and pore volume decrease with increasing pre-gel interval Δt and reaction temperature; pore size shows no clear trend. Nitrogen adsorption–desorption, FE-SEM and FE-STEM are reported. Full article remains uninspected.
- Updated PSG-030 assessment and database record; explicitly separated measured final-powder trends from the authors' percolation/packing interpretation and from wet-gel syneresis, which was not measured.
- Reassessed PSG-028 and PSG-029 using expanded publisher previews. Added the cation-specific qualification for lithium-silicate gel ripening and the reported SAXS/FTIR/chemical-analysis methods and Si7-type species in concentrated basic sodium silicate.
- Updated source assessments and claim-evidence matrix; no claims transfer these basic HCl-acidified silicate systems directly to industrial sulfuric-acid precipitated silica.
- Database remains at 30 records; structural validation to be rerun after this batch.

## 2026-11-11 — Full-text drying study and final-product confounder

- Added PSG-031 (Sarawade et al., 2011) after inspecting the full article PDF.
- Extracted the common wet-gel preparation and three drying routes (oven, microwave, pilot-plant spray drying), including reported endpoint texture values.
- Added `LITERATURE/source_assessments_batch_09.md` and C17 in the claim-evidence matrix.
- The drying study shows substantial protocol-dependent differences in final surface area, pore volume, pore diameter, porosity and tapping density. It does not measure wet-gel syneresis.
- Flagged an internal method-label ambiguity: Table 1 calls the surface-area method “BJH” while the paper otherwise discusses BET surface area. Avoid treating this as resolved.
- Database now contains 31 records; structural validation pending.
- Added a research-family note linking Sarawade et al. (2011) and Quang et al. (2012) as complementary outputs from the Hanyang/Sarawade–Quang–Kim programme, not independent external replications.

## 2026-11-11 — Source-integrity correction and method-label clarification

- Rechecked the ScienceDirect preview for PSG-030 (Quang et al., 2012) and found a serious title/abstract-content mismatch: the preview text shifts to aerogel modification, MTMS/TMCS and calcination rather than clearly describing the titled pilot-scale precipitated-silica gelation study.
- Withdrawn the previously inferred directional Δt/temperature/BET/pore-volume claims. PSG-030 is now marked verification-pending and quarantined; it no longer supports a substantive claim in the evidence matrix.
- Corrected the Sarawade et al. (2011) methods note: Section 2.4 specifies BET for specific surface area and BJH/desorption for pore volume and pore-size distribution, whereas Table 1 labels the surface-area column “BJH method”. Table 2 labels area as BET. This is an internal table-label inconsistency, likely typographical, not a reason to reclassify the measured endpoint trends.
- Clarified that the paper's stated RMS/replicate treatment explicitly covers porosity, packing density and absorption metrics; uncertainty for nitrogen-sorption values is not clearly reported.

## 2026-11-11 — Quang et al. source-integrity resolution (qualified)

- Further cross-checked PSG-030 against the ResearchGate publication page, which exposes publication-specific highlights and figure/full-text excerpts (including the BET-vs-Δt result at 40 and 60 °C).
- The ScienceDirect preview does contain relevant opening abstract text but appends unrelated aerogel-modification/calcination content. This is treated as publisher-page/indexing contamination rather than evidence that the article itself is mismatched.
- Restored the bounded directional trends to PSG-030 and C16, but kept the source at provisional class B because the original publisher PDF has not been independently inspected.
- The review claim remains strictly about final powder endpoints; no direct wet-gel syneresis mechanism is inferred.
