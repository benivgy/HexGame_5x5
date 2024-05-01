import pygame

import Button
from Screen import Screen
import numpy as np
import random
import Hexagon
import Group
import Dictionary
BLUE = (0,0,150)
RED = (150,0,0)
BLACK = (0,0,0)

class Game(Screen):
    def __init__(self):
        super().__init__()

        # Initialize game state variables
        self.blueTurn = True  # Indicates if it's currently blue player's turn
        self.board = np.zeros((self.boardSize, self.boardSize))  # Represents the game board
        self.win = False  # Indicates if the game has been won
        self.blueWin = False  # Indicates if the blue player has won

        '''Winning check:'''
        # Define board positions
        self.cells = [(i, j) for i in range(self.boardSize) for j in range(self.boardSize)]
        self.top_node = (-1, 0)
        self.bottom_node = (self.boardSize, 0)
        self.left_node = (0, -1)
        self.right_node = (0, self.boardSize)

        # Initialize disjoint sets for red and blue players
        self.ds_red = Group.DisjointSet(self.cells + [self.top_node, self.bottom_node])
        self.ds_blue = Group.DisjointSet(self.cells + [self.left_node, self.right_node])

        # Connect boundary cells to corresponding boundary nodes
        for i in range(self.boardSize):
            self.ds_red.union((0, i), self.top_node)
            self.ds_red.union((self.boardSize - 1, i), self.bottom_node)
            self.ds_blue.union((i, 0), self.left_node)
            self.ds_blue.union((i, self.boardSize - 1), self.right_node)

        # Initialize win counts
        self.blueWins = 0
        self.redWins = 0


        # reinforcment learning

        self.diction_1to5 = {}
        self.diction_1to5JSON = Dictionary.Dict("dictionaries/diction1-5.json")

        self.diction_6to10 = {}
        self.diction_6to10JSON = Dictionary.Dict("dictionaries/diction6-10.json")

        self.diction_11to15 = {}
        self.diction_11to15JSON = Dictionary.Dict("dictionaries/diction11-15.json")

        self.diction_16to20 = {}
        self.diction_16to20JSON = Dictionary.Dict("dictionaries/diction16-20.json")

        self.diction_21to25 = {}
        self.diction_21to25JSON = Dictionary.Dict("dictionaries/diction21-25.json")

        self.diction_1to5 = self.diction_1to5JSON.dic
        self.diction_6to10 = self.diction_6to10JSON.dic
        self.diction_11to15 = self.diction_11to15JSON.dic
        self.diction_16to20 = self.diction_16to20JSON.dic
        self.diction_21to25 = self.diction_21to25JSON.dic
        self.moves = 1




    def newGame(self):
        #Reset the variables for a new game
        self.blueTurn = True
        self.board = np.zeros((self.boardSize, self.boardSize))
        self.win=False
        self.blueWin=False

        # Reset disjoint sets for red and blue players
        self.ds_red = Group.DisjointSet(self.cells + [self.top_node, self.bottom_node])
        self.ds_blue = Group.DisjointSet(self.cells + [self.left_node, self.right_node])

        # Reconnect boundary cells to corresponding boundary nodes
        for i in range(self.boardSize):
            self.ds_red.union((0, i), self.top_node)
            self.ds_red.union((self.boardSize - 1, i), self.bottom_node)
            self.ds_blue.union((i, 0), self.left_node)
            self.ds_blue.union((i, self.boardSize - 1), self.right_node)

        # Reinitialize hexagons and buttons
        self.hexagons = [[0 for j in range(self.boardSize)] for i in range(self.boardSize)]
        for i in range(self.boardSize):
            for j in range(self.boardSize):
                self.hexagons[i][j] = (Hexagon.Hexagon(300 + 25 * j + 25 * 2 * i, 212 + 44 * j, 25))

        self.buttons = [[0 for j in range(self.boardSize)] for i in range(self.boardSize)]
        for i in range(self.boardSize):
            for j in range(self.boardSize):
                self.buttons[i][j] = (Button.Button_hex(300 + 25 * j + 25 * 2 * i, 212 + 44 * j, 25))

        self.moves=1

    def gameManager(self):
        keys = pygame.key.get_pressed()
        if self.showMenu:
            self.gameMode=self.menu(keys)
            if self.gameMode=="quit":
                self.showMenu=False
                return "quit"
            elif self.gameMode in ["1v1","random","dictionary"]:
                self.showMenu=False
        else:
            self.draw() #Create the game enviorment
                #Random game
            if self.gameMode=="random":
                self.showMessage("Easy mode", 140, 550, (0, 0, 0), 50)
                if not self.win:
                    if self.blueTurn:
                        self.showMessage("Blue turn", 140, 500, BLUE)
                        self.showMessage("Blue turn", 140, 503, BLACK)
                        self.pressHex()


                    if not self.blueTurn and not self.win:
                        self.randomRed(self.randomIndex())


                #Regular game --> 1v1
            #Display info on the screen
            if self.gameMode == "1v1":
                self.showMessage("1v1 mode", 140, 550, (0, 0, 0), 50)
                if not self.win:
                    self.pressHex()
                    if self.blueTurn:
                        self.showMessage("Blue turn", 140, 500, BLUE)
                        self.showMessage("Blue turn", 140, 503, BLACK)

                    if not self.blueTurn:
                        self.showMessage("Red turn", 140, 500, RED)
                        self.showMessage("Red turn", 140, 503, BLACK)


            if self.gameMode == "dictionary":
                self.showMessage("Average mode", 140, 550, (0, 0, 0), 50)
                if not self.win:
                    if self.blueTurn:
                        self.showMessage("Blue turn", 140, 500, BLUE)
                        self.showMessage("Blue turn", 140, 503, BLACK)
                        self.pressHex()

                        if not self.blueTurn and not self.win:
                            self.smartMove()


            if keys[pygame.K_ESCAPE]:
                self.showMenu=True
            if self.win:
                if self.blueWin:
                    self.showMessage("Blue wins", 140, 500, BLUE)
                    self.showMessage("Blue wins", 140, 503, BLACK)

                else:
                    self.showMessage("Red wins", 140, 500, RED)
                    self.showMessage("Red wins", 140, 503,BLACK)

            self.displayWins()



    def pressHex(self):
        for i in range(self.boardSize):
            for j in range(self.boardSize):
                if self.buttons[i][j].buttonPress():
                    if not self.hexagons[i][j].taken:

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
                        self.moves += 1


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
            self.winnerBlue()
        if player =="red":
            self.winnerRed()




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
        while  self.hexagons[i][j].taken:
            i = random.randint(0, self.boardSize-1)
            j = random.randint(0, self.boardSize-1)
        return (i,j)


    def randomBlue(self, index):
        self.hexagons[(index[0])][index[1]].color = BLUE
        self.board[index[1]][index[0]] = 1
        self.blueTurn = False

        self.hexagons[index[0]][index[1]].taken = True
        self.checkWinner(index[1],index[0],"blue")

    def randomRed(self,index):
        self.hexagons[(index[0])][index[1]].color = RED
        self.board[index[1]][index[0]] = 2
        self.blueTurn=True
        self.hexagons[index[0]][index[1]].taken = True
        self.checkWinner(index[1],index[0],"red")
        self.moves+=1



    def smartMove_index(self):
        #Returns the index of the cell --> dictionary
        row = -1
        col = -1
        if not self.blueTurn:
            maxGrade = -1
            for i in range(self.boardSize):
                for j in range(self.boardSize):
                    if not self.hexagons[j][i].taken:
                        self.board[i][j] = 2
                        stringBoard = self.hash()

                        if 1 <= self.moves <= 5:
                            if stringBoard in self.diction_1to5JSON.dic and self.diction_1to5JSON.dic[stringBoard][
                                0] > maxGrade:
                                maxGrade = self.diction_1to5JSON.dic[stringBoard][0]
                                row = i
                                col = j
                                # print("diction 1")

                        elif 6 <= self.moves <= 10:
                            if stringBoard in self.diction_6to10JSON.dic and self.diction_6to10JSON.dic[stringBoard][
                                0] > maxGrade:
                                maxGrade = self.diction_6to10JSON.dic[stringBoard][0]
                                row = i
                                col = j
                                # print("diction 2")


                        elif 11 <= self.moves <= 15:
                            if stringBoard in self.diction_11to15JSON.dic and self.diction_11to15JSON.dic[stringBoard][
                                0] > maxGrade:
                                maxGrade = self.diction_11to15JSON.dic[stringBoard][0]
                                row = i
                                col = j
                                # print("diction 3")


                        elif 16 <= self.moves <= 20:
                            if stringBoard in self.diction_16to20JSON.dic and self.diction_16to20JSON.dic[stringBoard][
                                0] > maxGrade:
                                maxGrade = self.diction_16to20JSON.dic[stringBoard][0]
                                row = i
                                col = j
                                # print("diction 4")

                        else:
                            if stringBoard in self.diction_21to25JSON.dic and self.diction_21to25JSON.dic[stringBoard][
                                0] > maxGrade:
                                maxGrade = self.diction_21to25JSON.dic[stringBoard][0]
                                row = i
                                col = j
                                # print("diction 5")

                        self.board[i][j] = 0
            if row == -1 and col == -1:
                print("random")
                return "random"

            self.board[row][col] = 2
            self.blueTurn = True

        return (row, col)

    def smartMove(self):
        smart = self.smartMove_index()
        if smart=="random":
            self.randomRed(self.randomIndex())
        else:
            i, j = smart
            self.board[i][j] = 2
            self.hexagons[j][i].color = RED
            self.hexagons[j][i].taken = True
            self.blueTurn = True
            self.checkWinner(i, j, "red")
            self.moves+=1


    def hash(self):
        str = np.array2string(self.board)
        str1 = ""
        for i in str:
            if i in ['1', '0', '2']:
                str1 += i
        return str1
