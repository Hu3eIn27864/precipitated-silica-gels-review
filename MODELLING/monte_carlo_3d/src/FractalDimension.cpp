#include "FractalDimension.hpp"

#include <algorithm>
#include <cmath>
#include <numeric>
#include <stdexcept>

namespace mc3d {

PowerLawFit fitMassRadiusPowerLaw(const std::vector<double>& radii,
                                  const std::vector<double>& meanMass,
                                  double fitMinimumRadius,
                                  double fitMaximumRadius) {
    if (radii.size() != meanMass.size() || radii.size() < 3 ||
        !std::isfinite(fitMinimumRadius) ||
        !std::isfinite(fitMaximumRadius) ||
        fitMinimumRadius <= 0.0 || fitMaximumRadius <= fitMinimumRadius) {
        throw std::invalid_argument("Invalid mass-radius data or fit interval");
    }

    std::vector<double> x;
    std::vector<double> y;
    for (std::size_t i = 0; i < radii.size(); ++i) {
        if (!std::isfinite(radii[i]) || radii[i] <= 0.0 ||
            !std::isfinite(meanMass[i]) || meanMass[i] <= 0.0 ||
            (i > 0 && radii[i] <= radii[i - 1])) {
            throw std::invalid_argument(
                "Radii must increase strictly and all radii/masses must be finite and positive");
        }
        if (radii[i] >= fitMinimumRadius && radii[i] <= fitMaximumRadius) {
            x.push_back(std::log(radii[i]));
            y.push_back(std::log(meanMass[i]));
        }
    }
    if (x.size() < 3) {
        throw std::invalid_argument("Mass-radius fit interval must contain at least three points");
    }

    const double meanX = std::accumulate(x.begin(), x.end(), 0.0) /
                         static_cast<double>(x.size());
    const double meanY = std::accumulate(y.begin(), y.end(), 0.0) /
                         static_cast<double>(y.size());
    double sxx = 0.0;
    double sxy = 0.0;
    double syy = 0.0;
    for (std::size_t i = 0; i < x.size(); ++i) {
        const double dx = x[i] - meanX;
        const double dy = y[i] - meanY;
        sxx += dx * dx;
        sxy += dx * dy;
        syy += dy * dy;
    }
    if (sxx <= 0.0 || syy <= 0.0) {
        throw std::invalid_argument("Mass-radius fit is singular or has no response variation");
    }

    const double slope = sxy / sxx;
    const double intercept = meanY - slope * meanX;
    double residualSumSquares = 0.0;
    for (std::size_t i = 0; i < x.size(); ++i) {
        const double residual = y[i] - (intercept + slope * x[i]);
        residualSumSquares += residual * residual;
    }

    PowerLawFit fit;
    fit.exponent = slope;
    fit.standardError = std::sqrt(
        std::max(0.0, residualSumSquares /
                          (static_cast<double>(x.size()) - 2.0) / sxx));
    fit.rSquared = std::clamp(1.0 - residualSumSquares / syy, 0.0, 1.0);
    fit.minimumRadius = fitMinimumRadius;
    fit.maximumRadius = fitMaximumRadius;
    fit.pointCount = x.size();
    return fit;
}

} // namespace mc3d
