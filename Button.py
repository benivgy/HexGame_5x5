import pygame
import math

from pygame import Rect

'''
This is a button that I created
'''

class Button_hex():
    def __init__(self, x, y, size=100):
        # Initialize the button with its center position (x, y) and size
        self.center = (x, y)
        self.size = size
        # Flag to track if the button is clicked or not
        self.clicked = False

    def buttonPress(self):
        # Function to detect button press
        coll = False  # Flag to indicate if the button is clicked
        pos = pygame.mouse.get_pos()  # Get the current mouse position
        # Calculate the distance between the mouse cursor and the center of the button
        distance = math.sqrt((self.center[0] - pos[0])**2 + (self.center[1] - pos[1])**2)
        # Check if the mouse cursor is within the button's boundary, left mouse button is pressed, and the button is not already clicked
        if distance <= self.size and pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
            # Set the clicked flag to True and coll to True to indicate a successful click
            self.clicked = True
            coll = True
        # Check if the left mouse button is released
        if pygame.mouse.get_pressed()[0] == 0:
            # Reset the clicked flag to False
            self.clicked = False
        # Return the coll flag indicating whether the button was clicked or not
        return coll

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
        surface.blit(picture, rect)


