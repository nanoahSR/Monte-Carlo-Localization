import Points
import IntersectionTest

# Xmin = 50
# Xmax = 750
# Ymin = 50
# Ymax = 500
global XMax, XMin, YMax, YMin

XMax, XMin, YMax, YMin = 0,0,0,0
MaxValue = 2000
MinValue = 0
# MapPoints = [[0][0] * 2 for i in range(4)]
# MapPoints = [
#     [Xmin, Ymin], [Xmax, Ymin], [Xmax, Ymax], [Xmin, Ymin]]
MapPoints = [
    [100, 30],
    [400, 30],
    [700, 30],
    # [600, 145],
    # [700, 145],
    [700, 530],
    [600, 530],
    [600, 330],
    [400, 330],
    [400, 200],
    [200, 200],
    [200, 270],
    [30, 270],
    [30, 150],
    [100, 150],
]


def InitializeMinsAndMaxs():
    global closestDistance, XMax, XMin, YMax, YMin
    XMin = MaxValue
    XMax = MinValue
    YMin = MaxValue
    YMax = MinValue

    for i in range(len(MapPoints)):
        if MapPoints[i][0] < XMin:
            XMin = MapPoints[i][0]
        if MapPoints[i][0] > XMax:
            XMax = MapPoints[i][0]
        if MapPoints[i][1] < YMin:
            YMin = MapPoints[i][1]
        if MapPoints[i][1] > YMax:
            YMax = MapPoints[i][1]
        # closestDistance = (XMax - XMin) if (XMax - XMin) > (YMax - YMin) else (YMax - YMin)


def GetClosestWallDistance(rayOriginX, rayOriginY, headDeg):
    """x,y,degree"""
    closestDistance = 2000

    for i in range(len(MapPoints)):
        point1 = MapPoints[i]
        point2 = MapPoints[(i + 1) % len(MapPoints)]

        distance = IntersectionTest.IntersectsAtDistanceDegree(rayOriginX, rayOriginY, headDeg, point1, point2)

        if distance < 0:
            continue
        if distance < closestDistance:
            closestDistance = distance
    return closestDistance
