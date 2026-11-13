# Research status — 13 November 2026

## Parallel synthesis and modelling work

This update records work completed while the numerical data-analysis facility was unavailable for the second-stage CSV audit. No new numerical curve results are claimed here.

### Completed synthesis outputs

- Added `SYNTHESIS/pH_dependent_network_permeability_syneresis_framework.md`.
  - Separates hydraulic transport, skeleton mechanics/relaxation, structural evolution and chemistry.
  - Defines five competing, non-exclusive hypotheses: transport-limited, mechanics/reorganisation-limited, coupled aging feedback, chemistry-mediated restructuring and apparatus-limited drainage.
  - Specifies a matched hydraulic/mechanical/rheological/structural/chemical measurement programme.
  - Explicitly distinguishes direct precipitated-silica evidence from alkoxide-derived and reactive water-glass comparator systems.

- Added `LITERATURE/common_form_syneresis_kinetic_analysis_protocol.md`.
  - Defines provenance classes for published fit parameters, AI-digitised combined traces and independently verified measured traces.
  - Pre-registers common stretched-exponential fits with n=1.23 and n=1.00 sensitivity cases.
  - Defines fit eligibility, digitisation uncertainty propagation, fit-window sensitivity and reporting language.
  - Prohibits treating the last plotted point as an asymptote or calling smooth AI-digitised traces raw measurements.

### Mechanistic synthesis: current defensible position

The literature supports a coupled framework in which pore-liquid transport and network viscoelasticity both affect syneresis. Scherer (1989) explicitly relates contraction kinetics and curve shape to permeability and viscoelastic properties and reports agreement using independently measured permeability, modulus and viscosity in alkoxide-derived silica gels. This is a conceptual precedent, not a direct parameter source for precipitated silica.

Wang, Winter & Auernhammer (2014) report logarithmic storage-modulus growth and low-frequency structural relaxation in reactive high-pH silica gels, attributed to finite silica solubility and bond lifetime. This justifies testing time-dependent mechanical response for alkaline reactive systems; it does not prove the same law applies to industrial precipitated-silica fragments.

Wilhelm & Kind (2015) report membrane-associated additional flow resistance for the base-gel pressure-cell series, affecting kinetics more than the endpoint. Thus, pressure-cell acid/base rate differences cannot be interpreted as intrinsic permeability differences without membrane/support controls.

### Next scientific priorities

1. Complete the 2015 acid/base digitised-curve audit when data analysis is available.
2. Independently verify the plotted measured traces against original Figure 12; the uploaded CSV identifies combined visible traces where measurement/model overlap is inseparable.
3. Do not fit combined traces as primary observations. Use them only in labelled exploratory sensitivity analyses.
4. Keep 2014 versus 2015 acid membrane-repeat comparisons separate from acid-versus-base chemistry comparisons.
5. Before any time-dependent poroelastic closure, obtain independent constraints on permeability and the relevant constrained/viscoelastic modulus.

### External source checks used in this synthesis

- Scherer (1989), *Mechanics of Syneresis I. Theory*, DOI 10.1016/0022-3093(89)90328-1.
- Scherer (1989), *Mechanics of Syneresis II. Experimental Study*, DOI 10.1016/0022-3093(89)90329-3.
- Scherer & Swiatek (1989), *Measurement of Permeability II: Silica Gel*, DOI 10.1016/0022-3093(89)90002-1.
- Wang, Winter & Auernhammer (2014), *Time and frequency dependent rheology of reactive silica gels*, DOI 10.1016/j.jcis.2013.09.035.

**Validation boundary:** these additions are literature synthesis and analysis protocol, not experimental validation of the proposed feedback model. No repository code tests were run in this workstream.
