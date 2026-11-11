# Examples

The first example configuration and executable smoke test will be added after
the pair-potential and configuration interfaces are implemented.

At this stage, the geometry test can be built from this directory's parent:

```bash
cmake -S . -B build
cmake --build build
ctest --test-dir build --output-on-failure
```

The current test suite covers periodic coordinate wrapping, minimum-image
displacements/distances, and invalid box dimensions. It does not yet test a
particle interaction or run a Monte Carlo trajectory.
