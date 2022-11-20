import pygame as pg
import sys
import pathlib
import itertools
import numpy as np
import random
import math


pg.init()
pg.font.init()


screenSize = 1000
screen = pg.display.set_mode((screenSize, screenSize))
pg.display.set_caption('GraphSim')


showLines = True
pointColor = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
changePointColor = pg.USEREVENT+1
pg.time.set_timer(changePointColor, 100)

def parabola(a, x, h, k):
    y = a * (x - h)**2 + k
    return y

def horizontal_parabola(a, y, b, c):
    x = a * y**2 + b * y + c
    return x

def get_parabola(start, end, a, h, k):
    line = [[x, parabola(a, x, h, k)] for x in range(start, end+1)]
    return line

def get_horizontal_parabola(start, end, a, b, c):
    line = [[horizontal_parabola(a, y, b, c), y] for y in range(start, end+1)]
    return line

def functionY(start, end):
    line = [[x, math.sqrt(x)] for x in range(start, end+1)]
    return line


lineAB = functionY(0, 76)
lineBC = get_parabola(-7, 7, a=-1, h=0, k=0)
lineCD = get_horizontal_parabola(-7, 7, a=-1, b=0, c=0)
lineDE = get_horizontal_parabola(-7, 7, a=1, b=0, c=0)

lines = [lineBC]


x_axis = []
y_axis = []

Gfont = "OpenSans-light.ttf"

white = (255,255,255)
blue = (0, 115, 255)
gridStart = 10
gridEnd = int((screenSize/2))-10
gridScale = 1
gridStep = 20

def draw_text(screen: pg.Surface,
              text: str,
              font_file: str,
              font_size: int,
              color: tuple,
              pos: tuple,
              backg=None,
              bold=False,
              italic=False,
              underline=False):
    if '.ttf' in font_file:
        font = pg.font.Font(pathlib.Path(font_file), font_size)
    else:
        font = pg.font.SysFont(font_file, font_size)
    font.set_bold(bold)
    font.set_italic(italic)
    font.set_underline(underline)
    if backg == None:
        t = font.render(text, True, color)
    t = font.render(text, True, color, backg)
    textRect = t.get_rect()
    textRect.center = pos
    screen.blit(t, textRect)

def drawLines(lines, x_axis, y_axis):
    x_axis.sort()
    x_data = list(x for x,_ in itertools.groupby(x_axis))
    y_axis.sort()
    y_data = list(x for x,_ in itertools.groupby(y_axis))
    for line in lines:
        points = []
        for point in line:
            x_, y_ = line[line.index(point)][0], line[line.index(point)][1]
            for x in x_data:
                for y in y_data:
                    if x_ == x[0] and line[line.index(point)][1] == y[0]:
                        x1_pos = x[1][0]
                        y1_pos = y[1][1]
                        pg.draw.circle(screen, pointColor, (x1_pos, y1_pos), 5)
                        points.append((x1_pos, y1_pos))


                        if len(points) >= 2:
                            if showLines:
                                pg.draw.lines(screen, white, False, points, 1)


def drawOrigin():
    pg.draw.circle(screen, blue, (screenSize/2, screenSize/2), 2)

def drawXYAxis():
    pg.draw.line(screen, blue, (screenSize/2, 0), (screenSize/2, screenSize))
    pg.draw.line(screen, blue, (0, screenSize/2), (screenSize, screenSize/2))


def drawXScale():
    tick_x_positions = [x for x in range(gridStart, gridEnd, gridStep)]
    tick_y_positions = int(screenSize/2) + 10
    tick_x_positions.reverse()
    i = 0
    for x_pos in tick_x_positions:
        i += gridScale
        draw_text(screen, f"-{i}", Gfont, 10, (255,255,255), (x_pos, tick_y_positions))
        x_axis.append([-i, (x_pos, tick_y_positions)])


    # Ticks between ticks
    # tick_x_mid_positions = [x for x in np.arange(gridStart/10, gridEnd+gridStep/10, gridStep/10)]
    # tick_y_mid_positions = int(screenSize/2) + 10
    # tick_x_mid_positions.reverse()
    # iMid = 0
    # for x_pos in tick_x_mid_positions:
    #     iMid += gridScale/10
    #     # draw_text(screen, f"{round(-i
    #     # Mid, 2)}", Gfont, 1, (255,255,255), (x_pos, tick_y_mid_positions))
    #     x_axis.append([round(-iMid, 2), (x_pos, tick_y_positions)])


    tick_x_positions2 = [x for x in range(gridEnd + gridStep, (screenSize - 10) + gridStep, gridStep)]
    tick_y_positions2 = int(screenSize/2) + 10
    i2 = 0
    for x_pos in tick_x_positions2:
        i2 += gridScale
        draw_text(screen, f"{i2}", Gfont, 10, (255,255,255), (x_pos, tick_y_positions))
        x_axis.append([i2, (x_pos, tick_y_positions)])

    # tick_x_mid_positions2 = [x for x in np.arange(gridEnd + gridStep/10, (screenSize - 10) + gridStep/10, gridStep/10)]
    # tick_y_mid_positions2 = int(screenSize/2) + 10
    # iMid2 = 0
    # for x_pos in tick_x_mid_positions2:
    #     iMid2 += gridScale/10
    #     # draw_text(screen, f"{iMid}", Gfont, 10, (255,255,255), (x_pos, tick_y_positions))
    #     x_axis.append([round(iMid2, 2), (x_pos, tick_y_mid_positions2)])

    x_axis.append([0, [screenSize/2, screenSize/2]])


def drawYScale():
    tick_y_positions = [y for y in range(gridStart, gridEnd, gridStep)]
    tick_x_positions = int(screenSize / 2) - 10
    tick_y_positions.reverse()
    i = 0
    for y_pos in tick_y_positions:
        i += gridScale
        draw_text(screen, f"{i}", Gfont, 10, (255,255,255), (tick_x_positions, y_pos))
        y_axis.append([i, (tick_x_positions, y_pos)])

    # tick_y_mid_positions = [y for y in np.arange(gridStart, gridEnd, gridStep/10)]
    # tick_x_mid_positions = int(screenSize / 2) - 10
    # tick_y_mid_positions.reverse()
    # iMid = 0
    # for y_pos in tick_y_mid_positions:
    #     iMid += gridScale/10
    #     # draw_text(screen, f"{round(iMid, 2)}", Gfont, 10, (255,255,255), (tick_x_mid_positions, y_pos))
    #     y_axis.append([round(iMid, 2), (tick_x_mid_positions, y_pos)])

    tick_y_positions2 = [y for y in range(gridEnd + gridStep, (screenSize - 10) + gridStep, gridStep)]
    tick_x_positions2 = int(screenSize / 2) - 10
    i2 = 0
    for y_pos in tick_y_positions2:
        i2 += gridScale
        draw_text(screen, f"-{i2}", Gfont, 10, (255,255,255), (tick_x_positions2, y_pos))
        y_axis.append([-i2, (tick_x_positions, y_pos)])

    # tick_y_mid_positions2 = [y for y in np.arange(gridEnd + gridStep, (screenSize - 10) + gridStep, gridStep/10)]
    # tick_x_mid_positions2 = int(screenSize / 2) - 10
    # tick_y_mid_positions2.reverse()
    # iMid2 = 0
    # for y_pos in tick_y_mid_positions2:
    #     iMid2 += gridScale/10
    #     # draw_text(screen, f"{round(-iMid2, 2)}", Gfont, 10, (255,255,255), (tick_x_mid_positions2, y_pos))
    #     y_axis.append([round(-iMid2, 2), (tick_x_mid_positions2, y_pos)])

    y_axis.append([0, [screenSize/2, screenSize/2]])


def updateDraw():
    pg.display.update()

clock = pg.time.Clock()
fps = 60

while True:
    clock.tick(fps)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                sys.exit()

            if event.key == pg.K_l and pg.key.get_mods() & pg.KMOD_CTRL:
                showLines = not showLines

        if event.type == pg.USEREVENT+1:
            pointColor = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    x_axis.sort()
    x_axis = list(x for x,_ in itertools.groupby(x_axis))
    y_axis.sort()
    y_axis = list(x for x,_ in itertools.groupby(y_axis))

    drawXScale()
    drawYScale()
    drawOrigin()
    drawLines(lines, x_axis, y_axis)
    drawXYAxis()
    updateDraw()
