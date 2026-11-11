#pragma once

#include "Particle.hpp"
#include "SimulationBox.hpp"

#include <cstddef>
#include <vector>

namespace mc3d {

struct ClusterObservables {
    std::size_t particleCount{0};
    std::size_t contactCount{0};
    double radiusOfGyration{0.0};
    double meanCoordination{0.0};
    bool periodicUnwrappingConsistent{true};
    // Graph-unwrapped coordinates in component traversal order. Only use for
    // spatial scaling when periodicUnwrappingConsistent is true.
    std::vector<Vec3> unwrappedPositions;
};

struct NetworkObservables {
    std::size_t particleCount{0};
    std::size_t contactCount{0};
    std::size_t componentCount{0};
    std::size_t largestComponentSize{0};
    double largestComponentFraction{0.0};
    double meanCoordination{0.0};
    std::vector<std::size_t> coordination;
    std::vector<ClusterObservables> components;
};

// Contacts are defined geometrically by distance <= contactDistance.
// Rg is calculated from a graph-unwrapped cluster, never wrapped coordinates.
NetworkObservables analyseNetwork(const std::vector<Particle>& particles,
                                  const SimulationBox& box,
                                  double contactDistance);

} // namespace mc3d
