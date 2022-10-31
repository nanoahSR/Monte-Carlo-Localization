#include "stdafx.h"
#include <iostream>
#include <cmath>
#include "Drive.h"
#include "Points.h"
#include "Map.h"


Move DriveCommand[25] = {
  { 5,0,1 },
  { 5,0,1 },
  { 5,0,1 },
  { 5,10,1 },
  { 5,10,1 },
  { 5,10,1 },
  { 5,10,1 },
  { 5,10,1 },
  { 5,10,1 },
  { 5,10,1 },
  { 5,10,1 },
  { 5,10,1 },
  //{ 5,30,1 },
  //{ 5,30,1 },
  { 5,0,1 },
  { 5,-30,1 },
  { 5,-30,1 },
  { 5,-30,1 },
  { 5,0,1 },
  { 5,0,1 },
  { 5,0,1 },
  { 5,0,1 },
  { 5,0,1 },
  { 5,0,1 },
  { 5,0,1 },
  { 5,0,1 },
  { 5,0,1 },
};

int loop = -1;

int DCLen = sizeof(DriveCommand)/sizeof(Move);

Pose RobotPose[30] = { 0 };



/*************************************************
// Method: MoveExact
// Description: Move Robot
// Author: RSN
// Date: 2019/05/19
// Returns: Pose (Position after move)
// Parameter: step 
// History: 
*************************************************/
Pose MoveExact(int step)
{
  Pose newRP; // new Robot Position
  
  if (step == -1)
  {
    newRP.x = RobotPose[0].x;
    newRP.y = RobotPose[0].y;
	newRP.theta = RobotPose[0].theta;
    return newRP;
  }
  else
  {
    double currentX = RobotPose[step].x;
    double currentY = RobotPose[step].y;
	double newThetaRad = ang2rad(RobotPose[step].theta);
    
    if (DriveCommand[step].omega != 0)
    {
      double vOverOmegaRad = DriveCommand[step].v * 1.0 / ang2rad(DriveCommand[step].omega);
      newRP.x = currentX - vOverOmegaRad * sin(newThetaRad) 
                  + vOverOmegaRad * sin(newThetaRad + ang2rad(DriveCommand[step].omega) * DriveCommand[step].time);
      newRP.y = currentY + vOverOmegaRad * cos(newThetaRad) 
                  - vOverOmegaRad * cos(newThetaRad + ang2rad(DriveCommand[step].omega) * DriveCommand[step].time);
	  newThetaRad = newThetaRad + ang2rad(DriveCommand[step].omega) * DriveCommand[step].time;
    }
    else
    {
      double distanceTravel = DriveCommand[step].v * DriveCommand[step].time;
      newRP.x = currentX + distanceTravel * cos(newThetaRad);
      newRP.y = currentY + distanceTravel * sin(newThetaRad);
    }

    RobotPose[step+1].x = newRP.x;
    RobotPose[step+1].y = newRP.y;
    RobotPose[step+1].theta = rad2ang(newThetaRad);
    DrawRobot(newRP.x, newRP.y);
    
    newRP.theta=rad2ang(newThetaRad);
    return newRP;
   }
}
