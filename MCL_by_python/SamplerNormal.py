import math
import random

c_AggregationCount = 12


def GetRandomInRange(b):
    return random.random() * 2 * b - b


def Sampler(variance):
    b = math.sqrt(variance)
    result = 0.0

    for i in range(0, c_AggregationCount):
        result += GetRandomInRange(b)
    return 0.5 * result
