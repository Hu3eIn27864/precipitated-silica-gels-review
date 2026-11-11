# Candidate validation data and simulation benchmarks

## Purpose

This file tracks published measurements that could independently test a future model. A dataset is not considered validation-ready merely because a paper contains a graph. We must establish material identity, protocol, independent parameter measurements, digitisation uncertainty, and whether the data were used for calibration.

## Priority benchmark A — Direct precipitated-silica syneresis

### Wilhelm & Kind (2015), natural and enforced syneresis

- Source: *Polymers* 7, 2504–2521, DOI 10.3390/polym7121528.
- Access: open full text and downloadable supplementary material are indicated on the publisher page.
- Material: sodium-silicate / sulfuric-acid precipitated silica; acid and alkaline gel recipes.
- Measured outputs: natural relative volume shrinkage versus time for cylinders and droplets; enforced syneresis under pressure; effects of pH, temperature, and sample size.
- Existing project extraction: 12 published fitted natural-syneresis parameter pairs (maximum shrinkage and characteristic time constant) from Tables 1 and 2 have now been added to `LITERATURE/quantitative_extraction_syneresis.csv`; six additional centrifugal forced-syneresis points from Wilhelm (2017) remain separately recorded.
- The natural-syneresis time-series are represented by the paper's empirical single-exponential fit, and the authors explicitly state that a physically based model remained future work. Tables 1 and 2 provide fitted parameters, not raw time-series observations. The publisher also lists supplementary material (including supplementary tables/figures for enforced syneresis); it is not raw time-series data.
- Candidate use: test geometry-dependent transport trends and assess whether a shared effective transport parameter can describe cylinders and droplets under explicit boundary conditions.
- Limitations: the empirical fit time constant is not automatically a pore-pressure diffusion eigen-time. The droplet shape and drainage boundary conditions are approximate; finite cylinders may have both radial and end drainage. The pressure-cell model is empirical. The dissertation repeats some 2015 data; do not count these as independent validation.
- A first-mode conversion has been documented in `MODELLING/transport_model/geometry_scaling_note.md` strictly as an apparent diffusivity diagnostic, not a measured material property.
- Status: high-priority, direct material relevance; tabulated fit parameters available; figure-level digitisation is still useful for residual checks and uncertainty appraisal, but should not be presented as raw data.

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


## 2026-11-11 refinement — What is actually reproducible from Scherer (1989)?

A further source check identified Scherer & Swiatek (1989), “Measurement of permeability II. Silica gel,” *J. Non-Cryst. Solids* 113(2–3), 119–129, DOI 10.1016/0022-3093(89)90002-1. Its abstract describes pressure-gradient measurements in approximately 2 mm alkoxide-derived silica-gel sheets. It reports order-of-magnitude Carman–Kozeny agreement for a homogeneous acid-catalysed gel, higher-than-predicted permeability for an inhomogeneous base-catalysed gel, and an approximately 100-fold permeability decrease after partial drying.

This adds a permeability-measurement comparator, but does not solve the data-access problem: the abstract gives no numerical permeability values or uncertainty. The material is alkoxide-derived, and the partial-drying observation is not a direct wet-syneresis permeability trajectory.

**Important downgrade in benchmark status:** Scherer (1989) Parts I–II are presently a mechanistic/conceptual benchmark, not a fully reproducible numerical benchmark using accessible abstracts alone. The Part II abstract says independently measured permeability, modulus and viscosity were used, but the numerical tables, raw shrinkage series, exact material recipe and uncertainties remain unavailable. Do not claim numerical reproduction until these are retrieved.

The first transport-model tests should therefore be mathematical verification (initial/long-time limits, dimensionless curve collapse, comparison with an independent numerical solution), followed by a literature-data reproduction only when sufficient original numerical data are available. Wilhelm & Kind (2015) remains the more direct precipitated-silica target dataset, but independent target-system permeability and modulus are still the main identifiability gap.


## Geometry audit and digitisation gate — 2026-11-11

The open full text of Wilhelm & Kind (2015) confirms 12 mm cylinder diameter and approximately 3 mL volume, plus approximately 3 mm droplets observed in a sealed PMMA microscopy cell with cover glasses. Assuming a right circular cylinder, the first two values imply a **calculated** height of about 26.5 mm; this is not a directly reported measured height. The droplet cannot be presumed to be a freely drained sphere, and its early thermal history includes an initial 20 °C period. The 2015 pressure-cell table uses 16 mm initial height, while the 2017 centrifugation data use 20 mm. See LITERATURE/experimental_geometry_audit_wilhelm.md.

The next data task is point-by-point figure digitisation under the rules in LITERATURE/syneresis_curve_digitisation_protocol.md. Measured markers and fitted curves must be stored separately; fit parameters in Tables 1–2 are not raw data. No diffusivity or permeability should be fitted until effective drainage lengths/boundaries and model identifiability have been addressed.


### Pressure-cell data added

The open Wilhelm & Kind (2015) Table 3 fit parameters have been transcribed into LITERATURE/pressure_cell_syneresis_comparison.csv: seven pressure intervals, acid/base gels, 20 °C, initial height 16 mm. They remain separate from the 2017 centrifugal data (20 mm initial height and height-averaged equivalent pressure). The article reports a membrane/filter-plate assembly; the dissertation identifies membrane-related flow resistance as a possible reason for different forced-syneresis time constants. Neither series is a direct intrinsic-permeability measurement.


## 2026-11-11 fit-curve reconstruction and parameter evidence audit

A small standard-library Python utility now reconstructs sampled curves from the published Smax and tau parameters in the natural/centrifugal comparison table and the separate pressure-cell table:
`MODELLING/transport_model/reconstruct_published_syneresis_fits.py`.
Its output is explicitly labelled `published_empirical_fit_reconstruction_not_digitised_data`. These points are useful for plotting and checking the consequences of the reported empirical fit, but they contain no experimental scatter, residuals, replicate variation, or digitisation uncertainty. They are not a substitute for marker-level figure digitisation. A dedicated unit test checks the equation and its limiting behaviour.

A separate parameter-evidence audit is in `LITERATURE/transport_parameter_evidence_audit.md`. Ragueh et al. (2015) is the strongest direct precipitated-silica bridge for network consolidation under pressure, but it characterises filter cakes rather than free-standing syneresing gels. It cannot supply an intrinsic gel permeability without a transfer model and matching boundary/state definitions. The current evidence set still lacks an independently measured permeability–modulus pair for the Wilhelm & Kind target gels. Therefore no target-system permeability or modulus fit is authorised at this stage.
