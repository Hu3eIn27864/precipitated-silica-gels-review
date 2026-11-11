# Initial evidence assessment — core precipitated-silica literature

**Status:** first-pass evidence map, 11 November 2026. This is a working research record, not a completed systematic review. Bibliographic verification, abstract inspection and full-text appraisal are tracked separately in `literature_database.csv`.

## 1. Evidence hierarchy

- **A — direct/core:** studies on inorganic precipitated silica made from silicate precursor and acid, directly measuring precipitation, gelation, consolidation or syneresis.
- **B — mechanistic comparator:** silica systems or models that illuminate a mechanism but differ in preparation route, chemistry, geometry or boundary conditions.
- **C — contextual:** foundational colloid or drying literature that may be cited sparingly for general concepts.
- **D — exclude:** outside scope or insufficiently reliable.
- **V — verification pending:** workflow status only; not a quality grade.

Evidence tags: **OBS** direct observation/measurement; **CALC** quantitative analysis/calculation; **SIM** simulation; **MODEL** theoretical or fitted model; **REVIEW** secondary synthesis; **HYP** hypothesis/inferred mechanism.

## 2. Core studies: first-pass appraisal

### PSG-001 — Schlomach & Kind (2004), semi-batch precipitation
**System and methods:** precipitation from sodium silicate and sulfuric acid; aggregation followed by photon-correlation spectroscopy. The paper divides the process into primary-particle production, aggregation to the gel point, and post-gel fragmentation/compaction.

**What it supports:** a process-history view in which the material structure evolves across distinct stages rather than being described by a single “particle formation” event. The reported aggregate fractal dimension rises from approximately 1.8 to approximately 2.4 after the gel point and then remains roughly constant over the reported interval.

**What it does not establish:** that these fractal dimensions are universal across precipitated-silica recipes, mixers, ionic strengths or scales; nor that the observed post-gel changes alone determine final product porosity or surface area.

**Appraisal:** A / OBS+CALC. Foundational direct evidence. Full-text extraction must capture recipe, sampling protocol, validity of photon-correlation analysis in the evolving concentrated system, and uncertainty of the fractal-dimension estimate.

### PSG-002 — Quarch & Kind (2010), gelation kinetics and gel properties
**System and focus:** inorganic precipitated silica gel; gelation kinetics and resulting gel properties.

**Role:** direct bridge between precipitation conditions and the state of the gel at/after gelation. It should be cross-read with Schlomach & Kind (2004), not treated as independent confirmation until overlap in experimental system and datasets is checked.

**Appraisal:** provisional A. The exact measured observables, experimental window, and relationship to the dissertation work must be extracted from the full text before making detailed claims.

### PSG-003 — Sahabi & Kind (2011), consolidation
**System and methods:** inorganic precipitated silica gel; consolidation studied with oedometer measurements. The article identifies pH and temperature among relevant parameters.

**What it supports:** consolidation is measurable as a time-dependent structural/volume response and is sensitive to chemical and thermal conditions in the studied system.

**What it does not establish:** a universal constitutive law for all precipitated silica gels. A fitted or semi-empirical description should not be confused with a uniquely validated microscopic mechanism.

**Appraisal:** A / OBS+CALC. Extract sample geometry, loading conditions, pore-liquid drainage boundary, pH/temperature range, repeatability and model residuals.

### PSG-004 — Sahabi & Kind (2011), model-like description of consolidation
**System and approach:** computational description of precipitated-silica gel-fragment consolidation, including particle-level interactions and comparison with experimental behaviour.

**What it can contribute:** a mechanistic hypothesis for how interparticle attraction and thermal motion may contribute to structural rearrangement.

**Critical boundary:** simulation inputs and idealisations are not direct measurements. The model should be evaluated for particle representation, interaction potential, solvent treatment, timescale mapping and sensitivity to initial structure.

**Appraisal:** A as a directly relevant modelling paper, but evidence tag MODEL/SIM must remain explicit. Do not cite it as proof that one interaction mechanism universally dominates.

### PSG-005 — Wilhelm & Kind (2014), natural versus enforced syneresis
**System and focus:** acidic precipitated silica; natural syneresis compared with mechanically accelerated/enforced syneresis.

**What it supports:** enforced syneresis can be investigated as an accelerated experimental route and correlated with natural syneresis for the studied acidic system.

**What it does not establish:** unrestricted equivalence between natural and enforced syneresis across pH, sample geometry, formulation, or mechanical loading. Correlation is not identity of mechanisms.

**Appraisal:** A / OBS+CALC+MODEL. Extract the calibration domain, observables used for correlation, prediction error, and conditions under which the correlation fails or was not tested.

### PSG-006 — Wilhelm & Kind (2015), pH, temperature and sample size
**System and methods:** sodium silicate/sulfuric acid-derived gels; both acidic and basic conditions; natural syneresis measured using pycnometer/optical methods and enforced syneresis using a mechanically loaded cell.

**Directly reported findings relevant to synthesis:** for the tested larger acidic samples, maximum natural shrinkage is reported near 0.20 over 20–60 °C, while the characteristic time decreases with temperature. For basic gels, both maximum shrinkage and rate show a different temperature response. Smaller samples consolidate more rapidly and to a greater extent than larger samples in the tested geometries. Under enforced loading, maximum shrinkage can be substantially larger than natural syneresis, and the temperature response of maximum shrinkage differs.

**Critical interpretation:** this paper itself demonstrates why “enforced syneresis” must not be used as an unqualified synonym or universal surrogate for natural syneresis. Geometry, drainage length, pH and loading conditions matter. The authors explicitly note that some process variables (e.g. ionic strength and silicate concentration) are outside the study’s scope.

**Appraisal:** A / OBS+CALC+MODEL. Strong direct source, but transferability is bounded by the tested precursor, acid/base recipes, dimensions and measurement setup.

## 3. Mechanistic comparators — use with explicit boundaries

### PSG-009 — Wijnen et al. (1991), SAXS of water-glass-derived silica gel
Useful for structural evolution, fractal aggregates and ageing. However, water-glass gel formation is not automatically equivalent to industrial acid precipitation. Keep it in a separate “related sodium-silicate gel” evidence tier and state the route difference at every point where it informs mechanism.

### PSG-010 — Matinfar & Nychka (2023), sodium-silicate review
Useful secondary source for solution speciation, gelation and syneresis background. It should guide backward tracing to primary studies, not replace them. Its broad sodium-silicate scope is wider than industrial precipitated silica.

### PSG-011/012/013/014 — Scherer and co-workers
Useful physical framework for viscoelasticity, permeability, stress response, shrinkage and drying in silica gels. Much of this literature concerns sol-gel/TEOS-derived systems. Do not transfer quantitative values or assume identical network chemistry. Distinguish syneresis (contraction during continued network formation/ageing with liquid expulsion) from drying (external solvent removal and associated capillary stresses).

### PSG-015 — Weitz & Oliveira (1984), gold colloids
Foundational aggregation context only. It is not silica evidence and should not occupy the core narrative unless a concise theoretical point genuinely requires it.

## 4. Cross-paper cautions and synthesis questions

1. **Do not conflate primary-particle formation, aggregation, gelation, fragmentation and consolidation.** They are temporally and physically distinct, even when coupled.
2. **Separate natural syneresis from enforced syneresis.** The latter changes the mechanical and drainage boundary conditions.
3. **Treat fractal dimension as scale- and method-dependent.** Report the measured length-scale window and technique whenever available.
4. **Separate measured response from interpretation.** Shrinkage, expelled-liquid volume, rheological modulus and scattering-derived structure are observables; “reorganisation” or a dominant interaction mechanism may be an interpretation.
5. **Control for repeated research lineage.** Articles, dissertations and follow-up papers from the same group may reuse formulations, apparatus or datasets. Do not count them as independent replication without checking.
6. **Do not over-generalise from TEOS-derived gels to industrial precipitated silica.** Use these sources for carefully bounded physical principles only.
7. **Final properties need direct linkage.** Claims connecting process history to final aggregate size, porosity, BET area or mechanical stability require studies measuring those endpoints, not only gel shrinkage.

## 5. Next extraction pass

For each A/B source, capture: exact formulation and pH definition; temperature; ionic strength/salt content; mixing and addition protocol; scale and geometry; time after mixing/gel point; measurement technique and length-scale window; replicate count/uncertainty; direct observables; fitted parameters; model assumptions; and final product properties measured. Then map overlaps between papers and dissertations before drafting the evidence synthesis.
