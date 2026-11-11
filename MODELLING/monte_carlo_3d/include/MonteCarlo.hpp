#pragma once

#include "Energy.hpp"
#include "Random.hpp"

#include <cstddef>
#include <cstdint>
#include <vector>

namespace mc3d {

struct MonteCarloStatistics {
    std::uint64_t attempted{0};
    std::uint64_t accepted{0};

    double acceptanceRate() const noexcept {
        return attempted == 0 ? 0.0 :
            static_cast<double>(accepted) / static_cast<double>(attempted);
    }
};

// Reversible single-particle Metropolis sampler in reduced units (kBT = 1).
// The proposal is a symmetric uniform displacement in each Cartesian component.
// This V1 kernel uses brute-force local energies as the correctness baseline.
class MonteCarlo {
public:
    MonteCarlo(const SimulationBox& box, const PairPotential& potential,
               double maximumComponentDisplacement, Random& random);

    bool attemptMove(std::vector<Particle>& particles);
    void sweep(std::vector<Particle>& particles);
    const MonteCarloStatistics& statistics() const noexcept { return statistics_; }
    void resetStatistics() noexcept { statistics_ = {}; }

private:
    const SimulationBox& box_;
    const PairPotential& potential_;
    double maxDisplacement_;
    Random& random_;
    MonteCarloStatistics statistics_{};
};

} // namespace mc3d
