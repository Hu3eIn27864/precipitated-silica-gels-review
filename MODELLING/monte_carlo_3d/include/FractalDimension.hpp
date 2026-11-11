#pragma once

#include <cstddef>
#include <vector>

namespace mc3d {

struct PowerLawFit {
    double exponent{0.0};
    double standardError{0.0};
    double rSquared{0.0};
    double minimumRadius{0.0};
    double maximumRadius{0.0};
    std::size_t pointCount{0};
};

// Fits meanMass(r) = A * r^Df by ordinary least squares in log-log space.
// The caller must supply a physically justified mass-radius curve and fit window.
PowerLawFit fitMassRadiusPowerLaw(const std::vector<double>& radii,
                                  const std::vector<double>& meanMass,
                                  double fitMinimumRadius,
                                  double fitMaximumRadius);

} // namespace mc3d
