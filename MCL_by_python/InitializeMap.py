from  tkinter import *
import math
import Main
import Points
import ButtonCommand
import Map
import time

top = Tk()
top.title("DraW")
# top.geometry("800x600")

can = Canvas(top, width=800, height=600)
can.pack()

top.update()

points1 = [0, 0]
points2 = [0, 0]
for i in range(len(Map.MapPoints)):
    if i < len(Map.MapPoints) - 1:
        points1, points2 = Map.MapPoints[i], Map.MapPoints[i + 1]
    else:
        points1, points2 = Map.MapPoints[i], Map.MapPoints[0]
    can.create_line(points1[0], points1[1], points2[0], points2[1])
# can.create_rectangle(50, 50, 750, 500)

can.b = Button(text="Reset", width=5, command=ButtonCommand.ResetCommand).pack(side=BOTTOM)
can.b = Button(text="Next", width=5, command=ButtonCommand.NextCommand).pack(side=BOTTOM)


global AllBall


class Ball:
    def __init__(self, canvas, x, y):
        self.can = canvas
        self.id = canvas.create_oval(x - 1, y - 1, x + 1, y + 1, fill='black')

    # def Draw(self, mx, my):
    #     self.can.create_oval(mx - 1, my - 1, mx + 1, my + 1)

    def helete(self):
        self.can.delete(self.id)

def InitiAll(particleCount):
    global AllBall
    AllBall = [[0] for i in range(particleCount)]

def DrawRobot(x, y, degree):
    radius = 5
    strokenThickness = 0.02
    can.create_oval(x - radius, y - radius, x + radius, y + radius, fill='red')
    x2 = x + radius * math.cos(math.radians(degree))
    y2 = y + radius * math.sin(math.radians(degree))
    can.create_line(x, y, x2, y2, fill='green')


def delete():
    global AllBall
    for i in range(len(AllBall)):
        AllBall[i].helete()
        # top.update_idletasks()
        # top.update()
        # time.sleep(0.01)


def DrawPoints(i, x, y):
    global AllBall
    AllBall[i] = Ball(can, x, y)
    # top.update_idletasks()
    # top.update()
    # time.sleep(0.01)


def InitPoints(i, x, y):
    global AllBall
    AllBall[i] = Ball(can, x, y)
    # top.update_idletasks()
    # top.update()
    # time.sleep(0.01)
    # headingRad = math.radians(heading)
    # radius = 1
    # can.create_oval(x - radius, y - radius, x + radius, y + radius,fill = 'black')
    # x2 = x + radius * math.cos(headingRad)
    # y2 = y + radius * math.sin(headingRad)
    # can.create_line(x, y, x2, y2, fill='red')


def DrawParticles():
    step = int(len(Points.Particles) / 250)
    for i in range(0, len(Points.Particles)):
        DrawPoints(i, Points.Particles[i][0], Points.Particles[i][1])