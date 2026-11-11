#pragma once

#include "SimulationBox.hpp"

#include <cstddef>
#include <vector>

namespace mc3d {

// Periodic uniform-cell broad phase. Query returns a superset of all particle
// indices within searchRadius; callers must apply their exact distance test.
class PeriodicCellList {
public:
    PeriodicCellList(const SimulationBox& box,
                     const std::vector<Vec3>& positions,
                     double searchRadius);

    std::vector<std::size_t> candidates(const Vec3& position) const;
    double cellWidth() const noexcept { return cellWidth_; }
    std::size_t cellsPerDimension() const noexcept { return cellsPerDimension_; }

private:
    std::size_t flatten(std::size_t x, std::size_t y, std::size_t z) const noexcept;
    std::size_t coordinate(double value) const noexcept;

    double boxLength_;
    double cellWidth_;
    std::size_t cellsPerDimension_;
    std::vector<std::vector<std::size_t>> cells_;
};

} // namespace mc3d
