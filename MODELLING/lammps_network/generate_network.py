#!/usr/bin/env python3
"""Generate a jittered simple-cubic network for LAMMPS atom_style bond.

This is a numerical toy network, not a structural model of real silica.
"""
from __future__ import annotations
import argparse
import random
from pathlib import Path

def generate(n: int, spacing: float, jitter_fraction: float,
             bond_probability: float, seed: int, output: Path) -> None:
    rng = random.Random(seed)
    atom_id, atoms = {}, []
    idx, jitter = 0, jitter_fraction * spacing
    for ix in range(n):
        for iy in range(n):
            for iz in range(n):
                idx += 1
                atom_id[(ix, iy, iz)] = idx
                xyz = [(q + 0.5) * spacing + rng.uniform(-jitter, jitter)
                       for q in (ix, iy, iz)]
                atoms.append((idx, 1, 1, *xyz))
    bonds = []
    for ix in range(n):
        for iy in range(n):
            for iz in range(n):
                a = atom_id[(ix, iy, iz)]
                for nb in (((ix+1) % n, iy, iz),
                           (ix, (iy+1) % n, iz),
                           (ix, iy, (iz+1) % n)):
                    if rng.random() <= bond_probability:
                        bonds.append((len(bonds)+1, 1, a, atom_id[nb]))
    box = n * spacing
    with output.open("w", encoding="utf-8") as h:
        h.write("Coarse-grained toy network; reduced units; not real silica\n\n")
        h.write(f"{len(atoms)} atoms\n{len(bonds)} bonds\n\n")
        h.write("1 atom types\n1 bond types\n\n")
        for axis in "xyz":
            h.write(f"0.0 {box:.10f} {axis}lo {axis}hi\n")
        h.write("\nMasses\n\n1 1.0\n\nAtoms # bond\n\n")
        for a in atoms:
            h.write(f"{a[0]} {a[1]} {a[2]} {a[3]:.10f} {a[4]:.10f} {a[5]:.10f}\n")
        h.write("\nBonds\n\n")
        for b in bonds:
            h.write(f"{b[0]} {b[1]} {b[2]} {b[3]}\n")
    print(f"Wrote {len(atoms)} beads and {len(bonds)} permanent bonds to {output}")

def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--n", type=int, default=8)
    p.add_argument("--spacing", type=float, default=1.25)
    p.add_argument("--jitter", type=float, default=0.025,
                   help="maximum positional jitter as fraction of spacing")
    p.add_argument("--bond-probability", type=float, default=0.95)
    p.add_argument("--seed", type=int, default=20261111)
    p.add_argument("--output", type=Path, default=Path("network.data"))
    a = p.parse_args()
    if a.n < 3 or a.spacing <= 0 or a.jitter < 0:
        p.error("n >= 3, spacing > 0, jitter >= 0 required")
    if not 0 < a.bond_probability <= 1:
        p.error("bond-probability must be in (0,1]")
    generate(a.n, a.spacing, a.jitter, a.bond_probability, a.seed, a.output)

if __name__ == "__main__":
    main()
