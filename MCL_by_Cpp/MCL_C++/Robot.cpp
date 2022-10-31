#include "stdafx.h"
#include <iostream>
#include "Robot.h"
#include "Map.h"
#include "BeamModel.h"
#include "Points.h"

int Sensor[5] = {-120, -60, 0, 60, 120};
int SenLen = sizeof(Sensor)/sizeof(int);

void* GetMeasurements(double *measurement, Pose nextPose)
{
    //double measurements[5] = {0, 0, 0, 0, 0, 0};
    double realDistanceToWall;
    for (int i=0; i<SenLen; i++)
    {
        double ThetaAddSensor =nextPose.theta + Sensor[i];
        realDistanceToWall = GetClosestWallDistance(nextPose.x, nextPose.y, ThetaAddSensor);
        measurement[i] = GetSample(realDistanceToWall);
    }
	return 0;
}

