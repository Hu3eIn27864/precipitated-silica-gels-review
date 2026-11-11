#include "DLCA.hpp"
#include "PeriodicCellList.hpp"
#include "PeriodicSweptCollision.hpp"

#include <algorithm>
#include <cmath>
#include <limits>
#include <memory>
#include <map>
#include <stdexcept>
#include <utility>

namespace mc3d {

DLCA::DLCA(const SimulationBox& box, DLCAConfig config, Random& random)
    : box_(box), config_(config), random_(random) {
    if (config_.particleCount == 0 ||
        !std::isfinite(config_.contactDistance) || config_.contactDistance <= 0.0 ||
        !std::isfinite(config_.maximumComponentStep) ||
        config_.maximumComponentStep <= 0.0 ||
        !std::isfinite(config_.mobilityExponent) || config_.mobilityExponent < 0.0 ||
        !std::isfinite(config_.targetCumulativeSquaredTranslation) ||
        config_.targetCumulativeSquaredTranslation < 0.0 ||
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
    if (config_.particleCount > std::numeric_limits<std::size_t>::max() / 100000) {
        throw std::invalid_argument("DLCA particle count is too large");
    }
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
    std::map<std::size_t, DLCAClusterMobilityStats> mobilityBySize;
    while (clusters.size() > 1 && result.attempts < config_.maximumAttempts &&
           (config_.targetCumulativeSquaredTranslation == 0.0 ||
            result.cumulativeSquaredClusterTranslation <
                config_.targetCumulativeSquaredTranslation)) {
        ++result.attempts;
        double weightSum = 0.0;
        for (const auto& cluster : clusters) {
            weightSum += std::pow(static_cast<double>(cluster.size()),
                                  -config_.mobilityExponent);
        }
        double draw = random_.uniform(0.0, weightSum);
        std::size_t moving = clusters.size() - 1;
        for (std::size_t i = 0; i < clusters.size(); ++i) {
            draw -= std::pow(static_cast<double>(clusters[i].size()),
                             -config_.mobilityExponent);
            if (draw <= 0.0) {
                moving = i;
                break;
            }
        }

        const std::size_t selectedClusterSize = clusters[moving].size();
        auto& mobilityStats = mobilityBySize[selectedClusterSize];
        mobilityStats.clusterSize = selectedClusterSize;
        ++mobilityStats.selectionCount;

        const Vec3 shift{
            random_.uniform(-config_.maximumComponentStep, config_.maximumComponentStep),
            random_.uniform(-config_.maximumComponentStep, config_.maximumComponentStep),
            random_.uniform(-config_.maximumComponentStep, config_.maximumComponentStep)};

        // Flatten the current aggregate positions and owner map. The periodic
        // cell list is a conservative broad phase; exact swept-sphere geometry
        // remains the narrow phase.
        std::vector<Vec3> positions;
        std::vector<std::size_t> owners;
        for (std::size_t c = 0; c < clusters.size(); ++c) {
            for (const auto& particle : clusters[c]) {
                positions.push_back(particle.position);
                owners.push_back(c);
            }
        }
        const double shift2 = normSquared(shift);
        const double shiftLength = std::sqrt(shift2);
        const double broadRadius = config_.contactDistance + shiftLength;
        std::unique_ptr<PeriodicCellList> broadPhase;
        if (shiftLength > 0.0 && broadRadius < 0.5 * box_.sideLength()) {
            try {
                broadPhase = std::make_unique<PeriodicCellList>(box_, positions, broadRadius);
            } catch (const std::length_error&) {
                // A dense grid would be wasteful for this geometry; exact scans remain the fallback.
            }
        }

        double firstContact = 1.0;
        bool collision = false;
        if (shiftLength > 0.0) {
            std::size_t movingFlat = 0;
            for (std::size_t c = 0; c < moving; ++c)
                movingFlat += clusters[c].size();

            for (std::size_t local = 0; local < clusters[moving].size(); ++local) {
                const auto flat = movingFlat + local;
                std::vector<std::size_t> candidates;
                if (broadPhase) {
                    candidates = broadPhase->candidates(clusters[moving][local].position);
                } else {
                    candidates.resize(positions.size());
                    for (std::size_t k = 0; k < positions.size(); ++k) candidates[k] = k;
                }
                for (const auto candidate : candidates) {
                    const std::size_t otherCluster = owners[candidate];
                    if (otherCluster == moving || candidate == flat) continue;
                    const Vec3 relative = box_.minimumImageDisplacement(
                        clusters[moving][local].position, positions[candidate]);
                    const double r2 = normSquared(relative);
                    if (r2 <= exclusion2) {
                        firstContact = 0.0;
                        collision = true;
                        continue;
                    }
                    const auto entry = firstPeriodicSweptSphereContact(
                        relative, shift, config_.contactDistance, box_.sideLength());
                    if (entry && *entry <= firstContact) {
                        firstContact = *entry;
                        collision = true;
                    }
                }
            }
        }

        const double travelFraction = collision ? firstContact : 1.0;
        const Vec3 realizedShift = shift * travelFraction;
        const double realizedDistanceSquared = normSquared(realizedShift);
        result.cumulativeSquaredClusterTranslation += realizedDistanceSquared;
        const double realizedDistance = std::sqrt(realizedDistanceSquared);
        result.cumulativeClusterTranslationPathLength += realizedDistance;
        mobilityStats.cumulativeSquaredTranslation += realizedDistanceSquared;
        mobilityStats.cumulativeTranslationPathLength += realizedDistance;
        for (auto& particle : clusters[moving]) {
            particle.position = box_.wrap(particle.position + shift * travelFraction);
        }
        if (collision) {
            std::vector<Vec3> finalPositions;
            std::vector<std::size_t> finalOwners;
            for (std::size_t c = 0; c < clusters.size(); ++c) {
                for (const auto& particle : clusters[c]) {
                    finalPositions.push_back(particle.position);
                    finalOwners.push_back(c);
                }
            }
            const double contactTolerance = config_.contactDistance * (1.0 + 1e-10);
            std::unique_ptr<PeriodicCellList> finalCells;
            if (contactTolerance < 0.5 * box_.sideLength()) {
                try {
                    finalCells = std::make_unique<PeriodicCellList>(
                        box_, finalPositions, contactTolerance);
                } catch (const std::length_error&) {
                    // Preserve exact contact identification when the dense grid is too large.
                }
            }
            std::vector<bool> hitFlag(clusters.size(), false);
            std::size_t movingFlat = 0;
            for (std::size_t c = 0; c < moving; ++c)
                movingFlat += clusters[c].size();
            for (std::size_t local = 0; local < clusters[moving].size(); ++local) {
                const auto flat = movingFlat + local;
                std::vector<std::size_t> candidates;
                if (finalCells) {
                    candidates = finalCells->candidates(clusters[moving][local].position);
                } else {
                    candidates.resize(finalPositions.size());
                    for (std::size_t k = 0; k < finalPositions.size(); ++k)
                        candidates[k] = k;
                }
                for (const auto candidate : candidates) {
                    const auto owner = finalOwners[candidate];
                    if (owner == moving || candidate == flat || hitFlag[owner]) continue;
                    if (box_.distanceSquared(clusters[moving][local].position,
                                             finalPositions[candidate]) <=
                        contactTolerance * contactTolerance) {
                        hitFlag[owner] = true;
                    }
                }
            }
            std::vector<std::size_t> hit;
            for (std::size_t c = 0; c < hitFlag.size(); ++c)
                if (hitFlag[c]) hit.push_back(c);

            if (!hit.empty()) {
                Cluster merged;
                std::vector<bool> remove(clusters.size(), false);
                remove[moving] = true;
                for (const auto j : hit) remove[j] = true;
                for (std::size_t j = 0; j < clusters.size(); ++j) {
                    if (remove[j])
                        merged.insert(merged.end(), clusters[j].begin(), clusters[j].end());
                }
                std::vector<Cluster> survivors;
                survivors.reserve(clusters.size() - hit.size());
                for (std::size_t j = 0; j < clusters.size(); ++j) {
                    if (!remove[j]) survivors.push_back(std::move(clusters[j]));
                }
                survivors.push_back(std::move(merged));
                clusters = std::move(survivors);
                result.successfulMerges += hit.size();
                mobilityStats.successfulMerges += hit.size();
            }
        }
    }

    result.displacementBudgetReached =
        config_.targetCumulativeSquaredTranslation > 0.0 &&
        result.cumulativeSquaredClusterTranslation >=
            config_.targetCumulativeSquaredTranslation;
    result.displacementBudgetOvershoot = result.displacementBudgetReached
        ? result.cumulativeSquaredClusterTranslation -
              config_.targetCumulativeSquaredTranslation
        : 0.0;
    result.attemptLimitReached =
        clusters.size() > 1 && !result.displacementBudgetReached &&
        result.attempts >= config_.maximumAttempts;

    for (const auto& entry : mobilityBySize)
        result.clusterMobilityStats.push_back(entry.second);

    for (const auto& cluster : clusters) {
        result.particles.insert(result.particles.end(), cluster.begin(), cluster.end());
    }
    std::sort(result.particles.begin(), result.particles.end(),
              [](const Particle& a, const Particle& b) { return a.id < b.id; });
    result.completed = clusters.size() == 1;
    return result;
}

} // namespace mc3d
