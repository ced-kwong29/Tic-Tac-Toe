import gameboard as ticTacToe
import tkinter as tk
from tkinter import messagebox
import socket


#Create player2 user interface
class gameUI():
    #Define class variable to store my tkinter object
    master = 0
    #Define my tkinter class variables
    serverID = 0
    portNum = 0
    username = 0

    #define class constructor
    def __init__(self):
        #Call my methods to create my canvas and add my widgets
        self.canvasSetup()
        self.initTKvariables()

        self.createSPEntry()
        self.createSPButton()

        self.createUsernameEntry()
        self.createUsernameButton()

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
        self.master.title("Tic Tac Toe-Client")
        self.master.geometry('970x600')
        self.master.configure(background='red')
        self.master.resizable(0, 0)

    #Define method to initialize my tk variables
    def initTKvariables(self):
        self.serverID = tk.StringVar()
        self.portNum = tk.IntVar()
        self.username = tk.StringVar()

    #Define method that creates a server and port entry
    def createSPEntry(self):
        self.serverLabel = tk.Label(self.master, text="Enter a server address below.")
        self.serverLabel.grid(row=0, column=3)

        self.serverEntry = tk.Entry(self.master, textvariable=self.serverID)
        self.serverEntry.grid(row=1, column=3)

        self.portLabel = tk.Label(self.master, text="Enter the server port below.")
        self.portLabel.grid(row=0, column=4)

        self.portEntry = tk.Entry(self.master, textvariable=self.portNum)
        self.portEntry.grid(row=1, column=4)

    #Define a method that creates a submit button for server and port entries
    def createSPButton(self):
        self.spButton = tk.Button(self.master, text="Submit", command=self.joiningSocket)
        self.spButton.grid(row=1, column=5)

    #Define a method that attempts to connect to a socket
    def connectToSocket(self, IP, port):
        connectionSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connectionSocket.connect((IP, port))
        return connectionSocket

    #Define a method takes widgets assoicated with the IP address and port off the GUI
    def clearSPWidgets(self):
        self.serverLabel.grid_forget()
        self.serverEntry.grid_forget()
        self.portLabel.grid_forget()
        self.portEntry.grid_forget()
        self.spButton.grid_forget()

    #Define a method that creates an entry for username
    def createUsernameEntry(self):
        self.gameLabel = tk.Label(self.master, text="You are connected!\n"
                                                    "Enter a username below.")
        self.usernameEntry = tk.Entry(self.master, textvariable=self.username)

    #Define a method that creates a button that submits a username
    def createUsernameButton(self):
        self.usernameButton = tk.Button(self.master, text="Submit", command=self.sendUsername)

    #Define a method that sends the client's username to the host and waits to receive the host's username
    def sendUsername(self):
        self.clientUsername = self.username.get()
        self.socketInfo.send(str.encode(self.clientUsername))
        #Waits to receive the host's username
        self.player1 = self.socketInfo.recv(1024).decode('ascii')

        self.usernameEntry.grid_forget()
        self.usernameButton.grid_forget()

        self.gameLabel.configure(text="You are now in a game with\n" + f'{self.player1}.')

        self.board = ticTacToe.BoardClass(self.clientUsername, self.player1, self.player1)
        self.turnLabel = tk.Label(self.master, text="Turn:  "+f'{self.clientUsername}(you)')
        self.turnLabel.grid(row=1, column=3)

    #Define a method that calls connectToSocket function to attempt to server connection
    def joiningSocket(self):
        IP, port = self.serverID.get(), self.portNum.get()
        #Attempts to connect to the server
        try:
            self.socketInfo = self.connectToSocket(IP, port)

            self.clearSPWidgets()
            self.gameLabel.grid(row=0, column=3)
            self.usernameEntry.grid(row=1, column=3)
            self.usernameButton.grid(row=1, column=4)

        #Handles failure to connect to the server
        except:
            failToConnect = messagebox.askretrycancel("Incorrect Entry", "Sorry. The server address or code you entered"
                                                                         " was invalid. Do you want to try again?")
            if failToConnect:
                return
            else:
                self.master.destroy()

    #Define a method that updates the board with both players' moves
    def markBoard(self, buttonID):
        #Client's turn to make a move and send it to the host
        if self.board.playMoveOnBoard('X', buttonID):
            self.boardList[buttonID].configure(text='X')
            self.socketInfo.sendall(str(buttonID).encode())
            #Check if the client's move ends the game
            if self.board.isGameFinished('X'):
                self.turnLabel.configure(text="Game Over.")
                self.master.update()
                #Asks if client wants to play again or quit
                replayQuit = messagebox.askretrycancel("End of game", "Do you want to play again?")
                if replayQuit:
                    self.boardCleanup()
                    #Sets host as last to make a move so that the client to make the first move to a new game
                    self.board.__lastPlayer__ = self.player1
                    return
                else:
                    self.quitPlaying(self.clientUsername, self.player1, self.clientUsername)
            else:
                self.turnLabel.configure(text="Turn: " + f'{self.player1}')
                self.master.update()

                #Host's turn to make and send a move to the client to update the board
                hostMove = int(self.socketInfo.recv(1024).decode('ascii'))
                self.board.opponentMove('O', hostMove)
                self.boardList[hostMove].configure(text='O')
                #Check if the host's move ends the game
                if self.board.isGameFinished('X'):
                    self.turnLabel.configure(text="Game Over.")
                    self.master.update()
                    #Asks if client wants to play again or quit
                    replayQuit = messagebox.askretrycancel("End of game", "Do you want to play again?")
                    if replayQuit:
                        self.boardCleanup()
                        return
                    else:
                        self.quitPlaying(self.clientUsername, self.player1, self.player1)
                else:
                    self.turnLabel.configure(text="Turn:  "+f'{self.clientUsername}(you)')

    #Define a method that resets the board for another game
    def boardCleanup(self):
        #Sends message to host to let them know to reset their board for a new game
        self.socketInfo.send(b'Play Again')
        self.board.resetGameBoard()
        for btn in range(9):
            self.boardList[btn].configure(text='')
        self.turnLabel.configure(text="Turn:  " + f'{self.clientUsername}(you)')

    #Define a method that handles the client choosing to quit after a game
    def quitPlaying(self, myUsername, theirUsername, lastPlayer):
        #Sends message to host to let them know that the client wants to stop playing
        self.socketInfo.send(b'Fun Times')
        self.gameLabel.configure(text="Goodbye, "+f"{self.clientUsername}!")
        #Gathers and display game statistics
        gameStats = self.board.computeStats(myUsername, theirUsername, lastPlayer)
        self.statsLabel = tk.Label(self.master, text="YOU: "+f'{gameStats[0]}      ' + "OPPONENT: "+f'{gameStats[1]}\n'
                                                     + "LAST MOVE BY: "+f'{gameStats[2]}\n'
                                                     + "Total Games: "+f'{gameStats[3]}\n'
                                                     + "Wins: "+f'{gameStats[4]}      ' + "Losses: "+f'{gameStats[5]}\n'
                                                     + "Ties: "+f'{gameStats[6]}')
        self.statsLabel.grid(row=2, column=3)
        self.quitLabel = tk.Label(self.master, text="Closing in 10 seconds...")
        self.quitLabel.grid(row=4, column=3)
        self.master.update()
        #Closes client's GUI after 10 seconds
        self.master.after(10000, self.master.destroy)

    #Define methods that create buttons that mark the board when both players make their moves
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
        self.quitButton.grid(row=4, column=0)

    #Define a method to start my UI
    def runUI(self):
        self.master.mainloop()


if __name__ == '__main__':
    gameplay = gameUI()
