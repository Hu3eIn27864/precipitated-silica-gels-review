#include "DLCA.hpp"
#include "Observables.hpp"
#include "PeriodicCellList.hpp"

#include <algorithm>
#include <cmath>
#include <exception>
#include <iostream>
#include <limits>
#include <stdexcept>
#include <vector>

namespace {
void require(bool ok, const char* message) {
    if (!ok) throw std::runtime_error(message);
}
bool near(double a, double b, double tol = 1e-10) {
    return std::abs(a - b) <= tol;
}

void testPeriodicUnwrappingAndGraph() {
    const mc3d::SimulationBox box(10.0);
    const std::vector<mc3d::Particle> p{
        {0, {9.6, 5.0, 5.0}}, {1, {0.4, 5.0, 5.0}},
        {2, {1.2, 5.0, 5.0}}, {3, {5.0, 5.0, 5.0}}
    };
    const auto a = mc3d::analyseNetwork(p, box, 0.81);
    require(a.componentCount == 2, "wrong connected-component count");
    require(a.largestComponentSize == 3, "wrong largest component size");
    require(a.contactCount == 2, "wrong unique contact count");
    require(a.coordination[0] == 1 && a.coordination[1] == 2 &&
            a.coordination[2] == 1, "wrong coordination numbers");
    const double expectedRg = std::sqrt(1.28 / 3.0);
    require(near(a.components[0].radiusOfGyration, expectedRg),
            "periodic cluster Rg was not calculated from unwrapped coordinates");
    require(a.components[0].periodicUnwrappingConsistent,
            "simple chain should unwrap consistently");

    const std::vector<mc3d::Particle> translated{
        {0, {0.6, 5.0, 5.0}}, {1, {1.4, 5.0, 5.0}},
        {2, {2.2, 5.0, 5.0}}, {3, {6.0, 5.0, 5.0}}
    };
    const auto b = mc3d::analyseNetwork(translated, box, 0.81);
    require(near(a.components[0].radiusOfGyration,
                 b.components[0].radiusOfGyration),
            "Rg changed when the cluster was translated across a periodic face");
}

void testPeriodicWindingIsFlagged() {
    const mc3d::SimulationBox box(9.0);
    const std::vector<mc3d::Particle> ring{
        {0, {1.0, 4.5, 4.5}}, {1, {4.0, 4.5, 4.5}},
        {2, {7.0, 4.5, 4.5}}
    };
    const auto a = mc3d::analyseNetwork(ring, box, 3.1);
    require(a.componentCount == 1, "periodic ring should be connected");
    require(!a.components[0].periodicUnwrappingConsistent,
            "periodic winding was not flagged");
}

void testDLCAReproducibilityAndNonOverlap() {
    const mc3d::SimulationBox box(12.0);
    mc3d::DLCAConfig cfg;
    cfg.particleCount = 12;
    cfg.contactDistance = 1.0;
    cfg.maximumComponentStep = 0.2;
    cfg.maximumAttempts = 30000;
    mc3d::Random ra(1234), rb(1234);
    const auto a = mc3d::DLCA(box, cfg, ra).generate();
    const auto b = mc3d::DLCA(box, cfg, rb).generate();
    require(a.particles.size() == cfg.particleCount &&
            b.particles.size() == cfg.particleCount,
            "DLCA particle count changed");
    require(a.attempts == b.attempts &&
            a.successfulMerges == b.successfulMerges &&
            a.completed == b.completed,
            "DLCA metadata not reproducible");
    for (std::size_t i = 0; i < a.particles.size(); ++i) {
        require(a.particles[i].id == b.particles[i].id,
                "DLCA particle IDs not reproducible");
        require(near(a.particles[i].position.x, b.particles[i].position.x) &&
                near(a.particles[i].position.y, b.particles[i].position.y) &&
                near(a.particles[i].position.z, b.particles[i].position.z),
                "DLCA coordinates not reproducible");
    }
    for (std::size_t i = 0; i < a.particles.size(); ++i) {
        for (std::size_t j = i + 1; j < a.particles.size(); ++j) {
            require(box.distance(a.particles[i].position,
                                 a.particles[j].position) >= 1.0 - 1e-10,
                    "DLCA generated overlapping particles");
        }
    }
    const auto obs = mc3d::analyseNetwork(a.particles, box, 1.0 + 1e-10);
    require(obs.particleCount == cfg.particleCount,
            "network analysis lost particles");
    require(obs.contactCount >= a.successfulMerges,
            "contact graph has fewer contacts than component-merging events");
    require(obs.componentCount ==
                (a.completed ? 1u : cfg.particleCount - a.successfulMerges),
            "component count inconsistent with DLCA merge accounting");
}

void testPeriodicCellListIsConservative() {
    const mc3d::SimulationBox box(12.0);
    const std::vector<mc3d::Vec3> positions{
        {0.1, 0.1, 0.1}, {11.8, 0.2, 0.1}, {6.0, 6.0, 6.0},
        {1.0, 0.1, 0.1}, {11.0, 11.0, 11.0}, {5.9, 6.0, 6.0}
    };
    const double radius = 1.25;
    const mc3d::PeriodicCellList cells(box, positions, radius);
    for (std::size_t i = 0; i < positions.size(); ++i) {
        const auto candidates = cells.candidates(positions[i]);
        for (std::size_t j = 0; j < positions.size(); ++j) {
            if (box.distance(positions[i], positions[j]) <= radius) {
                require(std::find(candidates.begin(), candidates.end(), j) !=
                            candidates.end(),
                        "cell list omitted a particle inside the search radius");
            }
        }
    }
    const mc3d::PeriodicCellList smallGrid(box, positions, 5.9);
    const auto candidates = smallGrid.candidates({0.1, 0.1, 0.1});
    require(std::find(candidates.begin(), candidates.end(), 1) != candidates.end(),
            "cell list failed across a periodic boundary on a small grid");
    const auto negativeQuery = cells.candidates({-0.2, 0.2, 0.1});
    require(std::find(negativeQuery.begin(), negativeQuery.end(), 1) !=
                negativeQuery.end(),
            "cell list failed to wrap negative query coordinates");
    bool rejectedNonFinite = false;
    try {
        (void)cells.candidates({std::numeric_limits<double>::infinity(), 0.0, 0.0});
    } catch (const std::invalid_argument&) {
        rejectedNonFinite = true;
    }
    require(rejectedNonFinite, "cell list accepted a non-finite query coordinate");
}

void testCellListRandomizedAgainstBruteForce() {
    const mc3d::SimulationBox box(30.0);
    constexpr std::size_t count = 240;
    std::vector<mc3d::Vec3> positions;
    positions.reserve(count);
    // Deterministic pseudo-random coordinates avoid coupling this regression
    // to the simulation RNG or platform-specific distribution implementations.
    std::uint64_t state = 0x9e3779b97f4a7c15ULL;
    const auto unit = [&state]() mutable {
        state = state * 6364136223846793005ULL + 1442695040888963407ULL;
        return static_cast<double>(state >> 11) / 9007199254740992.0;
    };
    for (std::size_t i = 0; i < count; ++i) {
        positions.push_back({30.0 * unit(), 30.0 * unit(), 30.0 * unit()});
    }
    const double radius = 2.3;
    const mc3d::PeriodicCellList cells(box, positions, radius);
    for (std::size_t q = 0; q < count; ++q) {
        const auto candidates = cells.candidates(positions[q]);
        for (std::size_t j = 0; j < count; ++j) {
            if (box.distanceSquared(positions[q], positions[j]) <= radius * radius) {
                require(std::find(candidates.begin(), candidates.end(), j) !=
                            candidates.end(),
                        "randomized cell-list query omitted a brute-force neighbour");
            }
        }
    }
}

void testCellListRejectsExcessiveDenseGrid() {
    const mc3d::SimulationBox box(100.0);
    const std::vector<mc3d::Vec3> positions{{1.0, 1.0, 1.0}};
    bool rejected = false;
    try {
        (void)mc3d::PeriodicCellList(box, positions, 0.01);
    } catch (const std::length_error&) {
        rejected = true;
    }
    require(rejected, "cell list did not reject an excessive dense-grid allocation");
}

void testEmptyNetwork() {
    const mc3d::SimulationBox box(10.0);
    const auto obs = mc3d::analyseNetwork({}, box, 1.0);
    require(obs.particleCount == 0 && obs.componentCount == 0,
            "empty network should have no components");
}
}

int main() {
    try {
        testPeriodicUnwrappingAndGraph();
        testPeriodicWindingIsFlagged();
        testDLCAReproducibilityAndNonOverlap();
        testPeriodicCellListIsConservative();
        testCellListRandomizedAgainstBruteForce();
        testCellListRejectsExcessiveDenseGrid();
        testEmptyNetwork();
    } catch (const std::exception& e) {
        std::cerr << "FAILED: " << e.what() << '\n';
        return 1;
    }
    std::cout << "All network tests passed.\n";
    return 0;
}
