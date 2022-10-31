from __future__ import print_function
import BeamModel
import ButtonCommand
import InitializeMap
import VelocityModel
import Map
import Robot
import math
import random

global ParticleCount, DeltaR, DeltaTheta, Particles, m_AggregatedWeights, m_TempNewParticles


def IsInside(x, y):
    isIn = False
    for i in range(len(Map.MapPoints)):
        j = (i + len(Map.MapPoints) - 1) % len(Map.MapPoints)
        if ((Map.MapPoints[i][1] > y) != (Map.MapPoints[j][1] > y)) and (
                x < (Map.MapPoints[j][0] - Map.MapPoints[i][0]) * (y - Map.MapPoints[i][1]) * 1.0 / (
                Map.MapPoints[j][1] - Map.MapPoints[i][1]) + Map.MapPoints[i][0]):
            isIn = not isIn
    return isIn


def CreateRandomPose():
    head = random.random() * (random.randint(0, 360))
    while (1):
        x = Map.XMin + random.random() * (Map.XMax - Map.XMin)
        y = Map.YMin + random.random() * (Map.YMax - Map.YMin)
        if IsInside(x, y):
            break
    return x, y, head


def InitializeParticles():
    global ParticleCount, Particles
    for i in range(ParticleCount):
        Particles[i] = CreateRandomPose()

        # if IsInside(Particles[i][0], Particles[i][1]):
        InitializeMap.InitPoints(i, Particles[i][0], Particles[i][1])
        # else:
        #     Particles[i] = CreateRandomPose()


def CalculateWeight(pose, measurements):
    """pose:x,y,degree"""
    weight = 1.00
    for i in range(0, 5):
        headDeg = pose[2] + Robot.SensorDirections[i]

        distance_to_wall = Map.GetClosestWallDistance(pose[0], pose[1], headDeg)

        Probability = BeamModel.Getprobability(measurements[i], distance_to_wall, DeltaR)
        weight = weight * Probability

    return weight


def DrawParticle(Random):
    global ParticleCount, Particles, m_AggregatedWeights
    # print('Points.61.Random = %d' % Random)
    low_index = 0
    high_index = ParticleCount - 1

    while low_index <= high_index:

        mid_num = int((low_index + high_index) / 2)
        # print('Points.61.mid_num = %d' % mid_num)

        range_lower = 0 if mid_num - 1 < 0 else m_AggregatedWeights[mid_num - 1]
        range_upper = m_AggregatedWeights[mid_num]

        if Random < range_lower:
            high_index = mid_num - 1
        elif Random >= range_upper:
            low_index = mid_num + 1
        elif range_lower <= Random < range_upper:
            return Particles[mid_num]
        else:
            print('Error')


def DrawParticles(sumOfWeights):
    global ParticleCount, m_TempNewParticles

    # global Particles
    m_swap = [[0] * 3 for i in range(ParticleCount)]
    for i in range(ParticleCount):
        Random = random.random() * sumOfWeights
        # DrawParticle(Random)
        m_TempNewParticles[i] = DrawParticle(Random)
        # InitializeMap.DrawPoints(m_TempNewParticles[i][0], m_TempNewParticles[i][1], m_TempNewParticles[i][2])
        m_swap = Particles[i]
        Particles[i] = m_TempNewParticles[i]
        m_TempNewParticles[i] = m_swap


def update(measurements):
    global ParticleCount, Particles, m_AggregatedWeights
    weights_sum = 0
    movedParticle = [0, 0, 0]  # X,Y,degree
    for i in range(ParticleCount):
        original_particle = Particles[i]
        movedParticle = VelocityModel.poseSample(original_particle, ButtonCommand.currentStep)

        while (not IsInside(movedParticle[0], movedParticle[1])):
            Particles[i] = CreateRandomPose()
            movedParticle = VelocityModel.poseSample(original_particle, ButtonCommand.currentStep)
            # if IsInside(Particles[i][0], Particles[i][1]):
            #     break

        # print movedParticle
        weight = CalculateWeight(movedParticle, measurements)

        weights_sum = weights_sum + weight
        m_AggregatedWeights[i] = weights_sum

        Particles[i] = movedParticle
    DrawParticles(weights_sum)


def MonteCarloLocalization(particleCount):
    global ParticleCount, DeltaR, DeltaTheta, Particles, m_AggregatedWeights, m_TempNewParticles

    ParticleCount = particleCount
    DeltaR = 3.0
    DeltaTheta = math.radians(5.0)

    Particles = [[0] * 3 for i in range(ParticleCount)]
    m_AggregatedWeights = [[0] for i in range(ParticleCount)]
    m_TempNewParticles = [[0] * 3 for i in range(ParticleCount)]

    InitializeParticles()


def updateUI():
    InitializeMap.delete()
    InitializeMap.DrawParticles()
