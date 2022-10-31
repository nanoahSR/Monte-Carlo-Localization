import CommonFunctions
import numpy as np
import WeighingFactors
import math

s_Sqrt2PI = math.sqrt(2 * math.pi)
global LambdaShort, MaxRange, m_MeasurementVariance, m_MeasurementSigma
m_MeasurementVariance, m_MeasurementSigma =0,0

def getMeasurementVariance():
    global m_MeasurementVariance
    return m_MeasurementVariance


def setMeasurementVariance(value):
    global m_MeasurementVariance
    if value != m_MeasurementVariance:
        m_MeasurementVariance = value
        sigma = math.sqrt(m_MeasurementVariance)
        m_NormalDistributionFactor = 1.0 / s_Sqrt2PI / sigma
        MeasurementSigma_set(sigma)
        # OnPropertyChanged("MeasurementVariance");
    else:
        pass


def MeasurementSigma_get():
    global m_MeasurementSigma
    return m_MeasurementSigma


def MeasurementSigma_set(value):
    global m_MeasurementVariance,  m_MeasurementSigma
    if value != m_MeasurementVariance:
        m_MeasurementSigma = value
        setMeasurementVariance (m_MeasurementSigma * m_MeasurementSigma)
    else:
        pass


def GetPHit(measuredDistance, realDistance, deltaR):
    if realDistance > MaxRange:
        return 1 - CommonFunctions.DistributionFunction(MaxRange, MaxRange, MaxRange)
    lower = CommonFunctions.DistributionFunction((measuredDistance - deltaR) * 1.0, realDistance * 1.0, getMeasurementVariance())
    upper = CommonFunctions.DistributionFunction((measuredDistance + deltaR) * 1.0, realDistance * 1.0, getMeasurementVariance())
    return upper - lower


def GetPShort(measuredDistance, realDistance, deltaR):
    if measuredDistance > realDistance:
        return 0.0
    else:
        lower = 1 - math.exp(-LambdaShort * (measuredDistance - deltaR))
        upper = 1 - math.exp(-LambdaShort * (measuredDistance + deltaR))
        return upper - lower
    # else:
    #     yita = 1.0 / (1 - math.exp(-LambdaShort * realDistance))
    #     ps = yita * LambdaShort * math.exp(-LambdaShort * measuredDistance)
    #     return ps


def GetPMax(measuredDistance, deltaR):
    if math.fabs(MaxRange - measuredDistance < deltaR):
        return 1.0 / deltaR
    else:
        return 0.0


def GetPRandom(measuredDistance, deltaR):
    if measuredDistance > MaxRange:
        return 0.0
    else:
        return deltaR / MaxRange


def Getprobability(robotToWall, particleToWall, deltaR):
    if particleToWall > MaxRange:
        particleToWall = MaxRange

    # GHit = WeighingFactors.ZHit
    # GPHit = GetPHit(robotToWall, particleToWall, deltaR)
    # 1.0 0.1 0.0 0.1
    probability = WeighingFactors.ZHit * GetPHit(robotToWall, particleToWall, deltaR) + \
                  WeighingFactors.ZShort * GetPShort(robotToWall, particleToWall, deltaR) + \
                  WeighingFactors.ZMax * GetPMax(robotToWall, deltaR) + \
                  WeighingFactors.ZRand * GetPRandom(robotToWall, deltaR)

    return probability


def SamplePHit(realDistance):
    # realDistance = int(realDistance)
    m_NormalDistribution = [realDistance, MeasurementSigma_get()]
    # m_NormalDistribution.Sigma = MeasurementSigma
    while True:
        measurementSample = np.random.normal(m_NormalDistribution[0], m_NormalDistribution[1])
        if measurementSample < MaxRange:
            break
    return measurementSample


def SamplePShort(realDistance):
    while True:
        measurementSample = np.random.exponential(realDistance)
        if measurementSample < realDistance:
            break
    return measurementSample


def SamplePRandom():
    return np.random.random() * MaxRange


def GetSample(realDistance):
    RealDistance = realDistance / 20.0
    effectiveDistance = MaxRange if realDistance > MaxRange else realDistance
    if realDistance > MaxRange:
        return MaxRange

    Random = np.random.random()

    if Random <= WeighingFactors.ZHit:
        return SamplePHit(effectiveDistance)
    elif Random <= WeighingFactors.ZHit + WeighingFactors.ZShort:
        return SamplePShort(effectiveDistance)
    elif Random <= WeighingFactors.ZHit + WeighingFactors.ZShort + WeighingFactors.ZMax:
        return MaxRange
    else:
        return SamplePRandom()


def BeamModel(maxRange, measurementVariance, lambdaShort):
    global MaxRange, LambdaShort
    MaxRange = maxRange
    setMeasurementVariance (measurementVariance)
    MeasurementSigma_set (math.sqrt(getMeasurementVariance()))
    LambdaShort = lambdaShort
