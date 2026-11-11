# Source assessments — batch 16: permeability and transport-mechanics benchmarks

## PSG-043 — Scherer & Swiatek (1989): Measurement of permeability II. Silica gel

**Reference:** G. W. Scherer and R. M. Swiatek, “Measurement of permeability II. Silica gel,” *Journal of Non-Crystalline Solids* 113(2–3) (1989), 119–129. DOI: 10.1016/0022-3093(89)90002-1.

**Bibliographic verification:** Elsevier and Princeton institutional publication records agree on authors, title, journal, volume, issue, pages and DOI.

**Access status:** Publisher abstract and institutional metadata inspected; full text not accessed.

**Study type and material:** Primary permeability measurement on alkoxide-derived silica gels. A pressure gradient was imposed across the pore liquid in thin sheets approximately 2 mm thick. The abstract distinguishes an acid-catalysed gel A with homogeneous microstructure from a base-catalysed gel B2 with an inhomogeneous network.

**What the abstract directly supports:**
- The thin geometry was selected to minimise viscoelastic effects discussed in the companion theoretical work.
- For acid-catalysed gel A, the measured permeability is reported to agree in order of magnitude with the Carman–Kozeny equation.
- For base-catalysed gel B2, permeability is higher than predicted, which the authors attribute presumptively to relatively large pores in the inhomogeneous network.
- Partial drying reduces permeability by approximately two orders of magnitude.

**What it does not establish:**
- The abstract does not provide numerical permeability values, uncertainty, pore-size distributions, exact formulations, or full pressure/flow protocols.
- The material is alkoxide-derived, not industrial sodium-silicate/sulfuric-acid precipitated silica.
- The partial-drying result is not a direct measurement of permeability evolution during wet-gel syneresis.
- The Carman–Kozeny comparison is not sufficient to establish a universal permeability law for silica gels.

**Modelling role:** Useful method/mechanistic comparator for permeability measurement and for checking the plausibility of structure–permeability relations. It cannot provide a target-system parameter set for precipitated silica without additional evidence. Full-text retrieval is required before extracting numerical permeability or using it as a quantitative benchmark.

**Evidence tags and provisional class:** OBS; B. Abstract-level appraisal.

## Revised interpretation of Scherer (1989) as a model benchmark

The three relevant lines of work should be kept distinct:
1. *Mechanics of syneresis I. Theory* gives the coupled continuum framework and geometry dependence.
2. *Mechanics of syneresis II. Experimental study* reports that shrinkage curves agree reasonably with calculations using independently measured permeability, modulus and viscosity.
3. *Measurement of permeability II. Silica gel* describes a separate pressure-driven permeability method in alkoxide-derived gels.

The available abstracts establish that independent parameter measurements were used in the syneresis comparison, but they do **not** expose the numerical parameter tables, raw shrinkage time series, exact sample chemistry, or uncertainties needed for an independent numerical reproduction. Therefore, Scherer is currently a **conceptual/mechanistic benchmark**, not yet a fully reproducible numerical benchmark from accessible information.

The first transport-model verification should be:
- verify the analytical solution against limiting cases and an independently implemented numerical solution;
- retrieve the full Scherer papers or sufficient author-provided data before claiming reproduction;
- only then attempt a quantitative cross-check;
- keep the target-system comparison with Wilhelm & Kind separate and report transferability limits explicitly.
