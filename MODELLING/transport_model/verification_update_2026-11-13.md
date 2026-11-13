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
- New workflows #360, #361, #362 and #363: all four complete integrated workflows succeeded, including the 1-D transport suite and downstream DLCA/pilot stages.
- No new silica material parameter was fitted or validated.
- Numerical convergence, eigenvalue consistency and discrete conservation are code verification, not experimental validation of precipitated-silica syneresis.

## Files added or extended

- Extended MODELLING/transport_model/test_layered_reference.py with off-grid interface test.
- Added MODELLING/transport_model/multilayer_reference.py.
- Added MODELLING/transport_model/test_multilayer_reference.py.
- Added MODELLING/transport_model/test_time_dependent_reference.py.


## 5. Interface-aware finite-volume implementation

Added interface_aware_1d.py. The caller supplies exact physical layer boundaries and one storage/mobility value per layer. The method integrates storage exactly over each cell-layer overlap, including cut cells. For each pressure-centre connection and drained boundary half-cell, it integrates 1/lambda exactly over the traversed layer segments and inverts the total series resistance to obtain conductance.

The backward-Euler FV system retains cell-centred representative pressures and mass-lumped capacity, while resolving the discontinuity geometry in both storage and flux conductance. A separate module preserves compatibility with the earlier array-based solver.

Tests in test_interface_aware_1d.py check the homogeneous limit, off-grid two-layer mean response against the independent eigenfunction series, exact cut-cell capacity, exact conductance across a face segment containing the interface, global conservation/positivity for a three-layer stack, and invalid geometry rejection.

This is an interface-aware piecewise-constant coefficient discretisation, not a general high-order embedded-interface scheme. It does not yet handle moving interfaces, contact resistance, nonlinear material laws, or within-layer smooth variation. The original interface-aware implementation and its five-test suite passed the full integrated CI workflow #374 (build, C++, Python, 1-D transport, syneresis sensitivity and DLCA stages): https://github.com/Hu3eIn27864/precipitated-silica-gels-review/actions/runs/43510730207.


## 6. Off-grid interface eigenmode: full-profile test

Extended `solve_interface_aware` with an optional cell-centred initial pressure profile while preserving the uniform scalar default. Added a manufactured transient based on the independent first eigenmode for the two-layer problem with interface at x=0.37. The analytical mode enforces both pressure continuity and nonzero Darcy-flux continuity; the test compares the full cell-centred numerical profile against its exact exponential decay for N=40,80,160. A separate invalid-profile test checks input validation. This is a profile-level interface verification, not merely a mean-pressure comparison. Hosted CI is running; convergence order and final pass status remain pending until the run is inspected.


CI follow-up: workflow #376 completed successfully, including build, C++ tests, Python ensemble tests, the complete 1-D transport test step (including the new off-grid full-profile eigenmode test), syneresis sensitivity, all DLCA pilot stages and artifact upload. Run: https://github.com/Hu3eIn27864/precipitated-silica-gels-review/actions/runs/43511164695.


Independent numerical cross-check of the full-profile test: a separate NumPy implementation of the same finite-volume equations, using the exact two-layer eigenmode and the test's grid/time sequence, gave RMS profile errors 1.428e-5, 2.301e-6 and 7.729e-7 for N=40,80,160 (dt=1.5625e-4, 3.90625e-5 and 9.765625e-6 s; final time 0.005 s). This independently confirms decreasing error and comfortable margin below the test threshold. The ratios are not used to claim a formal asymptotic order; the test itself asserts monotone refinement, not a prescribed order.


## Interface contact resistance extension

Added optional area-specific contact resistances (Pa s/m) to the interface-aware FV solver. For the transfer state q=lambda dp/dx, the interface conditions are q_left=q_right and p_right-p_left=R_c q. The actual Darcy flux is -q. When any contact resistance is positive, the FV graph is augmented with co-located minus/plus interface pressure unknowns. Their control volumes are split at the interface, with storage integrated separately on each side; the link between traces has conductance 1/R_c. This representation works for off-grid interfaces and for interfaces exactly at an original cell centre.

The independent multilayer transfer-matrix reference applies the same jump law. Its zero-contact limit recovers the previous reference; positive contact resistance reduces modal decay rates. The three-layer FV test checks slower pressure relaxation and exact global conservation. The full-profile eigenmode test compares the augmented transient solution with the analytical three-layer mode. This parameter is phenomenological, not a silica measurement.


## Two-sided interface pressure degrees of freedom

The interface-aware solver now inserts a co-located `minus`/`plus` pressure pair for every interface with positive contact resistance. The two adjacent control volumes terminate/start exactly at the interface and their storage is integrated on the appropriate material side. The contact link has conductance 1/R_c; bulk links use exact integrated piecewise resistance. Thus a contact at a cell centre is no longer rejected or hidden inside a single pressure unknown. The solver exposes augmented node profiles and side labels while retaining a projected original-cell-centre profile for API compatibility. Tests cover a contact exactly at x=0.3625 (a cell centre for N=40), the resulting nonzero pressure jump, exact 1/R_c conductance, and the existing three-layer transient eigenmode case. Hosted workflow #399 passed all 92 transport tests and the complete integrated pipeline, including build, C++, Python, syneresis sensitivity and DLCA stages: https://github.com/Hu3eIn27864/precipitated-silica-gels-review/actions/runs/43512476946.
