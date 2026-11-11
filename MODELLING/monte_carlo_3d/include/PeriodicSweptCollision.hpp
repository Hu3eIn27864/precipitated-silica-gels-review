#pragma once

#include "Vec3.hpp"

#include <optional>

namespace mc3d {

// Earliest contact fraction for a sphere swept by displacement through a
// cubic periodic box. 'relative' is the minimum-image displacement from the
// moving sphere to a stationary sphere at the beginning of the move.
std::optional<double> firstPeriodicSweptSphereContact(
    const Vec3& relative, const Vec3& displacement,
    double contactDistance, double boxLength);

} // namespace mc3d
