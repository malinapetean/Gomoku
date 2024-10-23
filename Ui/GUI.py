from tkinter import *

from Controllers.AIplayer  import AIPlayer
from Controllers.player import Player
from Model.move import Move
from Repo.moveRepo import MoveRepository
from Ui.UI import UI


class GUI(UI):

    def __init__(self, player1, player2, gameController):
        super().__init__(player1, player2, gameController)
        self.currentPlayer = player1
        self.backgroundColor = '#3BA28A'
        self.gameEnded = False
        self.window: Tk = None
        self.canvas: Canvas = None
        self.textarea = None
        self.squareWidth = 50
        self.padding = 5
        self.lineWidth = 2
        self.width = MoveRepository.dimensionX * self.squareWidth
        self.height = MoveRepository.dimensionY * self.squareWidth
        self.initializeWindow()
        self.initializeGrid()

    def run(self):
        self.window.mainloop()

    def initializeWindow(self):
        self.window = Tk()
        self.window.title("Gomoku")

        self.canvas = Canvas(self.window, width=self.width, height=self.height, background=self.backgroundColor)
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.onMouseClicked)
        self.textarea = Label(self.window, text="Player 1 begins", font=("Helvetica", 20))
        self.textarea.pack()

    def initializeGrid(self):
        canvas = self.canvas
        for i in range(1, MoveRepository.dimensionX):
            canvas.create_line(i * self.squareWidth, 0, i * self.squareWidth, self.height, width=self.lineWidth)
        for i in range(1, MoveRepository.dimensionY):
            canvas.create_line(0, i * self.squareWidth, self.width, i * self.squareWidth, width=self.lineWidth)

    def drawLastMove(self):
        lastMove: Move = self.gameController.getLastMove()
        self.canvas.create_oval(
            lastMove.xCoordinate * self.squareWidth + self.padding,
            lastMove.yCoordinate * self.squareWidth + self.padding,
            (lastMove.xCoordinate + 1) * self.squareWidth - self.padding,
            (lastMove.yCoordinate + 1) * self.squareWidth - self.padding,
            fill='black' if lastMove.sign == 'X' else 'white',
            outline=''
        )

    def resetGame(self):
        self.canvas.delete(ALL)
        self.initializeGrid()
        self.gameController.resetGame()
        self.canvas.config(background=self.backgroundColor)

    def onMouseClicked(self, event):
        if self.gameEnded:
            self.resetGame()
            self.gameEnded = False
            self.currentPlayer = self.player1
            self.show("Player 1 begins")
            return

        if type(self.currentPlayer) is Player:
            xCoordinate = event.x // self.squareWidth
            yCoordinate = event.y // self.squareWidth

            try:
                self.currentPlayer.makeMove(xCoordinate, yCoordinate)
            except:
                self.show("Invalid move!")
                return

        elif type(self.currentPlayer) is AIPlayer:
            self.currentPlayer.makeMove()
        self.drawLastMove()

        gameStatus = self.gameController.gameStatus()

        if id(self.currentPlayer) == id(self.player1):
            self.currentPlayer = self.player2
        else:
            self.currentPlayer = self.player1

        if gameStatus == 0:
            if type(self.currentPlayer) is Player:
                number = 1
                if id(self.currentPlayer) == id(self.player2):
                    number = 2
                self.show("Player {:d} makes his move".format(number))

            elif type(self.currentPlayer) is AIPlayer:
                self.show("Press anywhere for the AI to make his move")
        else:
            againText = " Press anywhere to play again!"
            self.canvas.config(background='purple')
            if gameStatus == -1:
                self.show("The game has ended in a tie!" + againText)
            elif gameStatus == 1:
                if id(self.currentPlayer) == id(self.player1):
                    self.show(text="Player 2 has won!" + againText)
                else:
                    self.show("Player 1 has won!" + againText)
            self.gameEnded = True

    def show(self, text):
        self.textarea.config(text=text)
