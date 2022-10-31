import math

a = 8.0 * (math.pi - 3) / (3 * math.pi * (4 - math.pi))
s_SquareRoot2 = math.sqrt(2.0)


def Sign(x):
    if x > 0:
        return 1
    elif x < 0:
        return -1
    else:
        return 0


def ErrorFunction(x):
    xSquared = x * x

    er = Sign(x) * math.sqrt(1 - math.exp(-xSquared * (4.0 / math.pi + a * xSquared) / (1 + a * xSquared)))

    return er


def DistributionFunction(x, mean, variance):
    return 0.5 * (1 + ErrorFunction((x - mean) * 1.0 / (math.sqrt(variance) * s_SquareRoot2)))
