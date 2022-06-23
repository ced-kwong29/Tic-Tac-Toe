class BoardClass():

    #Define class variables
    board = ['', '', '',
             '', '', '',
             '', '', '']
    __myUsername__ = ''
    __theirUsername__ = ''
    __lastPlayer__ = ''
    __gameCount__ = 0
    __winCount__ = 0
    __lossCount__ = 0
    __tieCount__ = 0

    #Define constructor for the game board class
    def __init__(self, myUsername, theirUsername, lastPlayer):
        #Intialize my class variables as part of my constructor
        self.board = ['', '', '',
                      '', '', '',
                      '', '', '']
        self.__myUsername__ = myUsername
        self.__theirUsername__ = theirUsername
        self.__lastPlayer__ = lastPlayer
        self.__gameCount__ = 0
        self.__winCount__ = 0
        self.__lossCount__ = 0
        self.__tieCount__ = 0

    #Define method that updates how many total games have been played
    def recordGamePlayed(self):
        self.__gameCount__ += 1

    #Define method that clears all moves from the game board
    def resetGameBoard(self):
        for placement in range(0, len(self.board)):
            self.board[placement] = ''

    #Define method that updates the game board with the player's move
    def playMoveOnBoard(self, mark, placement):
        if self.__lastPlayer__ == self.__myUsername__:
            return False
        if int(placement) in range(9):
            move = int(placement)
            if self.board[move] == '':
                self.board[move] = mark
                self.__lastPlayer__ = self.__myUsername__
                return True
            else:
                return False
        else:
            return False

    #Define a method that updates the game board with the opponent's move
    def opponentMove(self, mark, placement):
        self.board[int(placement)] = mark
        self.__lastPlayer__ = self.__theirUsername__

    #Define method that checks if the board is full
    def isBoardFull(self):
        if '' not in self.board:
            return True
        return False

    #Define a method that checks if the latest move resulted in a win, loss, or tie and updates wins, losses, and ties
    #count if the game is over
    def isGameFinished(self, playerMark):
        row1 = self.board[0] == self.board[1] == self.board[2] != ""
        row2 = self.board[3] == self.board[4] == self.board[5] != ""
        row3 = self.board[6] == self.board[7] == self.board[8] != ""

        column1 = self.board[0] == self.board[3] == self.board[6] != ""
        column2 = self.board[1] == self.board[4] == self.board[7] != ""
        column3 = self.board[2] == self.board[5] == self.board[8] != ""

        diagonal1 = self.board[0] == self.board[4] == self.board[8] != ""
        diagonal2 = self.board[2] == self.board[4] == self.board[6] != ""

        #Checks rows
        if row1:
            if self.board[0] == playerMark:
                self.__winCount__ += 1
            else:
                self.__lossCount__ += 1
            self.recordGamePlayed()
            return True
        elif row2:
            if self.board[3] == playerMark:
                self.__winCount__ += 1
            else:
                self.__lossCount__ += 1
            self.recordGamePlayed()
            return True
        elif row3:
            if self.board[6] == playerMark:
                self.__winCount__ += 1
            else:
                self.__lossCount__ += 1
            self.recordGamePlayed()
            return True
        #Checks columns
        elif column1:
            if self.board[0] == playerMark:
                self.__winCount__ += 1
            else:
                self.__lossCount__ += 1
            self.recordGamePlayed()
            return True
        elif column2:
            if self.board[1] == playerMark:
                self.__winCount__ += 1
            else:
                self.__lossCount__ += 1
            self.recordGamePlayed()
            return True
        elif column3:
            if self.board[2] == playerMark:
                self.__winCount__ += 1
            else:
                self.__lossCount__ += 1
            self.recordGamePlayed()
            return True
        #Checks diagonals
        elif diagonal1:
            if self.board[0] == playerMark:
                self.__winCount__ += 1
            else:
                self.__lossCount__ += 1
            self.recordGamePlayed()
            return True
        elif diagonal2:
            if self.board[2] == playerMark:
                self.__winCount__ += 1
            else:
                self.__lossCount__ += 1
            self.recordGamePlayed()
            return True
        #Checks Ties
        else:
            if self.isBoardFull():
                self.__tieCount__ += 1
                self.recordGamePlayed()
                return True
            else:
                return False

    #Define a method that gathers and returns the usernames of both players, the username of the player to make the last
    #move, the total number of games, the total number of wins, the total number of losses, and the total number of ties
    def computeStats(self, myUsername, theirUsername, lastPlayer):
        self.__myUsername__ = myUsername
        self.__theirUsername__ = theirUsername
        self.__lastPlayer__ = lastPlayer

        return self.__myUsername__, self.__theirUsername__, self.__lastPlayer__, self.__gameCount__, self.__winCount__,\
               self.__lossCount__, self.__tieCount__
