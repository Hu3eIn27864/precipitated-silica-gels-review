#pragma once

#include <cmath>
#include <limits>
#include <stdexcept>

namespace mc3d {

// Generic shifted/truncated Lennard-Jones test potential with a hard core.
// Reduced units: sigma = particle diameter, epsilon = kBT units.
// This is not a chemically calibrated silica force field.
class PairPotential {
public:
    PairPotential(double sigma, double epsilon, double cutoff)
        : sigma_(sigma), epsilon_(epsilon), cutoff_(cutoff) {
        if (!std::isfinite(sigma_) || sigma_ <= 0.0)
            throw std::invalid_argument("PairPotential sigma must be finite and positive");
        if (!std::isfinite(epsilon_) || epsilon_ < 0.0)
            throw std::invalid_argument("PairPotential epsilon must be finite and non-negative");
        if (!std::isfinite(cutoff_) || cutoff_ <= sigma_)
            throw std::invalid_argument("PairPotential cutoff must be finite and greater than sigma");
        const double sr = sigma_ / cutoff_;
        const double sr6 = std::pow(sr, 6);
        cutoffEnergy_ = 4.0 * epsilon_ * (sr6 * sr6 - sr6);
    }

    double sigma() const noexcept { return sigma_; }
    double epsilon() const noexcept { return epsilon_; }
    double cutoff() const noexcept { return cutoff_; }

    // Returns +infinity for hard-core overlap; zero at and beyond cutoff.
    double energy(double distance) const {
        if (!std::isfinite(distance) || distance < 0.0)
            throw std::invalid_argument("Pair distance must be finite and non-negative");
        if (distance < sigma_) return std::numeric_limits<double>::infinity();
        if (distance >= cutoff_ || epsilon_ == 0.0) return 0.0;
        const double sr = sigma_ / distance;
        const double sr6 = std::pow(sr, 6);
        return 4.0 * epsilon_ * (sr6 * sr6 - sr6) - cutoffEnergy_;
    }

    double energySquaredDistance(double distanceSquared) const {
        if (!std::isfinite(distanceSquared) || distanceSquared < 0.0)
            throw std::invalid_argument("Squared pair distance must be finite and non-negative");
        return energy(std::sqrt(distanceSquared));
    }

private:
    double sigma_;
    double epsilon_;
    double cutoff_;
    double cutoffEnergy_;
};

} // namespace mc3d
