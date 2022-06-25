# Python 3.4.3 with Pygame
import imp
from sys import exit
from turtle import color
from cv2 import line, rectangle
from numpy import tri
import pygame
import math
import random
import numpy as np
from game import ColorableCliqueGame
pygame.init()

WIDTH = HEIGHT = 300
window = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption('Crash!')

# Draw Once
# rectangle = pygame.draw.rect(window, (255, 0, 0), (100, 100, 100, 100))
pygame.display.update()


colors = [(255, 50, 50), (50, 50, 255)]
K6 = ColorableCliqueGame(WIDTH, HEIGHT, 6, colors)


run = True
# Main Loop
while run:
    # Mouse position and button clicking
    pos = pygame.mouse.get_pos()
    pressed1 = pygame.mouse.get_pressed()[0]

    event_list = pygame.event.get()
    for event in event_list:
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            exit()
        if event.type == pygame.VIDEORESIZE:
            # There's some code to add back window content here.
            surface = pygame.display.set_mode((event.w, event.h),
                                              pygame.RESIZABLE)
            WIDTH = event.w
            HEIGHT = event.h
            K6.rescale(WIDTH * 0.4, HEIGHT * 0.4)
            K6.transform((WIDTH / 2, HEIGHT / 2))

    window.fill(0)
    # linea.draw(window)
    # linea.update(event_list)
    K6.draw(window)
    K6.update(event_list)
    pygame.display.flip()
