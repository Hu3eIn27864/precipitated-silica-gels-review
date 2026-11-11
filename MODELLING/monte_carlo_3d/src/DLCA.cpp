#include "DLCA.hpp"

#include <algorithm>
#include <cmath>
#include <stdexcept>

namespace mc3d {

DLCA::DLCA(const SimulationBox& box, DLCAConfig config, Random& random)
    : box_(box), config_(config), random_(random) {
    if (config_.particleCount == 0 ||
        !std::isfinite(config_.contactDistance) || config_.contactDistance <= 0.0 ||
        !std::isfinite(config_.maximumComponentStep) ||
        config_.maximumComponentStep <= 0.0 ||
        !std::isfinite(config_.mobilityExponent) || config_.mobilityExponent < 0.0 ||
        config_.maximumAttempts == 0) {
        throw std::invalid_argument("Invalid DLCA configuration");
    }
    if (config_.maximumComponentStep * std::sqrt(3.0) >
        0.5 * config_.contactDistance) {
        throw std::invalid_argument("DLCA component step is too large for contact detection");
    }
    if (config_.contactDistance >= 0.5 * box_.sideLength()) {
        throw std::invalid_argument("DLCA contact distance must be below half the box length");
    }
}

DLCAResult DLCA::generate() const {
    using Cluster = std::vector<Particle>;
    std::vector<Cluster> clusters;
    clusters.reserve(config_.particleCount);
    const double exclusion2 = config_.contactDistance * config_.contactDistance;
    const std::size_t placementLimit = config_.particleCount * 100000;

    // Random sequential placement creates a dilute, non-overlapping monomer suspension.
    for (std::size_t i = 0; i < config_.particleCount; ++i) {
        bool placed = false;
        for (std::size_t trial = 0; trial < placementLimit; ++trial) {
            const Vec3 p{random_.uniform(0.0, box_.sideLength()),
                         random_.uniform(0.0, box_.sideLength()),
                         random_.uniform(0.0, box_.sideLength())};
            bool clear = true;
            for (const auto& cluster : clusters) {
                for (const auto& particle : cluster) {
                    if (box_.distanceSquared(p, particle.position) < exclusion2) {
                        clear = false;
                        break;
                    }
                }
                if (!clear) break;
            }
            if (clear) {
                clusters.push_back(Cluster{{i, p}});
                placed = true;
                break;
            }
        }
        if (!placed)
            throw std::runtime_error("DLCA initial placement failed; enlarge box or reduce particle count");
    }

    DLCAResult result;
    while (clusters.size() > 1 && result.attempts < config_.maximumAttempts) {
        ++result.attempts;
        double weightSum = 0.0;
        for (const auto& c : clusters)
            weightSum += std::pow(static_cast<double>(c.size()), -config_.mobilityExponent);
        double draw = random_.uniform(0.0, weightSum);
        std::size_t moving = clusters.size() - 1;
        for (std::size_t i = 0; i < clusters.size(); ++i) {
            draw -= std::pow(static_cast<double>(clusters[i].size()),
                             -config_.mobilityExponent);
            if (draw <= 0.0) { moving = i; break; }
        }

        const Vec3 shift{random_.uniform(-config_.maximumComponentStep,
                                         config_.maximumComponentStep),
                         random_.uniform(-config_.maximumComponentStep,
                                         config_.maximumComponentStep),
                         random_.uniform(-config_.maximumComponentStep,
                                         config_.maximumComponentStep)};
        for (auto& p : clusters[moving])
            p.position = box_.wrap(p.position + shift);

        std::vector<std::size_t> hit;
        for (std::size_t j = 0; j < clusters.size(); ++j) {
            if (j == moving) continue;
            bool touching = false;
            for (const auto& a : clusters[moving]) {
                for (const auto& b : clusters[j]) {
                    if (box_.distanceSquared(a.position, b.position) <= exclusion2) {
                        touching = true;
                        break;
                    }
                }
                if (touching) break;
            }
            if (touching) hit.push_back(j);
        }

        if (!hit.empty()) {
            Cluster merged;
            std::vector<bool> remove(clusters.size(), false);
            remove[moving] = true;
            for (const auto j : hit) remove[j] = true;
            for (std::size_t j = 0; j < clusters.size(); ++j)
                if (remove[j])
                    merged.insert(merged.end(), clusters[j].begin(), clusters[j].end());

            std::vector<Cluster> survivors;
            survivors.reserve(clusters.size() - hit.size());
            for (std::size_t j = 0; j < clusters.size(); ++j)
                if (!remove[j]) survivors.push_back(std::move(clusters[j]));
            survivors.push_back(std::move(merged));
            clusters = std::move(survivors);
            // Each hit cluster reduces the number of components by one.
            result.successfulMerges += hit.size();
        }
    }

    for (const auto& cluster : clusters)
        result.particles.insert(result.particles.end(), cluster.begin(), cluster.end());
    std::sort(result.particles.begin(), result.particles.end(),
              [](const Particle& a, const Particle& b) { return a.id < b.id; });
    result.completed = clusters.size() == 1;
    return result;
}

} // namespace mc3d
