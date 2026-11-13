# Independent review of heterogeneous 1-D solver verification — 13 November 2026

## Scope

Reviewed:
- `MODELLING/transport_model/heterogeneous_1d.py`
- `MODELLING/transport_model/test_heterogeneous_1d.py`
- hosted workflow [#342](https://github.com/Hu3eIn27864/precipitated-silica-gels-review/actions/runs/43493536161)

The solver advances
`S(x) dp/dt = d/dx(lambda(x) dp/dx)`
on a fixed, double-drained slab using cell-centred finite volumes, backward Euler and harmonic face mobility. Storage compliance and mobility are positive and piecewise constant per cell.

## Verified status

Hosted CI #342 passed the complete workflow. The transport-model discovery ran **62 tests successfully**. The heterogeneous solver tests include:
- homogeneous analytical recovery;
- spatial and time refinement against the homogeneous analytical solution;
- non-negativity and non-increasing mean pressure;
- piecewise coefficient execution;
- a non-grid-aligned, centre-classified interface-location refinement test;
- per-step and integrated boundary-outflow/storage-loss balance checks.

This establishes software regression status for the committed implementation. It is not experimental validation.

## Important qualification of the two apparent AP C closure tests

### Interface-location refinement

The test defines material properties by classifying cell centres as left/right of x=0.37, then compares N=40, 80 and 160 against N=320. This is a useful convergence diagnostic, but the discontinuity is represented at a grid face implied by the cell-centre classification. The represented interface therefore shifts with the grid. The test does **not** compare against an independent exact two-layer solution with the physical interface fixed at x=0.37, and it does not isolate the interface-location error from the bulk discretisation error.

### Integrated outflow versus storage loss

The solver constructs boundary outflow from the same finite-volume boundary conductances used in its matrix and reports it at each backward-Euler step. The test then sums this reported outflow and compares it with the cell storage loss. This is a valuable global conservation regression check. However, it is not an independent flux reconstruction from boundary gradients or an independent analytical flux benchmark. The per-step residual is also computed from the same discrete flux balance.

## Remaining AP C numerical gate

The next genuinely independent benchmark should be a two-layer slab with a fixed physical interface x=a, piecewise constant (S1, lambda1) and (S2, lambda2), uniform initial pressure, and p=0 at both outer boundaries.

For an eigenmode p=X(x) exp(-sigma t), define k_i=sqrt(sigma S_i/lambda_i), a left solution X1=A sin(k1 x), and a right solution X2=B sin(k2(L-x)). Continuity of pressure and flux at x=a gives the characteristic condition

`lambda1*k1*cot(k1*a) + lambda2*k2*cot(k2*(L-a)) = 0`.

A reference implementation can locate the eigenvalues and calculate the volume/storage-weighted modal expansion for the average pressure. Compare the transient finite-volume solver with this independent layered reference at early, intermediate and late times, while refining grid and time step separately. The reference should use the exact interface location, not the cell-centre classification used in the current test.

A second independent conservation check should reconstruct the physical boundary gradients from the numerical pressure profiles, integrate the resulting Darcy flux over time with a stated quadrature rule, and compare with total storage loss. Report both the time-integration error and the finite-volume balance residual; do not conflate them.

## Decision

- Existing AP C interface refinement and global balance regression tests: **implemented and passed in CI #342**.
- Independent fixed-interface layered analytical benchmark: **still open**.
- Independent boundary-gradient flux integration: **still open**.
- Time-varying storage, evolving porosity, moving boundaries and coupled mechanics: **deferred**.

No target-system fitting or pH-dependent constitutive law should begin until the independent layered benchmark and the remaining convergence/conservation checks pass.
