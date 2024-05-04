import pygame
import math



class Button_hex():
    def __init__(self, x, y, size=100, rotation=30):
        self.center = (x, y)
        self.size = size
        self.rotation = rotation
        self.clicked = False

    def buttonPress(self):
        coll = False
        pos = pygame.mouse.get_pos()
        distance = math.sqrt((self.center[0] - pos[0])**2 + (self.center[1] - pos[1])**2)
        if distance <= self.size and pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
            self.clicked = True
            coll = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        return coll
