#include "SimulationBox.hpp"

#include <cmath>
#include <stdexcept>

namespace mc3d {

SimulationBox::SimulationBox(double sideLength) : sideLength_(sideLength) {
    if (!std::isfinite(sideLength_) || sideLength_ <= 0.0) {
        throw std::invalid_argument("SimulationBox side length must be finite and positive");
    }
}

Vec3 SimulationBox::wrap(const Vec3& position) const {
    const auto wrapCoordinate = [this](double value) {
        if (!std::isfinite(value)) {
            throw std::invalid_argument("Cannot wrap a non-finite coordinate");
        }
        double wrapped = std::fmod(value, sideLength_);
        if (wrapped < 0.0) wrapped += sideLength_;
        // Guard against round-off returning exactly L.
        if (wrapped >= sideLength_) wrapped = 0.0;
        return wrapped;
    };
    return {wrapCoordinate(position.x), wrapCoordinate(position.y),
            wrapCoordinate(position.z)};
}

Vec3 SimulationBox::minimumImageDisplacement(const Vec3& from,
                                              const Vec3& to) const noexcept {
    const double half = 0.5 * sideLength_;
    const auto minimumImage = [this, half](double delta) {
        if (delta > half) delta -= sideLength_;
        else if (delta < -half) delta += sideLength_;
        return delta;
    };
    return {minimumImage(to.x - from.x), minimumImage(to.y - from.y),
            minimumImage(to.z - from.z)};
}

double SimulationBox::distanceSquared(const Vec3& a, const Vec3& b) const noexcept {
    return normSquared(minimumImageDisplacement(a, b));
}

double SimulationBox::distance(const Vec3& a, const Vec3& b) const noexcept {
    return std::sqrt(distanceSquared(a, b));
}

} // namespace mc3d
