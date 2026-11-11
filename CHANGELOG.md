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


## 2026-11-11 — 3-D C++ Monte Carlo workstream selected

- Reframed the preferred microscopic candidate as a 3-D off-lattice Monte Carlo model, motivated by (but not claiming to reproduce) Schlomach & Kind (2007) and Sahabi & Kind (2011).
- Specified a first scientific question, approximately 1000-particle starting scale, local translation/rearrangement, coordination-dependent detachment, reattachment, reversible/persistent contacts, structural observables, and verification requirements.
- Explicitly separated equilibrium Metropolis sampling from kinetic/rate-based events and stated that MC sweeps are not physical time without independent calibration.
- Clarified that imposed box compression is not equivalent to solvent drainage; the MC model will initially address structural reorganisation, while continuum transport remains a complementary workstream.
- Added `MODELLING/monte_carlo_3d/README.md` as a design specification. No C++ code or simulation results are claimed yet.
- Added a carefully bounded note on touch-screen coatings: silica aggregates and silica-sol coatings occur in anti-glare / optical surface applications, but this does not establish precipitated silica as the specific feedstock in those examples.


## 2026-11-11 — Multiscale MD–MC–CFD coupling architecture specified

- Added `MODELLING/multiscale_coupling/README.md` describing a staged MD → 3-D MC → structural upscaling → Darcy/poroelastic continuum workflow.
- Defined the scientific feedback hypothesis linking contact evolution, stiffness, permeability, pore pressure, drainage and compaction.
- Distinguished direct atomistic interactions from aggregate-scale MC rearrangement and continuum pore-fluid transport; specified measurable hand-off variables.
- Prioritised one-way coupling and representative-volume upscaling before any bidirectional staggered coupling.
- Clarified that the appropriate first continuum model is generally porous-medium Darcy flow coupled to a deformable skeleton, not fully resolved CFD across all nanoscale pores.
- Added validation ladders and cautions about force-field validity, MC physical-time mapping, RVE convergence and independent validation. No coupled code or simulation result is claimed.


## 2026-11-11 — C++ 3-D Monte Carlo technical specification

- Added `MODELLING/monte_carlo_3d/TECHNICAL_SPEC.md` as the implementation contract for the first off-lattice C++17 Monte Carlo version.
- Specified reduced units, reproducible RNG/build metadata, periodic geometry and cluster unwrapping, DLCA/import-based initial aggregate generation, a transparent effective pair potential, V1 Metropolis moves, observables, software modules, and unit/integration tests.
- Separated reversible equilibrium sampling (V1) from coordination-dependent kinetic detachment, persistent contacts and compaction (V2) to avoid mixing irreversible kinetics into an equilibrium sampler.
- Explicitly excluded pore-liquid drainage, pore pressure, physical syneresis time, pH-dependent chemistry and calibrated silica force fields from V1. Box contraction is not treated as solvent removal.
- Updated the MC overview and modelling strategy to link to the technical specification. No C++ source code has been implemented and no simulation has been run, calibrated, or validated.


## 2026-11-11 — Initial C++ Monte Carlo software scaffold

- Added a C++17/CMake/CTest project scaffold under `MODELLING/monte_carlo_3d/`.
- Added `Vec3`, `Particle`, cubic periodic `SimulationBox` (wrapping, minimum-image displacement and distance), and a seeded `std::mt19937_64` wrapper.
- Added geometry tests for periodic wrapping, minimum-image distances and invalid box dimensions, plus build instructions.
- Updated the MC README and technical specification to distinguish committed source from unimplemented modules.
- Verification limitation: GitHub repository cloning was unavailable in the execution environment, so compilation and CTest could not be run. No test-pass claim, simulation, calibration, or physical validation is made.


## 2026-11-11 — C++ interaction and neighbour-list layer

- Added a generic shifted/truncated Lennard-Jones 12-6 pair potential with hard-core overlap rejection and explicit reduced-unit parameters. It is a software test potential, not a calibrated silica force field.
- Added brute-force total and single-particle local energy evaluators.
- Added a periodic neighbour candidate list with cutoff-plus-skin radius, minimum-image distances, and a conservative rebuild validity check at maximum displacement greater than skin/2.
- Added interaction tests for hard-core behaviour, cutoff continuity, zero-attraction limit, local-vs-full energy differences, neighbour-list agreement and invalid list geometry.
- Registered the new source and test target with CMake and updated the technical specification and implementation status.
- Verification status unchanged: repository cloning/network access is unavailable in the execution environment; C++ compilation and CTest have not been run. No simulation, calibration or physical validation is claimed.


## 2026-11-11 — Reversible Metropolis kernel added

- Implemented a C++17 single-particle translation sampler with symmetric component-wise uniform proposals, periodic wrapping, hard-core overlap rejection and Metropolis acceptance in reduced units (kBT = 1).
- Defined one sweep as exactly N attempted moves and exposed attempted/accepted counters and acceptance rate.
- Kept brute-force local energy evaluation in the sampler as the correctness-first baseline; the neighbour list is not yet integrated into move acceptance.
- Added seeded reproducibility, sweep-count, empty-system and invalid-step tests; registered the kernel and test with CMake/CTest.
- No compilation or CTest execution has been possible in the current network-restricted environment. No physical time, silica-specific force field, calibrated parameter, or syneresis prediction is claimed.

- Added GitHub Actions workflow `.github/workflows/mc3d-ci.yml` to configure, compile and run CTest on changes to the MC3D project. The workflow has been committed; no completed CI result is yet available, so build/test success remains unverified.


## 2026-11-11 — V1 kernel compiled and regression-tested

- Corrected an overlap in the original neighbour-list test fixture: the periodic separation of the selected pair was below the hard-core diameter, so both local-energy implementations correctly returned infinity and the test's finite-only comparison failed. The fixture now uses a non-overlapping periodic separation, and the comparison helper handles matching infinities explicitly.
- Added a seeded 60-particle neighbour-list skin test. After bounded particle displacements, every pair within the interaction cutoff must remain in the candidate list and list energies must agree with brute force.
- Added a 1000-sweep Metropolis regression test (4000 attempted moves) checking finite total energy and no hard-core overlap.
- Built the committed C++17 source snapshot with GCC 14.2.0 and CMake 3.31.6. Release build completed and CTest passed 3/3 targets (geometry, interactions, metropolis).
- Repeated the build in Debug with AddressSanitizer and UndefinedBehaviorSanitizer; CTest passed 3/3 targets.
- Verification is limited to the tested software kernel. The neighbour list is not yet integrated into Metropolis; aggregate generation, observables, physical parameter calibration, and experimental validation remain open. Hosted GitHub Actions status has not been confirmed.
- Detailed commands and environment are recorded in `MODELLING/monte_carlo_3d/TEST_RESULTS.md`.


## 2026-11-11 — DLCA-style aggregate generation and network observables

- Added a seeded rigid-cluster Brownian aggregation generator with periodic boundaries, random sequential non-overlapping monomer placement, a configurable mass-dependent cluster mobility law, finite-step continuous collision detection, and explicit completion/attempt/merge diagnostics.
- Added contact-graph analysis for coordination numbers, unique contacts, connected components, largest-component fraction, mean coordination, and graph-unwrapped cluster radius of gyration. Periodic winding/inconsistent unwrapping is explicitly flagged.
- Added a network regression test and registered a fourth CTest target.
- Initial isolated C++ smoke testing of the new algorithm/analysis interfaces compiled and ran the equivalent module harness; periodic Rg, deterministic seeds, particle non-overlap, contact graph and merge accounting passed. This was not a full build of the repository snapshot; the new CTest target still requires full-project/CI verification.
- Corrected the first aggregation draft after a test exposed endpoint-overlap risk: collision detection now locates first contact along the translation segment rather than accepting penetrative endpoint configurations.
- Scientific limits: this is a simplified rigid-cluster DLCA-style algorithm, not a hydrodynamic Brownian-dynamics solver. No cluster rotation, hydrodynamic interactions, lubrication, electrostatics, or reaction-limited sticking. The mobility exponent is an explicit algorithmic assumption; no fractal dimension or silica parameter is prescribed or claimed.
- No physical calibration, fractal-dimension fit, or experimental validation is claimed.

- Extended the network regression suite to check (R_g) invariance under translation across a periodic face and explicit detection of a periodic-winding component. Local equivalent-harness check passed; full CMake/CI status remains unconfirmed.


## 2026-11-11 — Periodic cell-list broad phase

- Added a periodic uniform-cell candidate generator with wrapped 3×3×3 queries, duplicate-cell suppression for small grids, finite-query validation, and overflow checks.
- Integrated the cell list into DLCA swept-contact broad-phase queries and post-contact cluster identification; exact minimum-image and swept-sphere tests remain authoritative. Brute-force fallback is retained near half-box search radii.
- Added regression coverage comparing candidate sets against brute-force neighbour checks, including periodic boundaries and a small grid.
- Isolated C++17 ASan/UBSan cell-list checks passed; a separate isolated 12-particle DLCA smoke run completed without overlaps. These are not a full repository CMake build or hosted CI result.
- Initial placement is still brute force and the grid is rebuilt per attempted move; production performance claims require benchmarks and further optimisation.

- Hardened periodic coordinate reduction with `std::fmod` and added regression assertions for negative query coordinates and non-finite query rejection. Full CTest execution remains pending.


## 2026-11-11 — Cell-list memory guard and randomized reference tests

- Capped dense periodic cell-list storage at 1,000,000 cells to avoid pathological allocations for sparse, large boxes.
- Added a safe DLCA fallback to exact brute-force candidate scans when the cell-list grid exceeds its allocation/dimension limits; the narrow-phase contact geometry remains unchanged.
- Added deterministic pseudo-random candidate-completeness checks against brute-force minimum-image distances and a regression for excessive dense-grid sizing.
- This is a robustness change, not a performance benchmark. The new tests are registered in CTest but have not yet been run in a complete repository build; hosted CI remains unverified.


## 2026-11-11 — Mass-radius power-law regression utility

- Added a standalone log-log OLS helper for caller-supplied mean enclosed mass versus radius, returning the candidate exponent, slope standard error, R², point count and explicit fit interval.
- Added synthetic exact-power-law recovery and invalid-input regression tests; registered the source in CMake.
- Explicitly limited interpretation: the helper does not construct mass-radius data, choose a fit interval, resolve periodic unwrapping/finite-size effects, or prove a fractal scaling regime. No silica fractal dimension is claimed.
- Full CMake/CTest execution remains pending.


## 2026-11-11 — Mean enclosed mass-radius curve generator

- Added `calculateMassRadiusCurve`, which computes the mean number of particles enclosed within each requested radius, averaging over all supplied particle centres and including the centre particle.
- The API explicitly requires graph-unwrapped coordinates for one non-winding component; it does not silently perform periodic unwrapping or choose a scaling interval.
- Registered the new C++ source with CMake and added an analytic three-particle test, rigid-translation invariance, and invalid-radius rejection.
- The committed estimator source passed an isolated C++17 GCC ASan/UBSan analytic harness. This is not a full CMake/CTest result; the complete network test target remains unverified.
- Runtime is O(N² N_r); no large-system performance claim, fitted fractal dimension, or silica validation is made.


- Follow-up integration: network observables now retain graph-unwrapped component coordinates, and the network test source passes a periodic-boundary cluster directly into the mass-radius estimator. Winding components remain explicitly flagged and must be excluded from fractal fitting. This integration assertion is committed but awaits the full CMake/CTest run.


## 2026-11-11 — Mass-radius numerical hardening and known-geometry check

- Removed per-centre temporary distance-vector allocation from the mass-radius inner loop; the transparent estimator remains O(N² N_r).
- Earlier implementation rejected radii whose squared value overflowed; this was superseded by std::hypot-based distance comparison in the 2026-11-11 follow-up.
- Added a finite 1001-particle straight-chain regression. The expected exponent is near, not exactly, one because finite-chain boundaries bias mean enclosed mass. The test uses an explicit 0.05 exponent tolerance and R² > 0.995.
- An isolated C++17 GCC ASan/UBSan harness returned Df=0.964034 and R²=0.999992 for that geometry. This is not a full repository CMake/CTest result.


## 2026-11-11 — Fit-window sensitivity and robust mass-radius distances

- Added `scanMassRadiusFitWindows`, enumerating all contiguous fit windows with a configurable minimum point count. It is diagnostic only and does not select a physically valid scaling interval.
- Replaced squared-distance comparison in the mass-radius estimator with `std::hypot` to improve numerical robustness for large finite coordinates.
- Added test-source cases for exact power-law window stability, a constructed crossover, and large-coordinate distance evaluation. Full CMake/CTest execution remains outstanding.
- Corrected the earlier documentation: the estimator no longer rejects radii merely because their square overflows; it uses a stable distance comparison instead.


## 2026-11-11 — Compact and branched reference geometries

- Added finite cubic-lattice and three-arm cross reference cases to the mass-radius network tests to check distinction between compact and simple branched geometries.
- An isolated C++17 ASan/UBSan harness returned slopes 2.33099 and 1.07112, respectively. The full repository CMake/CTest suite remains unverified.


## 2026-11-11 — DLCA ensemble export and plateau-safe fitting

- Added the `mc3d_dlca_ensemble` executable with consecutive seed runs and separate run-summary, mass-radius and fit-window CSV outputs.
- Added safeguards to omit incomplete aggregates and periodic-winding components from whole-aggregate mass-radius analysis while preserving their run metadata.
- Fit-window scans now skip singular plateau-only intervals and return an empty result for a constant mass curve; input validation remains global.
- Added plateau-handling tests and documented command-line arguments, default reduced-unit settings and output schemas. The complete CMake build and end-to-end ensemble run remain unverified.


## 2026-11-11 — End-to-end DLCA ensemble smoke test registered

- Added a CTest smoke-test script that invokes the ensemble CLI with a small deterministic configuration and checks that all three CSV outputs exist and carry the expected headers.
- Registered the smoke test as the fifth CTest entry; the existing GitHub Actions workflow will run it on the next matching push or pull request.
- The smoke test deliberately checks the output contract rather than requiring stochastic aggregation completion or non-empty fit output.
- Updated the MC3D overview, example instructions and test record to state the new verification boundary. No build or CI pass is claimed until the workflow completes.


## 2026-11-11 — DLCA smoke-test row validation strengthened

- Extended the end-to-end CMake smoke script to require exactly one run-summary data row for the requested seed and validate its basic metadata structure.
- Re-ran the script locally against a temporary stand-in executable; the CMake harness passed. This does not substitute for building or running the actual C++ program.

 
## 2026-11-11 — Seed-level DLCA ensemble statistics

- Added a standard-library analysis script to compare independent DLCA runs across explicitly supplied particle counts using one common, predeclared mass-radius fit interval.
- Reports per-size completion/unwrapping/fit fractions, largest-component fraction, and per-seed exponent and Rg descriptive statistics.
- Excludes incomplete and periodically winding aggregates from exponent statistics; overlapping fit windows are not treated as independent observations.
- Added unit tests for fixed-window extraction, run exclusions, undefined Rg and duplicate seeds. Tests are committed but not yet executed.

- Extended the MC3D GitHub Actions workflow to run the Python ensemble-analysis unit tests in addition to the C++ build and CTest suite.

 
- Added a reproducible DLCA size-series runner with constant reduced number density and a corresponding scaling/input test. Documented a pilot workflow for (N=32,64,128) and a common diagnostic fit interval, with explicit caveats against interpreting it as silica calibration or proof of fractal scaling.

- Strengthened DLCA ensemble analysis by validating fit provenance against the underlying mass-radius observations, including system particle count, finite positive data, common radius grids, and fit point-count consistency.

- Added integrity checks for DLCA ensemble summaries: largest-component size cannot exceed the system size, and a completed run must contain all simulated particles in its largest component. Added a regression test for inconsistent completion metadata.

- Changed the DLCA size-series runner to allocate non-overlapping pseudorandom seed blocks across particle counts, avoiding accidental reuse of identical initial random streams in unpaired size comparisons.

- Added a regression test that rejects a DLCA fit summary when its point count disagrees with the underlying mass-radius observations; corrected the broad-window fixture to reflect its actual six source radii.
- 2026-11-11: Strengthened DLCA ensemble provenance validation by cross-checking mass-radius and fit rows against run-summary seeds and completion/unwrapping flags; added regression tests for orphaned fit rows and observations attached to unfinished runs. Full repository CI remains unverified.

- 2026-11-11: Fixed a periodic DLCA swept-collision edge case by testing neighbouring periodic images in the narrow phase; added deterministic regression coverage. C++ build/CTest execution remains pending.
- 2026-11-11: Isolated GCC C++17 compile and three-case runtime harness passed for the new periodic swept-collision helper using a minimal Vec3-compatible test interface. ASan execution was blocked by the environment's runtime-loading configuration; full CMake/CTest remains pending.
- 2026-11-11: Added deterministic randomized validation of periodic swept collision against 500 sampled trajectories (2,001 time fractions each); isolated GCC C++17 harness passed. The test explicitly uses r(t)=r(0)-clusterShift*t and verifies reported contact points.
- 2026-11-11: Added a fit-window sensitivity audit with unit tests, integrated it into the DLCA pilot workflow, and documented interpretation/validation gates. Hosted execution remains pending verification.
- 2026-11-11: Hardened the independent 1-D consolidation baseline against non-finite inputs; added series-truncation convergence tests and included its unit tests in CI.

## 2026-11-11 — Radial geometry scaling and DLCA parameter controls

- Added a standard-library utility for the ideal first-mode radial relations in infinite cylinders and spheres, including inverse conversion to diagnostic apparent diffusivity and finite/positive input checks.
- Added tests for inverse consistency and radius-squared scaling. This is a first-mode scaling utility, not a full transient radial consolidation solver or a direct permeability measurement.
- Extended the DLCA ensemble CLI with optional contact distance, maximum component displacement and mobility exponent; retained the original six-argument invocation through defaults.
- Recorded these three parameter values in each run-summary row and added them to the size-series runner so controlled sensitivity ensembles can be launched and traced.
- Updated the CMake smoke test to exercise non-default parameters and check the expanded output schema. Source and test changes are committed; full C++ build, CTest and Python repository test execution remain unverified in this environment.
- 2026-11-11: Normalised the DLCA mass-radius grid to multiples of the configured contact distance, keeping fit-window coordinates comparable in dimensionless contact units across contact-distance sensitivity runs. Updated the pilot protocol and usage notes; full C++/CI execution remains pending.
- 2026-11-11: Added a predeclared one-factor-at-a-time DLCA parameter-sensitivity plan with paired seed blocks, dimensionless fit bounds, and explicit completion/selection-bias reporting. No sensitivity simulations have been run yet.

- 2026-11-11: Added a bounded paired-seed DLCA parameter-sensitivity runner and unit tests; integrated six non-baseline one-factor variants into CI with per-variant summaries, fit-window audits and raw artifact retention. The full sensitivity matrix remains a separate, larger study; hosted execution is pending.

- 2026-11-11: Corrected the paired-seed sensitivity design: the baseline is now run inside the same N=32, seed-3000 block as all six one-factor variants, rather than reusing the separate pilot baseline with different seeds. CI analyses and retains outputs for all seven configurations.

- 2026-11-11: Added a paired seed-level sensitivity analyser and tests. It checks identical seed sets, retains incomplete runs, calculates largest-component-fraction deltas for all paired seeds, and restricts Rg/exponent deltas to pairs where both values are defined. Integrated paired summaries into the CI sensitivity workflow; no simulation result or CI pass is claimed.


- 2026-11-11: Hosted MC3D CI run #220 passed the Release build, all five CTest targets, MC3D Python analysis tests, 1-D transport tests, DLCA size-series pilot, and seven-configuration paired sensitivity screen. Uploaded artifacts were inspected. Size-series completion was 2/3 (N=32), 0/3 (N=64), and 0/3 (N=128); only two N=32 fits were available and the within-run fit-window exponent range averaged 0.394. The paired sensitivity baseline completed 0/3, leaving no valid paired Rg or Df comparisons. These are software/pilot diagnostics, not evidence for silica-specific scaling or physical parameter selection. See MODELLING/monte_carlo_3d/TEST_RESULTS.md.


- 2026-11-11: Added cumulative squared realized cluster translation and cumulative realized cluster-translation path length to DLCA run metadata. Extended the deterministic reproducibility assertions and smoke-test CSV contract. These diagnostics will support future equal-displacement comparisons; they are not physical time. Hosted validation is pending.


- 2026-11-11: Hosted CI run #234 passed after adding realized-displacement diagnostics to the DLCA result and CSV schema. The new metrics showed mean cumulative squared translation 2,000.71 for the baseline step 0.2 versus 500.30 for step 0.1 after the same 50,000 attempts; step 0.28 completed in a mean 25,665 attempts at mean cumulative squared translation 2,011.66. This confirms that fixed-attempt step-size comparisons mix structural and algorithmic-clock effects. A common-displacement stopping criterion is the next planned improvement.


## 2026-11-11 — Parallel next-step plan

- Added `MODELLING/NEXT_STEPS_PARALLEL_PLAN.md` with independently executable workstreams for pilot artifact audit, common-displacement DLCA protocol, radial transport solver verification, literature/validation evidence, and manuscript synthesis.
- Explicitly gated the full DLCA size matrix on completion, unwrapping, fit-window stability, and common algorithmic displacement; no physical-time or silica-calibration interpretation is permitted.
- Plan records current hosted CI verification boundary and distinguishes the latest successful workflow from physical model validity.


## 2026-11-11 — Parallel roadmap literature verification
- Extended `MODELLING/NEXT_STEPS_PARALLEL_PLAN.md` with a targeted source-verification note for Scherer's silica-gel syneresis studies (1989, 1996) and an infinite-cylinder consolidation numerical-method comparator.
- Clarified that permeability and network viscoelasticity/stiffness jointly control response; an effective consolidation coefficient must not be interpreted as permeability alone.
- Preserved transferability limits: the Scherer studies are mechanistic comparators and are not automatically independent validation data for industrial precipitated silica.
- No model parameters were fitted and no new physical claim was promoted to established fact.


## 2026-11-11 — Radial transport analytical benchmark
- Added volume-averaged eigenfunction-series references for the idealised infinite-cylinder and sphere diffusion/consolidation problems to the parallel work plan.
- Specified the initial condition, centre symmetry, perfectly drained outer boundary, volume-average weights, and first-mode time constants.
- Required finite-difference validation against the full series and retained explicit limits: constant effective coefficient, no evolving permeability or nonlinear skeleton mechanics, and no finite-cylinder end drainage.


- 2026-11-11: Downloaded and independently audited the raw artifact from hosted CI run #237 (artifact 13851749184). Added seed-level size-series outcomes, per-variant completion/Q/L summaries, fixed-window fit eligibility, fit-window sensitivity, and paired-comparison eligibility to `MODELLING/monte_carlo_3d/TEST_RESULTS.md`. Reconfirmed no valid completed baseline/variant Rg or Df pairs and no basis for finite-size scaling; full matrix remains gated. Common-Q stopping is the next DLCA implementation task, with Q and L both retained as algorithmic (not physical-time) progress diagnostics.


- 2026-11-11: Added a transient radial finite-volume benchmark for ideal infinite-cylinder and sphere consolidation, with backward-Euler time integration, conservative radial volume weighting, and independent eigenfunction-series references. Five isolated local unit tests passed, including series agreement and grid/time refinement. Added the transport-model path to CI triggers; hosted validation is pending. This is numerical verification work, not experimental validation or a silica-specific model.
- 2026-11-11: Completed seed-level audit of run #237 artifact and documented raw completion outcomes, per-variant movement diagnostics, fit eligibility, fit-window sensitivity, and the no-go decision for the full size matrix pending common-displacement stopping.


- 2026-11-11: Hosted CI run #239 passed after adding the radial finite-volume transport benchmark; the Release build, five CTest targets, Python analysis tests, and full transport test discovery all passed.
- 2026-11-11: Added optional common cumulative squared realized-translation stopping to the DLCA core and CLI, retaining legacy fixed-attempt behaviour at target Q=0. Added stop flags, independent attempt-cap status, and Q overshoot to run metadata; extended C++ tests, CLI smoke coverage, and Python runners with --target-q. Intermediate CI attempts exposed a mismatch between the expanded CSV header and row writer; corrected the writer and smoke assertion before final validation.
- 2026-11-11: Hosted CI run #254 passed the Release build, all five CTest targets, Python analysis tests, radial transport tests, fixed-attempt DLCA pilot/sensitivity workflow, and the new common-Q paired screen. At Q=450 all 21 N=32 runs reached the target without hitting the cap, but none completed aggregation. Equal Q did not equalise path length: mean L was about 4,321 (step 0.10), 2,159 (step 0.20), and 1,542 (step 0.28). No Df or completed-pair Rg comparison is available. See MODELLING/monte_carlo_3d/TEST_RESULTS.md.
- 2026-11-11: Added PSG-044, Scherer (1995), on pH-dependent silica-gel permeability and viscoelastic relaxation. The source is classified as a transferability-limited mechanistic comparator (class B); original full text and target-system precursor chemistry remain unverified.


- 2026-11-11: Audited the full CI #257 artifact. The fixed-attempt size pilot completed 2/3 N=32 runs and 0/3 at N=64/128; no cross-size Df inference is supported. Added Q/attempt, path-length/attempt and Q/successful-merge diagnostics to the written analysis.
- 2026-11-11: Added PSG-045, Manfoumbi, Roger & Meireles (2024), DOI 10.5802/crchim.347, to the literature database, source assessments and evidence matrix. The study links precipitation/pH history to SAXS-observed mesostructure and filtration-cake resistance; the assessment explicitly separates cake resistance from intrinsic gel permeability and syneresis.
- 2026-11-11: Began the next DLCA observability increment: core result now accumulates cluster-selection count, cumulative Q and path length by pre-move cluster-size class. Added conservation/reproducibility tests, per-size mobility CSV output and documentation. Hosted CI validation is pending.

- 2026-11-11: Extended size-resolved DLCA trajectory accounting to attribute successful component merges to the selected cluster's pre-move size class. Tests verify per-size merge totals equal the run-level successful-merge count; the mobility CSV exports the new field. Hosted CI validation pending.

- 2026-11-11: DLCA now distinguishes move-level successful merge events from the number of absorbed components. Per-size and run-level counters, CSV export, reproducibility/conservation tests and CLI smoke schema updated. Hosted CI validation pending.

- 2026-11-11: Added PSG-046, Ragueh et al. (2015), full author manuscript assessment. This provides direct industrial precipitated-silica SAXS/TEM, filtration-derived cake permeability and osmotic compression/percolation evidence, with explicit caveats against direct transfer to syneresis permeability.

- 2026-11-11: Added run-level `successful_merge_events` to DLCA run-summary CSV so per-size event totals can be independently reconciled in uploaded artifacts; updated CLI smoke schema and row validation. Hosted CI pending.

- 2026-11-11: Stabilised early-time evaluation of the analytical 1-D consolidation benchmark using the Poisson-transformed short-time asymptotic for dimensionless time below 0.01; added term-independence, square-root scaling and branch-continuity tests. Hosted CI pending.

- 2026-11-11: The new branch-continuity test exposed an incorrect eigenvalue exponent in the planar consolidation series (a factor of \(\pi^2/4\) was inverted). Corrected the exponent to \((2m+1)^2\pi^2 T_v/4\), and added an independent reference-value regression test at \(T_v=0.1\). The earlier CI failures were genuine test detections; rerun validation is in progress.

- 2026-11-11: Added corrected dimensionless planar-consolidation reference values and explicit identifiability note (c_v=k/(m_v\gamma_w)); expanded radial cylinder/sphere tests to check convergence under grid and time-step refinement. Hosted CI validation pending.

- 2026-11-11: Hosted CI #293–#295 passed expanded radial cylinder/sphere convergence checks and the corrected planar consolidation reference-table regression tests; full integrated DLCA and transport workflow passed in #295.


## 2026-11-11 — Parallel transport/data workstreams

- Added `LITERATURE/experimental_syneresis_comparison.csv` with 18 geometry- and protocol-tagged syneresis records, preserving fitted-parameter status and unresolved drainage conditions; validated all rows against a 17-column schema.
- Added a finite-cylinder first-mode time-constant helper with drained-end and sealed-end limits; added tests for the infinite-cylinder limit and geometry scaling.
- Added `poroelastic_coupling.py` for the classical `c_v = k M / gamma_w` identity and algebraic inversion, keeping permeability and constrained modulus separate and avoiding uncalibrated constitutive laws.
- Added regression tests for both additions and documented their strict limits: code verification only, no experimental calibration or silica-specific constitutive validation.

## 2026-11-11 — Dimensional correction of consolidation coefficient

- Distinguished hydraulic conductivity K [m/s] from intrinsic permeability κ [m²] throughout the coupling implementation.
- Added separate identities and inverses: cv = K M / γw and cv = κ M / μ.
- Corrected the README parameter-identifiability explanation; no generic 'permeability' symbol is used for both quantities.

## 2026-11-11 — Source-verified geometry and curve extraction plan

- Audited the open Wilhelm & Kind (2015) article and KIT dissertation for sample geometry and thermal/boundary conditions.
- Documented a conditional cylinder-height estimate (~26.5 mm from 12 mm diameter and ~3 mL, assuming a right circular cylinder) as derived, not measured.
- Flagged the ~3 mm droplets as confined in a sealed PMMA microscopy cell, so a free-sphere boundary cannot be assumed.
- Added a reproducible curve-digitisation protocol separating measured markers from empirical fit curves and keeping pressure-cell and centrifugal datasets distinct.
- No raw curve points were fabricated or added; curve digitisation remains an explicit next step.


- 2026-11-11: Added 14 separate pressure-cell forced-syneresis fit records from Wilhelm & Kind (2015), Table 3, preserving pressure intervals, initial height and membrane boundary metadata. Documented why these records must not be pooled with the 2017 centrifugal series.
