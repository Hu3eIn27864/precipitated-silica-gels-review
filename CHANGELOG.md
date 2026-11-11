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

## 2026-11-11 — Geometry-resolved syneresis extraction

- Re-read Wilhelm & Kind (2015) in the publisher full text and extracted the distinct natural-syneresis datasets for 12-mm cylinders (~3 mL) and ~3-mm droplets.
- Recorded that acid-catalysed cylinders show ~0.20 maximum shrinkage across 20–60 °C, whereas acid droplets show fitted maxima rising ~0.37→0.48; base-gel maxima rise ~0.30→0.51 in both reported geometry series, but characteristic times differ strongly.
- Added the droplet protocol's initial 20 °C period and subsequent temperature change as a thermal-history caveat.
- Refined C06/C07: geometry and drainage length are part of the measured response; “analogous” parameter dependencies between natural and enforced syneresis must not be read as quantitative or mechanistic equivalence.
- This reinforces the comparison rule: report geometry, drainage boundary, sample age and thermal history with every syneresis number.

## 2026-11-11 — Independent alkaline waterglass syneresis comparator (PSG-032)

- Added Hamouda & Akhlaghi Amiri (2014), *Energies* 7, 568–590, DOI 10.3390/en7020568, after inspecting the complete publisher text.
- Added assessment batch 10 and database record PSG-032. The study measures expelled-liquid mass from sealed alkaline sodium-silicate gels (3–6 wt%, HCl-adjusted pH 8.6–10.7), varying concentration, pH, temperature, divalent ions, pressure and container material.
- Key caution: the authors infer shrinkage from expelled-liquid mass under an equal-density assumption; this is not geometric ΔV/V0. Glass versus polypropylene changes the measured one-week shrinkage strongly (~2.3 vs ~12 wt% in one comparison).
- Added bounded claim C18 as an independent mechanistic comparator only. The system is dilute, alkaline and HCl-acidified, not industrial sulfuric-acid precipitated silica. Do not pool its numerical data with the Wilhelm geometric shrinkage series.

## 2026-11-11 — Alkaline granular consolidation and historical syneresis leads

- Added Kouassi et al. (2011), *Journal of Non-Crystalline Solids* 357, 3013–3021, DOI 10.1016/j.jnoncrysol.2011.04.006, as PSG-033. Publisher abstract and extended indexed text inspected; original PDF not accessed.
- The study combines concentrated HCl-acidified waterglass gel with crystalline silica powder and sand. Weight loss, FTIR, SEM and compression tests track composite consolidation. FTIR evolution is interpreted as dissolution/precipitation and the mechanical response depends on fine-silica content.
- Explicitly bounded the result: composite weight loss is not an isolated-gel syneresis measurement; crystalline silica/sand and alkaline waterglass differ from industrial amorphous acid-precipitated silica. Added C19 as mechanistic comparator only.
- Added historical leads Holmes, Kaufmann & Nicholas (1919), DOI 10.1021/ja02230a002, and Ferguson & Applebey (1930), DOI 10.1039/TF9302600642, as H-001/H-002 with status V. Holmes bibliographic metadata is confirmed by ACS, but full text is paywalled. Ferguson title/authors/year/DOI are indexed, while full pagination and publisher record remain to verify. No historical mechanistic claims are made.


## 2026-11-11 — Waterglass-mediated granular consolidation comparator

- Added PSG-034 (Lucas et al., 2011), *Journal of Non-Crystalline Solids* 357(4), 1310–1318, DOI 10.1016/j.jnoncrysol.2010.12.016, using the publisher record and extended article preview.
- The study combines quartz sand with alkaline sodium silicate and examines drying-temperature, sand-size and solution-dilution effects using thermal analysis, SEM, ICP, ATR-FTIR and compression testing.
- Added a bounded C20: the reported 70 °C glass-like adhesive layer and 150 °C dissolution–precipitation mechanism are author interpretations for a drying granular composite, not direct evidence for wet precipitated-silica gel syneresis.
- Added source assessment batch 12 and flagged the Tognonvi/Rossignol research-family relationship with Kouassi et al. (2011); independent dataset status remains to be checked.
- Database now contains 36 records; structural validation to be performed.


## 2026-11-11 — Modulus evolution during silica-gel syneresis (PSG-013 appraisal)

- Verified Scherer (1989), *Journal of Non-Crystalline Solids* 109, 183–190, DOI 10.1016/0022-3093(89)90030-6, against the Elsevier publisher record and abstract.
- Upgraded the bibliographic record and bounded the reported result: alkoxide-derived silica gels stiffen during syneresis; drying produces a much larger modulus increase with substantial contraction.
- Kept PSG-013 in class C as an abstract-level mechanistic comparator, not direct evidence for industrial precipitated silica. Full text remains uninspected.
- Added a detailed assessment to batch 01. The review synthesis should distinguish volume loss, permeability and modulus rather than treating shrinkage as a proxy for mechanical consolidation.


## 2026-11-11 — Syneresis transport–mechanics framework (Scherer 1989 Parts I–II)

- Added PSG-037 and PSG-038 for Scherer's *Mechanics of syneresis* Parts I and II, with publisher-verified metadata and abstract-level appraisal.
- Part I predicts sample-size/geometry dependence through pore-liquid flow resistance and network viscoelasticity; Part II reports reasonable agreement between shrinkage curves and calculations using independently measured permeability, modulus and viscosity.
- Added C22 as a bounded mechanistic framework. Exact precursor chemistry, assumptions, sample geometry and uncertainty require full-text inspection; no direct industrial precipitated-silica equivalence is assumed.
- Added source assessment batch 14. The synthesis now explicitly treats syneresis kinetics as coupled to transport and mechanical properties, not as a volume-change-only process.


## 2026-11-11 — Soviet-era polysilicic-acid hydrogel literature mapped (batch 15)

- Added PSG-039–PSG-042: Ponomareva et al. (1984) on hydrogel shrinkage kinetics; Kontorovich et al. (1988) on temperature-dependent syneresis; Kontorovich et al. (1988) on elastic modulus during syneresis; and Kontorovich et al. (1991) on electrolytes, polycondensation and syneresis.
- Bibliographic records are based on later scholarly reference lists and accessible institutional documents. Original journal texts have not yet been located; all four entries are marked V (verification pending), with no result inferred from title.
- Created source assessment batch 15. Flagged a pagination discrepancy for the 1991 paper (126–128 vs 126–129) and possible research-family/data overlap among the Kontorovich–Ponomareva–Sokolova group.
- No new claim was added to the evidence matrix because the primary experimental results remain unverified. These papers are retrieval priorities, not yet evidence for the review's conclusions.


## 2026-11-11 — Multiscale modelling workstream defined

- Added `MODELLING/modeling_strategy.md` to define a hypothesis-driven simulation pathway alongside the literature review.
- Distinguished coarse-grained LAMMPS network modelling, continuum poromechanics / OpenFOAM, CFD–DEM (including possible OpenFOAM–LIGGGHTS coupling), and atomistic MD / Monte Carlo by the questions each can and cannot answer.
- Set minimum requirements for parameter provenance, sensitivity, numerical checks, independent validation and reproducibility.
- Explicit go/no-go decision: no production simulations yet. Complete the evidence audit and identify a falsifiable, data-constrained question first; prefer the smallest adequate model.


## 2026-11-11 — Published validation-data roadmap

- Added `MODELLING/validation_data_roadmap.md` to map candidate published benchmarks to possible model classes.
- Prioritised direct precipitated-silica syneresis data from Wilhelm & Kind (2015), aggregation/fragmentation data from Schlomach & Kind (2004) and Quarch et al. (2010), and mechanistic continuum benchmarks from Scherer (1989).
- Identified a CC BY 4.0 public colloidal-silica transport dataset from the University of Strathclyde as an adjacent software/transport benchmark, not direct syneresis validation.
- Distinguished target-system validation from TEOS-derived and generic colloidal-silica comparators; recorded independent-validation and research-family overlap rules.
- No simulation has been run or calibrated; digitisation, full-text checks, and data suitability assessment remain pending.


## 2026-11-11 — First executable transport and LAMMPS prototypes

- Added a dependency-free Python 1-D double-drained slab consolidation benchmark in `MODELLING/transport_model/`, using the classical linear pore-pressure diffusion series and an explicitly prescribed ultimate shrinkage.
- Added a LAMMPS coarse-grained compression/unloading prototype and seeded network-data generator in `MODELLING/lammps_network/`.
- The LAMMPS prototype uses reduced LJ units, truncated/shifted LJ non-bonded interactions, permanent harmonic links, NVT equilibration, affine box compression/unloading, coordination output and pressure/box observables.
- Both prototypes are explicitly non-predictive baselines: the transport model is constant-coefficient 1-D poro-consolidation; the LAMMPS network is a jittered lattice, not measured fractal silica, and has no solvent, chemistry, or dynamic bond kinetics.
- Added execution instructions, assumptions, validation checks and model limitations. No parameter calibration or production simulation has been performed.
- LAMMPS command choices checked against the official manual for `pair_style lj/cut`, `bond_style harmonic`, and `fix deform`.


## 2026-11-11 — Transport benchmark refinement and LAMMPS network correction

- Added PSG-043, Scherer & Swiatek (1989), on pressure-driven permeability measurement in alkoxide-derived silica gels; added detailed assessment in `LITERATURE/source_assessments_batch_16.md`.
- Refined the validation roadmap: Scherer (1989) Parts I–II are currently a mechanistic/conceptual benchmark, not a numerically reproducible benchmark from accessible abstracts. Raw shrinkage series, independent parameter tables, exact material chemistry and uncertainty remain to be retrieved.
- Explicitly separated the permeability paper's partial-drying result from wet-gel syneresis; no direct transfer to industrial precipitated silica is assumed.
- Corrected the LAMMPS toy-network generator to include periodic nearest-neighbour bonds across all box faces, avoiding an artificial unbonded boundary in the periodic simulation cell. The simple-cubic topology remains an acknowledged idealisation.
- No simulations were executed and no physical silica parameters were fitted.


## 2026-11-11 — Transport-model code checks

- Added `MODELLING/transport_model/test_syneresis_1d.py` with checks for the initial condition, long-time limit, monotonicity and dimensionless scaling.
- Documented how to run the tests. These verify mathematical/code behaviour only and do not constitute validation against experimental silica-gel data.


## 2026-11-11 — Natural syneresis parameters extracted by geometry

- Re-inspected the open publisher full text of Wilhelm & Kind (2015), including the experimental methods, Tables 1–2 and the model discussion.
- Added 12 natural-syneresis fit-parameter records (maximum relative volume decrease and characteristic time constant) for acid/base gels, three temperatures, and cylinder/droplet geometries to `LITERATURE/quantitative_extraction_syneresis.csv`.
- Added `LITERATURE/source_assessments_batch_17.md` to document the extraction, source context, and limits. These are published empirical fit parameters, not digitised raw time-series or direct transport measurements.
- Updated `MODELLING/validation_data_roadmap.md` to distinguish tabulated fit parameters from raw curve data and supplementary forced-syneresis material.
- Added `MODELLING/transport_model/geometry_scaling_note.md` with a first-eigenmode dimensional diagnostic for idealised radial cylinder/sphere diffusion. Apparent diffusivities are explicitly not treated as measured material properties.
- Key model limitation recorded: the article's exponential shrinkage law is empirical; the authors state that a physically based model remained future work. A universal slab consolidation coefficient must not be fitted across cylinders and droplets without resolving geometry, boundary conditions and thermal history.
