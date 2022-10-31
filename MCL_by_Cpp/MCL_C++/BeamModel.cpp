#include "stdafx.h"
#include <iostream>
#include <cmath>
#include <ctime>
//#include <windows.system.h>
#include "BeamModel.h"
#include "CommonFunctions.h"
#include "Points.h"
#include "WeighingFactors.h"
using namespace std;

class MeasurementVariance{
private: 
  double x; 
public:  
  double getX()
  {
    return x;
  }
  	
  void setX(double value) 
  {
    x = value;
  }    
}MV;

class MeasurementSigma{
private: 
  double x; 
public:  
  double getX()
  {
    return x;
  }
  	
  void setX(double value) 
  {
    x = value;
  }    
}MS;

int MaxRange = 0;
double LambdaShort = 0;
double ZHit = 0, ZShort = 0, ZRand = 0, ZMax = 0;

void BeamModel(int maxRange, double measurementVariance, double lambdaShort, double deltar)
{
  /// Initial Beam_model parameter
  
  MaxRange = maxRange;
  MV.setX(measurementVariance);
  MS.setX(sqrt(MV.getX()));
  LambdaShort = lambdaShort;
  DeltaR = deltar;
}


double generateGaussianNoise(double mu, double sigma)
{
  /// Gaussian distribution
  
  //srand((unsigned int)time(0));
  while(1)
  {
    double u1 = double(rand() % 1000) / 1000, u2 = double(rand() % 1000) / 1000, r;
    static unsigned int seed = 0;
    r = mu + sqrt ( sigma)*sqrt(-2.0*(log(u1) / log(exp(1.0))))*cos(2 * p_PI * u2);
    if (!isinf(r) && !isnan(r))
    {
      return r;
    }
  }
};

double randomExponential(double lambda)
{
  /// Exponential distribution
  
    double pV = 0.0;
    while(true)
    {
        pV = (double)rand()/(double)RAND_MAX;
        if (pV != 1)
        {
            break;
        }
    }
    pV = (-1.0/lambda)*log(1-pV);
    return pV;
}

double GenerateRandom()
{
  //srand((unsigned int)time(0));
	
  return ((double)rand())/RAND_MAX;
}


double SamplePHit(double realDistance)
{
  /// Sample P hit
 
  double measurementSample;
  do
  {
    measurementSample = generateGaussianNoise(realDistance, MS.getX());
  }while (measurementSample > MaxRange || measurementSample < 0);
  
  return measurementSample;
}

double SamplePShort(double realDistance)
{
  /// Sample P short
  
  double measurementSample;
  do
  {
    measurementSample = randomExponential(LambdaShort);
  }while(measurementSample > realDistance);
  
  return measurementSample;
}

double SamplePRandom()
{
  /// Sample P rand
  
  return GenerateRandom() * MaxRange;
}

double GetSample(double realDistance)
{
    double effectiveDistance =  (realDistance > MaxRange) ? MaxRange : realDistance;
    if (realDistance > MaxRange)
        return MaxRange;
    
    
    /// Creates a distance measurement sample under the assumption that the real distance
    /// is the provided distance value.
    /// 
    /// A distance measurement sample.
    
    /// First we figure out what probability distribution to use
    
    
    double Random = GenerateRandom();  // Generate random number from 0 to 1

    if (Random <= ZHitRaw)
        return SamplePHit(effectiveDistance);
    else if (Random <= ZHitRaw + ZShort)
        return SamplePShort(effectiveDistance);
    else if (Random <= ZHitRaw + ZShort + ZMax)
        return MaxRange;
    else
        return SamplePRandom();
}


double GetPHit(double measuredDistance, double realDistance, double deltaR)
{
    if (realDistance > MaxRange)
        return 1 - DistributionFunction(MaxRange, MaxRange, MV.getX());
    else
    {
		double lower = DistributionFunction((measuredDistance - deltaR), realDistance, MV.getX());
		double upper = DistributionFunction((measuredDistance + deltaR), realDistance, MV.getX());
		return upper - lower;
    }
}

double GetPShort(double measuredDistance, double realDistance, double deltaR)
{
    if (measuredDistance > realDistance)
        return 0.0;
    else
    {
        double lower = 1 - exp(-LambdaShort * (measuredDistance - deltaR));
        double upper = 1 - exp(-LambdaShort * (measuredDistance + deltaR));
        return upper - lower;
    }
}

double GetPMax(double measuredDistance, double deltaR)
{
    if (fabs(MaxRange - measuredDistance < deltaR))
        return 1.0 / deltaR;
    else
        return 0.0;
}

double GetPRandom(double measuredDistance, double deltaR)
{
    if (measuredDistance > MaxRange)
        return 0.0;
    else
        return deltaR / MaxRange;
}


double Getprobability(double robotToWall, double particleToWall, double deltaR)
{
  /// Algorithm beam_range_finder_model(zt, xt, m)
  /// Probabilistic Robotics P119 

    if (particleToWall > MaxRange)
        particleToWall = MaxRange;
    
    // 1.0 0.1 0.0 0.1
    double probability = ZHit * GetPHit(robotToWall, particleToWall, deltaR) 
                         + ZShort * GetPShort(robotToWall, particleToWall, deltaR) 
			 + ZMax * GetPMax(robotToWall, deltaR) 
		         + ZRand * GetPRandom(robotToWall, deltaR);

    return probability;
}