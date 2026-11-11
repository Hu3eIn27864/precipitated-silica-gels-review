#include "Observables.hpp"

#include <algorithm>
#include <cmath>
#include <queue>
#include <stdexcept>

namespace mc3d {

NetworkObservables analyseNetwork(const std::vector<Particle>& particles,
                                  const SimulationBox& box,
                                  double contactDistance) {
    if (!std::isfinite(contactDistance) || contactDistance <= 0.0)
        throw std::invalid_argument("Contact distance must be finite and positive");

    const std::size_t n = particles.size();
    NetworkObservables out;
    out.particleCount = n;
    out.coordination.assign(n, 0);
    if (n == 0) return out;

    std::vector<std::vector<std::size_t>> graph(n);
    const double cutoff2 = contactDistance * contactDistance;
    for (std::size_t i = 0; i < n; ++i) {
        for (std::size_t j = i + 1; j < n; ++j) {
            if (box.distanceSquared(particles[i].position,
                                    particles[j].position) <= cutoff2) {
                graph[i].push_back(j);
                graph[j].push_back(i);
                ++out.coordination[i];
                ++out.coordination[j];
                ++out.contactCount;
            }
        }
    }
    out.meanCoordination = 2.0 * static_cast<double>(out.contactCount) /
                           static_cast<double>(n);

    std::vector<bool> visited(n, false);
    std::vector<Vec3> unwrapped(n);
    for (std::size_t root = 0; root < n; ++root) {
        if (visited[root]) continue;
        ++out.componentCount;
        std::queue<std::size_t> queue;
        std::vector<std::size_t> members;
        visited[root] = true;
        unwrapped[root] = particles[root].position;
        queue.push(root);

        ClusterObservables component;
        while (!queue.empty()) {
            const auto i = queue.front();
            queue.pop();
            members.push_back(i);
            component.contactCount += graph[i].size();
            for (const auto j : graph[i]) {
                const Vec3 candidate = unwrapped[i] +
                    box.minimumImageDisplacement(particles[i].position,
                                                 particles[j].position);
                if (!visited[j]) {
                    visited[j] = true;
                    unwrapped[j] = candidate;
                    queue.push(j);
                } else if (norm(candidate - unwrapped[j]) >
                           1e-8 * box.sideLength()) {
                    component.periodicUnwrappingConsistent = false;
                }
            }
        }

        component.particleCount = members.size();
        component.unwrappedPositions.reserve(members.size());
        for (const auto i : members) {
            component.unwrappedPositions.push_back(unwrapped[i]);
        }
        component.contactCount /= 2;
        Vec3 centre{};
        for (const auto i : members) centre += unwrapped[i];
        centre /= static_cast<double>(members.size());
        double rg2 = 0.0;
        double degreeSum = 0.0;
        for (const auto i : members) {
            rg2 += normSquared(unwrapped[i] - centre);
            degreeSum += static_cast<double>(out.coordination[i]);
        }
        component.radiusOfGyration =
            std::sqrt(rg2 / static_cast<double>(members.size()));
        component.meanCoordination =
            degreeSum / static_cast<double>(members.size());
        out.largestComponentSize = std::max(out.largestComponentSize,
                                            component.particleCount);
        out.components.push_back(component);
    }
    out.largestComponentFraction =
        static_cast<double>(out.largestComponentSize) / static_cast<double>(n);
    return out;
}

} // namespace mc3d
