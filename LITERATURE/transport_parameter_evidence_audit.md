# Transport-parameter evidence audit: permeability and mechanics

**Audit date:** 2026-11-11  
**Question:** Are independent permeability and mechanical data available for the target precipitated-silica gel, rather than merely fitted shrinkage time constants?

## Findings

| Source | Material / protocol | What it contributes | Transferability to syneresis model | Current use |
|---|---|---|---|---|
| Ragueh et al. (2015), *Separation and Purification Technology* 156, 2–11, DOI [10.1016/j.seppur.2015.10.005](https://doi.org/10.1016/j.seppur.2015.10.005) | Industrial precipitated silica aggregates; pressure filtration and osmotic compression of filter cakes; structural length scales | Direct evidence that the hierarchical aggregate network has a pressure-dependent consolidation response; the paper describes a percolation threshold and a cake-scale porous-medium treatment | **High material relevance, limited state/geometry transfer.** A filter cake is not the same initial condition or boundary-value problem as a free-standing wet gel undergoing natural syneresis. Cake permeability/resistance cannot be silently relabelled intrinsic gel permeability | Structural/mechanical trend comparator; extract exact numerical curves only after figure/table and material-grade audit |
| Wilhelm & Kind (2015), *Polymers* 7, 2504–2521, DOI [10.3390/polym7121528](https://doi.org/10.3390/polym7121528) | Sodium-silicate/sulfuric-acid precipitated silica; natural and pressure-cell syneresis | Smax and empirical tau values for natural cylinders/droplets and pressure-cell conditions | **Direct target chemistry**, but tau is an empirical curve parameter, not independently measured permeability or modulus; membrane/filter-plate resistance is part of forced-cell setup | Target observable; do not identify k and M separately from tau |
| Scherer (1989), *J. Non-Cryst. Solids* 108, 28–36, DOI [10.1016/0022-3093(89)90329-3](https://doi.org/10.1016/0022-3093(89)90329-3) | Silica-gel syneresis; abstract reports comparison with independently measured permeability, modulus and viscosity | Demonstrates a viable poro-viscoelastic syneresis strategy and the need for independent material inputs | **Mechanistic comparator only** until gel chemistry and numerical data are checked; not established as industrial precipitated silica | Reproduce only after full numerical inputs and specimen chemistry are recovered |
| Scherer & Swiatek (1989), *J. Non-Cryst. Solids* 113, 119–129, DOI [10.1016/0022-3093(89)90002-1](https://doi.org/10.1016/0022-3093(89)90002-1) | Alkoxide-derived silica-gel sheets; pressure-driven pore-liquid flow | Permeability measurement methodology; acid/base contrast and strong change during partial drying reported in abstract | **Low-to-moderate transferability** because synthesis route differs; no numerical values or uncertainty extracted yet | Method comparator; never copy absolute permeability values into precipitated-silica model |
| Park et al. (2006), *Environmental Science & Technology* 40, 2699–2705, DOI [10.1021/es0515304](https://doi.org/10.1021/es0515304) | Fractal aggregates deposited as membrane filter cakes; batch-cell and confocal microscopy | Links aggregate size, fractal dimension, transmembrane pressure, cake porosity and specific cake resistance; experimental check of collapsed-cake model | **Adjacent filtration comparator**, not precipitated-silica syneresis and not a direct gel permeability dataset | Qualitative structural/transport comparator only |

## Interpretation

1. **No independent target-system pair (permeability plus modulus) has yet been identified** for the exact precipitated-silica gels used in the Wilhelm & Kind syneresis series.
2. The Ragueh study is the strongest bridge from precipitated-silica network structure to pressure-dependent cake consolidation. Its response is useful for constraining qualitative trends, but it does not by itself provide a transferable constitutive law for a syneresing, unconfined gel.
3. Scherer's work shows why independent hydraulic and mechanical measurements matter, but the target chemistry and numerical availability must be verified before quantitative transfer.
4. Consequently, the model should currently be used for (i) mathematical verification, (ii) bounded sensitivity studies, and (iii) predictions of qualitative geometry/pressure trends. It should not yet report fitted target-system intrinsic permeability or modulus.

## Identifiability gate

For a linear poroelastic approximation,

\[
c_v=\frac{K}{m_v\gamma_w}=\frac{K M}{\gamma_w}
\qquad\text{or}\qquad
c_v=\frac{\kappa M}{\mu}.
\]

A single shrinkage curve constrains a lumped transport/mechanical timescale, additionally confounded by geometry and drainage boundaries. At least one independent hydraulic measurement and one independent mechanical measurement are needed to separate permeability from stiffness/compressibility. If either is unavailable, retain a family of admissible parameter pairs rather than selecting one fitted pair.

## Immediate extraction tasks

- Ragueh et al.: map each reported silica grade/sample to structural length scales, pressure range, porosity/solid fraction and cake resistance; resolve the already flagged S3 fractal-dimension table/text discrepancy before using that value.
- Scherer & Swiatek: recover full methods and numerical permeability curves, then mark alkoxide-derived gel values as comparator-only.
- Wilhelm & Kind: digitise measured markers separately from empirical fit curves; retain pressure-cell membrane resistance as a separate apparatus term.
- Do not calibrate the model against a dataset and then call the same dataset an independent validation.
