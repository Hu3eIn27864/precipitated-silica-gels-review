#include "MonteCarlo.hpp"

#include <cmath>
#include <exception>
#include <iostream>
#include <stdexcept>
#include <vector>

namespace {
void require(bool ok, const char* message) {
    if (!ok) throw std::runtime_error(message);
}

void testReproducibilityAndSweepCount() {
    const mc3d::SimulationBox box(15.0);
    const mc3d::PairPotential potential(1.0, 0.5, 2.5);
    const std::vector<mc3d::Particle> initial{
        {0, {2.0, 2.0, 2.0}}, {1, {3.2, 2.0, 2.0}},
        {2, {4.4, 2.0, 2.0}}, {3, {5.6, 2.0, 2.0}}
    };
    auto a = initial;
    auto b = initial;
    mc3d::Random rngA(123456), rngB(123456);
    mc3d::MonteCarlo mcA(box, potential, 0.08, rngA);
    mc3d::MonteCarlo mcB(box, potential, 0.08, rngB);
    mcA.sweep(a);
    mcB.sweep(b);
    require(mcA.statistics().attempted == initial.size(),
            "one sweep must attempt N moves");
    require(mcA.statistics().accepted == mcB.statistics().accepted,
            "same seed did not reproduce acceptance count");
    for (std::size_t i = 0; i < a.size(); ++i) {
        require(std::abs(a[i].position.x - b[i].position.x) < 1e-14 &&
                std::abs(a[i].position.y - b[i].position.y) < 1e-14 &&
                std::abs(a[i].position.z - b[i].position.z) < 1e-14,
                "same seed did not reproduce particle coordinates");
    }
}

void testLongRunMaintainsHardCore() {
    const mc3d::SimulationBox box(15.0);
    const mc3d::PairPotential potential(1.0, 0.5, 2.5);
    std::vector<mc3d::Particle> particles{
        {0, {2.0, 2.0, 2.0}}, {1, {3.2, 2.0, 2.0}},
        {2, {4.4, 2.0, 2.0}}, {3, {5.6, 2.0, 2.0}}
    };
    mc3d::Random random(987654321);
    mc3d::MonteCarlo sampler(box, potential, 0.12, random);
    for (int sweep = 0; sweep < 1000; ++sweep) sampler.sweep(particles);
    require(sampler.statistics().attempted == 4000,
            "1000 sweeps should make 4000 attempts");
    require(sampler.statistics().accepted <= sampler.statistics().attempted,
            "accepted move count exceeds attempts");
    require(std::isfinite(mc3d::totalEnergy(particles, box, potential)),
            "hard-core overlap or non-finite energy after MC run");
    for (std::size_t i = 0; i < particles.size(); ++i)
        for (std::size_t j = i + 1; j < particles.size(); ++j)
            require(box.distance(particles[i].position, particles[j].position) >= potential.sigma(),
                    "Metropolis accepted a hard-core overlap");
}

void testEmptySystem() {
    const mc3d::SimulationBox box(10.0);
    const mc3d::PairPotential potential(1.0, 1.0, 2.5);
    mc3d::Random rng(7);
    mc3d::MonteCarlo mc(box, potential, 0.1, rng);
    std::vector<mc3d::Particle> empty;
    mc.sweep(empty);
    require(mc.statistics().attempted == 0, "empty sweep should make no attempts");
}

void testInvalidStep() {
    const mc3d::SimulationBox box(10.0);
    const mc3d::PairPotential potential(1.0, 1.0, 2.5);
    mc3d::Random rng(7);
    bool threw = false;
    try { mc3d::MonteCarlo mc(box, potential, 0.0, rng); }
    catch (const std::invalid_argument&) { threw = true; }
    require(threw, "zero MC displacement should be rejected");
}
}

int main() {
    try {
        testReproducibilityAndSweepCount();
        testLongRunMaintainsHardCore();
        testEmptySystem();
        testInvalidStep();
    } catch (const std::exception& e) {
        std::cerr << "FAILED: " << e.what() << '\n';
        return 1;
    }
    std::cout << "All Metropolis tests passed.\n";
    return 0;
}
