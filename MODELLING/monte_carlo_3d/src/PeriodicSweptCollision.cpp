#include "PeriodicSweptCollision.hpp"

#include <cmath>
#include <stdexcept>

namespace mc3d {

std::optional<double> firstPeriodicSweptSphereContact(
    const Vec3& relative, const Vec3& displacement,
    double contactDistance, double boxLength) {
    if (!std::isfinite(relative.x) || !std::isfinite(relative.y) ||
        !std::isfinite(relative.z) || !std::isfinite(displacement.x) ||
        !std::isfinite(displacement.y) || !std::isfinite(displacement.z) ||
        !std::isfinite(contactDistance) || contactDistance <= 0.0 ||
        !std::isfinite(boxLength) || boxLength <= 0.0) {
        throw std::invalid_argument("Invalid periodic swept-collision input");
    }

    const double displacement2 = normSquared(displacement);
    const double contact2 = contactDistance * contactDistance;
    if (displacement2 == 0.0) {
        return normSquared(relative) <= contact2
            ? std::optional<double>{0.0} : std::nullopt;
    }

    double earliest = 1.0;
    bool found = false;
    // The initial vector is minimum-image. Its 26 neighbouring periodic
    // images are also checked: a finite move can cross a Voronoi face of
    // the minimum-image convention before reaching contact.
    for (int ix = -1; ix <= 1; ++ix) {
        for (int iy = -1; iy <= 1; ++iy) {
            for (int iz = -1; iz <= 1; ++iz) {
                const Vec3 image{
                    relative.x + static_cast<double>(ix) * boxLength,
                    relative.y + static_cast<double>(iy) * boxLength,
                    relative.z + static_cast<double>(iz) * boxLength};
                const double r2 = normSquared(image);
                if (r2 <= contact2) {
                    earliest = 0.0;
                    found = true;
                    continue;
                }
                // relative = stationary - moving, so the relative trajectory is
                // image - displacement * t; the entry-root projection is
                // therefore dot(image, displacement).
                const double projection = dot(image, displacement);
                if (projection <= 0.0) continue;
                const double discriminant =
                    projection * projection - displacement2 * (r2 - contact2);
                if (discriminant < 0.0) continue;
                const double entry =
                    (projection - std::sqrt(discriminant)) / displacement2;
                if (entry >= 0.0 && entry <= earliest) {
                    earliest = entry;
                    found = true;
                }
            }
        }
    }
    return found ? std::optional<double>{earliest} : std::nullopt;
}

} // namespace mc3d
