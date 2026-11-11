#pragma once

#include "Particle.hpp"
#include "PairPotential.hpp"
#include "SimulationBox.hpp"

#include <cstddef>
#include <vector>

namespace mc3d {

class NeighborList {
public:
    NeighborList(double cutoff, double skin);

    double cutoff() const noexcept { return cutoff_; }
    double skin() const noexcept { return skin_; }
    double listRadius() const noexcept { return cutoff_ + skin_; }
    std::size_t size() const noexcept { return neighbors_.size(); }

    void rebuild(const std::vector<Particle>& particles, const SimulationBox& box);
    bool validFor(const std::vector<Particle>& particles,
                  const SimulationBox& box) const;
    const std::vector<std::size_t>& neighborsOf(std::size_t particleIndex) const;

    // Pair energy involving one proposed particle position, using this list.
    // The caller must rebuild if validFor() is false before using this method.
    double localEnergy(std::size_t particleIndex, const Vec3& proposedPosition,
                      const std::vector<Particle>& particles,
                      const SimulationBox& box,
                      const PairPotential& potential) const;

private:
    double cutoff_;
    double skin_;
    std::vector<std::vector<std::size_t>> neighbors_;
    std::vector<Vec3> referencePositions_;
};

} // namespace mc3d
