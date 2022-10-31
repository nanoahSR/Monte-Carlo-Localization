import math
import InitializeMap
import Drive

global driveCommand, RobotPose

driveCommand = [
    # 右：90  左：-90
    #第一阶段
    [20, 0, 1],
    [20, 0, 1],
    [20, 0, 1],
    [20, 0, 1],
    # [20, 0, 3],
    [20, -30, 1],
    [20, -30, 1],
    [20, -30, 1],
    #第二阶段
    # [20, 0, 1],
    # [20, 0, 1],
    # [20, 0, 1],
    [20, 0, 1],
    # [20, 0, 4],
    [20, 30, 1],
    [20, 30, 1],
    [20, 30, 1],
    # [20, 0, 3],
    #第三阶段
    [20, 0, 1],
    [20, 0, 1],
    [20, 0, 1],
    [20, 0, 1],
    [20, 0, 1],
    [20, 0, 1],
    [20, 0, 1],
    [20, 0, 1],
    [20, 0, 1],
    [20, 0, 1],
    #第四阶段
    [20, 30, 1],
    [20, 30, 1],
    [20, 30, 1],
    [20, 0, 1],
    [20, 0, 1],
    [20, 0, 1],
    # [20, 0, 1],
    # [20, 0, 1],
    # [20, 0, 1],
    # [20, 0, 1],
    #第五阶段
    [20, -30, 1],
    [20, -30, 1],
    [20, -30, 1],
    [20, 0, 1],
    [20, 0, 1],
    [20, 0, 1],
    # [20, 0, 1],
    [20, 0, 1],
    [20, 0, 1],
    [20, 0, 1],
    #第六阶段
    [20, 30, 1],
    [20, 30, 1],
    [20, 30, 1],
    [20, 0, 1],
    [20, 0, 1],
    [20, 0, 1],
    #第七 掉头
    [0, -30, 1],
    [0, -30, 1],
    [0, -30, 1],
    [0, -30, 1],
    [0, -30, 1],
    [0, -30, 1],
    #第八
    [20, 0, 1],
    [20, 0, 1],
    [20, 0, 1],
    [20, 0, 1],
    [20, 0, 1],
    [20, 0, 1],
    [20, 0, 1],
    [20, 0, 1],
    [20, 0, 1],

    [20, 90, 1],
    [20, 0, 3],
    [20, 0, 4],
    [20, 90, 1],
    [20, 0, 4],
    [20, 0, 3],
    [20, 0, 3],
    [20, -90, 1],
    [20, 0, 3],
    [20, 0, 3],
    [20, 0, 3],
    [20, 0, 3],
    [20, 0, 3],
    [20, 0, 3],
    [20, 0, 3]
]

RobotPose = [[0] * 3 for i in range(len(driveCommand) + 1)]
RobotPose[0] = [50, 230, 0]


def MoveExact(i):
    global driveCommand, RobotPose

    if i == -1:

        return RobotPose[0][0], RobotPose[0][1], RobotPose[0][2]

    else:
        currentX = RobotPose[i][0]
        currentY = RobotPose[i][1]
        headRad = math.radians(RobotPose[i][2])
        if driveCommand[i][1] != 0:
            vOverOmegaRad = driveCommand[i][0] * 1.0 / math.radians(driveCommand[i][1])
            newX = currentX - vOverOmegaRad * math.sin(headRad) + vOverOmegaRad * math.sin(
                headRad + math.radians(driveCommand[i][1]) * driveCommand[i][2])
            newY = currentY + vOverOmegaRad * math.cos(headRad) - vOverOmegaRad * math.cos(
                headRad + math.radians(driveCommand[i][1]) * driveCommand[i][2])
            newThetaRad = headRad + math.radians(driveCommand[i][1]) * driveCommand[i][2]
        else:
            newThetaRad = headRad
            distanceTravel = driveCommand[i][0] * driveCommand[i][2]
            newX = currentX + distanceTravel * math.cos(headRad)
            newY = currentY + distanceTravel * math.sin(headRad)
        RobotPose[i + 1][0] = newX
        RobotPose[i + 1][1] = newY
        RobotPose[i + 1][2] = math.degrees(newThetaRad)
        print(newX, newY, newThetaRad)
        InitializeMap.DrawRobot(newX, newY, math.degrees(newThetaRad))

        return newX, newY, math.degrees(newThetaRad)
