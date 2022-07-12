import pygame
import math
import random
import numpy as np
pygame.init()

def nCr(n, k):
    s = n
    d = 1
    for i in range(1, k):
        s *= (n - i)
        d *= (i + 1)
    return int(s / d)


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



def IsTriangle(game, a,b,c):
    if game.adjecencyMatrix[(a,b)] == game.adjecencyMatrix[(a,c)] == game.adjecencyMatrix[(b,c)] and game.adjecencyMatrix[(a,b)] != 0:
        return int((-game.adjecencyMatrix[(a,b)] + 1) / 2)
    return -1

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
    """
    The player that creates a monochromatic K3 loses.
    """

    def __init__(self, width, height, k, colors) -> None:
        self.k = k
        self.default_color = (255, 255, 255)
        self.colors = colors
        self.frame_window = pygame.Surface((width, height), pygame.SRCALPHA)
        self.nodes = getCircle(
            self.k, width * 0.4, height * 0.4, (width / 2, height / 2))
        self.turn_in_a_row = 1
        self.turns = self.turn_in_a_row
        self.reset()

    def reset(self):
        self.player = 0
        self.winner = -1
        self.adjecencyMatrix = {}
        self.edges = {}
        self.movesMade = []
        for i in range(self.k):
            for j in range(i+1,self.k):
                key = (i, j)
                if i < j:
                    self.adjecencyMatrix[key] = 0
                    edge = ClickableLine(
                        self.nodes[i], self.nodes[j], self.default_color, 3)
                    self.edges[key] = edge

    def loadfrom1D(self, data: np.ndarray):
        if len(self.colors) != 2:
            #print("this mode doesnt support loading!")
            return False


        states = nCr(self.k, 2)
        data = data[:states]
        #print(len(data))
        if len(data) > states + 1 or len(data) < states:
            #print("data dont match for k - ", self.k)
            return False

        diff = (np.count_nonzero(data == -1) - np.count_nonzero(data == 1))
        if diff < 0 or diff > 1:
            #print("bad data! ",diff)
            return False

        self.player = 0
        self.winner = -1
        # print(self.k)
        index = 0
        for i in range(self.k):
            for j in range(i+1, self.k):
                key = (i, j)
                self.adjecencyMatrix[key] = data[index]
                if data[index] != 0:
                    player = int((data[index] + 1) / 2)
                    self.edges[key].color = self.colors[player]
                else:
                    self.edges[key].color = self.default_color
                index += 1

        if diff == 0:
            self.player = 0
        else:
            self.player = 1

        self.winner == -1
        for a in range(self.k):
            for b in range(a + 1,self.k):
                for c in range(b + 1,self.k):
                    t = IsTriangle(self,a,b,c)
                    if t != -1:
                        if self.winner != -1:
                            return False
                        self.winner = t
        return True

    def rescale(self, scaleX, scaleY):
        for node in self.nodes:
            node: Point
            node.rescale(scaleX, scaleY)

    def getMoves(self):
        if self.winner != -1:
            return []
        moves = []
        for key in self.adjecencyMatrix:
            if self.adjecencyMatrix[key] == 0:
                moves.append(key)
        return moves

    def undo(self):
        if len(self.movesMade) > 0:
            lastmove = self.movesMade.pop()
            if self.turns == self.turn_in_a_row:
                self.player = (self.player + 1) % len(self.colors)
                self.turns = 1
            else:
                self.turns += 1
            self.winner = -1
            self.adjecencyMatrix[lastmove] = 0
            edge = self.edges[lastmove]
            edge.color = self.default_color
        return self.player

    def applyMove(self, move):
        """
        The player that creates a monochromatic K3 loses.
        """
        if self.winner != -1:
            return True, self.player

        if self.adjecencyMatrix[move] == 0:
            self.movesMade.append(move)
            edge = self.edges[move]
            pc = self.player * 2 - 1
            self.adjecencyMatrix[move] = pc
            edge.color = self.colors[self.player]
            triangle = self.detectTriangle(move, pc)
            next_player = (self.player + 1) % len(self.colors)
            self.turns -= 1
            if self.turns == 0:
                self.player = next_player
                self.turns = self.turn_in_a_row
            if triangle:
                self.winner = next_player
                return True, self.winner
            return False, self.player
        return False, -1

    def transform(self, worldPos):
        for node in self.nodes:
            node: Point
            node.transform(worldPos)

    def frame(self):
        screen = self.frame_window
        # screen.fill(self.level.background.color)
        screen.fill((0, 0, 0))
        self.draw(self.frame_window)
        imgdata = pygame.surfarray.array3d(self.frame_window)
        return imgdata

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

    def state1D(self):
        arr = []
        for i in range(self.k):
            for j in range(i+1, self.k):
                key = (i, j)
                arr.append(self.adjecencyMatrix[key])
        arr.append(self.player * 2 - 1)
        return np.array(arr)

    def update(self, event_list):
        for key in self.edges:
            edge: ClickableLine = self.edges[key]
            if(edge.isClicked(event_list)):
                move = self.applyMove(key)
                if self.applyMove(key):
                    if move[0] == True:
                        print("player", move[1], "has won!")
                        self.reset()
                        return
                # print(int(random.random() * 255))
                # edge.color = (int(random.random() * 255),
                #               int(random.random() * 255), int(random.random() * 255))
                print(key, "was clicked")
        