#pragma once

#include <robotcontrolapp.grpc.pb.h>

#include <array>

namespace App
{
namespace DataTypes
{

/**
 * @brief A 4x4 matrix for cartesian positions and transformations. Values are to be interpreted as mm for positions and degrees for angles.
 */
class Matrix44
{
public:
    /**
     * @brief Constructor, initializes a 4x4 unit matrix
     */
    Matrix44();
    /**
     * @brief Constructor, copies values from GRPC matrix
     * @param other
     */
    Matrix44(const robotcontrolapp::Matrix44& other);

    /**
     * @brief Element access operator
     * @param row row number (0 - 3), throws exception of out of range
     * @param column column number (0 - 3), throws exception of out of range
     * @return matrix element value
     */
    double& operator()(int row, int column);
    /**
     * @brief Element access operator
     * @param row row number (0 - 3), throws exception of out of range
     * @param column column number (0 - 3), throws exception of out of range
     * @return matrix element value
     */
    double operator()(int row, int column) const;

    /**
     * @brief Element access operator
     * @param idx element index
     * @return matrix element value
     */
    double& operator[](size_t idx) { return m_data.at(idx); }
    /**
     * @brief Element access operator
     * @param idx element index
     * @return matrix element value
     */
    double operator[](size_t idx) const { return m_data.at(idx); };

    /**
     * @brief Gets the X position
     * @return X position value in mm
     */
    double GetX() const { return m_data[3]; }
    /**
     * @brief Gets the Y position
     * @return Y position value in mm
     */
    double GetY() const { return m_data[7]; }
    /**
     * @brief Gets the Z position
     * @return Z position value in mm
     */
    double GetZ() const { return m_data[11]; }
    /**
     * @brief Gets the A orientation
     * @return A orientation value in degrees
     */
    double GetA() const;
    /**
     * @brief Gets the B orientation
     * @return B orientation value in degrees
     */
    double GetB() const;
    /**
     * @brief Gets the Corientation
     * @return C orientation value in degrees
     */
    double GetC() const;
    /**
     * @brief Adds the given values to the position values
     * @param x X position in mm
     * @param y Y position in mm
     * @param z Z position in mm
     */
    void Translate(double x, double y, double z);

    /**
     * @brief Sets the X position
     * @param x new X position in mm
     */
    void SetX(double x) { m_data[3] = x; }
    /**
     * @brief Sets the Y position
     * @param y new Y position in mm
     */
    void SetY(double y) { m_data[7] = y; }
    /**
     * @brief Sets the Z position
     * @param z new Z position in mm
     */
    void SetZ(double z) { m_data[11] = z; }
    /**
     * @brief Sets the A orientation
     * @param a A angle in degrees
     */
    void SetA(double a);
    /**
     * @brief Sets the B orientation
     * @param b B angle in degrees
     */
    void SetB(double b);
    /**
     * @brief Sets the C orientation
     * @param c C angle in degrees
     */
    void SetC(double c);
    /**
     * @brief Gets the orientation
     * @param a A angle in degrees
     * @param b B angle in degrees
     * @param c C angle in degrees
     */
    void GetOrientation(double& a, double& b, double& c) const;
    /**
     * @brief Sets the orientation
     * @param a A angle in degrees
     * @param b B angle in degrees
     * @param c C angle in degrees
     */
    void SetOrientation(double a, double b, double c);

    /**
     * @brief Creates a GRPC matrix and copies the values
     * @return GRPC matrix
     */
    robotcontrolapp::Matrix44 ToGrpc() const;

private:
    // Contains the matrix data
    std::array<double, 16> m_data;
};

} // namespace DataTypes
} // namespace App
