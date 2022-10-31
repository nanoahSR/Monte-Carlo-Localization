import Drive
import Map
import BeamModel

SensorDirections = [-120, -60, 0, 60, 120]


def GetMeasurements(pose):
    measurements = [0, 0, 0, 0, 0, 0]
    for i in range(0, len(SensorDirections)):
        newHeadingDeg = pose[2] + SensorDirections[i]
        realDistanceToWall = Map.GetClosestWallDistance(pose[0], pose[1], newHeadingDeg)
        measurements[i] = BeamModel.GetSample(realDistanceToWall)
    return measurements
