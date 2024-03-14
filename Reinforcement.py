import random
import Group
import numpy as np
import Dictionary
class Learning:
    def __init__(self,boardSize):
        self.board = np.zeros((boardSize, boardSize))
        self.gama = 0.9
        self.epsilon = 0.0001
        self.matchList = []
        self.blueTurn = True

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



        self.turnsLeft = boardSize*boardSize
        self.moves=1
        self.boardSize=boardSize

        self.win = False
        self.blueWin = False
        self.winner = ""

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
    def newGame(self):
        self.board = np.zeros((self.boardSize, self.boardSize))
        self.matchList = []
        self.blueTurn = True

        self.turnsLeft = self.boardSize * self.boardSize
        self.moves=1

        self.win = False
        self.blueWin = False
        self.winner = ""

        self.ds_red = Group.DisjointSet(self.cells + [self.top_node, self.bottom_node])
        self.ds_blue = Group.DisjointSet(self.cells + [self.left_node, self.right_node])
        for i in range(self.boardSize):
            self.ds_red.union((0, i), self.top_node)
            self.ds_red.union((self.boardSize - 1, i), self.bottom_node)
            self.ds_blue.union((i, 0), self.left_node)
            self.ds_blue.union((i, self.boardSize - 1), self.right_node)




    def hash(self):
        str = np.array2string(self.board)
        str1 = ""
        for i in str:
            if i in ['1', '0', '2']:
                str1 += i
        return str1

    def randomIndex(self):  # Returns tuple of the random index
        i = random.randint(0, self.boardSize - 1)
        j = random.randint(0, self.boardSize - 1)
        while self.board[i][j]!= 0:
            i = random.randint(0, self.boardSize - 1)
            j = random.randint(0, self.boardSize - 1)
        return (i, j)

    def randomBlue(self, index):
        i,j = index
        self.board[i][j] = 1
        self.blueTurn = False
        self.checkWinner(i, j, "blue")
        self.turnsLeft -= 1
        self.moves+=1


    def randomRed(self, index):
        i,j = index
        self.board[i][j] = 2
        self.blueTurn = True
        self.checkWinner(i, j, "red")
        self.turnsLeft -= 1
        self.moves+=1
    def checkWinner(self, i, j, player):
        code = 1 if player == 'blue' else 2
        self.board[i][j] = code
        for nei_i, nei_j in [(i + 1, j), (i + 1, j - 1), (i, j + 1), (i, j - 1), (i - 1, j), (i - 1, j + 1)]:
            if 0 <= nei_i < self.boardSize and 0 <= nei_j < self.boardSize and code == self.board[nei_i][nei_j]:
                if player == 'red':
                    self.ds_red.union((nei_i, nei_j), (i, j))
                else:
                    self.ds_blue.union((nei_i, nei_j), (i, j))
        if self.winnerBlue():
            self.winner= "blue"
        elif self.winnerRed():
            self.winner= "red"




    def winnerBlue(self):
        if self.ds_blue.find(self.left_node) == self.ds_blue.find(self.right_node):
            self.win=True
            self.blueWin=True
            return True
        return False

    def winnerRed(self):
        if self.ds_red.find(self.top_node) == self.ds_red.find(self.bottom_node):
            self.win=True
            return True
        return False

    def randomVSrandom(self):
        while not self.win:
            if self.blueTurn:
                self.randomBlue(self.randomIndex())
            else:
                self.randomRed(self.randomIndex())
            self.matchList.append(self.hash())
            # print(self.board)
            # print(self.win)
        return self.winner

    def humanVSsmart_player(self):
        while not self.win:
            if self.blueTurn:
                user_input = input("Enter your move, separated with a comma: ")
                i,j =  tuple(int(x) for x in user_input.split(","))
                self.board[i][j] = 1
                self.blueTurn = False
                self.checkWinner(i, j, "blue")
                self.moves += 1

            else:
                i,j = self.smartMove()
                self.board[i][j] = 2
                self.blueTurn = True
                self.checkWinner(i, j, "red")
                self.moves += 1

            print(self.board)
            print(self.hash())

            # print(self.win)
        return self.winner

    def grading(self,reward):
        reversedLst = self.matchList[::-1]
        for i in range(len(reversedLst)):
            # if reversedLst[i] not in self.diction:
            #     self.diction[reversedLst[i]] = (pow(self.gama, i) * reward, 1)
            # else:
            #     newMark = (self.diction[reversedLst[i]][0] * self.diction[reversedLst[i]][1] + pow(self.gama,
            #                                                                                        i) * reward) / (
            #                           self.diction[reversedLst[i]][1] + 1)
            #     self.diction[reversedLst[i]] = (newMark, self.diction[reversedLst[i]][1] + 1)
            if 1<=len(reversedLst)-i<=5:
                if reversedLst[i] not in self.diction_1to5:
                    self.diction_1to5[reversedLst[i]]=(pow(self.gama,i)*reward,1)
                else:
                    newMark = (self.diction_1to5[reversedLst[i]][0]*self.diction_1to5[reversedLst[i]][1]+pow(self.gama,i)*reward)/(self.diction_1to5[reversedLst[i]][1]+1)
                    self.diction_1to5[reversedLst[i]]=(newMark,self.diction_1to5[reversedLst[i]][1]+1)
            elif 6<=len(reversedLst)-i<=10:
                if reversedLst[i] not in self.diction_6to10:
                    self.diction_6to10[reversedLst[i]]=(pow(self.gama,i)*reward,1)
                else:
                    newMark = (self.diction_6to10[reversedLst[i]][0]*self.diction_6to10[reversedLst[i]][1]+pow(self.gama,i)*reward)/(self.diction_6to10[reversedLst[i]][1]+1)
                    self.diction_6to10[reversedLst[i]]=(newMark,self.diction_6to10[reversedLst[i]][1]+1)
            elif 11<=len(reversedLst)-i<=15:
                if reversedLst[i] not in self.diction_11to15:
                    self.diction_11to15[reversedLst[i]]=(pow(self.gama,i)*reward,1)
                else:
                    newMark = (self.diction_11to15[reversedLst[i]][0]*self.diction_11to15[reversedLst[i]][1]+pow(self.gama,i)*reward)/(self.diction_11to15[reversedLst[i]][1]+1)
                    self.diction_11to15[reversedLst[i]]=(newMark,self.diction_11to15[reversedLst[i]][1]+1)
            elif 16<=len(reversedLst)-i<=20:
                if reversedLst[i] not in self.diction_16to20:
                    self.diction_16to20[reversedLst[i]]=(pow(self.gama,i)*reward,1)
                else:
                    newMark = (self.diction_16to20[reversedLst[i]][0]*self.diction_16to20[reversedLst[i]][1]+pow(self.gama,i)*reward)/(self.diction_16to20[reversedLst[i]][1]+1)
                    self.diction_16to20[reversedLst[i]]=(newMark,self.diction_16to20[reversedLst[i]][1]+1)
            else:
                if reversedLst[i] not in self.diction_21to25:
                    self.diction_21to25[reversedLst[i]]=(pow(self.gama,i)*reward,1)
                else:
                    newMark = (self.diction_21to25[reversedLst[i]][0]*self.diction_21to25[reversedLst[i]][1]+pow(self.gama,i)*reward)/(self.diction_21to25[reversedLst[i]][1]+1)
                    self.diction_21to25[reversedLst[i]]=(newMark,self.diction_21to25[reversedLst[i]][1]+1)

    def smartMove(self):
            row = -1
            col = -1
            if not self.blueTurn:
                maxGrade = -1
                for i in range(self.boardSize):
                    for j in range(self.boardSize):
                        if self.board[i][j] == 0:
                            self.board[i][j] = 2
                            stringBoard = self.hash()

                            if 1 <= self.moves <= 5:
                                if stringBoard in self.diction_1to5JSON.dic and self.diction_1to5JSON.dic[stringBoard][0] > maxGrade:
                                    maxGrade = self.diction_1to5JSON.dic[stringBoard][0]
                                    row = i
                                    col = j

                            elif 6 <= self.moves <= 10:
                                if stringBoard in self.diction_6to10JSON.dic and self.diction_6to10JSON.dic[stringBoard][0] > maxGrade:
                                    maxGrade = self.diction_6to10JSON.dic[stringBoard][0]
                                    row = i
                                    col = j

                            elif 11 <= self.moves <= 15:
                                if stringBoard in self.diction_11to15JSON.dic and self.diction_11to15JSON.dic[stringBoard][0] > maxGrade:
                                    maxGrade = self.diction_11to15JSON.dic[stringBoard][0]
                                    row = i
                                    col = j

                            elif 16 <= self.moves <= 20:
                                if stringBoard in self.diction_16to20JSON.dic and self.diction_16to20JSON.dic[stringBoard][0] > maxGrade:
                                    maxGrade = self.diction_16to20JSON.dic[stringBoard][0]
                                    row = i
                                    col = j
                            else:
                                if stringBoard in self.diction_21to25JSON.dic and self.diction_21to25JSON.dic[stringBoard][0] > maxGrade:
                                    maxGrade = self.diction_21to25JSON.dic[stringBoard][0]
                                    row = i
                                    col = j


                            self.board[i][j] = 0
                if row==-1 and col==-1:
                    # print("random")
                    row, col = self.randomIndex()


                self.board[row][col] = 2
                self.blueTurn = True

            return (row,col)

def terminalGame():
    lr = Learning(5)
    print(lr.humanVSsmart_player())
    lr.newGame()

def milGames():
    lr = Learning(5)
    for i in range(10000):
        winner = lr.randomVSrandom()
        if winner=="red":
           lr.grading(1)
        else:
            lr.grading(-1)
        if i%100000==0:
            print(i)
        lr.newGame()

    lr.diction_1to5JSON.dumpDic(lr.diction_1to5)
    lr.diction_6to10JSON.dumpDic(lr.diction_6to10)
    lr.diction_11to15JSON.dumpDic(lr.diction_11to15)
    lr.diction_16to20JSON.dumpDic(lr.diction_16to20)
    lr.diction_21to25JSON.dumpDic(lr.diction_21to25)

    # lr.dictionJSON.dumpDic(lr.diction)

if __name__=="__main__":
    # milGames()
    while True:
        terminalGame()
