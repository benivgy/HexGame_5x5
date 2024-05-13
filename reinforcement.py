import copy
import random
import Group
import numpy as np
import Dictionary
from tensorflow import keras

class Learning:
    def __init__(self,boardSize):
        self.board = np.zeros((boardSize, boardSize))
        self.gama = 0.9
        self.epsilon = 0.0001
        self.matchList = []
        self.dicList=[]
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

        self.diction_1to5 = self.diction_1to5JSON.dic
        self.dicList.append(self.diction_1to5)

        self.diction_6to10 = self.diction_6to10JSON.dic
        self.dicList.append(self.diction_6to10)

        self.diction_11to15 = self.diction_11to15JSON.dic
        self.dicList.append(self.diction_11to15)

        self.diction_16to20 = self.diction_16to20JSON.dic
        self.dicList.append(self.diction_16to20)

        self.diction_21to25 = self.diction_21to25JSON.dic
        self.dicList.append(self.diction_21to25)

        self.webModel = keras.models.load_model('my_model.h5')


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
        #Reset the variables for a new game

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
        return self.winner

    def smart70VSrandom(self):
        while not self.win:
            if self.blueTurn:
                self.randomBlue(self.randomIndex())
            else:
                smartORrandom = random.random()
                if smartORrandom <=-10:
                    self.randomRed(self.randomIndex())
                else:
                    i, j = self.smartMove()
                    self.board[i][j] = 2
                    self.blueTurn = True
                    self.checkWinner(i, j, "red")
                    self.moves += 1
            self.matchList.append(self.hash())
        return self.winner

    def smart_playerVSrandom(self):
        while not self.win:
            if self.blueTurn:
                self.randomBlue(self.randomIndex())
            else:
                i, j = self.smartMove()
                self.board[i][j] = 2
                self.blueTurn = True
                self.checkWinner(i, j, "red")
                self.moves += 1

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

            self.matchList.append(self.hash())
            print(self.board)

            # print(self.win)
        return self.winner

    def grading(self,reward):
        reversedLst = self.matchList[::-1]
        for i in range(len(reversedLst)):
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
                                    # print("diction 1")

                            elif 6 <= self.moves <= 10:
                                if stringBoard in self.diction_6to10JSON.dic and self.diction_6to10JSON.dic[stringBoard][0] > maxGrade:
                                    maxGrade = self.diction_6to10JSON.dic[stringBoard][0]
                                    row = i
                                    col = j
                                    # print("diction 2")


                            elif 11 <= self.moves <= 15:
                                if stringBoard in self.diction_11to15JSON.dic and self.diction_11to15JSON.dic[stringBoard][0] > maxGrade:
                                    maxGrade = self.diction_11to15JSON.dic[stringBoard][0]
                                    row = i
                                    col = j
                                    # print("diction 3")


                            elif 16 <= self.moves <= 20:
                                if stringBoard in self.diction_16to20JSON.dic and self.diction_16to20JSON.dic[stringBoard][0] > maxGrade:
                                    maxGrade = self.diction_16to20JSON.dic[stringBoard][0]
                                    row = i
                                    col = j
                                    # print("diction 4")

                            else:
                                if stringBoard in self.diction_21to25JSON.dic and self.diction_21to25JSON.dic[stringBoard][0] > maxGrade:
                                    maxGrade = self.diction_21to25JSON.dic[stringBoard][0]
                                    row = i
                                    col = j
                                    # print("diction 5")



                            self.board[i][j] = 0
                if row==-1 and col==-1:
                    # print("random")
                    row, col = self.randomIndex()


                self.board[row][col] = 2
                self.blueTurn = True

            return (row,col)
    def getWebGrade(self):
        data_array = np.array(list(map(int, self.hash())))
        return self.webModel.predict(data_array.reshape(1, -1))[0][0]
    def smartMove_web(self):
        if not self.blueTurn:
            maxGrade = -1
            for i in range(self.boardSize):
                for j in range(self.boardSize):
                    if  self.board[i][j] == 0:
                        self.board[i][j] = 2
                        grade=self.getWebGrade()
                        if grade>maxGrade:
                            maxGrade=grade
                            row=i
                            col=j
                        self.board[i][j]=0
            self.board[row][col] = 2
            self.blueTurn = True
            self.checkWinner(row, col, "red")
            self.moves += 1
    def randomVSnetwork(self):
        while not self.win:
            if self.blueTurn:
               self.randomBlue(self.randomIndex())
            else:
               self.smartMove_web()

        return self.winner


def terminalGame(lr):
    for i in range(1):
        winner = lr.humanVSsmart_player()
        print(winner)
        lr.newGame()


def networkGames(lr,games):
    redWins = 0
    blueWins = 0
    games = int(games)
    for i in range(games):
        winner=lr.randomVSnetwork()
        if winner == "red":
            redWins += 1
        else:
            blueWins += 1
        if i % 10000 == 0:
            print(i)
        lr.newGame()

    print(
        f"Blue wins: {blueWins}-->{blueWins / (blueWins + redWins) * 100}%\nRed wins: {redWins} -->{redWins / (blueWins + redWins) * 100}%")


def cleanDic(lr):
    lr.diction_1to5={key: value for key, value in lr.diction_1to5.items() if not (-0.2 <= value[0] <= 0.2)}
    lr.diction_6to10={key: value for key, value in lr.diction_6to10.items() if not (-0.2 <= value[0] <= 0.2)}
    lr.diction_11to15={key: value for key, value in lr.diction_11to15.items() if not (-0.2 <= value[0] <= 0.2)}
    lr.diction_16to20={key: value for key, value in lr.diction_16to20.items() if not (-0.2 <= value[0] <= 0.2)}
    lr.diction_21to25={key: value for key, value in lr.diction_21to25.items() if not (-0.2 <= value[0] <= 0.2)}


    lr.diction_1to5JSON.dumpDic(lr.diction_1to5)
    lr.diction_6to10JSON.dumpDic(lr.diction_6to10)
    lr.diction_11to15JSON.dumpDic(lr.diction_11to15)
    lr.diction_16to20JSON.dumpDic(lr.diction_16to20)
    lr.diction_21to25JSON.dumpDic(lr.diction_21to25)
def statistics(lr):
    #Print the number of boards for each dictionary -> overall 43,455,945 boards out of 3^25 possible (8.47*10^11)
    x=len(lr.diction_1to5JSON.dic.values())+len(lr.diction_6to10JSON.dic.values())+len(lr.diction_16to20JSON.dic.values())+len(lr.diction_11to15JSON.dic.values())+len(lr.diction_21to25JSON.dic.values())
    print(len(lr.diction_1to5JSON.dic.values()))
    print(len(lr.diction_6to10JSON.dic.values()))
    print(len(lr.diction_11to15JSON.dic.values()))
    print(len(lr.diction_16to20JSON.dic.values()))
    print(len(lr.diction_21to25JSON.dic.values()))
    print(x)

def train_70_30(gamesNumber,lr):
    gamesNumber = int(gamesNumber)
    print("___________________")
    for i in range(gamesNumber):
        winner = lr.smart70VSrandom()
        if winner=="red":
           lr.grading(1)
        else:
            lr.grading(-1)
        if i%10000==0:
            print(i)
        lr.newGame()

    lr.diction_1to5JSON.dumpDic(lr.diction_1to5)
    lr.diction_6to10JSON.dumpDic(lr.diction_6to10)
    lr.diction_11to15JSON.dumpDic(lr.diction_11to15)
    lr.diction_16to20JSON.dumpDic(lr.diction_16to20)
    lr.diction_21to25JSON.dumpDic(lr.diction_21to25)

def checkWinningRate(gamesNumber,lr):
    redWins = 0
    blueWins =0
    gamesNumber = int(gamesNumber)
    for i in range(gamesNumber):
        winner = lr.smart_playerVSrandom()
        # print(winner)
        if winner=="red":
            redWins+=1
        else:
            blueWins+=1
        if i%10000==0:
            print(i)
        lr.newGame()

    print(f"Blue wins: {blueWins}-->{blueWins/(blueWins+redWins)*100}%\nRed wins: {redWins} -->{redWins/(blueWins+redWins)*100}%")



def train(gamesNumber,lr):
    gamesNumber=int(gamesNumber)
    for i in range(gamesNumber):
        winner = lr.randomVSrandom()
        if winner=="red":
           lr.grading(1)
        else:
            lr.grading(-1)
        if i%10000==0:
            print(i)
        lr.newGame()

    lr.diction_1to5JSON.dumpDic(lr.diction_1to5)
    lr.diction_6to10JSON.dumpDic(lr.diction_6to10)
    lr.diction_11to15JSON.dumpDic(lr.diction_11to15)
    lr.diction_16to20JSON.dumpDic(lr.diction_16to20)
    lr.diction_21to25JSON.dumpDic(lr.diction_21to25)

    # lr.dictionJSON.dumpDic(lr.diction)

def erase(lr):

    lr.diction_1to5 = {}
    lr.diction_6to10 = {}
    lr.diction_11to15 = {}
    lr.diction_16to20 = {}
    lr.diction_21to25 = {}

    lr.diction_1to5JSON.dumpDic(lr.diction_1to5)
    lr.diction_6to10JSON.dumpDic(lr.diction_6to10)
    lr.diction_11to15JSON.dumpDic(lr.diction_11to15)
    lr.diction_16to20JSON.dumpDic(lr.diction_16to20)
    lr.diction_21to25JSON.dumpDic(lr.diction_21to25)

def convertTOcsv(lr):
    with open('nl_data.csv', 'w') as output_file:
        for dic in lr.dicList:
            for key in dic:
                k = [*key]
                str1 = ''
                for x in k:
                    str1 = str1 + x + ','
                output_file.write("%s,%s\n" % (str1[:-1],dic[key][0]))
    output_file.close()


if __name__=="__main__":
    print("Loading dictionaries")
    lr = Learning(5)
    run=True
    while run:
        print("Welcome to the reinforcement learning section of the project")
        print("Chose an option:")
        print("1 - play 3 million games")
        print("2 - play against a smart player")
        print("3 - clean the dictionary (removes all the values between -0.2 to 0.2)")
        print("4 - show information")
        print("5 - 70-30")
        print("6 - check winning rate")
        print("7 - Erase dictionaries")
        print("8 - Export to a CSV file")
        print("9 - Neural Network winning rate")

        print("-99 - EXIT")

        mode = input()
        while int(mode) not in [1,2,3,4,5,6,7,8,9,-99]:
            mode=input("Invalid input, try again")

        mode=int(mode)

        if mode==1:
            print("playing 3 million games...")
            train(input("Enter number of games to play: "),lr)
        elif mode==2:
            print("playing against a smart player...")
            while True:
                terminalGame(lr)
        elif mode==3:
            print("Cleaning dic...")
            cleanDic(lr)
        elif mode ==4:
            print("Showing statistics...")
            statistics(lr)
        elif mode == 5:
            print("Plating 70-30...")
            games_to_play=input("Enter number of games: ")
            train_70_30(games_to_play,lr)
        elif mode==6:
            print("Playing smart games")
            games_to_play=input("Enter number of games: ")
            checkWinningRate(games_to_play,lr)
        elif mode==7:
            print("Erasing dictionaries...")
            erase(lr)
        elif mode==8:
            print("Creating CSV file")
            convertTOcsv(lr)
        elif mode==9:
            games_to_play = input("Enter number of games: ")
            networkGames(lr,games_to_play)

        elif mode==-99:
            run=False
