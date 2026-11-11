#include "MassRadius.hpp"

#include <algorithm>
#include <cmath>
#include <stdexcept>

namespace mc3d {

std::vector<MassRadiusPoint> calculateMassRadiusCurve(
    const std::vector<Vec3>& unwrappedPositions,
    const std::vector<double>& radii) {
    if (unwrappedPositions.empty() || radii.empty()) {
        throw std::invalid_argument("Mass-radius calculation requires positions and radii");
    }
    for (const auto& p : unwrappedPositions) {
        if (!std::isfinite(p.x) || !std::isfinite(p.y) || !std::isfinite(p.z)) {
            throw std::invalid_argument("Mass-radius positions must be finite");
        }
    }
    for (std::size_t i = 0; i < radii.size(); ++i) {
        if (!std::isfinite(radii[i]) || radii[i] <= 0.0 ||
            (i > 0 && radii[i] <= radii[i - 1])) {
            throw std::invalid_argument("Mass-radius radii must be finite, positive and strictly increasing");
        }
    }

    std::vector<MassRadiusPoint> curve;
    curve.reserve(radii.size());
    std::vector<double> distances;
    distances.reserve(unwrappedPositions.size());
    for (const double radius : radii) {
        const double radiusSquared = radius * radius;
        double totalMass = 0.0;
        for (const auto& centre : unwrappedPositions) {
            distances.clear();
            for (const auto& particle : unwrappedPositions) {
                const double dx = particle.x - centre.x;
                const double dy = particle.y - centre.y;
                const double dz = particle.z - centre.z;
                distances.push_back(dx * dx + dy * dy + dz * dz);
            }
            totalMass += static_cast<double>(std::count_if(
                distances.begin(), distances.end(),
                [radiusSquared](double d2) { return d2 <= radiusSquared; }));
        }
        curve.push_back({radius, totalMass /
            static_cast<double>(unwrappedPositions.size())});
    }
    return curve;
}

} // namespace mc3d
