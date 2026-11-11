#pragma once

#include "Vec3.hpp"

#include <cstddef>

namespace mc3d {

struct Particle {
    std::size_t id{0};
    Vec3 position{};
};

} // namespace mc3d
