#include "NeighborList.hpp"

#include <cmath>
#include <stdexcept>

namespace mc3d {

NeighborList::NeighborList(double cutoff, double skin)
    : cutoff_(cutoff), skin_(skin) {
    if (!std::isfinite(cutoff_) || cutoff_ <= 0.0)
        throw std::invalid_argument("NeighborList cutoff must be finite and positive");
    if (!std::isfinite(skin_) || skin_ < 0.0)
        throw std::invalid_argument("NeighborList skin must be finite and non-negative");
}

void NeighborList::rebuild(const std::vector<Particle>& particles,
                           const SimulationBox& box) {
    if (listRadius() >= 0.5 * box.sideLength())
        throw std::invalid_argument("NeighborList cutoff plus skin must be less than half the box length");
    neighbors_.assign(particles.size(), {});
    referencePositions_.clear();
    referencePositions_.reserve(particles.size());
    const double radius2 = listRadius() * listRadius();
    for (const auto& particle : particles)
        referencePositions_.push_back(box.wrap(particle.position));

    for (std::size_t i = 0; i < particles.size(); ++i) {
        for (std::size_t j = i + 1; j < particles.size(); ++j) {
            if (box.distanceSquared(particles[i].position, particles[j].position) <= radius2) {
                neighbors_[i].push_back(j);
                neighbors_[j].push_back(i);
            }
        }
    }
}

bool NeighborList::validFor(const std::vector<Particle>& particles,
                            const SimulationBox& box) const {
    if (particles.size() != referencePositions_.size()) return false;
    const double maxDisplacement2 = 0.25 * skin_ * skin_;
    for (std::size_t i = 0; i < particles.size(); ++i) {
        if (box.distanceSquared(referencePositions_[i], particles[i].position) >
            maxDisplacement2) return false;
    }
    return true;
}

const std::vector<std::size_t>& NeighborList::neighborsOf(
    std::size_t particleIndex) const {
    if (particleIndex >= neighbors_.size())
        throw std::out_of_range("NeighborList particle index out of range");
    return neighbors_[particleIndex];
}

double NeighborList::localEnergy(std::size_t particleIndex,
                                 const Vec3& proposedPosition,
                                 const std::vector<Particle>& particles,
                                 const SimulationBox& box,
                                 const PairPotential& potential) const {
    if (particles.size() != neighbors_.size() || particleIndex >= particles.size())
        throw std::out_of_range("NeighborList is unbuilt or incompatible with particle array");
    double energy = 0.0;
    for (const auto j : neighbors_[particleIndex]) {
        const double pair = potential.energySquaredDistance(
            box.distanceSquared(proposedPosition, particles[j].position));
        if (!std::isfinite(pair)) return pair;
        energy += pair;
    }
    return energy;
}

} // namespace mc3d
