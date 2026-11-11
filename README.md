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
