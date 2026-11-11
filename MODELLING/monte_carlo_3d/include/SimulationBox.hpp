#pragma once

#include "Vec3.hpp"

namespace mc3d {

class SimulationBox {
public:
    explicit SimulationBox(double sideLength);

    double sideLength() const noexcept { return sideLength_; }

    // Map each coordinate into the half-open interval [0, L).
    Vec3 wrap(const Vec3& position) const;

    // Return the minimum-image displacement from 'from' to 'to'.
    Vec3 minimumImageDisplacement(const Vec3& from, const Vec3& to) const noexcept;

    double distanceSquared(const Vec3& a, const Vec3& b) const noexcept;
    double distance(const Vec3& a, const Vec3& b) const noexcept;

private:
    double sideLength_;
};

} // namespace mc3d
