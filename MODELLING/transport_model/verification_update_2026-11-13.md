# Transport solver: four-step verification update — 13 November 2026

## Scope

This update closes the prior CI check and adds three independent verification branches. It distinguishes completed test steps from full workflow completion.

## 1. Previous nonzero-flux two-layer eigenmode

GitHub Actions workflow #359 completed successfully. Build, C++ tests, Python ensemble analysis, 1-D transport tests, syneresis leave-one-out sensitivity, DLCA pilot tasks and artifact upload all succeeded.

Run: https://github.com/Hu3eIn27864/precipitated-silica-gels-review/actions/runs/43508296549

## 2. Off-grid material interface

Added a test in test_layered_reference.py using a two-layer jump at x=0.37 with N=40,80,160. These grids do not align the interface with a cell face. The solver uses coefficients sampled at cell centres; the test compares the computed mean pressure with the independent fixed-interface eigenfunction expansion and requires error reduction under refinement.

Interpretation: this is a basic convergence check for the current representation. It is not evidence of a specified convergence order. In particular, cell-centre sampling does not explicitly represent the subcell interface location. A more accurate interface-aware FV method should integrate storage compliance over cut cells and calculate face conductance from the exact series resistance of the material segments between adjacent pressure unknowns.

CI #360 1-D transport test step: passed. Full workflow was still running at note time.

## 3. Three-layer transfer-matrix eigenvalue reference

Added multilayer_reference.py. In each layer, the state vector (p,q), q=lambda dp/dx, is propagated using the exact constant-coefficient transfer matrix. The drained-slab eigencondition is p(L)=0.

Tests cover:
- recovery of the homogeneous eigenvalue spectrum when three identical layers are stacked;
- ordered eigenvalues for a heterogeneous three-layer stack;
- small characteristic residual at each returned root;
- rejection of invalid layer arrays.

CI #362 1-D transport test step: passed. Full workflow was still running at note time.

Interpretation: this is an independent multilayer eigenvalue reference. A transient multilayer FV convergence benchmark and nonzero-flux multilayer eigenfunction test remain future work.

## 4. Time-dependent mobility reference

Added test_time_dependent_reference.py for the existing per-step prescribed-mobility solver. For spatially uniform mobility lambda(t)=1+0.5t and fixed storage S=1, the PDE reduces to the constant-coefficient slab under transformed time theta(t)=integral(lambda/S dt). The test compares mean pressure with the independent two-layer series reference in the identical-material limit and checks time-step refinement. A second test checks stepwise global storage/flux balance and nonnegative pressure.

CI #363 1-D transport test step: passed. Full workflow was still running at note time.

Interpretation: the solver still has fixed storage compliance and prescribed mobility schedule. It is not a coupled aging law and does not include evolving modulus, porosity, geometry, or feedback from network restructuring.

## Overall status and physical limits

- Previous workflow #359: full integrated workflow successful.
- New workflows #360, #362, #363: their 1-D transport test steps passed; integrated DLCA/pilot stages had not yet all completed at the time of this note.
- Workflow #361 (the standalone transfer-matrix module commit) was still in progress at the last check; its code is exercised by the subsequent #362 transport test step.
- No new silica material parameter was fitted or validated.
- Numerical convergence, eigenvalue consistency and discrete conservation are code verification, not experimental validation of precipitated-silica syneresis.

## Files added or extended

- Extended MODELLING/transport_model/test_layered_reference.py with off-grid interface test.
- Added MODELLING/transport_model/multilayer_reference.py.
- Added MODELLING/transport_model/test_multilayer_reference.py.
- Added MODELLING/transport_model/test_time_dependent_reference.py.
