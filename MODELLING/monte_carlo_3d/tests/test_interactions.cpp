#include "Energy.hpp"

#include <cmath>
#include <exception>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>

namespace {
void require(bool ok, const std::string& message) {
    if (!ok) throw std::runtime_error(message);
}
bool near(double a, double b, double tol = 1e-10) {
    return std::abs(a - b) <= tol;
}

void testPotential() {
    const mc3d::PairPotential p(1.0, 1.0, 2.5);
    require(std::isinf(p.energy(0.9)), "hard-core overlap must have infinite energy");
    require(near(p.energy(2.5), 0.0), "potential must be zero at cutoff");
    require(p.energy(1.5) < 0.0, "potential should be attractive near its minimum");
    require(std::abs(p.energy(2.5 - 1e-7)) < 1e-5, "shifted potential is discontinuous at cutoff");
    const mc3d::PairPotential zero(1.0, 0.0, 2.5);
    require(near(zero.energy(1.2), 0.0), "zero-attraction limit is not zero");
}

void testBruteForceLocalEnergy() {
    const mc3d::SimulationBox box(12.0);
    const mc3d::PairPotential potential(1.0, 0.8, 2.5);
    std::vector<mc3d::Particle> p{
        {0, {1.0, 1.0, 1.0}}, {1, {2.2, 1.0, 1.0}},
        {2, {5.0, 1.0, 1.0}}, {3, {11.2, 1.0, 1.0}}
    };
    const mc3d::Vec3 proposal{1.1, 1.0, 1.0};
    const double oldLocal = mc3d::localEnergy(0, p[0].position, p, box, potential);
    const double newLocal = mc3d::localEnergy(0, proposal, p, box, potential);
    const double oldTotal = mc3d::totalEnergy(p, box, potential);
    auto moved = p;
    moved[0].position = proposal;
    const double newTotal = mc3d::totalEnergy(moved, box, potential);
    require(near(newLocal - oldLocal, newTotal - oldTotal),
            "local energy difference differs from full-system energy difference");
}

void testNeighborList() {
    const mc3d::SimulationBox box(12.0);
    const mc3d::PairPotential potential(1.0, 0.7, 2.5);
    std::vector<mc3d::Particle> p{
        {0, {0.4, 1.0, 1.0}}, {1, {11.5, 1.0, 1.0}},
        {2, {3.0, 1.0, 1.0}}, {3, {7.0, 1.0, 1.0}}
    };
    mc3d::NeighborList list(2.5, 0.4);
    list.rebuild(p, box);
    require(list.validFor(p, box), "fresh neighbor list should be valid");
    const double fromList = list.localEnergy(0, p[0].position, p, box, potential);
    const double brute = mc3d::localEnergy(0, p[0].position, p, box, potential);
    require(near(fromList, brute), "neighbor-list local energy differs from brute force");
    p[0].position.x += 0.21;
    require(!list.validFor(p, box), "neighbor list should invalidate after skin/2 displacement");
}

void testInvalidNeighborList() {
    bool threw = false;
    try { mc3d::NeighborList list(2.5, 0.5); list.rebuild({}, mc3d::SimulationBox(6.0)); }
    catch (const std::invalid_argument&) { threw = true; }
    require(threw, "list radius >= half box length should be rejected");
}
}

int main() {
    try {
        testPotential();
        testBruteForceLocalEnergy();
        testNeighborList();
        testInvalidNeighborList();
    } catch (const std::exception& e) {
        std::cerr << "FAILED: " << e.what() << '\n';
        return 1;
    }
    std::cout << "All interaction tests passed.\n";
    return 0;
}
