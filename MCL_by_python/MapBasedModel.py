from Tkinter import *
import InitializeMap
import math

def DrawRobot(x,y):


    pose_X = x
    pose_Y = y

    radius = 0.2
    strokenThickness = 0.02

    create_oval(pose_X,pose_Y,x+2*radius,y+2*radius)

    #line_X = pose_X
    #line_Y = pose_Y
    #line_X2 = pose_X + radius * math.cos(pose.Heading.Rads);
    #line_Y2 = pose_Y + radius * math.sin(pose.Heading.Rads);
    #create_line(line_X, line_Y, x2, y2)