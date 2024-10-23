from unittest import TestCase

from Controllers.player import Player
from Repo.moveRepo import MoveRepository


class TestPlayer(TestCase):
    def testMakeMove(self):
        repository = MoveRepository()
        player = Player("X", repository)
        player.makeMove(0, 0)
        self.assertEqual(repository.getMove(0, 0).sign, "X")