# Source assessment — Ragueh et al. (2015): filtration, permeability and compression of precipitated silica

**Record:** PSG-046  
**Citation:** D. M. Ragueh, M. Meireles, B. Cabane and J. Gummel, “Filtration of precipitated silica aggregates: Length scales, percolation threshold and yielding behaviour,” *Separation and Purification Technology* **156** (2015), 2–11. DOI: [10.1016/j.seppur.2015.10.005](https://doi.org/10.1016/j.seppur.2015.10.005).  
**Evidence grade:** A for the measured structure, filtration and compression behaviour of the three industrial silica dispersions studied; B for transfer to syneresis of gel fragments.  
**Access:** Full author-deposited manuscript inspected via the LCM-D repository / CORE-OATAO archive.

## Why this source matters

This is a particularly valuable bridge between the structural and transport parts of our review. Unlike general sol-gel silica studies, it examines three industrial, highly dispersible precipitated-silica dispersions sampled directly from a precipitation reactor. The authors combine TEM, SAXS/USAXS, pressure filtration and osmotic compression. They therefore connect multiscale aggregate structure to both liquid transport through filtration cakes and resistance to compression.

## Experimental design

- Three industrial aqueous silica dispersions (S1–S3), with different synthesis pathways and specific surface areas.
- TEM and SAXS/USAXS to examine hierarchical structure from nanometre to sub-millimetre scales.
- Constant-pressure filtration at 25 °C and 400–600 kPa. Permeate mass was followed gravimetrically; five repeats were performed to assess reproducibility.
- Cake-specific resistance was obtained from the filtration rate using Darcy-based filtration analysis. Cake permeability was then inferred using measured silica content/volume fraction and structural length scales.
- Osmotic compression of dispersion in dialysis bags, with PEG solutions spanning an osmotic pressure range of roughly 100 Pa to 700 kPa, to assess network resistance and yielding.

## Main reported findings

1. The industrial precipitated silicas have hierarchical structures: small silica beads are connected into denser aggregates, which are further organised into branched networks.
2. Much of the SAXS-observed local/multiscale structure is retained in filtration cakes over the investigated pressure range. A notable exception is S3 at the highest pressure, where low-q scattering indicates formation of denser lumps.
3. Osmotic compression shows three regimes: dilute dispersion, a percolation threshold, and yielding. The reported percolation volume fractions are approximately 0.06 for S3, 0.08 for S1 and 0.09 for S2. In the osmotic-compression comparison, changing ionic strength mainly affected the yielding regime; the higher-ionic-strength samples showed nearly threefold greater compression resistance in that regime. The reported pressure–volume-fraction power-law response in the yielding regime differed between the two ionic-strength conditions (approximately cubic versus eighth power).
4. Above the percolation threshold, the connected network resists a substantial increase in applied osmotic pressure before yielding. In the yielding regime, the volume fraction rises and large dense regions can form.
5. The authors use an effective-medium representation in Darcy's law, with aggregate/bead size and inter-aggregate spacing as structural length scales, to reproduce filtration-derived permeability trends.

## Critical distinctions for our synthesis

The filtration-derived permeability is a property inferred for a concentrated filtration cake under the tested filtration conditions. It is **not** a direct measurement of the intrinsic permeability of freely suspended precipitated-silica gel fragments, and it is not a time-resolved permeability measurement during natural syneresis.

Likewise, osmotic compression is slow and approximately isotropic, whereas pressure varies with height in a filtration cake. The authors explicitly caution against directly equating pressure thresholds between these two loading paths. The volume-fraction comparison is more defensible than a direct pressure-threshold transfer.

Therefore:
- This source directly supports a link between industrial precipitated-silica hierarchy, cake transport and compression/percolation behaviour.
- It supports using a structural length-scale / porosity description in a cake-scale Darcy model.
- It does not by itself supply a syneresis permeability law, a gel-fragment constitutive relation, or a time-dependent consolidation coefficient.
- Do not use its cake permeability values as direct calibration data for the radial syneresis solver without matching the material state, solids fraction, loading path and geometry.

## Model implications

This source strengthens the case for a two-level transport architecture:
1. a structural state description (aggregate size, inter-aggregate spacing, volume fraction, connectivity / percolation);
2. a continuum transport law (Darcy permeability) coupled to mechanical resistance / yielding.

It also warns against collapsing all structural change into a single fractal dimension. The same material can retain local SAXS structure while changing larger-scale network connectivity and cake transport; under stronger loading, local or low-q structural changes may appear.

## Defensible review claim

For the industrial precipitated-silica dispersions studied by Ragueh et al., filtration-derived cake permeability and compression response can be related to hierarchical aggregate length scales and network volume fraction. Osmotic compression identifies percolation and yielding regimes, while filtration cakes largely retain their local structure over the investigated pressure range, with system-specific restructuring at the highest pressure.

This is direct evidence for structure–transport–mechanics coupling in precipitated silica, but not a direct syneresis-permeability dataset.
