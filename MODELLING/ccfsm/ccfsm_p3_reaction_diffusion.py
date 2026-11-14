"""CCFSM P3: conservative finite-volume reaction-diffusion operator.

Pure-Python reference semidiscretization on a uniform Cartesian cell grid.
Concentrations are mol Si-equivalent per m^3 pore liquid. The outer boundary
is no-flux. This is a numerical reference operator, not a calibrated solver.
"""
from __future__ import annotations

from dataclasses import dataclass
from itertools import product
import math

from ccfsm_p2_chemical_affinity import (
    ChemicalParametersP2, ChemicalStateP2, p2_rhs,
)


@dataclass(frozen=True)
class P3Grid:
    shape: tuple[int, ...]
    spacing: tuple[float, ...]

    def __post_init__(self):
        if not self.shape or len(self.shape) not in (1, 2, 3):
            raise ValueError("grid must have one, two, or three dimensions")
        if len(self.shape) != len(self.spacing):
            raise ValueError("shape and spacing dimensions must agree")
        if any(not isinstance(n, int) or n < 1 for n in self.shape):
            raise ValueError("each grid extent must be a positive integer")
        if any(not math.isfinite(h) or h <= 0.0 for h in self.spacing):
            raise ValueError("grid spacings must be finite and positive")

    @property
    def cell_count(self) -> int:
        n = 1
        for extent in self.shape:
            n *= extent
        return n

    @property
    def cell_volume(self) -> float:
        result = 1.0
        for h in self.spacing:
            result *= h
        return result

    @property
    def strides(self) -> tuple[int, ...]:
        out = []
        for axis in range(len(self.shape)):
            stride = 1
            for extent in self.shape[axis + 1:]:
                stride *= extent
            out.append(stride)
        return tuple(out)

    def neighbors(self, flat_index: int):
        """Yield (neighbor_index, axis, inverse_spacing_squared)."""
        if flat_index < 0 or flat_index >= self.cell_count:
            raise IndexError("flat cell index outside grid")
        strides = self.strides
        for axis, (extent, h, stride) in enumerate(zip(self.shape, self.spacing, strides)):
            coordinate = (flat_index // stride) % extent
            inv_h2 = 1.0 / (h * h)
            if coordinate > 0:
                yield flat_index - stride, axis, inv_h2
            if coordinate + 1 < extent:
                yield flat_index + stride, axis, inv_h2


def p3_rhs(
    concentrations: tuple[tuple[float, ...], ...],
    grid: P3Grid,
    diffusivities: tuple[float, float, float, float],
    porosity: float,
    parameters: ChemicalParametersP2,
) -> tuple[tuple[float, ...], ...]:
    """Return semidiscrete dc_i/dt with no-flux finite-volume diffusion.

    The four outer tuples are M, O, N, B; each contains one value per cell.
    Pairwise neighbor fluxes cancel exactly in the global cell sum.
    """
    if len(concentrations) != 4 or len(diffusivities) != 4:
        raise ValueError("exactly four species and diffusivities are required")
    if not math.isfinite(porosity) or not 0.0 < porosity <= 1.0:
        raise ValueError("porosity must lie in (0, 1]")
    fields = []
    for i, field in enumerate(concentrations):
        if len(field) != grid.cell_count:
            raise ValueError("each species field must match grid cell count")
        values = tuple(float(v) for v in field)
        if any(not math.isfinite(v) or v < 0.0 for v in values):
            raise ValueError("concentrations must be finite and nonnegative")
        d = float(diffusivities[i])
        if not math.isfinite(d) or d <= 0.0:
            raise ValueError("diffusivities must be finite and positive")
        fields.append(values)

    out = [[0.0] * grid.cell_count for _ in range(4)]
    for cell in range(grid.cell_count):
        local = ChemicalStateP2(*(fields[s][cell] for s in range(4)))
        reaction = p2_rhs(local, parameters)
        for s in range(4):
            out[s][cell] = reaction[s]

    # Symmetric two-point finite-volume flux; porosity cancels from
    # phi*dc/dt = div(phi*D*grad(c)) + phi*R for constant phi.
    for cell in range(grid.cell_count):
        for neighbor, axis, inv_h2 in grid.neighbors(cell):
            if neighbor <= cell:
                continue
            for s in range(4):
                flux_rate = diffusivities[s] * inv_h2 * (
                    fields[s][neighbor] - fields[s][cell]
                )
                out[s][cell] += flux_rate
                out[s][neighbor] -= flux_rate

    return tuple(tuple(field) for field in out)


def p3_total_silicon(
    concentrations: tuple[tuple[float, ...], ...],
    grid: P3Grid,
    porosity: float,
) -> float:
    """Compute pore-volume weighted total Si-equivalent amount."""
    if len(concentrations) != 4 or any(len(f) != grid.cell_count for f in concentrations):
        raise ValueError("four fields matching the grid are required")
    if not math.isfinite(porosity) or not 0.0 < porosity <= 1.0:
        raise ValueError("porosity must lie in (0, 1]")
    return porosity * grid.cell_volume * sum(sum(f) for f in concentrations)


def p3_regularized_bridge_fraction(
    network: float, bridge: float, delta_bridge: float
) -> float:
    """Regularized P3 bridge fraction c_B/(c_N+c_B+delta_B)."""
    values = (network, bridge, delta_bridge)
    if any(not math.isfinite(float(v)) for v in values):
        raise ValueError("bridge concentrations must be finite")
    network, bridge, delta_bridge = map(float, values)
    if network < 0.0 or bridge < 0.0 or delta_bridge <= 0.0:
        raise ValueError("network/bridge must be nonnegative and delta positive")
    return bridge / (network + bridge + delta_bridge)
