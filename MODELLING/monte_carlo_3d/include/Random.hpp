#pragma once

#include <cstddef>
#include <cstdint>
#include <stdexcept>
#include <random>

namespace mc3d {

class Random {
public:
    explicit Random(std::uint64_t seed) : seed_(seed), engine_(seed) {}

    std::uint64_t seed() const noexcept { return seed_; }

    double uniform01() {
        return std::generate_canonical<double, 53>(engine_);
    }

    double uniform(double lower, double upper) {
        return std::uniform_real_distribution<double>(lower, upper)(engine_);
    }

    std::size_t uniformIndex(std::size_t upperExclusive) {
        if (upperExclusive == 0) {
            throw std::invalid_argument("uniformIndex requires a positive upper bound");
        }
        return std::uniform_int_distribution<std::size_t>(0, upperExclusive - 1)(engine_);
    }

private:
    std::uint64_t seed_;
    std::mt19937_64 engine_;
};

} // namespace mc3d
