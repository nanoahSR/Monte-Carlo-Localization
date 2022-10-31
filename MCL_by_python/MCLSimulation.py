import Points
import Robot
import VelocityModel

TruePose = [0,0,0]

def Drive(driveCommand):
    TruePose = VelocityModel.MoveExact(driveCommand)
    simulatedMeasurements = Robot.GetMeasurements(TruePose)
    Points.update(simulatedMeasurements)
    Points.updateUI()
