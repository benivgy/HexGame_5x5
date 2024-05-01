import pygame
import math

from pygame import Rect

'''
This is a button that I created
'''

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

    def draw(self, surface):
        # Draw hexagon
        for i in range(6):
            start = (self.center[0] + self.size * math.cos((i * math.pi / 3) + self.rotation),
                     self.center[1] + self.size * math.sin((i * math.pi / 3) + self.rotation))
            end = (self.center[0] + self.size * math.cos(((i + 1) * math.pi / 3) + self.rotation),
                   self.center[1] + self.size * math.sin(((i + 1) * math.pi / 3) + self.rotation))
            pygame.draw.line(surface, (255, 255, 255), start, end)


class Button_rect():
    def __init__(self, x, y,xSize=200,ySize=100):
        self.rect = Rect(0,0,xSize,ySize)
        self.rect.center = (x,y)
        self.x = x
        self.y = y
        self.clicked = False #Whereas the button was pressed or not

    def getXpos(self): #Returns the top left x position of the button
        return self.rect.topleft[0]
    def getYpos(self):#Returns the top left y position of the button
        return self.rect.topleft[1]

    def buttonPress(self): #Returns whereas the button was pressed
        # Mouse collision
        coll = False
        # get mouse position
        pos = pygame.mouse.get_pos()

        # check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                coll = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        return coll

    def showButton(self,picture,rect,surface):
        #Show where the button is located - used for monitoring
        rect.center=self.rect.center
        surface.blit(picture,rect)

    def mouseCollision(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())


