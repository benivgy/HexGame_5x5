import pygame
import Button
import Hexagon

'''
This class is in charge of the game environment
'''

#colors
YELL0W = (255,232,0)
RED = (200,0,0)
RED_dark = (75,0,0)
GRAY = (45,45,45)
WHITE = (255,255,255)
GREEN = (76,208,56)
BLACK = (0,0,0)
BLUE = (0,0,255)
BLUE_dark = (0,0,75)


pygame.init()
class Screen:

    def __init__(self):
        self.RES= (900,600) #Screen resolution


        self.WIN = pygame.display.set_mode(self.RES) #Set the window

        self.FPS = 60 #Refresh rate

        # The clock will control the number of times the screen refreshes
        self.clock = pygame.time.Clock()

        self.gameMode="menu" # 1v1 , random , smart ,  menu, none, quit

        self.boardSize=5 #Size of the board will be 5*5

        self.menuOption="play" #used for the menu (play, quit, options)
        self.settingSelection = "1v1"


        ''' Menu '''
        self.showMenu = True
        self.optionsPage=False
        self.menu_surface = pygame.Surface(self.RES, pygame.SRCALPHA)
        self.menu_surface.fill((35, 85, 75))

        #Pictures for the buttons

        self.play1Pic = pygame.transform.scale((pygame.image.load('images/PLAY1.png')), (200,50))
        self.play2Pic = pygame.transform.scale((pygame.image.load('images/PLAY2.png')), (200,50))
        self.quit1Pic = pygame.transform.scale((pygame.image.load('images/QUIT1.png')), (200,50))
        self.quit2Pic = pygame.transform.scale((pygame.image.load('images/QUIT2.png')), (200,50))
        self._1v1_1Pic = pygame.transform.scale((pygame.image.load('images/1V1_1.png')), (200, 50))
        self._1v1_2Pic = pygame.transform.scale((pygame.image.load('images/1V1_2.png')), (200, 50))
        self.average1Pic = pygame.transform.scale((pygame.image.load('images/AVERAGE1.png')), (200, 50))
        self.average2Pic = pygame.transform.scale((pygame.image.load('images/AVERAGE2.png')), (200, 50))
        self.back1Pic = pygame.transform.scale((pygame.image.load('images/BACK1.png')), (200, 50))
        self.back2Pic = pygame.transform.scale((pygame.image.load('images/BACK2.png')), (200, 50))
        self.easy1Pic = pygame.transform.scale((pygame.image.load('images/EASY1.png')), (200, 50))
        self.easy2Pic = pygame.transform.scale((pygame.image.load('images/EASY2.png')), (200, 50))
        self.hard1Pic = pygame.transform.scale((pygame.image.load('images/HARD1.png')), (200, 50))
        self.hard2Pic = pygame.transform.scale((pygame.image.load('images/HARD2.png')), (200, 50))
        self.about1Pic = pygame.transform.scale((pygame.image.load('images/ABOUT1.png')), (200, 50))
        self.about2Pic = pygame.transform.scale((pygame.image.load('images/ABOUT2.png')), (200, 50))









        self.up_arrow_pressed = False
        self.down_arrow_pressed = False

        self.hexagons= [[0 for j in range(self.boardSize)] for i in range(self.boardSize)]
        for i in range(self.boardSize):
            for j in range(self.boardSize):
                self.hexagons[i][j]=(Hexagon.Hexagon(300+25*j+25*2*i,212+44*j,25))

        self.hexagons_Shadow = [[0 for j in range(self.boardSize)] for i in range(self.boardSize)]
        for i in range(self.boardSize):
            for j in range(self.boardSize):
                self.hexagons_Shadow[i][j] = (Hexagon.Hexagon(310 + 25 * j + 25 * 2 * i, 220 + 44 * j, 25))

        self.buttons = [[0 for j in range(self.boardSize)] for i in range(self.boardSize)]
        for i in range(self.boardSize):
            for j in range(self.boardSize):
                self.buttons[i][j]=(Button.Button_hex(300+25*j+25*2*i,212+44*j,25))

    def draw_hexagon(self, hex,shadow,width=0):
        #Draw the given hexagon
        if hex.color == WHITE:
            width=3

        if hex.mouseCollision(pygame.mouse.get_pos()):
            pygame.draw.polygon(self.WIN, (0,0,0),shadow.points)
            width=0

        if hex.color!=WHITE:
            pygame.draw.polygon(self.WIN, (0,0,0),shadow.points)
        pygame.draw.polygon(self.WIN, hex.color,hex.points,width)


    def draw_grid(self):
        for i in range(self.boardSize):
            for j in range(self.boardSize):
                self.draw_hexagon(self.hexagons[i][j],self.hexagons_Shadow[i][j])

    def menu(self,keys):
        pressedKey = self.check_arrow_keys(keys)
        self.WIN.blit((self.menu_surface), (0, 0))
        if not self.optionsPage:
            self.showMessage("Welcome to HEX" , self.RES[0] / 2, self.RES[1] / 10 * 8 + 5, BLACK, 50)
            self.showMessage("Welcome to HEX" , self.RES[0] / 2, self.RES[1] / 10 * 8, WHITE, 50)

            self.showMessage("HEX", 603,295, GRAY,200)
            self.showMessage("HEX", 600,300, BLACK,200)

            self.showMessage("This game was developed by Yogev Ben-Ivgy", self.RES[0] / 2, self.RES[1] / 9 * 8 + 5, BLACK, 36)
            self.showMessage("This game was developed by Yogev Ben-Ivgy", self.RES[0] / 2, self.RES[1] / 9 * 8, (95,135,95), 36)

            self.showMessage("To navigate through the menu use the up and down arrows (Enter to apply)", self.RES[0] / 2, self.RES[1] / 8 * 8 - 12 , BLACK, 30)



            if self.menuOption == "play":
                if pressedKey =="up":
                    self.menuOption = "quit"
                elif pressedKey =="down":
                    self.menuOption="about"

            elif self.menuOption == "about":
                if pressedKey == "up":
                    self.menuOption = "play"
                elif pressedKey == "down":
                    self.menuOption = "quit"

            elif self.menuOption == "quit":
                if pressedKey == "up":
                    self.menuOption = "about"
                elif pressedKey == "down":
                    self.menuOption = "play"
            self.play(150,150)
            self.about(150,250)
            self.quit(150,350)

            if pressedKey=="enter":
                if self.menuOption=="quit":
                    return "quit"
                elif self.menuOption=="play":
                    self.optionsPage=True

        else:
            return self.gameOptions(pressedKey)

            # return self.menuOption
        return "menu"


    def gameOptions(self,pressedKey):
        if self.settingSelection == "1v1":
            if pressedKey == "up":
                self.settingSelection = "back"

            elif pressedKey == "down":
                self.settingSelection = "easy"

        elif self.settingSelection  == "easy":
            if pressedKey == "up":
                self.settingSelection = "1v1"

            elif pressedKey == "down":
                self.settingSelection  = "average"

        elif self.settingSelection == "average":
            if pressedKey == "up":
                self.settingSelection = "easy"

            elif pressedKey == "down":
                self.settingSelection = "hard"

        elif self.settingSelection == "hard":
            if pressedKey == "up":
                self.settingSelection = "average"

            elif pressedKey == "down":
                self.settingSelection = "back"

        elif self.settingSelection == "back":
            if pressedKey == "up":
                self.settingSelection = "hard"

            elif pressedKey == "down":
                self.settingSelection = "1v1"

        if pressedKey == "enter":
            if self.settingSelection == "1v1":
                return "1v1"
            elif self.settingSelection == "easy":
                return "random"
            elif self.settingSelection == "average":
                return "dictionary"
            elif self.settingSelection == "hard":
                return "web"
            elif self.settingSelection == "back":
                self.optionsPage = False

        self._1v1(350,100)
        self.easy(350,200)
        self.average(350,300)
        self.hard(350,400)
        self.back(350,500)

        print(self.settingSelection, self.gameMode)



    def check_arrow_keys(self,keys):

        # Check for up arrow key
        if keys[pygame.K_UP] and not self.up_arrow_pressed:
            self.up_arrow_pressed = True
            return "up"  # Return "up" if up arrow key is pressed for the first time
        elif not keys[pygame.K_UP]:
            self.up_arrow_pressed = False

        # Check for down arrow key
        if keys[pygame.K_DOWN] and not self.down_arrow_pressed:
            self.down_arrow_pressed = True
            return "down"  # Return "down" if down arrow key is pressed for the first time
        elif not keys[pygame.K_DOWN]:
            self.down_arrow_pressed = False

        # Check for enter key
        if keys[pygame.K_RETURN] and not self.enter_pressed:
            self.enter_pressed = True
            return "enter"  # Return "enter" if enter key is pressed for the first time
        elif not keys[pygame.K_RETURN]:
            self.enter_pressed = False

        return None  # Return None if neither arrow key is pressed or if they are held down

    def play(self,x,y):
        if self.menuOption=="play":
            self.WIN.blit(self.play2Pic, (x, y))
        else:
            self.WIN.blit(self.play1Pic, (x, y))
    def _1v1(self,x,y):
        if self.settingSelection == "1v1":
            self.WIN.blit(self._1v1_2Pic, (x, y))
        else:
            self.WIN.blit(self._1v1_1Pic, (x, y))
    def quit(self,x,y):
        if self.menuOption == "quit":
            self.WIN.blit(self.quit2Pic, (x, y))
        else:
            self.WIN.blit(self.quit1Pic, (x, y))
    def average(self,x,y):
        if self.settingSelection == "average":
            self.WIN.blit(self.average2Pic, (x, y))
        else:
            self.WIN.blit(self.average1Pic, (x, y))
    def back(self,x,y):
        if self.settingSelection == "back":
            self.WIN.blit(self.back2Pic,(x, y))
        else:
            self.WIN.blit(self.back1Pic, (x, y))
    def easy(self,x,y):
        if self.settingSelection == "easy":
            self.WIN.blit(self.easy2Pic,(x, y))
        else:
            self.WIN.blit(self.easy1Pic, (x, y))
    def hard(self,x,y):
        if self.settingSelection == "hard":
            self.WIN.blit(self.hard2Pic,(x, y))
        else:
            self.WIN.blit(self.hard1Pic, (x, y))

    def about(self,x,y):
        if self.menuOption == "about":
            self.WIN.blit(self.about2Pic,(x, y))
        else:
            self.WIN.blit(self.about1Pic, (x, y))







    ''' Display things on the screen'''
    def draw(self):
        #Game enviorment
        self.WIN.fill(GREEN)
        self.draw_grid()


    # Shows a message on the screen
    def showMessage(self, str, x, y, color, size=72, font="Ariel"):
        FONT = pygame.font.SysFont(font, size)
        text_surface = FONT.render(str, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.WIN.blit(text_surface, text_rect)



