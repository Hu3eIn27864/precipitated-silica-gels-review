# Mechanistic synthesis: pH-dependent network evolution, permeability and syneresis

**Working note; 13 November 2026**  
**Status:** hypothesis framework for the review, not a claim that the proposed feedback has been measured directly in precipitated-silica fragments.

## 1. Central distinction

The observed shrinkage curve is a coupled response, not a direct permeability measurement. A useful minimal description separates:

- hydraulic transport through the evolving pore network, represented by intrinsic permeability \\(\\kappa\\) and liquid viscosity \\(\\mu\\);
- mechanical resistance and relaxation of the silica skeleton, represented by a constrained modulus or a viscoelastic constitutive response;
- structural evolution, including porosity, pore-throat scale, aggregate connectivity/contact number and possible dissolution–reprecipitation.

For a saturated, small-strain reference model, the characteristic consolidation scale is

\\[
t_c \\sim \\frac{L_d^2\\mu}{\\kappa M},
\\]

where \\(L_d\\) is drainage length and \\(M\\) the relevant constrained modulus. This scaling is a framework, not a way to infer \\(\\kappa\\) and \\(M\\) separately from one shrinkage curve.

## 2. What the literature supports — and what it does not

### Directly relevant precipitated-silica evidence

Wilhelm & Kind (2014, 2015) report pressure-dependent enforced-syneresis curves and empirical fit parameters for acid- and base-catalysed precipitated silica gels. The 2015 paper also reports that a thin layer on the membrane in the base-gel tests introduced additional hydraulic resistance affecting kinetics more than the endpoint. This is an important apparatus-level confounder: a shorter fitted time cannot automatically be attributed to an intrinsic network permeability.

Sahabi & Kind (2011) provide a particle/network consolidation model for precipitated silica, but the model omits pore-fluid flow. It therefore addresses structural rearrangement under load rather than the complete transport–mechanics feedback.

### Mechanistic comparators, not direct parameter sources

Scherer (1989, *Mechanics of Syneresis I/II*) shows that contraction-rate and curve-shape depend on sample size, permeability and viscoelastic network properties; the experimental study used independently measured permeability, modulus and viscosity to predict shrinkage curves. This is a strong conceptual precedent for a coupled model, but the material route is alkoxide-derived silica gel.

Scherer & Swiatek (1989) report that permeability of alkoxide-derived silica gel can differ from a simple Carman–Kozeny expectation in a base-catalysed inhomogeneous network, and can fall strongly during partial drying. This supports testing structure-aware hydraulic closures, not transferring numerical permeability values to precipitated silica.

Wang, Winter & Auernhammer (2014) report logarithmic growth of storage modulus and low-frequency structural relaxation in reactive high-pH silica gels, attributed to finite silica solubility and finite bond lifetime. This makes a purely elastic, time-independent skeleton a questionable universal assumption for alkaline reactive gels. The studied reactive sodium-silicate gel is a comparator; the result does not establish the same relaxation law in industrial precipitated-silica fragments.

## 3. Competing hypotheses to retain

**H1 — Transport-limited consolidation.** The network mechanics are comparatively fast, while liquid drainage through low-permeability pore throats controls the observed timescale. Prediction: characteristic time scales strongly with drainage length and independently measured \\(\\kappa^{-1}\\), after accounting for viscosity and modulus.

**H2 — Mechanics/reorganisation-limited consolidation.** Contact formation, bond rearrangement or viscoelastic relaxation controls the rate. Prediction: shrinkage kinetics correlate with creep/recovery or rheological relaxation even when hydraulic geometry is held fixed.

**H3 — Coupled aging feedback.** Compaction increases contact number and skeleton stiffness while changing porosity and pore-throat connectivity. Permeability may decrease as pores constrict, but may also change non-monotonically if rearrangement opens or closes connected pathways. Prediction: time-dependent \\(\\kappa(t)\\) and \\(M(t)\\) are both required; a single fitted \\(\\tau\\) is not enough to separate them.

**H4 — Chemistry-mediated restructuring.** At sufficiently high pH, silica dissolution/reprecipitation and finite bond lifetime may modify network relaxation and connectivity. Prediction: pH effects depend on dissolved silica, ionic strength and solution history, and cannot be reduced to pH as a categorical label alone.

**H5 — Apparatus-limited drainage.** Membrane fouling, cake formation or external hydraulic resistance contributes materially to the measured response. Prediction: changing membrane/support conditions changes kinetics while the intrinsic gel endpoint or independently measured structure changes little.

These hypotheses are not mutually exclusive. The experiment should discriminate their relative contributions rather than select one from the shape of a single curve.

## 4. Acid/base comparison: cautious interpretation

The published pressure-cell fit summaries show shorter characteristic times for the 2015 base-gel series than for the acid-gel series at broadly comparable pressures. This is a descriptive observation from one research programme, not proof that alkaline gels have intrinsically higher permeability. Pressure ranges, curve-fit forms, membrane effects and network chemistry must be kept distinct.

For the acid 2014/2015 comparison, the papers report no significant membrane-related difference for the acid gel after switching NF270 to NP010. The authors explicitly do not extend that statement to the base gel, where a membrane-associated layer affected flow resistance. Thus, a simple acid-versus-base rate ratio is not a clean material-property contrast.

## 5. Minimum discriminating experimental programme

Use matched precipitation batches and record pH, temperature, ionic strength, dissolved silica and age at each measurement.

1. **Hydraulic:** measure permeability under a low pressure gradient while simultaneously monitoring sample height/volume and expelled liquid. Repeat at more than one drainage length. Correct for sample deformation and external membrane/support resistance.
2. **Mechanical:** perform confined compression or creep/recovery on matched specimens to estimate the relevant constrained response; do not substitute (G') or an instantaneous modulus without a constitutive conversion.
3. **Rheological aging:** measure (G'(t,\\omega)) and (G''(t,\\omega)) across a frequency window broad enough to detect low-frequency relaxation.
4. **Structure:** track porosity, pore-throat distribution, aggregate/fragment size and contact/network descriptors at matched aging times.
5. **Chemistry:** quantify dissolved silica and ionic composition of pore liquid and expelled liquid.
6. **Boundary controls:** compare membrane/support materials and include a hydraulic blank or inert porous reference to identify external resistance.

A decisive test is whether measured \\(\\kappa(t)\\), \\(M(t)\\), viscosity and drainage geometry predict shrinkage without refitting an arbitrary time constant to the same curve.

## 6. Modelling sequence and stop rules

- Retain the fixed-coefficient 1-D solver as a verification baseline.
- First add prescribed, independently constrained \\(\\kappa(t)\\) or spatial heterogeneity while keeping the other closure fixed; do not fit both from one shrinkage curve.
- Introduce viscoelastic memory only if creep/rheology demonstrates it is needed.
- Add chemistry-dependent restructuring only when dissolved-silica and structural measurements constrain it.
- Add pressure/compaction feedback to the particle/MC model only after the one-way transport model is identifiable and stable.
- Do not call a fitted effective diffusivity an independently measured permeability or modulus.

## References

- Wilhelm & Kind (2014), *Polymers* 6, 2896–2911. DOI: 10.3390/polym6122896.
- Wilhelm & Kind (2015), *Polymers* 7, 2504–2521. DOI: 10.3390/polym7121528.
- Sahabi & Kind (2011), *Polymers* 3, 2156–2171. DOI: 10.3390/polym3042156.
- Scherer (1989), *J. Non-Cryst. Solids* 108, 18–27 and 28–36. DOI: 10.1016/0022-3093(89)90328-1 and 10.1016/0022-3093(89)90329-3.
- Scherer & Swiatek (1989), *J. Non-Cryst. Solids* 113, 119–129. DOI: 10.1016/0022-3093(89)90002-1.
- Wang, Winter & Auernhammer (2014), *J. Colloid Interface Sci.* 413, 159–166. DOI: 10.1016/j.jcis.2013.09.035.


## Additional mechanistic constraint from Wilhelm & Kind (2015)

The 2015 study distinguishes acid- and base-catalysed condensation pathways: acidic conditions are described as favouring more linear, weakly branched structures, whereas basic conditions favour more highly branched clusters. It also discusses the strong increase in monomeric silicic-acid solubility above approximately pH 8. These observations imply that pH can affect both network topology and dissolution/reprecipitation, not merely the rate constant of one common syneresis law. The reported trends should be interpreted within the specific sodium-silicate/sulfuric-acid formulations and conditions used by Wilhelm & Kind, not universalised to all silica gels.

**Model consequence:** do not encode pH only as a scalar multiplier on permeability or on a common kinetic rate. Treat acid/base route as potentially different structural and chemical closures, and test whether a common hydraulic equation remains adequate after independently measuring permeability and mechanics.
