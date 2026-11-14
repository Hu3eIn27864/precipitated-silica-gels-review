"""CCFSM P4: conservative variable-capacity advection-diffusion-reaction operator."""
from __future__ import annotations
from dataclasses import dataclass
import math
from ccfsm_p2_chemical_affinity import ChemicalParametersP2, ChemicalStateP2, p2_rhs


@dataclass(frozen=True)
class P4Grid:
    shape: tuple[int, ...]
    spacing: tuple[float, ...]

    def __post_init__(self):
        if not self.shape or len(self.shape) not in (1, 2, 3):
            raise ValueError("grid must have one, two, or three dimensions")
        if len(self.shape) != len(self.spacing):
            raise ValueError("shape and spacing dimensions must agree")
        if any(not isinstance(n, int) or n < 1 for n in self.shape):
            raise ValueError("grid extents must be positive integers")
        if any(not math.isfinite(h) or h <= 0 for h in self.spacing):
            raise ValueError("grid spacings must be finite and positive")

    @property
    def cell_count(self):
        result = 1
        for n in self.shape:
            result *= n
        return result

    @property
    def cell_volume(self):
        result = 1.0
        for h in self.spacing:
            result *= h
        return result

    @property
    def strides(self):
        result = []
        for axis in range(len(self.shape)):
            stride = 1
            for n in self.shape[axis + 1:]:
                stride *= n
            result.append(stride)
        return tuple(result)

    def faces(self):
        """Yield (axis, left, right, spacing) for each interior face once."""
        for axis, (extent, h, stride) in enumerate(
            zip(self.shape, self.spacing, self.strides)
        ):
            for left in range(self.cell_count):
                coordinate = (left // stride) % extent
                if coordinate + 1 < extent:
                    yield axis, left, left + stride, h

    def face_counts(self):
        return tuple(
            (self.cell_count // extent) * max(extent - 1, 0)
            for extent in self.shape
        )


def p4_rhs(concentrations, theta, grid, diffusivities, face_fluxes, parameters):
    """Return (dc_i/dt, dtheta/dt); Q is oriented low-to-high on each axis."""
    if len(concentrations) != 4 or len(diffusivities) != 4:
        raise ValueError("exactly four species and diffusivities are required")
    if len(theta) != grid.cell_count:
        raise ValueError("theta must match grid cell count")
    th = tuple(float(v) for v in theta)
    if any(not math.isfinite(v) or v <= 0 for v in th):
        raise ValueError("theta must be finite and strictly positive")
    fields = []
    ds = tuple(float(v) for v in diffusivities)
    if any(not math.isfinite(v) or v <= 0 for v in ds):
        raise ValueError("diffusivities must be finite and positive")
    for field in concentrations:
        if len(field) != grid.cell_count:
            raise ValueError("each species field must match grid cell count")
        values = tuple(float(v) for v in field)
        if any(not math.isfinite(v) or v < 0 for v in values):
            raise ValueError("concentrations must be finite and nonnegative")
        fields.append(values)
    if len(face_fluxes) != len(grid.shape):
        raise ValueError("one face-flux array is required per spatial axis")
    q_fields = tuple(tuple(float(q) for q in axis) for axis in face_fluxes)
    if any(any(not math.isfinite(q) for q in axis) for axis in q_fields):
        raise ValueError("face fluxes must be finite")
    if tuple(map(len, q_fields)) != grid.face_counts():
        raise ValueError("face-flux array lengths do not match the grid")

    theta_rhs = [0.0] * grid.cell_count
    mass_rhs = [[0.0] * grid.cell_count for _ in range(4)]
    for cell in range(grid.cell_count):
        reaction = p2_rhs(
            ChemicalStateP2(*(fields[s][cell] for s in range(4))), parameters
        )
        for s in range(4):
            mass_rhs[s][cell] = th[cell] * reaction[s]

    face_positions = [0] * len(grid.shape)
    for axis, left, right, h in grid.faces():
        pos = face_positions[axis]
        q = q_fields[axis][pos]
        face_positions[axis] += 1
        theta_rhs[left] -= q / h
        theta_rhs[right] += q / h
        theta_face = 0.5 * (th[left] + th[right])
        for s in range(4):
            c_left, c_right = fields[s][left], fields[s][right]
            c_upwind = c_left if q >= 0.0 else c_right
            total_flux = q * c_upwind - theta_face * ds[s] * (
                c_right - c_left
            ) / h
            mass_rhs[s][left] -= total_flux / h
            mass_rhs[s][right] += total_flux / h

    concentration_rhs = tuple(tuple(
        (mass_rhs[s][cell] - fields[s][cell] * theta_rhs[cell]) / th[cell]
        for cell in range(grid.cell_count)
    ) for s in range(4))
    return concentration_rhs, tuple(theta_rhs)


def p4_total_silicon(concentrations, theta, grid):
    """Reference-volume integral of total Si-equivalent pore inventory."""
    if len(concentrations) != 4 or len(theta) != grid.cell_count:
        raise ValueError("four species and a matching theta field are required")
    if any(len(field) != grid.cell_count for field in concentrations):
        raise ValueError("each species field must match grid cell count")
    return grid.cell_volume * sum(
        float(theta[cell]) * sum(float(concentrations[s][cell]) for s in range(4))
        for cell in range(grid.cell_count)
    )
