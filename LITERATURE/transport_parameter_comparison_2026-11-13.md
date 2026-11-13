# Transport-parameter evidence comparison — 13 November 2026

## Decision question

Can the existing literature identify intrinsic wet-gel permeability (or hydraulic mobility) and the constrained mechanical modulus on the same precipitated-silica formulation and state, so that the poroelastic coefficient can be independently constrained?

**Answer: not yet.** The evidence is substantially stronger than a simple absence-of-data statement: direct target-chemistry rheology, forced consolidation, industrial precipitated-silica cake filtration, and precipitation-pathway/mesostructure data exist. They measure different observables and states, however, and do not yet supply a matched intrinsic permeability–constrained-modulus pair.

## Evidence comparison

| Source | Material and protocol | Directly measured / reported | What it can constrain | What it cannot identify |
|---|---|---|---|---|
| Sahabi & Kind (2011), *Polymers* 3, 1423–1432, [DOI](https://doi.org/10.3390/polym3031423) | Sodium-silicate/sulfuric-acid precipitated-silica gels; acid pH about -0.97 and alkaline pH about 9; double-drained oedometer, about 15 bar, NF90 membrane | Fitted t90: acid 31,506 s (20 °C), 5,625 s (80 °C); alkaline 40,401 s (20 °C), 11,236 s (80 °C) | Direct pH- and temperature-dependent forced consolidation response; informs lumped transport/mechanical timescale under the stated pressure and boundary conditions | No independent intrinsic permeability or constrained modulus; t90 includes geometry, drainage and membrane effects; not natural syneresis |
| Wilhelm & Kind (2014), *Journal of Sol-Gel Science and Technology* 70, [DOI](https://doi.org/10.1007/s10971-014-3292-7) | Acidic precipitated silica; natural cylinders and plunger-enforced pressure cell | Natural 20/40/60 °C: Smax 0.197/0.197/0.198; tau 21.7/11.1/5.6 h; forced pressure series starts at 0.8 bar | Natural versus forced syneresis observables and geometry/pressure sensitivity | No independent permeability or modulus; natural zero-pressure forced response is extrapolated |
| Wilhelm & Kind (2015), *Polymers* 7, 2504–2521, [DOI](https://doi.org/10.3390/polym7121528) | Sodium-silicate/sulfuric-acid precipitated silica; natural and pressure-cell syneresis | Empirical amplitudes and time constants for cylinders/droplets and pressure-cell conditions | Target-system kinetic observables; tests of geometry and apparatus effects | Fitted tau is not permeability or a physical consolidation time; pressure-cell membrane/filter-plate resistance is part of the apparatus |
| Kaide, Saeki & Kikuchi (2011), [DOI](https://doi.org/10.1678/rheology.39.205) | Y-reactor sodium-silicate/sulfuric-acid silica sol; dynamic rheology, creep/recovery, SPM | At pH 2, gel time 40 h at 25 °C and 4.5 h at 50 °C; pH changes E0 and gel evolution | Direct precursor-chemistry mechanical ageing and pH/temperature trends | E0 is an instantaneous creep-model modulus, not automatically the constrained poroelastic modulus M; no matched permeability |
| Ragueh et al. (2015), *Separation and Purification Technology* 156, 2–11, [DOI](https://doi.org/10.1016/j.seppur.2015.10.005) | Three industrial precipitated-silica dispersions; TEM/SAXS/USAXS, filtration at 400–600 kPa (five repeats), osmotic compression | Percolation thresholds about phi=0.06, 0.08, 0.09; cake resistance and derived cake permeability; aggregate radii 82/125/175 nm | Strong target-material link among hierarchical structure, cake transport and compression/yielding | Permeability is inferred for filter cakes, not freely suspended or syneresising gel fragments; loading/drainage paths differ; source has unresolved S3 Df and sample-label inconsistencies |
| Manfoumbi, Roger & Meireles (2024), *Comptes Rendus Chimie* 27, S4, 111–122, [DOI](https://doi.org/10.5802/crchim.347) | Highly acidic hydrometallurgical precipitation; sodium-silicate/sulfuric-acid model at 90 °C; SAXS and dead-end filtration at 700 kPa, 25 °C, n=3 | Silicate addition at pH 9 changes high-q SAXS behaviour from near q^-2 toward q^-4 and reduces cake-specific resistance by roughly two orders of magnitude | Process-history/mesostructure effect on filterability; strong qualitative reason to retain precipitation history as a state variable | Cake resistance is not intrinsic wet-gel permeability; high ionic strength and hydrometallurgical conditions limit transfer; SAXS slopes alone do not define unique Df |
| Scherer (1989), *Mechanics of syneresis II*, [DOI](https://doi.org/10.1016/0022-3093(89)90329-3) | Silica-gel syneresis; abstract reports independent permeability, modulus and viscosity inputs | Mechanistic syneresis curves compared with measured shrinkage | Establishes a viable coupled transport/viscoelastic model strategy | Exact precursor and numerical data need full-text verification; not established as industrial precipitated silica |
| Scherer & Swiatek (1989), [DOI](https://doi.org/10.1016/0022-3093(89)90002-1) | Alkoxide-derived silica-gel sheets; pressure-gradient permeability measurement | Acid/base gel permeability comparison; permeability falls by about two orders after partial drying (abstract-level) | Method precedent for direct gel permeability measurement and structural sensitivity | Different synthesis route; numerical values and uncertainties not recovered; no direct transfer to sodium-silicate/sulfuric-acid precipitated silica |

## Ragueh et al. (2015): numerical cake-resistance diagnostics

The published Table 4 reports specific cake resistance on a relative, undisclosed reference scale R. At 400 kPa the reported values are 2.50 (S1), 1.50 (S2) and 0.77 (S3); at 600 kPa they are 3.63, 2.40 and 1.20. Derived increases from 400 to 600 kPa are 45.2%, 60.0% and 55.8%, respectively.

At fixed pressure, the S1/S3 relative-resistance ratios are 3.25 (400 kPa), 2.56 (500 kPa) and 3.03 (600 kPa). These ratios are legitimate within-paper comparisons on the reported relative scale. They are **not absolute permeability values**. One 600 kPa S1 table entry lacks the reference symbol, so that point remains flagged as provisional. The middle sample label is printed inconsistently as S3 in parts of the article and is likely S2, but the repository preserves the printed discrepancy rather than silently correcting it.

## Identifiability conclusion

For the simplified poroelastic relation

\[
c_v=\frac{\kappa M}{\mu},
\]

a fitted c_v (or empirical shrinkage time constant) identifies at most a lumped combination under assumed geometry and boundary conditions. A cake-derived permeability, a rheological E0, an oedometer t90 and a free-syneresis tau are not interchangeable inputs.

The current evidence matrix therefore supports:
1. A structural state description that retains precipitation history, aggregation/fragment size, network connectivity and volume fraction.
2. Separate hydraulic and mechanical constitutive terms.
3. Apparatus boundary resistance as a separate term for pressure-cell data.
4. Bounded sensitivity studies over plausible parameter families, not a single target-system calibration.

It does **not** yet support a numerical intrinsic permeability or constrained modulus for the exact Wilhelm & Kind wet-gel states.

## Next evidence actions

1. Search for direct pressure-driven permeability measurements on wet sodium-silicate/sulfuric-acid precipitated-silica gels before drying or cake formation.
2. Seek mechanical measurements that can be mapped to the constrained modulus M (or provide sufficient creep/relaxation data to identify a constitutive conversion), on the same formulations and ageing states.
3. Where only filtration cake data exist, retain them as structure/transport comparators and do not use them as direct solver calibration.
4. Where only oedometer or syneresis time constants exist, retain them as lumped-response targets and do not invert them to permeability without independent mechanical and geometry information.
5. For any future matched dataset, record formulation, pH history, ionic strength, solids fraction, ageing time, temperature, pressure path, drainage length, membrane/filter resistance, and uncertainty before parameter fitting.
