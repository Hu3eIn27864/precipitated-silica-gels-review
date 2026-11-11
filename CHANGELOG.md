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
