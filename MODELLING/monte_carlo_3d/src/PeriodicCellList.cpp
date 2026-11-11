#include "PeriodicCellList.hpp"

#include <algorithm>
#include <cmath>
#include <limits>
#include <stdexcept>

namespace mc3d {

PeriodicCellList::PeriodicCellList(const SimulationBox& box,
                                   const std::vector<Vec3>& positions,
                                   double searchRadius)
    : boxLength_(box.sideLength()), cellWidth_(0.0), cellsPerDimension_(0) {
    if (!std::isfinite(searchRadius) || searchRadius <= 0.0 ||
        searchRadius >= 0.5 * boxLength_) {
        throw std::invalid_argument("Cell-list search radius must be positive and below half the box length");
    }
    const double requestedCells = std::floor(boxLength_ / searchRadius);
    if (!std::isfinite(requestedCells) ||
        requestedCells > static_cast<double>(std::numeric_limits<std::size_t>::max())) {
        throw std::length_error("Periodic cell-list grid dimensions overflow");
    }
    cellsPerDimension_ = std::max<std::size_t>(
        1, static_cast<std::size_t>(requestedCells));
    if (cellsPerDimension_ >
        std::numeric_limits<std::size_t>::max() / cellsPerDimension_ ||
        cellsPerDimension_ * cellsPerDimension_ >
        std::numeric_limits<std::size_t>::max() / cellsPerDimension_) {
        throw std::length_error("Periodic cell-list allocation size overflows");
    }
    cellWidth_ = boxLength_ / static_cast<double>(cellsPerDimension_);
    cells_.resize(cellsPerDimension_ * cellsPerDimension_ * cellsPerDimension_);
    for (std::size_t i = 0; i < positions.size(); ++i) {
        const Vec3 p = box.wrap(positions[i]);
        cells_[flatten(coordinate(p.x), coordinate(p.y), coordinate(p.z))].push_back(i);
    }
}

std::size_t PeriodicCellList::flatten(std::size_t x, std::size_t y,
                                      std::size_t z) const noexcept {
    return (x * cellsPerDimension_ + y) * cellsPerDimension_ + z;
}

std::size_t PeriodicCellList::coordinate(double value) const noexcept {
    const double wrapped = value - boxLength_ * std::floor(value / boxLength_);
    const auto raw = static_cast<std::size_t>(wrapped / cellWidth_);
    return std::min(raw, cellsPerDimension_ - 1);
}

std::vector<std::size_t> PeriodicCellList::candidates(const Vec3& position) const {
    if (!std::isfinite(position.x) || !std::isfinite(position.y) ||
        !std::isfinite(position.z)) {
        throw std::invalid_argument("Cell-list query position must be finite");
    }
    const Vec3 p{position.x - boxLength_ * std::floor(position.x / boxLength_),
                 position.y - boxLength_ * std::floor(position.y / boxLength_),
                 position.z - boxLength_ * std::floor(position.z / boxLength_)};
    const std::size_t cx = coordinate(p.x);
    const std::size_t cy = coordinate(p.y);
    const std::size_t cz = coordinate(p.z);
    std::vector<std::size_t> result;

    // For a cell width >= search radius, the 3x3x3 neighbourhood is a
    // conservative superset. Deduplicate wrapped cells for small grids.
    std::vector<std::size_t> visitedCells;
    visitedCells.reserve(27);
    for (int dx = -1; dx <= 1; ++dx) {
        for (int dy = -1; dy <= 1; ++dy) {
            for (int dz = -1; dz <= 1; ++dz) {
                const auto wrapIndex = [this](std::size_t c, int delta) {
                    const auto n = static_cast<long long>(cellsPerDimension_);
                    auto v = (static_cast<long long>(c) + delta) % n;
                    if (v < 0) v += n;
                    return static_cast<std::size_t>(v);
                };
                const auto index = flatten(wrapIndex(cx, dx),
                                           wrapIndex(cy, dy),
                                           wrapIndex(cz, dz));
                if (std::find(visitedCells.begin(), visitedCells.end(), index) !=
                    visitedCells.end()) continue;
                visitedCells.push_back(index);
                const auto& bucket = cells_[index];
                result.insert(result.end(), bucket.begin(), bucket.end());
            }
        }
    }
    return result;
}

} // namespace mc3d
