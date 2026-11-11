#include "DLCA.hpp"
#include "Observables.hpp"

#include <cmath>
#include <exception>
#include <iostream>
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
    require(near(a.components[0].radiusOfGyration,
                 std::sqrt((0.8*0.8 + 0.0 + 0.8*0.8)/3.0)),
            "periodic cluster Rg was not calculated from unwrapped coordinates");
    require(a.components[0].periodicUnwrappingConsistent,
            "simple chain should unwrap consistently");
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
    for (std::size_t i = 0; i < a.particles.size(); ++i)
        for (std::size_t j = i + 1; j < a.particles.size(); ++j)
            require(box.distance(a.particles[i].position,
                                 a.particles[j].position) >= 1.0 - 1e-10,
                    "DLCA generated overlapping particles");
    const auto obs = mc3d::analyseNetwork(a.particles, box, 1.0 + 1e-10);
    require(obs.particleCount == cfg.particleCount,
            "network analysis lost particles");
    require(obs.contactCount == a.successfulMerges,
            "tree-like DLCA contact count differs from successful merge count");
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
        testDLCAReproducibilityAndNonOverlap();
        testEmptyNetwork();
    } catch (const std::exception& e) {
        std::cerr << "FAILED: " << e.what() << '\n';
        return 1;
    }
    std::cout << "All network tests passed.\n";
    return 0;
}
