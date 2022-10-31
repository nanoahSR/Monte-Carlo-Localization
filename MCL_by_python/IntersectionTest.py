import math
import sys


def IntersectsAtDistanceDegree(rayOriginX, rayOriginY, heading, point1, point2):

    cosTheta = math.cos(math.radians(heading))
    sinTheta = math.sin(math.radians(heading))
    deltaX = point2[0] - point1[0]
    deltaY = point2[1] - point1[1]

    if math.fabs(deltaY * cosTheta - deltaX * sinTheta) < sys.float_info.epsilon:
        return -1
    else:
        s = (deltaY * (point1[0] - rayOriginX) - deltaX * (point1[1] - rayOriginY)) / (
            deltaY * cosTheta - deltaX * sinTheta)
        t = (sinTheta * (point1[0] - rayOriginX) - cosTheta * (point1[1] - rayOriginY)) / (
            deltaY * cosTheta - deltaX * sinTheta)
        if s < 0:
            return -1
        elif t < 0 or t > 1:
            return -1
        else:
            return s


def IntersectsDegree(rayOrigin1, rayOrigin2, heading, point1, point2):
    return IntersectsAtDistanceDegree(rayOrigin1, rayOrigin2, heading, point1, point2) >= 0
