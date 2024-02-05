#pragma once

#include <string>

#include "Matrix44.h"

namespace App
{
namespace DataTypes
{

/**
 * @brief Program variable base type
 */
class ProgramVariable
{
public:
    /**
     * @brief Constructor
     * @param name variable name
     */
    ProgramVariable(const std::string& name) : m_name(name) {}
    /**
     * @brief Destructor
     * Note: this only exists since we need at least one virtual method for dynamic polymorphism
     */
    virtual ~ProgramVariable() = default;

    /**
     * @brief Gets the variable name
     * @return variable name
     */
    const std::string& GetName() const { return m_name; }
    /**
     * @brief Sets the variable name
     * @param name variable name
     */
    void SetName(const std::string& name) { m_name = name; }

private:
    /// Variable name
    std::string m_name;
};

/**
 * @brief Number variable
 */
class NumberVariable : public ProgramVariable
{
public:
    /**
     * @brief Constructor
     * @param name variable name
     * @param value variable value
     */
    NumberVariable(const std::string& name, double value = 0) : ProgramVariable(name), m_value(value) {}

    /**
     * @brief Gets the variable value
     * @return variable value
     */
    double GetValue() const { return m_value; }
    /**
     * @brief Sets the variable value
     * @param value variable value
     */
    void SetValue(double value) { m_value = value; }

private:
    /// Variable value
    double m_value;
};

/**
 * @brief Position variable
 */
class PositionVariable : public ProgramVariable
{
public:
    // Max number of robot axes
    static constexpr size_t ROBOT_AXES_COUNT = 6;
    // Max number of external axes
    static constexpr size_t EXTERNAL_AXES_COUNT = 3;

    /**
     * @brief Constructor for a cartesian position, joints are set to 0
     * @param name variable name
     * @param cartesian cartesian position and orientation
     * @param externalAxes external axes
     */
    PositionVariable(const std::string& name, const Matrix44 cartesian, const std::array<double, EXTERNAL_AXES_COUNT>& externalAxes)
        : ProgramVariable(name), m_cartesian(cartesian), m_externalAxes(externalAxes)
    {
        m_robotAxes.fill(0);
    }

    /**
     * @brief Constructor for a joint position, cartesian is set to 0
     * @param name variable name
     * @param robotAxes robot axes
     * @param externalAxes external axes
     */
    PositionVariable(const std::string& name, const std::array<double, ROBOT_AXES_COUNT>& robotAxes,
                     const std::array<double, EXTERNAL_AXES_COUNT>& externalAxes)
        : ProgramVariable(name), m_robotAxes(robotAxes), m_externalAxes(externalAxes)
    {}

    /**
     * @brief Constructor for both joint and cartesian position
     * @param name variable name
     * @param cartesian cartesian position and orientation
     * @param robotAxes robot axes
     * @param externalAxes external axes
     */
    PositionVariable(const std::string& name, const Matrix44 cartesian, const std::array<double, ROBOT_AXES_COUNT>& robotAxes,
                     const std::array<double, EXTERNAL_AXES_COUNT>& externalAxes)
        : ProgramVariable(name), m_cartesian(cartesian), m_robotAxes(robotAxes), m_externalAxes(externalAxes)
    {}

    /**
     * @brief Gets the robot axes
     * @return array of robot axes
     */
    const std::array<double, ROBOT_AXES_COUNT>& GetRobotAxes() const { return m_robotAxes; }
    /**
     * @brief Gets the external axes
     * @return array of external axes
     */
    const std::array<double, EXTERNAL_AXES_COUNT>& GetExternalAxes() const { return m_externalAxes; }
    /**
     * @brief Gets the cartesian position and orientation
     * @return cartesian transformation matrix
     */
    const Matrix44& GetCartesian() const { return m_cartesian; }

    /**
     * @brief Sets the robot axes
     * @param axes robot axes array
     */
    void SetRobotAxes(const std::array<double, ROBOT_AXES_COUNT>& axes) { m_robotAxes = axes; }
    /**
     * @brief Sets the external axes
     * @param axes external axes array
     */
    void SetExternalAxes(std::array<double, EXTERNAL_AXES_COUNT>& axes) { m_externalAxes = axes; }
    /**
     * @brief Sets the cartesian position and orientation
     * @param cartesian cartesian transformation matrix
     */
    void SetCartesian(Matrix44 cartesian) { m_cartesian = cartesian; }

private:
    /// Robot axes
    std::array<double, ROBOT_AXES_COUNT> m_robotAxes;
    /// External axes
    std::array<double, EXTERNAL_AXES_COUNT> m_externalAxes;
    /// Cartesian transformation matrix
    Matrix44 m_cartesian;
};

} // namespace DataTypes
} // namespace App
