import Button
from Screen import Screen
import numpy as np
import random
import Hexagon
import Group
BLUE = (0,0,255)
RED = (200,0,0)

class Game(Screen):
    def __init__(self):
        super().__init__()
        self.blueTurn = True
        self.board=np.zeros((self.boardSize,self.boardSize))
        self.turnsLeft = self.boardSize*self.boardSize

        self.win=False
        self.blueWin=False

        self.cells = [(i, j) for i in range(self.boardSize) for j in range(self.boardSize)]
        self.top_node = (-1, 0)
        self.bottom_node = (self.boardSize, 0)
        self.left_node = (0, -1)
        self.right_node = (0, self.boardSize)
        self.ds_red = Group.DisjointSet(self.cells + [self.top_node, self.bottom_node])
        self.ds_blue = Group.DisjointSet(self.cells + [self.left_node, self.right_node])
        for i in range(self.boardSize):
            self.ds_red.union((0, i), self.top_node)
            self.ds_red.union((self.boardSize - 1, i), self.bottom_node)
            self.ds_blue.union((i, 0), self.left_node)
            self.ds_blue.union((i, self.boardSize - 1), self.right_node)


        self.blueWins = 0
        self.redWins = 0


    def newGame(self):
        #Reset the variables for a new game
        self.blueTurn = True
        self.board = np.zeros((self.boardSize, self.boardSize))
        self.turnsLeft = self.boardSize*self.boardSize
        self.win=False
        self.blueWin=False


        self.ds_red = Group.DisjointSet(self.cells + [self.top_node, self.bottom_node])
        self.ds_blue = Group.DisjointSet(self.cells + [self.left_node, self.right_node])
        for i in range(self.boardSize):
            self.ds_red.union((0, i), self.top_node)
            self.ds_red.union((self.boardSize - 1, i), self.bottom_node)
            self.ds_blue.union((i, 0), self.left_node)
            self.ds_blue.union((i, self.boardSize - 1), self.right_node)

        self.hexagons = [[0 for j in range(self.boardSize)] for i in range(self.boardSize)]
        for i in range(self.boardSize):
            for j in range(self.boardSize):
                self.hexagons[i][j] = (Hexagon.Hexagon(300 + 25 * j + 25 * 2 * i, 212 + 44 * j, 25))

        self.buttons = [[0 for j in range(self.boardSize)] for i in range(self.boardSize)]
        for i in range(self.boardSize):
            for j in range(self.boardSize):
                self.buttons[i][j] = (Button.Button_hex(300 + 25 * j + 25 * 2 * i, 212 + 44 * j, 25))

    def gameManager(self):
        self.draw() #Create the game enviorment
            #Random game
        if self.gameMode=="random":

            self.showMessage("Random mode", 140, 550, (0, 0, 0), 50)
            if not self.win:
                self.randomBlue(self.randomIndex())
                self.randomRed(self.randomIndex())


            #Regular game --> 1v1


        #Display info on the screen
        if self.gameMode != "random":
            self.showMessage("1v1 mode", 140, 550, (0, 0, 0), 50)
            if not self.win:
                self.pressHex()
                if self.blueTurn:
                    self.showMessage("Blue turn", 140, 500, (0, 0, 0))
                if not self.blueTurn:
                    self.showMessage("Red turn", 140, 500, (0, 0, 0))

        if self.win:
            if self.blueWin:
                self.showMessage("Blue wins", 140, 500, (0, 0, 0))
            else:
                self.showMessage("Red wins", 140, 500, (0, 0, 0))

        self.displayWins()



    def pressHex(self):
        for i in range(self.boardSize):
            for j in range(self.boardSize):
                if self.buttons[i][j].buttonPress():
                    if not self.hexagons[i][j].taken:
                        self.turnsLeft-=1

                        if self.blueTurn:
                            self.hexagons[i][j].color = BLUE
                            self.board[j][i]=1
                            self.checkWinner(j,i,"blue")

                        else:
                            self.hexagons[i][j].color = RED
                            self.board[j][i]=2
                            self.checkWinner(j, i, "red")

                        self.blueTurn=not self.blueTurn
                        self.hexagons[i][j].taken=True

    def checkWinner(self, i, j, player):
        code = 1 if player == 'blue' else 2
        self.board[i][j] = code
        for nei_i, nei_j in [(i + 1, j), (i + 1, j - 1), (i, j + 1), (i, j - 1), (i - 1, j), (i - 1, j + 1)]:
            if 0 <= nei_i < self.boardSize and 0 <= nei_j < self.boardSize and code == self.board[nei_i][nei_j]:
                if player == 'red':
                    self.ds_red.union((nei_i, nei_j), (i, j))
                else:
                    self.ds_blue.union((nei_i, nei_j), (i, j))
        if player=="blue":
            print(f'{self.winnerBlue()} ==> Blue')
        else:
            print(f'{self.winnerRed()} ==> Red')



    def winnerBlue(self):
        if self.ds_blue.find(self.left_node) == self.ds_blue.find(self.right_node):
            self.win=True
            self.blueWin=True
            self.blueWins+=1
            return True
        return False

    def winnerRed(self):
        if self.ds_red.find(self.top_node) == self.ds_red.find(self.bottom_node):
            self.win=True
            self.redWins+=1
            return True
        return False


    def displayWins(self):
        self.showMessage(f"Blue: {self.blueWins} wins",450,75, BLUE,font="Corbel")
        self.showMessage(f"Red: {self.redWins} wins",450,140, RED,font="Corbel")

    '''Random moves for blue and red'''
    def randomIndex(self): #Returns tuple of the random index
        i = random.randint(0, self.boardSize-1)
        j = random.randint(0, self.boardSize-1)
        while  self.hexagons[i][j].taken and self.turnsLeft>0:
            i = random.randint(0, self.boardSize-1)
            j = random.randint(0, self.boardSize-1)
        return (i,j)


    def randomBlue(self, index):
        self.hexagons[(index[0])][index[1]].color = BLUE
        self.board[index[1]][index[0]] = 1
        self.blueTurn = False

        self.hexagons[index[0]][index[1]].taken = True
        self.checkWinner(index[1],index[0],"blue")
        self.turnsLeft -= 1

    def randomRed(self,index):
        self.hexagons[(index[0])][index[1]].color = RED
        self.board[index[1]][index[0]] = 2
        self.blueTurn=True

        self.hexagons[index[0]][index[1]].taken = True
        self.checkWinner(index[1],index[0],"red")

        self.turnsLeft -= 1

    def neighbors(self,index): #Returns a list of the neighbors of a caertain hexagon
        neighbors=[]
        row , col = index

        if row-1>=0:
            neighbors.append((row-1,col))
            if col+1<self.boardSize:
                neighbors.append((row-1,col+1))
        if col-1>=0:
            neighbors.append((row,col-1))
        if col + 1 < self.boardSize:
            neighbors.append((row, col + 1))

        if row+1<self.boardSize:
            neighbors.append((row+1,col))
            if col - 1 >= 0:
                neighbors.append((row+1, col - 1))
        return neighbors

