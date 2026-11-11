#pragma once

#include "Vec3.hpp"

#include <optional>

namespace mc3d {

// Earliest contact fraction for a sphere swept by displacement through a
// cubic periodic box. 'relative' is stationary minus moving position at the start. Since the
// moving sphere is translated by displacement, relative(t) = relative -
// displacement * t.
std::optional<double> firstPeriodicSweptSphereContact(
    const Vec3& relative, const Vec3& displacement,
    double contactDistance, double boxLength);

} // namespace mc3d
