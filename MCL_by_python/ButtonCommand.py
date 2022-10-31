import Drive
import MCLSimulation
import Points
import InitializeMap
import Robot
import time

global currentStep
currentStep = -1
TruePose = [0, 0, 0]


def NextCommand():
    global currentStep
    # if currentStep == -1:
    #     MCLSimulation.Drive(currentStep)
    TruePose = Drive.MoveExact(currentStep)
    simulated_measurements = Robot.GetMeasurements(TruePose)
    Points.update(simulated_measurements)
    Points.updateUI()

    currentStep = currentStep + 1


def ResetCommand():
    global currentStep
    current = 0
    InitializeMap.delete()
