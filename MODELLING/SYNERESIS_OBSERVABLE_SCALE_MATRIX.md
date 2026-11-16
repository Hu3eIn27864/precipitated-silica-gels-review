# Syneresis evidence: observable and scale separation

Updated 16 November 2026. This note prevents measurements from different physical scales and boundary conditions being treated as interchangeable observations of one scalar “syneresis rate”.

## Evidence ladder

| Level | State / process | Observable | Project sources | What it can constrain | What it cannot establish alone |
|---|---|---|---|---|---|
| 0. Solution chemistry | Dissolved silicate speciation and condensation precursors | 29Si NMR species fractions; pH; silica/alkali ratio; ionic composition | PSG-010 (Matinfar & Nychka, 2023; review) | Initial chemical state and plausible reaction pathways | Macroscopic gel contraction, permeability, modulus |
| 1. Primary particles and clusters | Particle formation, aggregation and intracluster restructuring | Hydrodynamic particle/cluster size; fluorescence anisotropy dynamics | PSG-050 (Birch & Geddes, 2000; abstract-level appraisal) | Nanoscale particle/cluster growth and post-gelation restructuring timescales | Bulk sample-volume loss or expelled-liquid flux |
| 2. Network morphology | Percolated network and pore/aggregate architecture | SAXS/USAXS exponents, characteristic lengths, microscopy | PSG-045, PSG-046 | Mesostructure, aggregation and filtration-cake architecture under stated conditions | Unique pore-throat distribution, intrinsic permeability, or load-bearing modulus without a closure |
| 3. Free gel contraction | Unforced natural syneresis of an aged gel specimen | Sample volume/height versus time; exudate mass/volume; water/Si balance | PSG-006, PSG-049 (Wilhelm lineage) | Direct macroscopic natural-syneresis kinetics under the reported formulation and geometry | Loaded compressibility or universal transfer across chemistry and geometry |
| 4. Loaded mechanical/transport response | Oedometer consolidation, osmotic compression, filtration-cake drainage | Void ratio/compression curve, constrained response, hydraulic conductivity or cake resistance | PSG-046, PSG-047, PSG-048 | State-dependent mechanical/transport response under explicit stress and drainage boundary conditions | Free syneresis kinetics or intrinsic permeability without conversion assumptions |
| 5. Drying/suction history | Evaporation during curing, suction development and resaturation | Mass/volume loss, suction, post-resaturation compression response | PSG-048 (RH-cured specimen) | Drying-induced shrinkage, suction and irreversible history/preconsolidation effects | Natural syneresis in a saturated, unforced specimen |

## Consequences for CCFSM

1. **Keep at least two clocks.** Chemical/particle evolution can proceed on minutes-to-days scales while bulk sample shrinkage and liquid expulsion have their own hydraulic/mechanical response. A single fitted exponential may be a useful reduced observable model, but it must not be interpreted as one universal microscopic rate.
2. **Keep intrinsic contraction and observed volume loss separate.** Network contraction potential is not automatically equal to sample volume loss when fluid can drain only through finite permeability and boundaries. Conversely, a specimen can lose water by evaporation without the same mechanism as saturated syneresis.
3. **Do not convert hydraulic conductivity to intrinsic permeability without fluid properties and test-state control.** Oedometer-derived conductivity and filtration-cake permeability/resistance refer to different geometries, stress paths and drainage configurations.
4. **Do not infer pore connectivity from one fractal exponent.** SAXS/USAXS exponents constrain scattering regimes and structural length scales; pore-throat distributions, connectivity and transport require additional information or independently validated closures.
5. **Match formulations before transferring parameters.** Waterglass/acid precipitation, commercial electrolyte-triggered colloidal silica, and industrial precipitated-silica slurries are distinct material routes. pH, silica concentration, silica/alkali ratio, ionic strength, temperature and gel age must be recorded.

## Minimum matched experiment for a stronger CCFSM bridge

For one fixed formulation and temperature, use matched specimens and record:
- solution composition and pH at mixing/gel point;
- gelation time and ageing history;
- free sample volume/height versus time under a stated drainage condition;
- exudate mass/volume and evaporation control;
- total and dissolved/exuded silicon where feasible;
- at least one structural observable (SAXS/USAXS or microscopy);
- at least one mechanical/transport observable at a matched age and state.

A useful design includes both sealed/saturated ageing (to isolate natural syneresis) and a controlled drainage or loading arm (to identify the hydraulic/mechanical response), with replicate specimens and uncertainty estimates.

## Scope

This is an evidence-integration framework, not a validated constitutive model. The table indicates which parameters each source may constrain; it does not imply that data from different rows can be combined in one fit without a shared-state model.
