#include "DLCA.hpp"
#include "FractalDimension.hpp"
#include "MassRadius.hpp"
#include "Observables.hpp"

#include <algorithm>
#include <cstdint>
#include <cmath>
#include <cstdlib>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <limits>
#include <stdexcept>
#include <string>
#include <vector>

namespace {
std::size_t parseSize(const char* value, const char* name) {
    std::size_t consumed = 0;
    const std::string input(value);
    if (input.empty() || input.find_first_not_of("0123456789") != std::string::npos)
        throw std::invalid_argument(std::string("Invalid ") + name);
    const unsigned long long parsed = std::stoull(input, &consumed);
    if (consumed != input.size() || parsed == 0 ||
        parsed > std::numeric_limits<std::size_t>::max()) {
        throw std::invalid_argument(std::string("Invalid ") + name);
    }
    return static_cast<std::size_t>(parsed);
}

std::uint64_t parseSeed(const char* value) {
    std::size_t consumed = 0;
    const std::string input(value);
    if (input.empty() || input.find_first_not_of("0123456789") != std::string::npos)
        throw std::invalid_argument("Invalid seed");
    const unsigned long long parsed = std::stoull(input, &consumed);
    if (consumed != input.size()) throw std::invalid_argument("Invalid seed");
    return static_cast<std::uint64_t>(parsed);
}

double parsePositiveDouble(const char* value, const char* name) {
    std::size_t consumed = 0;
    const std::string input(value);
    const double parsed = std::stod(input, &consumed);
    if (consumed != input.size() || !std::isfinite(parsed) || parsed <= 0.0)
        throw std::invalid_argument(std::string("Invalid ") + name);
    return parsed;
}

double parseNonnegativeDouble(const char* value, const char* name) {
    std::size_t consumed = 0;
    const std::string input(value);
    const double parsed = std::stod(input, &consumed);
    if (consumed != input.size() || !std::isfinite(parsed) || parsed < 0.0)
        throw std::invalid_argument(std::string("Invalid ") + name);
    return parsed;
}
}

int main(int argc, char** argv) {
    try {
        if (argc < 7 || argc > 10) {
            std::cerr << "Usage: mc3d_dlca_ensemble <particle_count> <box_length> "
                         "<seed_start> <seed_count> <maximum_attempts> <output_prefix> "
                         "[contact_distance [maximum_component_step [mobility_exponent]]]\n";
            return 2;
        }

        const std::size_t particleCount = parseSize(argv[1], "particle count");
        const double boxLength = parsePositiveDouble(argv[2], "box length");
        const std::uint64_t seedStart = parseSeed(argv[3]);
        const std::size_t seedCount = parseSize(argv[4], "seed count");
        const std::size_t maximumAttempts = parseSize(argv[5], "maximum attempts");
        const std::string prefix(argv[6]);
        const double contactDistance = argc >= 8
            ? parsePositiveDouble(argv[7], "contact distance") : 1.0;
        const double maximumComponentStep = argc >= 9
            ? parsePositiveDouble(argv[8], "maximum component step") : 0.2;
        const double mobilityExponent = argc >= 10
            ? parseNonnegativeDouble(argv[9], "mobility exponent") : 1.0;
        if (contactDistance >= 0.5 * boxLength)
            throw std::invalid_argument("Contact distance must be below half the box length");
        if (maximumComponentStep * std::sqrt(3.0) > 0.5 * contactDistance)
            throw std::invalid_argument("Maximum component step is too large for contact detection");
        if (seedCount - 1 > std::numeric_limits<std::uint64_t>::max() - seedStart)
            throw std::invalid_argument("Seed range overflows uint64_t");

        const std::string runsPath = prefix + "_runs.csv";
        const std::string curvePath = prefix + "_mass_radius.csv";
        const std::string fitsPath = prefix + "_fit_windows.csv";
        std::ofstream runs(runsPath), curves(curvePath), fits(fitsPath);
        if (!runs || !curves || !fits)
            throw std::runtime_error("Could not open one or more output CSV files");

        runs << "seed,completed,attempts,successful_merges,component_count,"
                "largest_component_size,largest_component_rg,unwrapping_consistent,"
                "contact_distance,maximum_component_step,mobility_exponent\n";
        curves << "seed,particle_count,radius,mean_enclosed_mass\n";
        fits << "seed,fit_minimum_radius,fit_maximum_radius,exponent,"
                "standard_error,r_squared,point_count\n";
        runs << std::setprecision(17);
        curves << std::setprecision(17);
        fits << std::setprecision(17);

        const mc3d::SimulationBox box(boxLength);
        mc3d::DLCAConfig config;
        config.particleCount = particleCount;
        config.contactDistance = contactDistance;
        config.maximumComponentStep = maximumComponentStep;
        config.mobilityExponent = mobilityExponent;
        config.maximumAttempts = maximumAttempts;
        const std::vector<double> radii{1.5, 2.0, 2.5, 3.0, 4.0, 5.0, 6.0, 8.0};

        for (std::size_t runIndex = 0; runIndex < seedCount; ++runIndex) {
            const std::uint64_t seed = seedStart + runIndex;
            mc3d::Random random(seed);
            const auto generated = mc3d::DLCA(box, config, random).generate();
            const auto network = mc3d::analyseNetwork(
                generated.particles, box, config.contactDistance * (1.0 + 1e-10));

            const auto largest = std::max_element(
                network.components.begin(), network.components.end(),
                [](const mc3d::ClusterObservables& a,
                   const mc3d::ClusterObservables& b) {
                    return a.particleCount < b.particleCount;
                });
            const bool hasLargest = largest != network.components.end();
            const double rg = hasLargest ? largest->radiusOfGyration :
                std::numeric_limits<double>::quiet_NaN();
            const bool unwrapped = hasLargest && largest->periodicUnwrappingConsistent;

            runs << seed << ',' << (generated.completed ? 1 : 0) << ','
                 << generated.attempts << ',' << generated.successfulMerges << ','
                 << network.componentCount << ','
                 << (hasLargest ? largest->particleCount : 0) << ','
                 << rg << ',' << (unwrapped ? 1 : 0) << ','
                 << config.contactDistance << ',' << config.maximumComponentStep << ','
                 << config.mobilityExponent << '\n';

            // Only a completed, consistently unwrapped aggregate is suitable
            // for this whole-aggregate mass-radius export.
            if (!generated.completed || !hasLargest || !unwrapped) continue;
            const auto curve = mc3d::calculateMassRadiusCurve(
                largest->unwrappedPositions, radii);
            std::vector<double> masses;
            masses.reserve(curve.size());
            for (const auto& point : curve) {
                curves << seed << ',' << largest->particleCount << ','
                       << point.radius << ',' << point.meanEnclosedMass << '\n';
                masses.push_back(point.meanEnclosedMass);
            }
            for (const auto& fit :
                 mc3d::scanMassRadiusFitWindows(radii, masses, 3)) {
                fits << seed << ',' << fit.minimumRadius << ','
                     << fit.maximumRadius << ',' << fit.exponent << ','
                     << fit.standardError << ',' << fit.rSquared << ','
                     << fit.pointCount << '\n';
            }
        }

        std::cout << "Wrote " << runsPath << ", " << curvePath
                  << " and " << fitsPath << '\n';
        std::cout << "Fit-window rows are diagnostics only; no interval is "
                     "automatically selected.\n";
        return 0;
    } catch (const std::exception& error) {
        std::cerr << "Error: " << error.what() << '\n';
        return 1;
    }
}
