import math
import datetime
import time
from AppClient import AppClient
from robotcontrolapp_pb2 import AppFunction, AppUIElement, KinematicState
from google.protobuf.internal import containers as protobufContainers


class MathToolsApp(AppClient):
    def __init__(self, appName: str, target: str):
        """Initializes the app. Pass the app name (as defined in rcapp.xml) and socket to connect to (default: "localhost:5000")"""
        AppClient.__init__(self, appName, target)
        self.__startTime = datetime.datetime.now()

    def _UiUpdateHandler(self, updates: protobufContainers.RepeatedCompositeFieldContainer[AppUIElement]):
        """Gets called on remote UI update requests received from the robot control"""
        return

    def _AppFunctionHandler(self, function: AppFunction):
        """Gets called on remote app function calls received from the robot control"""
        try:
            # Select the app function to call
            if function.name == "jointToCart":
                self.JointToCart(function)
            elif function.name == "cartToJoint":
                self.CartToJoint(function)
            elif function.name == "xyz_distance":
                self.XYZDistance(function)
            elif function.name == "is_near":
                self.IsNear(function)
            elif function.name == "sqrt":
                self.SquareRoot(function)
            elif function.name == "pow":
                self.Exponentiation(function)
            elif function.name == "min":
                self.Minimum(function)
            elif function.name == "max":
                self.Maximum(function)
            elif function.name == "copy_position":
                self.CopyPosition(function)
            elif function.name == "get_time_seconds":
                self.GetTimeSeconds(function)
            elif function.name == "get_time_minutes":
                self.GetTimeMinutes(function)
            elif function.name == "get_time_hours":
                self.GetTimeHours(function)
            elif function.name == "wait_by_variable":
                self.WaitByVariable(function)
            else:
                self.SendFunctionFailed(function.call_id, "unknown function")
        except Exception as ex:
            print(f"Function call failed: {ex}")
            self.SendFunctionFailed(function.call_id, str(ex))
            #raise # uncomment for debugging

    def GetNumber(self, statement: str) -> float:
        """Evaluates the statement for a number or scalar variable, returns the number or variable value. This allows entering both variables and numbers in text boxes."""

        if statement is None or len(statement) == 0:
            raise RuntimeError("no number or variable given")

        if statement[0].isnumeric():
            return float(statement)

        variable = self.GetNumberVariable(statement)
        return variable.GetValue()

    def GetParameter(self, function: AppFunction, parameterName: str, fieldType: str) -> AppFunction.Parameter:
        """Helper function to get the requested parameter from the parameter list"""
        for parameter in function.parameters:
            if parameter.name == parameterName:
                if parameter.HasField(fieldType + "_value"):
                    return parameter
                else:
                    raise RuntimeError("invalid parameter type '" + fieldType + "' for '" + parameterName + "'")
        raise RuntimeError("missing parameter '" + parameterName + "'")

    def JointToCart(self, function: AppFunction):
        """Translates the joint components of a variable to cartesian position"""
        # Get parameters
        sourceVariableName = self.GetParameter(function, "source_variable", "string").string_value
        targetVariableName = self.GetParameter(function, "target_variable", "string").string_value
        abortOnError = self.GetParameter(function, "abort_on_error", "bool").bool_value
        successGSig = self.GetParameter(function, "success_gsig", "int64").int64_value

        # Get variables
        sourceVariable = self.GetPositionVariable(sourceVariableName)

        # Translate position
        joints = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        for i in range(0, min(6, len(sourceVariable.GetRobotAxes()))):
            joints[i] = sourceVariable.GetRobotAxes()[i]
        for i in range(0, min(3, len(sourceVariable.GetExternalAxes()))):
            joints[6+i] = sourceVariable.GetExternalAxes()[i]
        (position, state) = self.TranslateJointToCart(joints)

        if state == KinematicState.KINEMATIC_NORMAL:
            self.SetGlobalSignal(successGSig, True)
            self.SetPositionVariableBoth(targetVariableName, position, joints[0], joints[1], joints[2], joints[3], joints[4], joints[5], joints[6], joints[7], joints[8])
        else:
            self.SetGlobalSignal(successGSig, False)
            if abortOnError:
                self.SendFunctionFailed(function.call_id, f"Joint-to-Cart translation failed: Kinematic error {state}")
                return
        self.SendFunctionDone(function.call_id)
    
    def CartToJoint(self, function: AppFunction):
        """Translates the cartesian components of a variable to joint positions"""
        # Get parameters
        sourceVariableName = self.GetParameter(function, "source_variable", "string").string_value
        targetVariableName = self.GetParameter(function, "target_variable", "string").string_value
        abortOnError = self.GetParameter(function, "abort_on_error", "bool").bool_value
        successGSig = self.GetParameter(function, "success_gsig", "int64").int64_value

        # Get variables
        sourceVariable = self.GetPositionVariable(sourceVariableName)

        # Translate position
        initialJoints = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        for i in range(0, min(6, len(sourceVariable.GetRobotAxes()))):
            initialJoints[i] = sourceVariable.GetRobotAxes()[i]
        for i in range(0, min(3, len(sourceVariable.GetExternalAxes()))):
            initialJoints[6+i] = sourceVariable.GetExternalAxes()[i]
        sourcePosition = sourceVariable.GetCartesian()
        (jointsResult, state) = self.TranslateCartToJoint(sourcePosition.GetX(), sourcePosition.GetY(), sourcePosition.GetZ(), sourcePosition.GetA(), sourcePosition.GetB(), sourcePosition.GetC(), initialJoints)

        if state == KinematicState.KINEMATIC_NORMAL:
            self.SetGlobalSignal(successGSig, True)
            self.SetPositionVariableBoth(targetVariableName, sourcePosition, jointsResult[0], jointsResult[1], jointsResult[2], jointsResult[3], jointsResult[4], jointsResult[5], jointsResult[6], jointsResult[7], jointsResult[8])
        else:
            self.SetGlobalSignal(successGSig, False)
            if abortOnError:
                self.SendFunctionFailed(function.call_id, f"Cart-to-Joint translation failed: Kinematic error {state}")
                return
        self.SendFunctionDone(function.call_id)
    
    def XYZDistance(self, function: AppFunction):
        """Calculates the cartesian distance"""
        # Get parameters
        posAVarName = self.GetParameter(function, "position_a", "string").string_value
        posBVarName = self.GetParameter(function, "position_b", "string").string_value
        posResultVarName = self.GetParameter(function, "target_variable", "string").string_value

        # Get variables
        posAVar = self.GetPositionVariable(posAVarName)
        posBVar = self.GetPositionVariable(posBVarName)

        dx = posAVar.GetCartesian().GetX() - posBVar.GetCartesian().GetX()
        dy = posAVar.GetCartesian().GetY() - posBVar.GetCartesian().GetY()
        dz = posAVar.GetCartesian().GetZ() - posBVar.GetCartesian().GetZ()

        dist = math.sqrt(dx*dx + dy*dy + dz*dz)
        self.SetNumberVariable(posResultVarName, dist)

        self.SendFunctionDone(function.call_id)

    def IsNear(self, function: AppFunction):
        """Sets a global signal depending on whether two positions are within a given distance"""
        # Get parameters
        posAVarName = self.GetParameter(function, "position_a", "string").string_value
        posBVarName = self.GetParameter(function, "position_b", "string").string_value
        distMaxStatement = self.GetParameter(function, "dist_max", "string").string_value
        successGSig = self.GetParameter(function, "success_gsig", "int64").int64_value

        # Get variables
        posAVar = self.GetPositionVariable(posAVarName)
        posBVar = self.GetPositionVariable(posBVarName)

        dx = posAVar.GetCartesian().GetX() - posBVar.GetCartesian().GetX()
        dy = posAVar.GetCartesian().GetY() - posBVar.GetCartesian().GetY()
        dz = posAVar.GetCartesian().GetZ() - posBVar.GetCartesian().GetZ()

        distMax = self.GetNumber(distMaxStatement)
        dist = math.sqrt(dx*dx + dy*dy + dz*dz)
        if dist <= distMax:
            self.SetGlobalSignal(successGSig, True)
        else:
            self.SetGlobalSignal(successGSig, False)
        
        self.SendFunctionDone(function.call_id)

    def SquareRoot(self, function: AppFunction):
        """Calculates the square root"""
        # Get parameters
        numberStatement = self.GetParameter(function, "number", "string").string_value
        resultVar = self.GetParameter(function, "result", "string").string_value

        # Get values
        number = self.GetNumber(numberStatement)
        result = math.sqrt(number)

        # Set result
        self.SetNumberVariable(resultVar, result)

        self.SendFunctionDone(function.call_id)

    def Exponentiation(self, function: AppFunction):
        """Calculates the exponentiation"""
        # Get parameters
        baseStatement = self.GetParameter(function, "base", "string").string_value
        expnentStatement = self.GetParameter(function, "exponent", "string").string_value
        resultVar = self.GetParameter(function, "result", "string").string_value

        # Get values
        base = self.GetNumber(baseStatement)
        exponent = self.GetNumber(expnentStatement)
        result = math.pow(base, exponent)

        # Set result
        self.SetNumberVariable(resultVar, result)

        self.SendFunctionDone(function.call_id)

    def Minimum(self, function: AppFunction):
        """Copies the minimum value to the result variable"""
        # Get parameters
        valueAStatement = self.GetParameter(function, "value_a", "string").string_value
        valueBStatement = self.GetParameter(function, "value_b", "string").string_value
        resultVar = self.GetParameter(function, "result", "string").string_value

        # Get values
        valueA = self.GetNumber(valueAStatement)
        valueB = self.GetNumber(valueBStatement)
        result = min(valueA, valueB)

        # Set result
        self.SetNumberVariable(resultVar, result)

        self.SendFunctionDone(function.call_id)

    def Maximum(self, function: AppFunction):
        """Copies the maximum value to the result variable"""
        # Get parameters
        valueAStatement = self.GetParameter(function, "value_a", "string").string_value
        valueBStatement = self.GetParameter(function, "value_b", "string").string_value
        resultVar = self.GetParameter(function, "result", "string").string_value

        # Get values
        valueA = self.GetNumber(valueAStatement)
        valueB = self.GetNumber(valueBStatement)
        result = max(valueA, valueB)

        # Set result
        self.SetNumberVariable(resultVar, result)

        self.SendFunctionDone(function.call_id)

    def CopyPosition(self, function: AppFunction):
        """Copies only the specified position components to the result variable"""
        # Get parameters
        fromVariableName = self.GetParameter(function, "from", "string").string_value
        toVariableName = self.GetParameter(function, "to", "string").string_value

        copyX = self.GetParameter(function, "copy_x", "bool").bool_value
        copyY = self.GetParameter(function, "copy_y", "bool").bool_value
        copyZ = self.GetParameter(function, "copy_z", "bool").bool_value
        copyA = self.GetParameter(function, "copy_a", "bool").bool_value
        copyB = self.GetParameter(function, "copy_b", "bool").bool_value
        copyC = self.GetParameter(function, "copy_c", "bool").bool_value
        copyA1 = self.GetParameter(function, "copy_a1", "bool").bool_value
        copyA2 = self.GetParameter(function, "copy_a2", "bool").bool_value
        copyA3 = self.GetParameter(function, "copy_a3", "bool").bool_value
        copyA4 = self.GetParameter(function, "copy_a4", "bool").bool_value
        copyA5 = self.GetParameter(function, "copy_a5", "bool").bool_value
        copyA6 = self.GetParameter(function, "copy_a6", "bool").bool_value
        copyE1 = self.GetParameter(function, "copy_e1", "bool").bool_value
        copyE2 = self.GetParameter(function, "copy_e2", "bool").bool_value
        copyE3 = self.GetParameter(function, "copy_e3", "bool").bool_value

        # Get variables
        fromVariable = self.GetPositionVariable(fromVariableName)
        toVariable = self.GetPositionVariable(toVariableName)

        # Copy values
        targetMat = toVariable.GetCartesian()
        a = targetMat.GetA()
        b = targetMat.GetB()
        c = targetMat.GetC()
        a1 = toVariable.GetRobotAxes()[0]
        a2 = toVariable.GetRobotAxes()[1]
        a3 = toVariable.GetRobotAxes()[2]
        a4 = toVariable.GetRobotAxes()[3]
        a5 = toVariable.GetRobotAxes()[4]
        a6 = toVariable.GetRobotAxes()[5]
        e1 = toVariable.GetExternalAxes()[0]
        e2 = toVariable.GetExternalAxes()[1]
        e3 = toVariable.GetExternalAxes()[2]

        if copyX:
            targetMat.SetX(fromVariable.GetCartesian().GetX())
        if copyY:
            targetMat.SetY(fromVariable.GetCartesian().GetY())
        if copyZ:
            targetMat.SetZ(fromVariable.GetCartesian().GetZ())
        if copyA:
            a = fromVariable.GetCartesian().GetA()
        if copyB:
            b = fromVariable.GetCartesian().GetB()
        if copyC:
            c = fromVariable.GetCartesian().GetC()
        targetMat.SetOrientation(a,b,c)

        if copyA1:
            a1 = fromVariable.GetRobotAxes()[0]
        if copyA2:
            a2 = fromVariable.GetRobotAxes()[1]
        if copyA3:
            a3 = fromVariable.GetRobotAxes()[2]
        if copyA4:
            a4 = fromVariable.GetRobotAxes()[3]
        if copyA5:
            a5 = fromVariable.GetRobotAxes()[4]
        if copyA6:
            a6 = fromVariable.GetRobotAxes()[5]
        if copyE1:
            e1 = fromVariable.GetExternalAxes()[0]
        if copyE2:
            e2 = fromVariable.GetExternalAxes()[1]
        if copyE3:
            e3 = fromVariable.GetExternalAxes()[2]
        
        self.SetPositionVariableBoth(toVariableName, targetMat, a1,a2,a3,a4,a5,a6,e1,e2,e3)

        self.SendFunctionDone(function.call_id)

    def GetTimeSeconds(self, function: AppFunction):
        """Gets a steadily counting time value"""
        seconds = (datetime.datetime.now() - self.__startTime).total_seconds()
        self.SetNumberVariable(self.GetParameter(function, "target", "string").string_value, seconds)
        self.SendFunctionDone(function.call_id)
        
    def GetTimeMinutes(self, function: AppFunction):
        """Gets a steadily counting time value"""
        seconds = (datetime.datetime.now() - self.__startTime).total_seconds()
        self.SetNumberVariable(self.GetParameter(function, "target", "string").string_value, seconds / 60)
        self.SendFunctionDone(function.call_id)

    def GetTimeHours(self, function: AppFunction):
        """Gets a steadily counting time value"""
        seconds = (datetime.datetime.now() - self.__startTime).total_seconds()
        self.SetNumberVariable(self.GetParameter(function, "target", "string").string_value, seconds / (60 * 60))
        self.SendFunctionDone(function.call_id)

    def WaitByVariable(self, function: AppFunction):
        """Gets a steadily counting time value"""
        durationSeconds = self.GetNumberVariable(self.GetParameter(function, "duration", "string").string_value).GetValue()
        time.sleep(durationSeconds)
        self.SendFunctionDone(function.call_id)
