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
GRAY = (75,75,75)
WHITE = (255,255,255)
GREEN = (76,208,56)
BLACK = (0,0,0)
BLUE = (0,0,255)
BLUE_dark = (0,0,75)


pygame.init()
class Screen:

    def __init__(self):
        #Screen resolution
        self.RES= (900,600)

        #Set the window
        self.WIN = pygame.display.set_mode(self.RES)
        self.FPS = 60

        # The clock will control the number of times the screen refreshes
        self.clock = pygame.time.Clock()

        self.gameMode="1v1" # 1v1 , random , none

        self.boardSize=5

        ''' Menus '''
        #Pregame
        self.menu_surface = pygame.Surface(self.RES, pygame.SRCALPHA)
        self.menu_surface.fill((0, 0, 0, 200))  # The last value (128) represents the alpha (transparency)

        #Random mode:
        #Pictures for the button
        self.randomOnPic=pygame.image.load('images/switchON.png')
        self.randomOnPic = pygame.transform.scale(self.randomOnPic, (200,100))
        self.onRect = self.randomOnPic.get_rect()

        self.randomOffPic = pygame.image.load('images/switchOFF.png')
        self.randomOffPic = pygame.transform.scale(self.randomOffPic, (200, 100))
        self.offRect = self.randomOffPic.get_rect()
        #Button:
        self.randomMode_button = Button.Button_rect(self.RES[0]/2,0.6*self.RES[1])

        #Endgame
        # self.closeGame = pygame.image.load('images/I Quit .png')
        # self.closeGame=pygame.transform.scale(self.closeGame, (200,200))

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
        if hex.color == WHITE:
            width=3
        if hex.color!=WHITE:
            pygame.draw.polygon(self.WIN, (0,0,0),shadow.points,width)
        pygame.draw.polygon(self.WIN, hex.color,hex.points,width)




    def draw_grid(self):
        for i in range(self.boardSize):
            for j in range(self.boardSize):
                self.draw_hexagon(self.hexagons[i][j],self.hexagons_Shadow[i][j])



    #Start / continue game manu
    def menu(self,start_or_continue):
        self.draw()
        self.WIN.blit(self.menu_surface, (0, 0))

        self.showMessage("Press SPACE to "+start_or_continue, self.RES[0]/2, self.RES[1]/10*8+5, BLACK,50)
        self.showMessage("Press SPACE to "+start_or_continue, self.RES[0]/2, self.RES[1]/10*8, WHITE,50)

        self.showMessage("Hex",self.RES[0]/2,self.RES[1]/3,GRAY,250)
        self.showMessage("Hex", self.RES[0] / 2, self.RES[1] / 3+5, BLACK, 250)

        if self.gameMode=="random":
            self.randomMode_button.showButton(self.randomOnPic,self.onRect,self.WIN)
            if self.randomMode_button.buttonPress():
                self.gameMode="1v1"
        if self.gameMode != "random":
            self.randomMode_button.showButton(self.randomOffPic,self.onRect,self.WIN)
            if self.randomMode_button.buttonPress():
                self.gameMode="random"

        self.showMessage("Random Mode",self.RES[0]/2,0.6*self.RES[1]+2,BLACK,40)
        self.showMessage("Random Mode",self.RES[0]/2,0.6*self.RES[1],GRAY,40)




    ''' Display things on the screen'''
    def draw(self):
        #Game enviorment
        self.WIN.fill(GREEN)
        self.draw_grid()

    #Show a picture on the screen
    def show(self, pic):
        self.WIN.blit(pic.pic, pic.rect)

    # Shows a message on the screen
    def showMessage(self, str, x, y, color,size=72):
        FONT = pygame.font.SysFont('Corbel', size)
        text_surface = FONT.render(str, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.WIN.blit(text_surface, text_rect)


    #End game manu
    def gameOver(self,score):
        self.WIN.fill(GRAY)
        self.showMessage("GAME OVER - You lost", self.RES[0] / 2, self.RES[1] / 10 * 8+5, BLACK, 50)
        self.showMessage("GAME OVER - You lost", self.RES[0] / 2, self.RES[1] / 10 * 8, WHITE, 50)
        self.showMessage(f"SCORE: {score}", self.RES[0] / 2 , self.RES[1] / 10+7, BLACK, 100)
        self.showMessage(f"SCORE: {score}", self.RES[0] / 2, self.RES[1] / 10, RED, 100)

        exitBtn = Button.Button(150,150)
        self.WIN.blit(self.closeGame,(150,150))
        if exitBtn.buttonPress(self.WIN):
            return False
        return True



