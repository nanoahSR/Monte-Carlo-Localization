#include "stdafx.h"
#include <iostream>
#include "stdlib.h"
#include <cmath>
#include <ctime>
#include "string.h"
#include "Points.h"
#include "BeamModel.h"
#include "CommonFunctions.h"
#include "Drive.h"
#include "Map.h"
#include "Robot.h"
#include "VelocityModel.h"
using namespace std;

#define random(x) (rand()%x)

int ParticlesCount = 0;
double DeltaR = 0;
double m_AggregatedWeights[10000] = {0};
Pose m_TempNewParticles[10000] = {0};
Pose Particles[10000] = {0};

//Pose::Pose(double x, double y, double theta): x(x), y(y), theta(theta) {};

void Pose::printX()
{
    cout << "x = " << x << endl;
    cout << "y = " << y << endl;
    cout << "theta = " << theta << endl;
};

double Pose::rad()
{
  double temp = theta;
  double flag = (theta < 0) ? -1.0 : 1.0;  //  Judgement the positive or negative
  if (theta < 0)
    temp = theta * (-1.0);
  
  return   flag * (temp * p_PI) / 180;
};

// double Pose::ang(double angle)
// {
//   
//   double flag = (angle < 0) ? -1.0 : 1.0;  //  Judgement the positive or negative
//   if (angle < 0)
//     angle = angle * (-1.0);
//   
//   return flag * (angle * p_PI) / 180;
// 
// };


double rad2ang(double rad)
{
  double flag = (rad < 0) ? -1.0 : 1.0;  //  Judgment the positive or negative
  if (rad < 0)
    rad = rad * (-1.0);
  
  return flag * (rad * 180) / p_PI;
}

double ang2rad(double angle)
{
  double flag = (angle < 0) ? -1.0 : 1.0;  //  Judgment the positive or negative
  if (angle < 0)
    angle = angle * (-1.0);
  
 return flag * (angle * p_PI) / 180;
}



Pose CreateRandomPose()
{
  // srand((int)time(0));
  Pose CRPose = { 0 };
  CRPose.theta= random(1000)%360;
  do
  {
	  CRPose.x = XMin + GenerateRandom()*(XMax - XMin);
	  CRPose.y = YMin + GenerateRandom()*(YMax - YMin);
  } while (!IsInside(CRPose.x, CRPose.y));
  
  return CRPose;
}

void InitializeParticles()
{
  for (int i=0; i<ParticlesCount; i++)
  {
    Particles[i] = CreateRandomPose();
    InitParicle(Particles[i].x, Particles[i].y);
  }
}

void MonteCarloLocalization(int particleCount)
{
  ///  Initial parameter
  
  ParticlesCount = particleCount;
  //DeltaR = 3.0;
  
  InitializeParticles();
}


double CalculateWeight(Pose pose, double measurements[5])
{
    ///  pose:x,y,degree
  
    double weight = 1.00;
    double headAng, distanceToWall, Probability;
    for (int i=0; i<SenLen;i++)
    {
      headAng = pose.theta + Sensor[i];
      distanceToWall = GetClosestWallDistance(pose.x, pose.y, headAng);

	  weight *= Getprobability(measurements[i], distanceToWall, DeltaR);
      
    }
    return weight;
}


Pose DrawParticle(double random)
{
	// binary search for the index; see http://www.dreamincode.net/code/snippet1835.htm
	// 二进制搜索索引
	int lowIndex = 0;
	int highIndex = ParticlesCount;

	// loop while the low index is less or equal to the high index
	// 当低指数小于或等于高指数时循环
	while (lowIndex <= highIndex)
	{
		//get the middle point in the array
		int midNum = (lowIndex + highIndex) / 2;

		double rangeLower = midNum - 1 < 0 ? 0 : m_AggregatedWeights[midNum - 1];
		double rangeUpper = m_AggregatedWeights[midNum];

		//now start checking the values
		if (random < rangeLower)
		{
			//search value is lower than this index of our array
			//so set the high number equal to the middle number - 1
			highIndex = midNum - 1;
		}
		else if (random >= rangeUpper)
		{
			//search value is higher than this index of our array
			//so set the low number to the middle number + 1
			lowIndex = midNum + 1;
		}
		else if (random >= rangeLower && random < rangeUpper)
		{
			//we found a match
			//Debug.WriteLine(rangeLower + " - " + rangeUpper + ": " + random);
			return Particles[midNum];
		}
	}
	cout << "Program error" << endl;
    return ;
}


void DrawParticles(double sumOfWeights)
{
  /// Redistribute particles
  
  Pose m_swap[10000] = {0};
  double Random;
  for(int i=0; i<ParticlesCount; i++)
  {
        Random = GenerateRandom() * sumOfWeights;
        //DrawParticle(Random)
        m_TempNewParticles[i] = DrawParticle(Random);
        //InitializeMap.DrawPoints(m_TempNewParticles[i][0], m_TempNewParticles[i][1], m_TempNewParticles[i][2]);    
  }
  memcpy(m_swap, Particles, sizeof(Particles));
  memcpy(Particles, m_TempNewParticles, sizeof(Particles));
  memcpy(m_TempNewParticles, m_swap, sizeof(m_AggregatedWeights));
}

void update(double measurements[5])
{
  /* Calculate each particle weight, 
     calculate the weight accumulation sum, 
      and update the particle distribution. */

  double weights_sum = 0;
  Pose MovedParticle = { 0, 0, 0 };  // x, y, angle
  Pose OriParticle = { 0, 0, 0 };  // x, y, angle
    
  for (int i=0; i<ParticlesCount; i++)
  {
	  //cout << i << endl;
	  if (i == 500)
		  i = i;
    OriParticle = Particles[i];
    MovedParticle = poseSample(OriParticle);
      
    while (!IsInside(MovedParticle.x, MovedParticle.y))
    {
      OriParticle = CreateRandomPose();
      MovedParticle = poseSample(OriParticle);
    }

    double weight = CalculateWeight(MovedParticle, measurements);

    weights_sum = weights_sum + weight;
    m_AggregatedWeights[i] = weights_sum;
      
    Particles[i] = MovedParticle; // 
  }
    
  DrawParticles(weights_sum);
}