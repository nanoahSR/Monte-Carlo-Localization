from tkinter import *
import BeamModel
import Drive
import InitializeMap
import Points
import Robot
import Map
import WeighingFactors


def main():
    particleCount = 10000
    InitializeMap.InitiAll(particleCount)

    Map.InitializeMinsAndMaxs()
    InitializeMap.DrawRobot(50, 230, 0)
    # Points.InitializeParticles()

    #maxrange, mV, lamda
    BeamModel.BeamModel(120, 6.0, 0.5)
    WeighingFactors.WeighingFactors(1.0, 0.1, 0.0, 0.1)

    # 与InitializeMap.AllBall同时更改
    Points.MonteCarloLocalization(particleCount)

    mainloop()


if __name__ == '__main__':
    main()
