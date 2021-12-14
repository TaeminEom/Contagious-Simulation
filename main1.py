import pygame as pg
import random as rd
import math
import copy
import numpy as np

def distance(g1, n1, g2, n2):
    pos1 = np.array(student[g1][n1].pos)
    pos2 = np.array(student[g2][n2].pos)

    d = np.abs(pos1 - pos2)
    d = (d[0] ** 2 + d[1] ** 2) ** 0.5
    return d

def checkInfection(g1, n1, g2, n2):
    return student[g1][n1].infection != student[g2][n2].infection

def infection():
    for g1 in range(8):
        for n1 in range(24):
            for g2 in range(g1, 8):
                for n2 in range(n1 + 1, 24):
                    if rd.random() > 0.5 + distance(g1, n1, g2, n2) * 0.01988 and checkInfection(g1, n1, g2, n2):
                        student[g1][n1].infection = 1
                        student[g2][n2].infection = 1
                        timelapse.append(t)


def draw():
    screen.fill(WHITE)

    pg.draw.rect(screen, BLACK, [50, 50, 500, 600], 2)
    for i in range(4):
        pos = [50, 50 + i * 150, 200, 150]
        pg.draw.rect(screen, BLACK, pos, 2)
    for i in range(4):
        pos = [350, 50 + i * 150, 200, 150]
        pg.draw.rect(screen, BLACK, pos, 2)

    for g in range(8):
        for n in range(24):
            student[g][n].draw()

    pg.display.flip()

class Student:
    def __init__(self, group, number, pos):
        self.infection = 0
        self.group = group
        self.number = number
        self.groupPos = pos[group]
        self.fixed_pos = [self.groupPos[0] + 25 + number % 6 * 30, self.groupPos[1] + 40 + number // 6 * 25]
        self.pos = copy.deepcopy(self.fixed_pos)
        self.dir = rd.random() * 2 * math.pi
        self.corridor = False

    def setClass(self):
        self.pos = copy.deepcopy(self.fixed_pos)

    def setCorridor(self):
        self.pos = [250 + rd.randint(0, 100), 50 + rd.randint(0, 600)]

    def lockClass(self):
        if self.pos[0] > self.groupPos[0] + 200:
            self.pos[0] = self.groupPos[0] + 200
            self.dir = rd.random() * 2 * math.pi
        if self.pos[1] > self.groupPos[1] + 150:
            self.pos[1] = self.groupPos[1] + 150
            self.dir = rd.random() * 2 * math.pi
        if self.pos[0] < self.groupPos[0]:
            self.pos[0] = self.groupPos[0]
            self.dir = rd.random() * 2 * math.pi
        if self.pos[1] < self.groupPos[1]:
            self.pos[1] = self.groupPos[1]
            self.dir = rd.random() * 2 * math.pi

    def lockCorridor(self):
        if self.pos[0] > 350:
            self.pos[0] = 350
            self.dir = rd.random() * 2 * math.pi
        if self.pos[1] > 650:
            self.pos[1] = 650
            self.dir = rd.random() * 2 * math.pi
        if self.pos[0] < 250:
            self.pos[0] = 250
            self.dir = rd.random() * 2 * math.pi
        if self.pos[1] < 50:
            self.pos[1] = 50
            self.dir = rd.random() * 2 * math.pi

    def breakTimeInClass(self):
        self.dir += (rd.random() - 0.5) * 2
        self.pos[0] += math.cos(self.dir)
        self.pos[1] += math.sin(self.dir)

        self.lockClass()

    def breakTimeInCorridor(self):
        self.dir += (rd.random() - 0.5) * 2
        self.pos[0] += math.cos(self.dir)
        self.pos[1] += math.sin(self.dir)

        self.lockCorridor()


    def draw(self):
        if self.infection == 0:
            pg.draw.circle(screen, YELLOW, self.pos, 4)
        if self.infection == 1:
            pg.draw.circle(screen, RED, self.pos, 4)


pg.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 212, 0)
RED = (255, 0, 0)

size = [600, 700]
screen = pg.display.set_mode(size)

pg.display.set_caption("Infective Simulator")

group = [[50, 50], [50, 200], [50, 350], [50, 500], [350, 50], [350, 200], [350, 350], [350, 500]]

timelapseAll = []

for try20 in range(27):
    student = []
    for g in range(8):
        student.append([])
        for n in range(24):
            student[g].append(Student(g, n, group))
    student[0][0].infection = 1

    start = 0
    t = 0
    breakTime = False

    timelapse = [1]

    done = False
    while not done:
        start += 1
        t += 1

        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True

        if start > 300 and breakTime == True:
            start = 0
            breakTime = False
            for g in range(8):
                for n in range(24):
                    student[g][n].setClass()
                    student[g][n].corridor = False
        if start > 1500 and breakTime == False:
            start = 0
            breakTime = True
            for g in range(8):
                for n in range(24):
                    if rd.random() < 0.4:
                        student[g][n].setCorridor()
                        student[g][n].corridor = True
        for g in range(8):
            for n in range(24):
                if breakTime == True and student[g][n].corridor == True:
                    student[g][n].breakTimeInCorridor()
                if breakTime == True and student[g][n].corridor == False:
                    student[g][n].breakTimeInClass()
                if breakTime == False:
                    pass

        infection()

        draw()
        infectionCnt = 0
        print("\r", start, t, try20, end="")
        for g in range(8):
            for n in range(24):
                infectionCnt += student[g][n].infection
        if infectionCnt == 192:
            done = 1
    timelapseAll.append(timelapse)
pg.quit()
print()

for i in timelapseAll:
    print()
    print(i)