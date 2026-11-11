# Source assessment — Manfoumbi, Roger & Meireles (2024): mesostructure control and filterability

**Record:** PSG-045  
**Citation:** C. Manfoumbi, K. Roger and M. Meireles, “Filtering the unfilterable: tuning the mesostructure of precipitating silica gels to improve the filterability of acidic lixiviation slurries,” *Comptes Rendus Chimie* **27** (2024), special issue S4, 111–122. DOI: [10.5802/crchim.347](https://doi.org/10.5802/crchim.347). CC-BY 4.0.  
**Evidence class:** B — highly relevant precipitation/mesostructure/filtration comparator; not a direct syneresis experiment.  
**Access:** Publisher full-text HTML/PDF indexed content inspected.

## Experimental scope

The study addresses silica precipitation during highly acidic hydrometallurgical leaching. It combines real ore leachates with a simpler model system based on sodium silicate and sulfuric acid. The model precipitation is conducted at 90 °C in a high-acidity, high-ionic-strength medium, intentionally unlike many standard colloidal-silica preparations.

The authors use solution analysis to follow silicon dissolution/precipitation, SAXS to probe the evolving mesostructure, and constant-pressure dead-end filtration to quantify cake-specific resistance. Filtration was performed at 700 kPa and 25 °C; filtration experiments were repeated three times. The model precipitation route includes an acidic polymer-gel stage, a pH increase to 9, additional silicate dosing at pH 9, and return to acidic pH.

## Main observations reported

- Acidic precipitation produces a polymer-like silica network with a high-q SAXS power law close to q^-2.
- Raising pH alone changes the structure only modestly.
- Adding silicate at basic pH produces a much denser particle-like mesostructure; the high-q scattering approaches Porod q^-4 behaviour.
- This structural change is retained after returning to acidic pH.
- The change in mesostructure is accompanied by a roughly two-orders-of-magnitude decrease in specific filtration-cake resistance in the model and real-ore systems.
- The real-ore result demonstrates process relevance beyond the model solution.

The SAXS intensities were not on an absolute concentration scale. The reported power-law exponents describe scattering regimes and should not be converted directly into an absolute fractal dimension or a unique microscopic structure without the required model and q-range analysis.

## Relevance to our project

This is one of the closest recent process-relevant sources for the central link between precipitation history, silica network structure and liquid transport. It supports the view that pH history and additional silicate can reorganise the mesostructure and strongly change filtration behaviour.

It also motivates a process-history variable in the model: a gel network cannot be represented solely by its instantaneous pH or solids content if prior pH/silicate dosing changes its mesostructure irreversibly or hysteretically.

## Critical distinction: cake resistance is not gel permeability

The filtration response is a cake-specific resistance measured during dead-end filtration. It is not the intrinsic permeability of a freely suspended or consolidating gel, and it does not directly measure syneresis kinetics, pore-pressure relaxation, elastic modulus, or the permeability evolution during gel shrinkage. Cake formation, particle retention, compressibility, solids loading, and filter-cloth boundary conditions contribute to the measured response.

Therefore:
- Use the study to support qualitative coupling of process history, mesostructure and filtration resistance.
- Do not use the reported two-order change as a two-order change in intrinsic gel permeability.
- Do not use it to calibrate the radial syneresis solver.
- Do not pool it with Wilhelm/Kind syneresis curves or treat cake filtration as a syneresis measurement.

## Evidence disposition

**Strongest defensible claim:** Under the studied highly acidic hydrometallurgical conditions, changing the precipitation pathway by adding silicate at basic pH changes the SAXS-observed silica mesostructure and substantially improves filterability.

**Not established:** a universal pH-dependent permeability law; direct permeability evolution during syneresis; a mechanical modulus change; applicability to all commercial precipitated-silica processes; or a unique fractal dimension inferred from q^-2/q^-4 slopes.

## Model implications

1. Include precipitation/pH history as a candidate structural state variable, not just current pH.
2. Keep filtration-cake resistance, intrinsic gel permeability and syneresis time constants as separate observables.
3. Future experiments should measure SAXS/structure, cake resistance, direct gel permeability and mechanical response on matched samples if a quantitative coupling is sought.
