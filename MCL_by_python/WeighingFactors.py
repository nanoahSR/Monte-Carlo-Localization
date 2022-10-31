global ZHit,ZShort,ZMax,ZRand
global m_ZHitRaw, m_ZShortRaw,m_ZMaxRaw,m_ZRandRaw


def getZHitRaw():
    global m_ZHitRaw
    return m_ZHitRaw


def getZShortRaw():
    global m_ZShortRaw
    return m_ZShortRaw

def getZMaxRaw():
    global m_ZMaxRaw
    return m_ZMaxRaw


def getZRandRaw():
    global m_ZRandRaw
    return m_ZRandRaw

def Normalize():
    global ZHit, ZShort, ZMax, ZRand

    total = getZHitRaw() + getZShortRaw() + getZMaxRaw() + getZRandRaw()

    ZHit = getZHitRaw() / total
    ZShort = getZShortRaw() / total
    ZMax = getZMaxRaw() / total
    ZRand = getZRandRaw() / total


def WeighingFactors(zHit, zShort, zMax, zRand):
    global m_ZHitRaw, m_ZShortRaw, m_ZMaxRaw, m_ZRandRaw
    m_ZHitRaw = zHit
    m_ZShortRaw = zShort
    m_ZMaxRaw = zMax
    m_ZRandRaw = zRand
    Normalize()