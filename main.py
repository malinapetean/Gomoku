from Controllers.AIplayer import AIPlayer
from settings import Settings
from Controllers.game import GameController
from Controllers.player import Player
from Repo.moveRepo import MoveRepository
from Ui.UI import UI
from Ui.ConsoleUI import ConsoleUI
from Ui.GUI import GUI

settings = Settings()
moveRepository = MoveRepository()
gameController = GameController(moveRepository)

player1 = Player("X", moveRepository)
if settings["player1"] == "machine":
    player1 = AIPlayer(player1, gameController)

player2 = Player("O", moveRepository)
if settings["player2"] == "machine":
    player2 = AIPlayer(player2, gameController)

ui: UI = None
if settings["ui"] == "ConsoleUI":
    ui = ConsoleUI(player1, player2, gameController)
if settings["ui"] == "GUI":
    ui = GUI(player1,player2,gameController)


ui.run()
