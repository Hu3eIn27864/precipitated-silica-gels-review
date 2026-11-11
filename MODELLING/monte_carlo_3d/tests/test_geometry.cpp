#include "SimulationBox.hpp"

#include <cmath>
#include <exception>
#include <iostream>
#include <stdexcept>
#include <string>

namespace {

void require(bool condition, const std::string& message) {
    if (!condition) throw std::runtime_error(message);
}

bool near(double a, double b, double tolerance = 1e-12) {
    return std::abs(a - b) <= tolerance;
}

void testWrapping() {
    const mc3d::SimulationBox box(10.0);
    const auto p = box.wrap({-1.0, 10.0, 21.5});
    require(near(p.x, 9.0), "negative coordinate did not wrap");
    require(near(p.y, 0.0), "coordinate at L did not wrap to zero");
    require(near(p.z, 1.5), "coordinate above L did not wrap");
}

void testMinimumImage() {
    const mc3d::SimulationBox box(10.0);
    const auto d = box.minimumImageDisplacement({0.2, 5.0, 9.8},
                                                 {9.8, 5.0, 0.2});
    require(near(d.x, -0.4), "minimum-image x displacement incorrect");
    require(near(d.y, 0.0), "minimum-image y displacement incorrect");
    require(near(d.z, 0.4), "minimum-image z displacement incorrect");
    require(near(box.distance({0.2, 5.0, 9.8}, {9.8, 5.0, 0.2}),
                 std::sqrt(0.32)), "minimum-image distance incorrect");
}

void testInvalidBox() {
    bool threw = false;
    try { mc3d::SimulationBox invalid(0.0); }
    catch (const std::invalid_argument&) { threw = true; }
    require(threw, "zero-sized box should throw");
}

} // namespace

int main() {
    try {
        testWrapping();
        testMinimumImage();
        testInvalidBox();
    } catch (const std::exception& error) {
        std::cerr << "FAILED: " << error.what() << '\n';
        return 1;
    }
    std::cout << "All geometry tests passed.\n";
    return 0;
}
