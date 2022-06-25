import pygame
import math
import random
import numpy as np
pygame.init()

WIDTH = HEIGHT = 300
window = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption('Crash!')


class Point:
    def __init__(self, x, y) -> None:
        self._localX = x
        self._localY = y
        self._scaleX = 1
        self._scaleY = 1
        self._worldPosX = 0
        self._worldPosY = 0

    def scale(self, scaleX, scaleY):
        self._localX *= scaleX
        self._localY *= scaleY
        self._scaleX *= scaleX
        self._scaleY *= scaleY

    def rescale(self, scaleX, scaleY):
        self.scale(1 / self._scaleX, 1 / self._scaleY)
        self.scale(scaleX, scaleY)

    def transform(self, worldPos):
        self._worldPosX = worldPos[0]
        self._worldPosY = worldPos[1]

    def pos(self):
        return (self._localX + self._worldPosX, self._localY + self._worldPosY)


class ClickableLine:
    def __init__(self, startPoint: Point, endPoint: Point, color, width) -> None:
        self.start = startPoint
        self.end = endPoint
        self.color = color
        self.width = width
        self.line_resulution = 50
        self.click_range = 4

    def draw(self, window):
        sp = self.start.pos()
        ep = self.end.pos()
        # center = ((sp[0] + ep[0])/2, (sp[1] + ep[1]) / 2)
        self.line = pygame.draw.line(
            window, self.color, sp, ep, self.width)

        self.buttons = []

        directionx = ep[0] - sp[0]
        directiony = ep[1] - sp[1]
        # print("-------------")
        for i in range(self.line_resulution):
            frac = (i + 1) / (self.line_resulution + 1)
            # print(frac)
            centerx = sp[0] + directionx * frac
            centery = sp[1] + directiony * frac
            self.buttons.append(pygame.Rect(
                centerx - self.click_range, centery - self.click_range, self.click_range * 2, self.click_range * 2))

            # self.button = pygame.Rect(
            #     center[0] - 20, center[1] - 20, 40, 40)
            # self.circle = pygame.draw.circle(window, self.color, self.center, 10)

    def isClicked(self, event_list):
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in self.buttons:
                    if button.collidepoint(event.pos):
                        return True

            # self.image = self.click_image if self.clicked else self.original_image


def getCircle(folds, scaleX, scaleY, worldPos):
    points = []
    for i in range(folds):
        angle = math.pi * 2 * (i / folds)
        point = Point(math.sin(angle), math.cos(angle))
        point.scale(scaleX, scaleY)
        point.transform(worldPos)
        points.append(point)
    return points


class ColorableCliqueGame:
    def __init__(self, width, height, k, colors) -> None:
        self.k = k
        self.colors = colors
        self.nodes = getCircle(
            self.k, width * 0.4, height * 0.4, (width / 2, height / 2))
        self.reset()

    def reset(self):
        self.player = 0
        self.winner = -1
        self.adjecencyMatrix = {}
        self.edges = {}
        for i in range(self.k):
            for j in range(self.k):
                key = (i, j)
                if i < j:
                    self.adjecencyMatrix[key] = 0
                    edge = ClickableLine(
                        self.nodes[i], self.nodes[j], (255, 255, 255), 3)
                    self.edges[key] = edge

    def rescale(self, scaleX, scaleY):
        for node in self.nodes:
            node: Point
            node.rescale(scaleX, scaleY)

    def transform(self, worldPos):
        for node in self.nodes:
            node: Point
            node.transform(worldPos)

    def draw(self, window):
        for node in self.nodes:
            node: Point
            pygame.draw.circle(window, (155, 195, 255), node.pos(), 7)

        for edge in self.edges.values():
            edge: ClickableLine
            edge.draw(window)

    def detectTriangle(self, startEdge, playerColor):
        triangle = False
        for n in range(len(self.nodes)):
            if n == startEdge[0] or n == startEdge[1]:
                continue
            keya = (n, startEdge[0])
            if n > startEdge[0]:
                keya = (startEdge[0], n)
            if self.adjecencyMatrix[keya] != playerColor:
                continue

            keyb = (n, startEdge[1])
            if n > startEdge[1]:
                keyb = (startEdge[1], n)
            if self.adjecencyMatrix[keyb] != playerColor:
                continue
            triangle = True
        return triangle

    def state(self):
        arr = []
        for i in range(self.k):
            arr.append([])
            for j in range(self.k):
                if i < j:
                    key = (i, j)
                    arr[i].append(self.adjecencyMatrix[key])
                elif i == j:
                    arr[i].append(0)
                else:
                    key = (j, i)
                    arr[i].append(self.adjecencyMatrix[key])
        return np.array(arr), self.player * 2 - 1

    def update(self, event_list):
        for key in self.edges:
            edge: ClickableLine = self.edges[key]
            if(edge.isClicked(event_list)):
                if self.adjecencyMatrix[key] == 0:
                    pc = self.player * 2 - 1
                    self.adjecencyMatrix[key] = pc
                    edge.color = self.colors[self.player]
                    triangle = self.detectTriangle(key, pc)
                    if triangle:
                        print("player", self.player, "has won!")
                        self.winner = self.player
                        self.reset()
                        return

                    self.player = (self.player + 1) % len(self.colors)
                    print(self.state())
                # print(int(random.random() * 255))
                    # edge.color = (int(random.random() * 255),
                    #               int(random.random() * 255), int(random.random() * 255))
                print(key, "was clicked")
