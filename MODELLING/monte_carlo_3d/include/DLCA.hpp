#pragma once

#include "Particle.hpp"
#include "Random.hpp"
#include "SimulationBox.hpp"

#include <cstddef>
#include <vector>

namespace mc3d {

struct DLCAConfig {
    std::size_t particleCount{100};
    double contactDistance{1.0};
    double maximumComponentStep{0.2};
    double mobilityExponent{1.0};
    std::size_t maximumAttempts{1000000};
    // Zero disables the common cumulative squared-translation stopping rule.
    double targetCumulativeSquaredTranslation{0.0};
};

struct DLCAClusterMobilityStats {
    std::size_t clusterSize{0};
    std::size_t selectionCount{0};
    std::size_t successfulMergeEvents{0};
    std::size_t successfulMerges{0};
    double cumulativeSquaredTranslation{0.0};
    double cumulativeTranslationPathLength{0.0};
};

struct DLCAResult {
    std::vector<Particle> particles;
    std::size_t attempts{0};
    std::size_t successfulMergeEvents{0};
    std::size_t successfulMerges{0};
    double cumulativeSquaredClusterTranslation{0.0};
    double cumulativeClusterTranslationPathLength{0.0};
    bool displacementBudgetReached{false};
    bool attemptLimitReached{false};
    double displacementBudgetOvershoot{0.0};
    std::vector<DLCAClusterMobilityStats> clusterMobilityStats;
    bool completed{false};
};

// Rigid-cluster Brownian aggregation with periodic boundaries. Cluster
// selection is weighted by mass^(-mobilityExponent); this is a declared
// algorithmic mobility law, not a hydrodynamic calculation.
class DLCA {
public:
    DLCA(const SimulationBox& box, DLCAConfig config, Random& random);
    DLCAResult generate() const;

private:
    const SimulationBox& box_;
    DLCAConfig config_;
    Random& random_;
};

} // namespace mc3d
