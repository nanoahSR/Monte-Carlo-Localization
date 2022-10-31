#include "stdafx.h"
#include <cmath>
#include "VelocityModel.h"
#include "BeamModel.h"
#include "Points.h"
#include "SamlperNormal.h"
#include "Drive.h"

double A[6] = { 0.01, 0.001, 0.001, 0.01, 0.01, 0.01 };

Pose Sample(Pose particle)
{
  /// Algorithm sample_motion_model_velocity(ut, x(t-1))
  /// Probabilistic Robotics P93
  
    double velocity = DriveCommand[loop].v;
    double omegaRad = ang2rad(DriveCommand[loop].omega);
    double DeltaTime = DriveCommand[loop].time;

    double headRad = particle.rad();

    double vSquared = velocity * velocity;
    double omegaRadSquared = omegaRad * omegaRad;

    double vVariance = A[0] * vSquared + A[1] * omegaRadSquared;
    double vNoisy = velocity + Sampler(vVariance);

    double omegaVariance = A[2] * vSquared + A[3] * omegaRadSquared;
    double omegaRadNoisy = omegaRad + Sampler(omegaVariance);

    double gammaVariance = A[4] * vSquared + A[5] * omegaRadSquared;
    double gammaNoisy = Sampler(gammaVariance);

    double vOverOmegaNoisy = vNoisy * 1.0 / omegaRadNoisy;
    
    Pose newPose = {0,0,0};

    newPose.x = particle.x - vOverOmegaNoisy * sin(headRad) 
                  +  vOverOmegaNoisy * sin(headRad + omegaRadNoisy * DeltaTime);

    newPose.y = particle.y + vOverOmegaNoisy * cos(headRad) 
                  - vOverOmegaNoisy * cos(headRad + omegaRadNoisy * DeltaTime);

    double newThetaRad = headRad + omegaRadNoisy * DeltaTime + gammaNoisy * DeltaTime;

    newPose.theta = rad2ang(newThetaRad);
    
    return newPose;
}

    
Pose poseSample(Pose currentPose)
{
    if (loop == -1)
        return currentPose;
    else
        return Sample(currentPose);
}