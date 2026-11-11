# Candidate validation data and simulation benchmarks

## Purpose

This file tracks published measurements that could independently test a future model. A dataset is not considered validation-ready merely because a paper contains a graph. We must establish material identity, protocol, independent parameter measurements, digitisation uncertainty, and whether the data were used for calibration.

## Priority benchmark A — Direct precipitated-silica syneresis

### Wilhelm & Kind (2015), natural and enforced syneresis

- Source: *Polymers* 7, 2504–2521, DOI 10.3390/polym7121528.
- Access: open full text and downloadable supplementary material are indicated on the publisher page.
- Material: sodium-silicate / sulfuric-acid precipitated silica; acid and alkaline gel recipes.
- Measured outputs: natural relative volume shrinkage versus time for cylinders and droplets; enforced syneresis under pressure; effects of pH, temperature, and sample size.
- Existing project extraction: cylinder and droplet endpoint/time-scale values are in source assessment batch 01; separate centrifugation data from Wilhelm (2017) are in `LITERATURE/quantitative_extraction_syneresis.csv`.
- Candidate use: external check of a continuum drainage/poroelastic model's trends with geometry, temperature, and gel type.
- Limitations: fitted kinetic curves and reported endpoint/time constants are not a full independent constitutive dataset. The pressure-cell model is empirical. The dissertation repeats some 2015 data; do not count these as independent validation.
- Status: high-priority, direct material relevance; extract figure-level time series and supplementary files before model fitting.

## Priority benchmark B — Direct precipitated-silica aggregation and fragmentation

### Schlomach & Kind (2004), semi-batch precipitation

- Source: *Journal of Colloid and Interface Science* 277, 316–326, DOI 10.1016/j.jcis.2004.04.051.
- Material: sodium silicate + sulfuric acid, semi-batch precipitation.
- Reported measurements: photon-correlation spectroscopy; primary particle size 22.7 nm; aggregate/gel evolution; fractal dimension rises from about 1.8 to 2.4 after gel point; specific surface area decreases from 480 to 300 m²/g; gel fragmentation/compaction.
- Candidate use: qualitative/quantitative trend checks for a coarse-grained aggregation/fragmentation model; not sufficient alone to calibrate contact laws.
- Limitations: DLS interpretation and fractal scaling window must be checked in full text; dataset overlaps with Schlomach dissertation and repeat experiments in Quarch dissertation.
- Status: high process relevance; independent dataset lineage must be treated as one research family.

### Quarch et al. (2010), mechanical fragmentation

- Source: *Chemical Engineering Research and Design* 88, 1639–1647, DOI 10.1016/j.cherd.2010.01.007.
- Material: industrially relevant precipitated silica gel fragments.
- Reported measurements: fragment size under stirred-tank, Taylor–Couette and ultrasound energy input; fragment strength depends on age, solids, pH, salt, and temperature.
- Candidate use: test rank-order trends or fragment-size response in a CFD–DEM / breakage model, if exact experimental operating conditions and numerical data can be recovered.
- Limitations: operational ultrasound resistance is not identical to in-reactor breakage; research-family overlap with Quarch dissertation and companion publications.
- Status: promising, but requires full-text/figure extraction.

## Mechanistic comparator C — Silica-gel syneresis and permeability (not industrial precipitated silica)

### Scherer (1989), Mechanics of syneresis I and II

- Sources: *Journal of Non-Crystalline Solids* 108, 18–27 and 28–36; DOI 10.1016/0022-3093(89)90328-1 and 10.1016/0022-3093(89)90329-3.
- Reported result: contraction rate and curve shape depend on sample size, permeability, and viscoelastic network properties; the experimental paper reports reasonable agreement between measured shrinkage curves and calculations using independently measured permeability, modulus, and viscosity.
- Candidate use: reproduce the published continuum benchmark before applying the model to precipitated silica. This is a useful verification exercise for transport/poroelastic implementation.
- Limitations: the companion Scherer (1989) modulus paper explicitly uses TEOS/alkoxide-derived gels. Do not treat this as direct industrial precipitated-silica validation. The exact syneresis-paper sample chemistry and raw numerical data must be checked in full text.
- Status: high mechanistic value; transferability-limited.

### Scherer & Swiatek (1989), Measurement of permeability II: Silica gel

- Source: *Journal of Non-Crystalline Solids* 113, 119–129, DOI 10.1016/0022-3093(89)90002-1.
- Reported measurements: permeability of alkoxide-derived silica gels from pressure-driven pore-liquid flow in thin (~2 mm) gel sheets; acid and base gel differences; permeability decreases by about two orders of magnitude after partial drying.
- Candidate use: parameter-scale and method benchmark for permeability implementation.
- Limitations: TEOS-derived gel chemistry, not precipitated silica; do not transfer absolute permeability values without evidence.
- Status: mechanistic comparator; exact data extraction pending.

### Scherer (1989), Effect of shrinkage on modulus of silica gel

- Source: *Journal of Non-Crystalline Solids* 109, 183–190, DOI 10.1016/0022-3093(89)90030-6.
- Access: a repository-hosted copy is indexed at INRAE.
- Reported measurements: shear modulus during ageing/syneresis and drying in acid- and base-catalysed TEOS-derived gels; modulus increases during syneresis.
- Candidate use: compare qualitative coupling between contraction and stiffening in a network model; possible digitisation of modulus/strain curves.
- Limitations: drying dominates the largest modulus changes; material is alkoxide-derived. This is not a direct parameter set for industrial precipitated silica.
- Status: accessible mechanistic comparator; digitisation and full methods review pending.

## Adjacent open dataset D — Colloidal silica transport

### Pedrotti et al., data for “A transport model for the permeation of colloidal silica”

- Dataset DOI: 10.15129/cff3fd37-9260-4b54-a952-dc896e78816d; CC BY 4.0; University of Strathclyde repository.
- Contents: XLSX data for figures 3, 4, 13, 14 and 15 of a colloidal-silica permeation study, including experiment, numerical model, injection results and viscosity data.
- Candidate use: independent software/transport-model verification on colloidal silica permeation, not syneresis.
- Limitations: different physical problem and likely different material/flow regime; no direct validation of precipitated silica gel consolidation.
- Status: open dataset identified; inspect spreadsheet and associated article before any use.

## Model question shortlist and evidence requirements

### Q1 — Can a poro-viscoelastic model predict geometry-dependent syneresis?

**Current leading question.** Reproduce Scherer's silica-gel benchmark first, then test trends against Wilhelm & Kind's precipitated-silica natural-syneresis curves without refitting all parameters to the target curves.

Required parameters:
- permeability as a function of state / consolidation;
- elastic or viscoelastic modulus and relaxation time;
- sample geometry and drainage boundary;
- initial condition and external liquid boundary condition.

Key test: predict how contraction time changes with drainage length/sample size, not merely fit one curve. If permeability and modulus are not independently available for the target material, perform bounded sensitivity analysis and label predictions as non-unique.

### Q2 — Can a coarse-grained network model reproduce consolidation trends?

Required independent checks:
- structural descriptors (fractal dimension over stated length scales, coordination/contact statistics if reported, SAXS or microscopy);
- mechanical response or modulus evolution;
- shrinkage/volume change.
A particle simulation should not be calibrated and validated against the same single curve. Existing industrial precipitated-silica literature may not yet provide all observables simultaneously.

### Q3 — Can CFD–DEM predict gel-fragment breakage?

Required independent checks:
- reactor geometry and flow/energy input;
- initial fragment-size distribution and material age/solids/pH/salt/temperature;
- measured fragment-size distribution across operating conditions;
- defensible contact/breakage parameters.
Current literature appears promising but exact, machine-readable conditions and distributions remain to be extracted. Do not begin CFD–DEM before this gap is resolved.

## Data handling rules

- Separate direct target-system validation from mechanistic comparator validation.
- Digitised graph points must be labelled as digitised, with pixel/axis uncertainty and source figure number.
- Do not use data from a publication to both tune and independently validate the same model.
- Treat dissertations and companion articles as one research lineage when they reuse experiments.
- Preserve raw reported values and units; never silently convert fitted characteristic times into measured elementary rate constants.
- Record inaccessible full texts as a limitation; do not infer numerical data from abstracts.
