#pragma once

#include "Vec3.hpp"

#include <vector>

namespace mc3d {

struct MassRadiusPoint {
    double radius{0.0};
    double meanEnclosedMass{0.0};
};

// Averages the number of particles within each radius over every particle
// used as a centre. The central particle is included in the count.
// Coordinates must already be graph-unwrapped for one non-winding component.
std::vector<MassRadiusPoint> calculateMassRadiusCurve(
    const std::vector<Vec3>& unwrappedPositions,
    const std::vector<double>& radii);

} // namespace mc3d
