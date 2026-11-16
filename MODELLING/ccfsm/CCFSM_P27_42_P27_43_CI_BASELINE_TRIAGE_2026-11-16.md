# P27.42/P27.43 — CI baseline triage (2026-11-16)

## Purpose

This note separates the new interval-arithmetic work from existing CCFSM test
failures. The comparison is against the exact base commit of PR #13, not
against an assumption that the failures are harmless.

## Runs compared

- PR #13 base commit: 54465db7b7870a4c558af3f2304164cc29266712
- Isolated baseline branch: audit/p27-43-ci-baseline-2026-11-16
- Baseline run: 43793591370; 673 tests; 8 failures and 1 error.
- PR #13 run before the final P2742 adapter: 43793522030; 676 tests; 8 failures and 1 error.
- All ten P27.43 rational-checker tests in the PR run passed, including the
  end-to-end comparison against the existing P27.34 interval producer.
- The same nine failing test identifiers occurred in the isolated baseline
  branch and in the PR branch. The PR therefore did not introduce these
  failures. The baseline branch contains only the rational checker and its
  focused tests on top of the PR base.

## Reproduced failures and triage

| Module | Failing test | Observed mismatch | Recommended next action |
|---|---|---|---|
| P27.10 | test_unused_coordinate_vertex_is_reported_outside_mesh_complex | expected locally_manifold_audited; got link_inconsistent | Review the intended treatment of unused coordinate vertices and the edge/link audit preconditions |
| P27.13 | test_invalid_mesh_stops_pipeline | expected mesh_geometry_gate_failed; got integrated_mesh_audit_failed | Align gate ordering and public failure-status contract |
| P27.17 | test_all_processes_close | RHS reconstruction defect 1.0 despite zero global silicon-balance defect | Audit the M/O/N/B field ordering and independent RHS reconstruction |
| P27.17 | test_nonuniform_widths | same RHS reconstruction defect 1.0 on nonuniform cells | Fix together with the P27.17 field-order/reconstruction audit |
| P27.18 | test_bad_positive_domain | uncaught ValueError: concentration must be positive | Decide whether invalid input should raise or be returned as a structured rejection; make the test and API agree |
| P27.23 | test_energy_and_dissipation_units | mechanical-energy integral 19.0; fixture expects 20.0 | Re-derive the discrete quadrature and unit conversion from the test fixture |
| P27.28 | test_exact_polynomial_reference_and_separate_budgets | chemical boundary work 18.24; fixture expects 18.21 | Reconcile exact polynomial integration, boundary-work sign, and separate budget terms |
| P27.37 | test_depth_limit_is_reported | complete returned true when the depth-limit test expects false | Treat every unresolved depth-limited leaf as incomplete; audit the aggregate completeness flag |
| P27.37 | test_root_at_subdivision_boundary_is_not_double_counted | complete returned true when the boundary-root test expects false | Revisit split-point ownership and whether a boundary root is certified, excluded, or unresolved |

## Priority

1. **P27.37 completeness semantics.** A false positive completeness flag can
   overstate what root isolation has established. It should be corrected before
   P27.44 consumes these certificates.
2. **P27.17 process balance and P27.23/P27.28 ledgers.** These affect numerical
   conservation/energy diagnostics and require equation-level audits, not just
   expected-value edits.
3. **P27.10/P27.13 mesh-gate status contracts.** Resolve the state machine and
   status semantics.
4. **P27.18 invalid-domain API behavior.** Make rejection semantics explicit.

These are separate work packages. They are intentionally not changed in PR #13
because they are outside the P27.42/P27.43 interval-certificate scope.

## Interpretation

The rational verifier itself passed all focused tests in the current PR run.
The P27.42 Lean kernel passed before the latest P27.42-to-P27.38 adapter change;
that adapter is being checked by a new Lean run. The Python package workflow is
red because of the nine reproduced baseline failures above, not because of
the new rational-checker tests.

Neither test result validates CCFSM constitutive physics or material
parameters. No CCFSM version number or physical model equation is changed.
