#include "stdafx.h"
#include <iostream>
#include <ctime>
#include "Map.h"
#include "BeamModel.h"
#include "WeighingFactors.h"
#include "Points.h"
#include "Drive.h"
#include "Robot.h"

using namespace std;

int main(int argc, char** argv)
{
  srand((int)time(0));

  InitializeMap();
  InitializeMinsAndMaxs();
  
  RobotPose[0] = { 60, 50, 0 };
  DrawRobot (RobotPose[0].x, RobotPose[0].y);

  BeamModel (120, 3.0, 0.1, 5.0);  // (MaxRange, mV, LamdaShort, DeltaR)
  WeighingFactor (1.0, 0.1, 0.0, 0.1);  // (zHit, zShort, zMax, zRand)
  
  // 与Points同时更改
  int particleCount = 10000;  //  Specify the number of particles
  MonteCarloLocalization ( particleCount ); //  Initialize particles
  
  showUI();

  //  mainloop();
  Pose TruePose;
  double simulated_measurements[5];

  for ( ; loop<DCLen; loop++)
  {

    cout << "loop =  " << loop << endl;
    
    TruePose = MoveExact(loop); // Move Robot

    GetMeasurements(simulated_measurements, TruePose);  // Measuring distances of the robot from the 5 directions of the wall;
    update(simulated_measurements); // Update particles' position

    showUI();
   }
  
  return 0;
}