import gameboard as ticTacToe
import tkinter as tk
from tkinter import messagebox
import socket


#Create player1 user interface
class gameUI():
    #Define class variable to store my tkinter object
    master = 0
    #Define my tkinter class variables
    serverID = 0
    portNum = 0

    #define class constructor
    def __init__(self):
        #Call my methods to create my canvas and add my widgets
        self.canvasSetup()
        self.initTKvariables()

        self.createSPEntry()
        self.createSPButton()

        self.boardList = []
        self.createButton1()
        self.createButton2()
        self.createButton3()
        self.createButton4()
        self.createButton5()
        self.createButton6()
        self.createButton7()
        self.createButton8()
        self.createButton9()

        self.createQuitButton()
        self.runUI()

    #Define method to set up my canvas
    def canvasSetup(self):
        #initialize my tkinter canvas
        self.master = tk.Tk()
        self.master.title("Tic Tac Toe-Host")
        self.master.geometry('970x600')
        self.master.configure(background='blue')
        self.master.resizable(0, 0)

    #Define method to initialize my tk variables
    def initTKvariables(self):
        self.serverID = tk.StringVar()
        self.portNum = tk.IntVar()

    #Define method that creates a server and port entry
    def createSPEntry(self):
        self.serverLabel = tk.Label(self.master, text="1) Enter your server address\nbelow.")
        self.serverLabel.grid(row=0, column=3)

        self.serverEntry = tk.Entry(self.master, textvariable=self.serverID)
        self.serverEntry.grid(row=1, column=3)

        self.portLabel = tk.Label(self.master, text="2) Create a port.")
        self.portLabel.grid(row=0, column=4)

        self.portEntry = tk.Entry(self.master, textvariable=self.portNum)
        self.portEntry.grid(row=1, column=4)

    #Define a method that creates a submit button for server and port entries
    def createSPButton(self):
        self.spButton = tk.Button(self.master, text="Submit", command=self.startServer)
        self.spButton.grid(row=1, column=5)

    #Define a method that establishes a socket and waits for incoming connections
    def startServer(self):
        IP, port = self.serverID.get(), self.portNum.get()
        #Attempts to establish a socket
        try:
            self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.serverSocket.bind((IP, port))
            self.serverSocket.listen(1)

            self.clearSPWidgets()
            self.gameLabel = tk.Label(self.master, text="Server has been established!\n"
                                                        "Waiting for another player...")
            self.gameLabel.grid(row=0, column=3)
            self.createSPLabel()
            self.master.update()

            #Waits for incoming requests to connect to server
            self.waitingForPlayers()
            self.board = ticTacToe.BoardClass('player1', self.player2, 'player1')
            #Waits to receive client's first move that starts the game
            self.firstMove()

        #Handles failure to establish a socket
        except Exception:
            failToStart = messagebox.askretrycancel("Incorrect Entry", "Sorry. The server address or port you entered "
                                                                       "was invalid. Do you want to try again?")
            if failToStart:
                return
            else:
                self.master.destroy()

    #Define a method that takes widgets assoicated with the IP address and port off the GUI
    def clearSPWidgets(self):
        self.serverLabel.grid_forget()
        self.serverEntry.grid_forget()
        self.portLabel.grid_forget()
        self.portEntry.grid_forget()
        self.spButton.grid_forget()

    #Define a method that displays the server address and port after establishment
    def createSPLabel(self):
        self.spLabel = tk.Label(self.master, text='SERVER ID: ' + f'{self.serverID.get()}\n'
                                                  'Code: ' + f'{self.portNum.get()}')
        self.spLabel.grid(row=3, column=3)

    #Define a method that waits for another player to connect to the server
    def waitingForPlayers(self):
        self.clientSocket, clientAddress = self.serverSocket.accept()
        self.player2 = self.clientSocket.recv(1024).decode('ascii')
        self.gameLabel.configure(text="You are in a game with\n" + f'{self.player2}.')
        #Send username to the client
        self.clientSocket.send(b'player1')

    #Define a method the creates a label that displays whose turn it is
    def createTurnLabel(self):
        self.turnLabel = tk.Label(self.master, text="Turn: " + f'{self.player2}')
        self.turnLabel.grid(row=1, column=3)
        self.master.update()

    #Define a method that waits to receive the first move from the client
    def firstMove(self):
        self.createTurnLabel()
        clientMove = int(self.clientSocket.recv(1024).decode('ascii'))
        self.board.opponentMove('X', clientMove)
        self.boardList[clientMove].configure(text='X')

    #Define a method that updates the board with both players' moves
    def markBoard(self, buttonID):
        #Host's turn to make a move and send it to the client
        if self.board.playMoveOnBoard('O', buttonID):
            self.boardList[buttonID].configure(text='O')
            self.clientSocket.sendall(str(buttonID).encode())
            #Check if the host's move ends the game
            if self.board.isGameFinished('O'):
                self.turnLabel.configure(text="Game Over.")
                self.master.update()
                #Wait for client's confirmation to play again or quit
                replayQuit = self.clientSocket.recv(1024).decode('ascii')
                if replayQuit == "Play Again":
                    self.boardCleanup()
                else:
                    self.clientQuit('player1', self.player2, 'player1')
            else:
                self.turnLabel.configure(text="Turn: " + f'{self.player2}')
                self.master.update()

            #Client's turn to make and send a move to the host to update the board
            clientMove = int(self.clientSocket.recv(1024).decode('ascii'))
            self.board.opponentMove('X', clientMove)
            self.boardList[clientMove].configure(text='X')
            #Check if the client's move ends the game
            if self.board.isGameFinished('O'):
                self.turnLabel.configure(text='Game Over.')
                self.master.update()
                #Wait for client's confirmation to play again or quit
                replayQuit = self.clientSocket.recv(1024).decode('ascii')
                if replayQuit == "Play Again":
                    self.boardCleanup()
                    self.board.__lastPlayer__ = 'player1'
                    self.firstMove()
                else:
                    self.clientQuit('player1', self.player2, self.player2)
            else:
                self.turnLabel.configure(text="Turn: player1(you)")

    #Define a method that resets the board for another game
    def boardCleanup(self):
        self.board.resetGameBoard()
        for btn in range(9):
            self.boardList[btn].configure(text='')
        self.turnLabel.configure(text="Turn: " + f'{self.player2}')
        self.master.update()

    #Define a method that displays game stats after client chooses to stop playing
    def clientQuit(self, myUsername, theirUsername, lastPlayer):
        self.gameLabel.configure(text=f"{self.player2} decided to stop playing.")
        #Gather and display game statistics
        gameStats = self.board.computeStats(myUsername, theirUsername, lastPlayer)
        self.statsLabel = tk.Label(self.master, text="YOU: "+f'{gameStats[0]}      ' + "OPPONENT: "+f'{gameStats[1]}\n'
                                                     + "LAST MOVE BY: "+f'{gameStats[2]}\n'
                                                     + "Games Played: "+f'{gameStats[3]}\n'
                                                     + "Wins: "+f'{gameStats[4]}      ' + "Losses: "+f'{gameStats[5]}\n'
                                                     + "Ties: "+f'{gameStats[6]}')
        self.statsLabel.grid(row=2, column=3)
        self.master.update()

    #Define methods that create the board's placement buttons
    def createButton1(self):
        button1 = tk.Button(self.master, text='', command=lambda: self.markBoard(0), width=19, height=9)
        button1.grid(row=0, column=0)
        self.boardList.append(button1)
    def createButton2(self):
        button2 = tk.Button(self.master, text='', command=lambda: self.markBoard(1), width=19, height=9)
        button2.grid(row=0, column=1)
        self.boardList.append(button2)
    def createButton3(self):
        button3 = tk.Button(self.master, text='', command=lambda: self.markBoard(2), width=19, height=9)
        button3.grid(row=0, column=2)
        self.boardList.append(button3)
    def createButton4(self):
        button4 = tk.Button(self.master, text='', command=lambda: self.markBoard(3), width=19, height=9)
        button4.grid(row=1, column=0)
        self.boardList.append(button4)
    def createButton5(self):
        button5 = tk.Button(self.master, text='', command=lambda: self.markBoard(4), width=19, height=9)
        button5.grid(row=1, column=1)
        self.boardList.append(button5)
    def createButton6(self):
        button6 = tk.Button(self.master, text='', command=lambda: self.markBoard(5), width=19, height=9)
        button6.grid(row=1, column=2)
        self.boardList.append(button6)
    def createButton7(self):
        button7 = tk.Button(self.master, text='', command=lambda: self.markBoard(6), width=19, height=9)
        button7.grid(row=2, column=0)
        self.boardList.append(button7)
    def createButton8(self):
        button8 = tk.Button(self.master, text='', command=lambda: self.markBoard(7), width=19, height=9)
        button8.grid(row=2, column=1)
        self.boardList.append(button8)
    def createButton9(self):
        button9 = tk.Button(self.master, text='', command=lambda: self.markBoard(8), width=19, height=9)
        button9.grid(row=2, column=2)
        self.boardList.append(button9)

    #Define a method that creates a quit button
    def createQuitButton(self):
        self.quitButton = tk.Button(self.master, text="Quit", command=self.master.destroy)
        self.quitButton.grid(row=3, column=0)

    #Define a method to start my UI
    def runUI(self):
        self.master.mainloop()


if __name__ == '__main__':
    gameplay = gameUI()
