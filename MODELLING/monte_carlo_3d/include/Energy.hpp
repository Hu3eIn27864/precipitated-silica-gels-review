#pragma once

#include "NeighborList.hpp"

#include <cmath>
#include <stdexcept>
#include <vector>

namespace mc3d {

inline double totalEnergy(const std::vector<Particle>& particles,
                          const SimulationBox& box,
                          const PairPotential& potential) {
    double energy = 0.0;
    for (std::size_t i = 0; i < particles.size(); ++i) {
        for (std::size_t j = i + 1; j < particles.size(); ++j) {
            const double pair = potential.energySquaredDistance(
                box.distanceSquared(particles[i].position, particles[j].position));
            if (!std::isfinite(pair)) return pair;
            energy += pair;
        }
    }
    return energy;
}

inline double localEnergy(const std::size_t particleIndex,
                          const Vec3& position,
                          const std::vector<Particle>& particles,
                          const SimulationBox& box,
                          const PairPotential& potential) {
    if (particleIndex >= particles.size())
        throw std::out_of_range("Local energy particle index out of range");
    double energy = 0.0;
    for (std::size_t j = 0; j < particles.size(); ++j) {
        if (j == particleIndex) continue;
        const double pair = potential.energySquaredDistance(
            box.distanceSquared(position, particles[j].position));
        if (!std::isfinite(pair)) return pair;
        energy += pair;
    }
    return energy;
}

} // namespace mc3d
