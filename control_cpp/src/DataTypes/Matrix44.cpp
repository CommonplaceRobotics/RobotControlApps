#include "Matrix44.h"

#include <exception>

#include "MathDefinitions.h"

namespace App
{
namespace DataTypes
{

/**
 * @brief Constructor, initializes a 4x4 unit matrix
 */
Matrix44::Matrix44()
{
    // initialize to unit matrix
    m_data.fill(0);
    m_data[0] = 1;
    m_data[5] = 1;
    m_data[10] = 1;
    m_data[15] = 1;
}

/**
 * @brief Constructor, copies values from GRPC matrix
 * @param other
 */
Matrix44::Matrix44(const robotcontrolapp::Matrix44& other)
{
    if (other.data().size() != (int)m_data.size()) throw std::runtime_error("could not initialize Matrix44, GRPC matrix had invalid element count " + std::to_string(m_data.size()));
    std::copy_n(other.data().data(), m_data.size(), m_data.data());
}

/**
 * @brief Element access operator
 * @param row row number (0 - 3), throws exception of out of range
 * @param column column number (0 - 3), throws exception of out of range
 * @return matrix element value
 */
double& Matrix44::operator()(int row, int column)
{
    if (row < 0 || row >= 4 || column < 0 || column >= 4) throw std::out_of_range("matrix index out of range");
    return m_data[4 * row + column];
}

/**
 * @brief Element access operator
 * @param row row number (0 - 3), throws exception of out of range
 * @param column column number (0 - 3), throws exception of out of range
 * @return matrix element value
 */
double Matrix44::operator()(int row, int column) const
{
    if (row < 0 || row >= 4 || column < 0 || column >= 4) throw std::out_of_range("matrix index out of range");
    return m_data[4 * row + column];
}

/**
 * @brief Adds the given values to the position values
 * @param x X position in mm
 * @param y Y position in mm
 * @param z Z position in mm
 */
void Matrix44::Translate(double x, double y, double z)
{
    SetX(GetX() + x);
    SetY(GetY() + y);
    SetZ(GetZ() + z);
}

/**
 * @brief Gets the A orientation
 * @return A orientation value
 */
double Matrix44::GetA() const
{
    double a = 0, b = 0, c = 0;
    GetOrientation(a, b, c);
    return a;
}

/**
 * @brief Gets the B orientation
 * @return B orientation value
 */
double Matrix44::GetB() const
{
    double a = 0, b = 0, c = 0;
    GetOrientation(a, b, c);
    return b;
}

/**
 * @brief Gets the C orientation
 * @return C orientation value
 */
double Matrix44::GetC() const
{
    double a = 0, b = 0, c = 0;
    GetOrientation(a, b, c);
    return c;
}

/**
 * @brief Sets the A orientation
 * @param a A angle in degrees
 */
void Matrix44::SetA(double a)
{
    SetOrientation(a, GetB(), GetC());
}

/**
 * @brief Sets the B orientation
 * @param b B angle in degrees
 */
void Matrix44::SetB(double b)
{
    SetOrientation(GetA(), b, GetC());
}

/**
 * @brief Sets the C orientation
 * @param c C angle in degrees
 */
void Matrix44::SetC(double c)
{
    SetOrientation(GetA(), GetB(), c);
}

/**
 * @brief Gets the orientation
 * @param a A angle in degrees
 * @param b B angle in degrees
 * @param c C angle in degrees
 */
void Matrix44::GetOrientation(double& a, double& b, double& c) const
{
    constexpr double eps = 0.001;
    b = atan2(-m_data[8], sqrt((m_data[0] * m_data[0] + m_data[4] * m_data[4])));

    if (fabs(b - M_PI / 2.0) < eps) // singularity b = Pi/2
    {
        a = 0.0;
        c = atan2(m_data[1], m_data[5]);
    }
    else if (fabs(b + M_PI / 2.0) < eps) // singularity b = - PI/2
    {
        a = 0.0;
        c = -atan2(m_data[1], m_data[5]);
    }
    else // normal case
    {
        double cb = cos(b);
        a = atan2(m_data[4] / cb, m_data[0] / cb);
        c = atan2(m_data[9] / cb, m_data[10] / cb);
    }

    a *= rad2deg;
    b *= rad2deg;
    c *= rad2deg;
}

/**
 * @brief Sets the orientation
 * @param a A angle in degrees
 * @param b B angle in degrees
 * @param c C angle in degrees
 */
void Matrix44::SetOrientation(double a, double b, double c)
{
    double alpha = a * deg2rad;
    double beta = b * deg2rad;
    double gamma = c * deg2rad;

    double sa = sin(alpha);
    double ca = cos(alpha);
    double sb = sin(beta);
    double cb = cos(beta);
    double sg = sin(gamma);
    double cg = cos(gamma);

    m_data[0] = ca * cb;
    m_data[1] = ca * sb * sg - sa * cg;
    m_data[2] = ca * sb * cg + sa * sg;
    m_data[4] = sa * cb;
    m_data[5] = sa * sb * sg + ca * cg;
    m_data[6] = sa * sb * cg - ca * sg;
    m_data[8] = -sb;
    m_data[9] = cb * sg;
    m_data[10] = cb * cg;
}

/**
 * @brief Creates a GRPC matrix and copies the values
 * @return GRPC matrix
 */
robotcontrolapp::Matrix44 Matrix44::ToGrpc() const
{
    robotcontrolapp::Matrix44 result;
    for (double val : m_data) result.add_data(val);
    return result;
}

} // namespace DataTypes
} // namespace App
