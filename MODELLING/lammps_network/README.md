# LAMMPS coarse-grained network starter

## Purpose

A minimal compression–unloading test for a pre-connected bead network:
unit-mass beads in reduced LJ units, truncated/shifted LJ non-bonded
interactions, permanent harmonic links on a jittered simple-cubic skeleton,
NVT equilibration, 10% isotropic compression and unloading, coordination
output and global pressure/box dimensions.

This is a workflow prototype, not a real silica structure or a prediction of
industrial gel properties.

## Run

Requires Python 3 and a LAMMPS executable built with the MOLECULE package
(required for atom_style bond and bond_style harmonic):

    python3 generate_network.py --n 8 --seed 20261111 --output network.data
    lmp -in in.network_compress_unload.lmp

Executable names depend on installation. No accelerator package is required.

## Manual basis

- LAMMPS manual: https://docs.lammps.org/Manual.html
- pair_style lj/cut: https://docs.lammps.org/pair_lj.html
- bond_style harmonic: https://docs.lammps.org/bond_harmonic.html
- fix deform: https://docs.lammps.org/fix_deform.html

The harmonic bond potential is E=K(r-r0)^2; LAMMPS includes the conventional
factor 1/2 in its definition of K. fix deform with remap x affinely remaps
coordinates and is appropriate for solid-like deformation.

## Crucial limitations

- Initial network is a jittered lattice, not a measured fractal aggregate.
- Permanent harmonic bonds cannot break or reform and do not represent
  siloxane chemistry.
- LJ parameters are arbitrary reduced units, not fitted silica potentials.
- No solvent, hydrodynamic drainage, electrostatics, pH, ions, or surface
  chemistry is represented.
- Simple-cubic skeleton introduces artificial anisotropy and coordination.
- This does not simulate syneresis; it probes mechanical network response.
- Coordination cutoff 1.60 is an analysis convention and needs sensitivity
  testing.

## Required checks

1. Run a zero-deformation control; check energy and temperature stability.
2. Vary timestep and minimisation tolerances.
3. Vary network size, seed, bond probability, LJ epsilon, and harmonic K.
4. Repeat over multiple initial networks and report ensemble spread.
5. Compare compression/recovery, residual strain, coordination, and contact
   persistence.
6. Do not use the same curve for both calibration and validation.
7. Replace the lattice with a structure constrained by experimental data
   before making silica-specific claims.

Next step: compare permanent-bond and reversible-contact networks. Add
kinetic bond formation/breakage only after checking the exact LAMMPS fix or
potential semantics in the installed manual.
