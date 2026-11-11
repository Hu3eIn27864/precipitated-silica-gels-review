#include "DLCA.hpp"
#include "FractalDimension.hpp"
#include "MassRadius.hpp"
#include "Observables.hpp"
#include "PeriodicCellList.hpp"
#include "PeriodicSweptCollision.hpp"

#include <algorithm>
#include <cmath>
#include <cstdint>
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
    require(a.components[0].unwrappedPositions.size() == 3,
            "component did not retain graph-unwrapped coordinates");
    const auto periodicMassRadius =
        mc3d::calculateMassRadiusCurve(a.components[0].unwrappedPositions,
                                        {0.81, 1.61});
    require(near(periodicMassRadius[0].meanEnclosedMass, 7.0 / 3.0) &&
            near(periodicMassRadius[1].meanEnclosedMass, 3.0),
            "mass-radius estimator did not use graph-unwrapped periodic coordinates");

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
            near(a.cumulativeSquaredClusterTranslation,
                 b.cumulativeSquaredClusterTranslation) &&
            near(a.cumulativeClusterTranslationPathLength,
                 b.cumulativeClusterTranslationPathLength) &&
            a.completed == b.completed,
            "DLCA metadata not reproducible");
    require(std::isfinite(a.cumulativeSquaredClusterTranslation) &&
            a.cumulativeSquaredClusterTranslation >= 0.0 &&
            std::isfinite(a.cumulativeClusterTranslationPathLength) &&
            a.cumulativeClusterTranslationPathLength >= 0.0 &&
            a.cumulativeSquaredClusterTranslation <=
                a.cumulativeClusterTranslationPathLength *
                a.cumulativeClusterTranslationPathLength + 1e-10,
            "DLCA realized translation diagnostics are invalid");
    require(a.cumulativeClusterTranslationPathLength > 0.0,
            "DLCA did not record any realized cluster translation");
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


void testDLCACommonDisplacementBudgetAndAttemptCap() {
    const mc3d::SimulationBox box(12.0);
    mc3d::DLCAConfig targetConfig;
    targetConfig.particleCount = 12;
    targetConfig.contactDistance = 1.0;
    targetConfig.maximumComponentStep = 0.2;
    targetConfig.maximumAttempts = 30000;
    targetConfig.targetCumulativeSquaredTranslation = 1e-8;
    mc3d::Random targetRandom(4321);
    const auto targetResult =
        mc3d::DLCA(box, targetConfig, targetRandom).generate();
    require(targetResult.displacementBudgetReached,
            "DLCA did not stop after reaching the cumulative displacement target");
    require(!targetResult.attemptLimitReached,
            "DLCA incorrectly reported the attempt cap after reaching the displacement target");
    require(targetResult.attempts == 1,
            "DLCA should check the displacement target after the first complete move");
    require(targetResult.displacementBudgetOvershoot >= 0.0 &&
            near(targetResult.displacementBudgetOvershoot,
                 targetResult.cumulativeSquaredClusterTranslation - 1e-8),
            "DLCA displacement-budget overshoot was not recorded");

    mc3d::DLCAConfig cappedConfig = targetConfig;
    cappedConfig.maximumAttempts = 1;
    cappedConfig.targetCumulativeSquaredTranslation = 1e9;
    mc3d::Random cappedRandom(4321);
    const auto cappedResult =
        mc3d::DLCA(box, cappedConfig, cappedRandom).generate();
    require(!cappedResult.displacementBudgetReached &&
            cappedResult.attemptLimitReached,
            "DLCA did not report the hard attempt safety cap");
    require(cappedResult.displacementBudgetOvershoot == 0.0,
            "DLCA reported overshoot when the displacement target was not reached");

    mc3d::DLCAConfig legacyConfig = targetConfig;
    legacyConfig.targetCumulativeSquaredTranslation = 0.0;
    legacyConfig.maximumAttempts = 1;
    mc3d::Random legacyRandom(4321);
    const auto legacyResult =
        mc3d::DLCA(box, legacyConfig, legacyRandom).generate();
    require(!legacyResult.displacementBudgetReached &&
            legacyResult.attemptLimitReached,
            "zero displacement target should preserve legacy fixed-attempt behaviour");
}

void testPeriodicSweptCollisionChecksNeighbouringImages() {
    // A particle starts just inside the positive half-box image boundary.
    // Moving in +x takes the nearest image from +4.99 to -3.01; checking
    // only the initial minimum image would miss this collision.
    const auto contact = mc3d::firstPeriodicSweptSphereContact(
        {4.99, 0.0, 0.0}, {-2.0, 0.0, 0.0}, 4.9, 10.0);
    require(contact.has_value(),
            "periodic swept collision missed a neighbouring image");
    require(near(*contact, 0.055, 1e-10),
            "periodic swept collision returned the wrong first-contact fraction");

    const auto noContact = mc3d::firstPeriodicSweptSphereContact(
        {4.0, 0.0, 0.0}, {0.0, 1.0, 0.0}, 1.0, 10.0);
    require(!noContact.has_value(),
            "periodic swept collision reported a false contact");

    const auto overlap = mc3d::firstPeriodicSweptSphereContact(
        {0.5, 0.0, 0.0}, {0.1, 0.0, 0.0}, 1.0, 10.0);
    require(overlap.has_value() && *overlap == 0.0,
            "periodic swept collision did not detect initial overlap");
}

void testPeriodicSweptCollisionAgainstSampledTrajectories() {
    constexpr double boxLength = 10.0;
    constexpr double contactDistance = 1.0;
    std::uint64_t state = 0x6a09e667f3bcc909ULL;
    const auto unit = [&state]() {
        state = state * 2862933555777941757ULL + 3037000493ULL;
        return static_cast<double>(state >> 11) / 9007199254740992.0;
    };
    const auto signedUnit = [&unit]() { return 2.0 * unit() - 1.0; };
    for (int sample = 0; sample < 500; ++sample) {
        const mc3d::Vec3 relative{
            0.5 * boxLength * signedUnit(), 0.5 * boxLength * signedUnit(),
            0.5 * boxLength * signedUnit()};
        const mc3d::Vec3 displacement{
            0.24 * signedUnit(), 0.24 * signedUnit(), 0.24 * signedUnit()};
        const auto contact = mc3d::firstPeriodicSweptSphereContact(
            relative, displacement, contactDistance, boxLength);
        bool sampledContact = false;
        double firstSample = 1.0;
        for (int step = 0; step <= 2000; ++step) {
            const double fraction = static_cast<double>(step) / 2000.0;
            const mc3d::Vec3 point = relative - displacement * fraction;
            const mc3d::Vec3 minimumImage{
                point.x - boxLength * std::nearbyint(point.x / boxLength),
                point.y - boxLength * std::nearbyint(point.y / boxLength),
                point.z - boxLength * std::nearbyint(point.z / boxLength)};
            if (mc3d::normSquared(minimumImage) <=
                contactDistance * contactDistance) {
                sampledContact = true;
                firstSample = fraction;
                break;
            }
        }
        if (sampledContact) {
            require(contact.has_value(),
                    "analytic periodic sweep missed a sampled trajectory contact");
            require(*contact <= firstSample + 1e-12,
                    "analytic periodic sweep reported contact after sampled contact");
        }
        if (contact) {
            const mc3d::Vec3 point = relative - displacement * *contact;
            const mc3d::Vec3 minimumImage{
                point.x - boxLength * std::nearbyint(point.x / boxLength),
                point.y - boxLength * std::nearbyint(point.y / boxLength),
                point.z - boxLength * std::nearbyint(point.z / boxLength)};
            require(mc3d::normSquared(minimumImage) <=
                        contactDistance * contactDistance + 1e-10,
                    "analytic periodic sweep returned a non-contacting fraction");
        }
    }
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
    const auto unit = [&state]() {
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

void testMassRadiusPowerLawRegression() {
    std::vector<double> radii;
    std::vector<double> mass;
    for (int i = 1; i <= 9; ++i) {
        const double r = static_cast<double>(i);
        radii.push_back(r);
        mass.push_back(1.7 * std::pow(r, 1.65));
    }
    const auto fit = mc3d::fitMassRadiusPowerLaw(radii, mass, 2.0, 8.0);
    require(near(fit.exponent, 1.65, 1e-10),
            "mass-radius regression did not recover a known power-law exponent");
    require(near(fit.rSquared, 1.0, 1e-12),
            "exact power law should have unit R-squared");
    require(fit.pointCount == 7 && fit.minimumRadius == 2.0 &&
            fit.maximumRadius == 8.0,
            "mass-radius fit did not preserve its declared fit window");

    bool rejected = false;
    try {
        (void)mc3d::fitMassRadiusPowerLaw({1.0, 2.0, 3.0},
                                          {1.0, 0.0, 3.0}, 1.0, 3.0);
    } catch (const std::invalid_argument&) {
        rejected = true;
    }
    require(rejected, "mass-radius fit accepted a non-positive mass");
}

void testMassRadiusFitWindowSensitivityScan() {
    const std::vector<double> radii{1, 2, 3, 4, 5, 6, 7, 8, 9};
    std::vector<double> exactMass;
    for (const double radius : radii)
        exactMass.push_back(2.4 * std::pow(radius, 1.4));
    const auto stable = mc3d::scanMassRadiusFitWindows(radii, exactMass, 3);
    require(stable.size() == 28,
            "fit-window scan did not enumerate every contiguous window");
    for (const auto& fit : stable) {
        require(std::abs(fit.exponent - 1.4) < 1e-10,
                "exact power law changed exponent across fit windows");
    }

    std::vector<double> crossoverMass;
    for (const double radius : radii) {
        crossoverMass.push_back(radius <= 4.0 ? radius : 4.0 * std::pow(radius / 4.0, 2.0));
    }
    const auto sensitive =
        mc3d::scanMassRadiusFitWindows(radii, crossoverMass, 3);
    double minimumExponent = sensitive.front().exponent;
    double maximumExponent = sensitive.front().exponent;
    for (const auto& fit : sensitive) {
        minimumExponent = std::min(minimumExponent, fit.exponent);
        maximumExponent = std::max(maximumExponent, fit.exponent);
    }
    require(maximumExponent - minimumExponent > 0.2,
            "fit-window scan failed to reveal a constructed crossover");
}

void testMassRadiusCompactAndBranchedReferenceGeometries() {
    // Finite, fully occupied cubic lattice: boundary effects lower the
    // apparent exponent below three, but it should remain distinctly compact.
    std::vector<mc3d::Vec3> cube;
    for (int x = 0; x < 9; ++x)
        for (int y = 0; y < 9; ++y)
            for (int z = 0; z < 9; ++z)
                cube.push_back({static_cast<double>(x), static_cast<double>(y),
                                static_cast<double>(z)});
    const std::vector<double> cubeRadii{1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5};
    const auto cubeCurve = mc3d::calculateMassRadiusCurve(cube, cubeRadii);
    std::vector<double> cubeMass;
    for (const auto& point : cubeCurve) cubeMass.push_back(point.meanEnclosedMass);
    const auto cubeFit = mc3d::fitMassRadiusPowerLaw(cubeRadii, cubeMass, 1.0, 4.5);
    require(cubeFit.exponent > 2.0 && cubeFit.exponent < 3.0,
            "finite compact cubic reference did not show compact scaling");

    // Three intersecting one-dimensional arms form a simple branched reference.
    // This is a geometry check, not a claim that the object is a fractal.
    std::vector<mc3d::Vec3> branch;
    for (int q = -100; q <= 100; ++q) {
        branch.push_back({static_cast<double>(q), 0.0, 0.0});
        if (q != 0) branch.push_back({0.0, static_cast<double>(q), 0.0});
        if (q != 0) branch.push_back({0.0, 0.0, static_cast<double>(q)});
    }
    const std::vector<double> branchRadii{5.0, 8.0, 12.0, 16.0, 20.0};
    const auto branchCurve = mc3d::calculateMassRadiusCurve(branch, branchRadii);
    std::vector<double> branchMass;
    for (const auto& point : branchCurve) branchMass.push_back(point.meanEnclosedMass);
    const auto branchFit =
        mc3d::fitMassRadiusPowerLaw(branchRadii, branchMass, 5.0, 20.0);
    require(branchFit.exponent > 1.0 && branchFit.exponent < 1.3,
            "branched reference geometry produced an unexpected mass-radius slope");
}

void testMassRadiusFitWindowScanSkipsPlateaus() {
    const std::vector<double> radii{1, 2, 3, 4, 5, 6};
    const auto plateauPrefix =
        mc3d::scanMassRadiusFitWindows(radii, {1, 1, 1, 2, 3, 4}, 3);
    require(!plateauPrefix.empty(),
            "fit-window scan discarded all valid windows after a plateau");
    const auto constant =
        mc3d::scanMassRadiusFitWindows(radii, {1, 1, 1, 1, 1, 1}, 3);
    require(constant.empty(),
            "fit-window scan should return no slopes for a constant mass curve");
}

void testMassRadiusRecoversOneDimensionalScaling() {
    std::vector<mc3d::Vec3> line;
    line.reserve(1001);
    for (int i = 0; i <= 1000; ++i) {
        line.push_back({static_cast<double>(i), 0.0, 0.0});
    }
    const std::vector<double> radii{10, 15, 20, 25, 30, 40, 50};
    const auto curve = mc3d::calculateMassRadiusCurve(line, radii);
    std::vector<double> masses;
    masses.reserve(curve.size());
    for (const auto& point : curve) masses.push_back(point.meanEnclosedMass);
    const auto fit = mc3d::fitMassRadiusPowerLaw(radii, masses, 10.0, 50.0);
    require(std::abs(fit.exponent - 1.0) < 0.05,
            "mass-radius estimator did not recover line-like Df near one");
    require(fit.rSquared > 0.995,
            "line-like mass-radius scaling should be strongly linear in log-log space");

    const std::vector<mc3d::Vec3> widelySeparated{
        {0.0, 0.0, 0.0}, {1.0e200, 0.0, 0.0}
    };
    const auto largeScale = mc3d::calculateMassRadiusCurve(widelySeparated, {1.0e199});
    require(near(largeScale[0].meanEnclosedMass, 1.0),
            "overflow-resistant distance calculation failed at large coordinate scales");
}

void testMassRadiusCurveGeneration() {
    const std::vector<mc3d::Vec3> positions{
        {0.0, 0.0, 0.0}, {1.0, 0.0, 0.0}, {3.0, 0.0, 0.0}
    };
    const auto curve = mc3d::calculateMassRadiusCurve(positions, {1.0, 3.0});
    require(curve.size() == 2, "mass-radius curve has wrong number of radii");
    require(near(curve[0].meanEnclosedMass, 5.0 / 3.0),
            "mean enclosed mass at radius one is incorrect");
    require(near(curve[1].meanEnclosedMass, 3.0),
            "large-radius mass should include the complete cluster");

    const std::vector<mc3d::Vec3> translated{
        {7.0, -2.0, 4.0}, {8.0, -2.0, 4.0}, {10.0, -2.0, 4.0}
    };
    const auto shifted = mc3d::calculateMassRadiusCurve(translated, {1.0, 3.0});
    require(near(curve[0].meanEnclosedMass, shifted[0].meanEnclosedMass) &&
            near(curve[1].meanEnclosedMass, shifted[1].meanEnclosedMass),
            "mass-radius curve changed under rigid translation");

    bool rejected = false;
    try {
        (void)mc3d::calculateMassRadiusCurve(positions, {1.0, 1.0});
    } catch (const std::invalid_argument&) {
        rejected = true;
    }
    require(rejected, "mass-radius curve accepted non-increasing radii");
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
        testDLCACommonDisplacementBudgetAndAttemptCap();
        testPeriodicSweptCollisionChecksNeighbouringImages();
        testPeriodicSweptCollisionAgainstSampledTrajectories();
        testPeriodicCellListIsConservative();
        testCellListRandomizedAgainstBruteForce();
        testCellListRejectsExcessiveDenseGrid();
        testMassRadiusPowerLawRegression();
        testMassRadiusFitWindowSensitivityScan();
        testMassRadiusFitWindowScanSkipsPlateaus();
        testMassRadiusCurveGeneration();
        testMassRadiusRecoversOneDimensionalScaling();
        testMassRadiusCompactAndBranchedReferenceGeometries();
        testEmptyNetwork();
    } catch (const std::exception& e) {
        std::cerr << "FAILED: " << e.what() << '\n';
        return 1;
    }
    std::cout << "All network tests passed.\n";
    return 0;
}
