# Precipitated Silica Gels — Critical Review Project

**Working title:** *Structural Evolution and Interparticle Interactions in Precipitated Silica Gels: From Aggregation to Consolidation and Syneresis*

## Purpose
A critical, evidence-led review of how the process history of precipitated silica governs structural evolution, interparticle interactions, consolidation, syneresis, and final material properties.

## Central question
**How does the process history of precipitated silica gels influence their subsequent reorganisation, consolidation, and syneresis?**

## Scope and conceptual pathway
Precipitation and primary-particle formation → aggregation and gelation → fragmentation → consolidation and structural reorganisation → natural/enforced syneresis → final properties (aggregate/agglomerate size, porosity, surface area, mechanical stability).

The review will distinguish industrially precipitated silica from related but non-equivalent systems (e.g. water-glass-derived model gels, TEOS/alkoxide sol–gel materials, and generic colloidal silica).

## Editorial principles
- Evidence before narrative: claims must be traceable to specific sources and results.
- Separate direct experimental evidence, indirect evidence, simulations, theoretical models, and review-level interpretation.
- Do not infer industrial transferability merely from chemical similarity.
- Record limitations, contradictory findings, and uncertainty.
- Avoid novelty claims until the literature search and comparison with existing reviews are complete.
- Target journal: *Langmuir* (subject to a later fit and editorial-scope assessment).
- Publication route: subscription publication; no assumption of an APC budget. Verify current publisher policies before submission.

## Repository map
- `REVIEW_SCOPE.md` — scope, research questions, inclusion/exclusion boundaries.
- `METHODS/` — search and evidence-appraisal protocol.
- `LITERATURE/` — source database, individual assessments, and exclusions.
- `OUTLINE/` — proposed review architecture.
- `MANUSCRIPT/` — draft text.
- `FIGURES/` — figure concepts and evidence mapping.
- `MODELLING/` — hypothesis-driven model strategy, candidate validation datasets, and starter transport/LAMMPS prototypes.
- `MODELLING/ROADMAP_STATUS_2026-11-13.md` — current AP/work-package status, gates, and immediate execution order.
- `CHANGELOG.md` — substantive project decisions.

## Evidence grades
- **A** — direct, strong evidence relevant to precipitated silica.
- **B** — valuable mechanistic or methodological evidence, with transferability limits.
- **C** — indirect/background evidence.
- **D** — exclude from the evidential core (irrelevant, unreliable, or redundant).
- **V** — verification pending (bibliographic record, full text, or methods not yet checked).

A/B/C/D are provisional until the source has been checked at the appropriate depth. **V is a workflow status, not a quality grade.** Scientific quality and relevance to this review are assessed separately.

## Current status
The literature database and claim–evidence synthesis are under active development, with source-family overlap and access status tracked explicitly. The optional modelling workstream has been defined; first executable 1-D transport and coarse-grained LAMMPS prototypes are available as non-predictive baselines. No production simulation has been calibrated or run, and no model parameter is yet claimed to represent measured silica properties.


## Current parallel research plan

The next gated work packages for DLCA robustness, radial transport verification, literature validation, and manuscript synthesis are maintained in [MODELLING/NEXT_STEPS_PARALLEL_PLAN.md](MODELLING/NEXT_STEPS_PARALLEL_PLAN.md). This plan separates software checks from physical validation and records explicit stop rules.

Latest execution notes: [heterogeneous transport-solver verification review](MODELLING/transport_model/heterogeneous_1d_verification_review_2026-11-13.md), [transport-parameter evidence comparison](LITERATURE/transport_parameter_comparison_2026-11-13.md) (including the new PSG-047 silica-sol comparator), and [latest DLCA test/artifact audit](MODELLING/monte_carlo_3d/TEST_RESULTS.md).

## Digitized syneresis curves — provenance and reuse

The curve-digitization dataset used in the syneresis analysis was independently digitized from figures in:

Wilhelm, S.; Kind, M. (2015). *Influence of pH, Temperature and Sample Size on Natural and Enforced Syneresis of Precipitated Silica*. **Polymers**, 7(12), 2504–2521. https://doi.org/10.3390/polym7121528

The article is published under the **Creative Commons Attribution 4.0 International (CC BY 4.0)** license (https://creativecommons.org/licenses/by/4.0/). Reuse and adaptation of material covered by that license are permitted subject to its terms. Before redistributing any particular figure or figure-derived material, check its caption and credit line for third-party material or a separate rights notice; such material may not be covered by the article's general license.

The CSV is an independently produced, figure-derived digitization for quantitative analysis and model development. It is **not** the authors' original experimental dataset and should not be cited or described as raw measurement data supplied by the authors. Cite the source publication whenever using or redistributing the digitized values, identify the values as digitized, and describe any subsequent processing or modifications.

**Trace limitation:** in some panels, experimental and model traces overlap or cannot be distinguished reliably. The affected series are therefore labelled as combined visible traces; they must not be presented as exclusively experimental measurements. The original figures are not reproduced in this dataset.

Suggested attribution: “Data digitized from figures in Wilhelm and Kind (2015), *Polymers* 7(12), 2504–2521, https://doi.org/10.3390/polym7121528 (CC BY 4.0). Digitization and any subsequent processing by this project; values are figure-derived, not original author-supplied raw data.”
