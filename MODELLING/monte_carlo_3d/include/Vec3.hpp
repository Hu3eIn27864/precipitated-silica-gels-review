#pragma once

#include <cmath>
#include <stdexcept>

namespace mc3d {

struct Vec3 {
    double x{0.0};
    double y{0.0};
    double z{0.0};

    Vec3& operator+=(const Vec3& rhs) noexcept {
        x += rhs.x; y += rhs.y; z += rhs.z; return *this;
    }
    Vec3& operator-=(const Vec3& rhs) noexcept {
        x -= rhs.x; y -= rhs.y; z -= rhs.z; return *this;
    }
    Vec3& operator*=(double scalar) noexcept {
        x *= scalar; y *= scalar; z *= scalar; return *this;
    }
    Vec3& operator/=(double scalar) {
        if (scalar == 0.0) throw std::invalid_argument("Vec3 division by zero");
        x /= scalar; y /= scalar; z /= scalar; return *this;
    }
};

inline Vec3 operator+(Vec3 lhs, const Vec3& rhs) noexcept { return lhs += rhs; }
inline Vec3 operator-(Vec3 lhs, const Vec3& rhs) noexcept { return lhs -= rhs; }
inline Vec3 operator*(Vec3 value, double scalar) noexcept { return value *= scalar; }
inline Vec3 operator*(double scalar, Vec3 value) noexcept { return value *= scalar; }
inline Vec3 operator/(Vec3 value, double scalar) { return value /= scalar; }

inline double dot(const Vec3& a, const Vec3& b) noexcept {
    return a.x*b.x + a.y*b.y + a.z*b.z;
}
inline double normSquared(const Vec3& value) noexcept { return dot(value, value); }
inline double norm(const Vec3& value) noexcept { return std::sqrt(normSquared(value)); }

} // namespace mc3d
