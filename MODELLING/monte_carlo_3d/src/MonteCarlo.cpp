#include "MonteCarlo.hpp"

#include <cmath>
#include <stdexcept>

namespace mc3d {

MonteCarlo::MonteCarlo(const SimulationBox& box,
                       const PairPotential& potential,
                       double maximumComponentDisplacement,
                       Random& random)
    : box_(box), potential_(potential),
      maxDisplacement_(maximumComponentDisplacement), random_(random) {
    if (!std::isfinite(maxDisplacement_) || maxDisplacement_ <= 0.0)
        throw std::invalid_argument("Maximum MC displacement must be finite and positive");
}

bool MonteCarlo::attemptMove(std::vector<Particle>& particles) {
    if (particles.empty()) return false;
    ++statistics_.attempted;

    const std::size_t index = random_.uniformIndex(particles.size());
    const Vec3 displacement{
        random_.uniform(-maxDisplacement_, maxDisplacement_),
        random_.uniform(-maxDisplacement_, maxDisplacement_),
        random_.uniform(-maxDisplacement_, maxDisplacement_)
    };
    const Vec3 proposed = box_.wrap(particles[index].position + displacement);

    const double oldEnergy = mc3d::localEnergy(
        index, particles[index].position, particles, box_, potential_);
    if (!std::isfinite(oldEnergy))
        throw std::logic_error("Initial configuration contains a hard-core overlap");

    const double newEnergy = mc3d::localEnergy(
        index, proposed, particles, box_, potential_);
    if (!std::isfinite(newEnergy)) return false;

    const double delta = newEnergy - oldEnergy;
    const bool accept = delta <= 0.0 || random_.uniform01() < std::exp(-delta);
    if (accept) {
        particles[index].position = proposed;
        ++statistics_.accepted;
    }
    return accept;
}

void MonteCarlo::sweep(std::vector<Particle>& particles) {
    const std::size_t attempts = particles.size();
    for (std::size_t i = 0; i < attempts; ++i) attemptMove(particles);
}

} // namespace mc3d
