import ButtonCommand
import SamplerNormal
import InitializeMap
import Points
import Drive
import math

A = [0.001, 0.001, 0.001, 0.001, 0.001, 0.001]


def Sample(particle, driveCommand):
    velocity = driveCommand[0]
    omegaRad = math.radians(driveCommand[1])
    deltat = driveCommand[2]

    headRad = math.radians(particle[2])

    vSquared = velocity * velocity
    omegaRadSquared = omegaRad * omegaRad

    vVariance = A[0] * vSquared + A[1] * omegaRadSquared
    vNoisy = velocity + SamplerNormal.Sampler(vVariance)

    omegaVariance = A[2] * vSquared + A[3] * omegaRadSquared
    omegaRadNoisy = omegaRad + SamplerNormal.Sampler(omegaVariance)

    gammaVariance = A[4] * vSquared + A[5] * omegaRadSquared
    gammaNoisy = SamplerNormal.Sampler(gammaVariance)

    vOverOmegaNoisy = vNoisy * 1.0 / omegaRadNoisy

    newX = particle[0] - vOverOmegaNoisy * math.sin(headRad) + \
               vOverOmegaNoisy * math.sin(headRad + omegaRadNoisy * deltat)

    newY = particle[1] + vOverOmegaNoisy * math.cos(headRad) - \
               vOverOmegaNoisy * math.cos(headRad + omegaRadNoisy * deltat)

    newThetaRad = headRad + omegaRadNoisy * deltat + gammaNoisy * deltat

    return newX, newY, math.degrees(newThetaRad) % 360.0


def poseSample(currentPose, step):
    if step == -1:
        return currentPose
    else:
        return Sample(currentPose, Drive.driveCommand[step])
