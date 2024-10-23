from Repo.moveRepo import MoveRepository
from Validation.validator import Validator, MoveInvalid


class GameController:
    """
    Provides the main game logic
    """

    def __init__(self, moveRepository):
        self.__moveRepository = moveRepository

    def getMoves(self):
        """
        Returns the move matrix
        :return: A list of lists of moves
        """
        return self.__moveRepository.moves

    def getLastMove(self):
        """
        Returns the last move made
        :return: A Move object
        """
        return self.__moveRepository.lastMove

    def resetGame(self):
        """
        Resets the game
        """
        self.__moveRepository.__init__()

    def gameStatus(self):
        """
        Provides information about the game status
        :returns: 1 if the game has been won by the last player who moved
                -1 if the game ended in a tie
                 0 if the game can be continued
        """
        lastMove = self.__moveRepository.lastMove

        directions = [
            (0, 1),
            (1, 1),
            (1, 0),
            (1, -1)
        ]

        for direction in directions:
            if self.__count(lastMove, direction) + self.__count(lastMove,
                                                                self.__invert(
                                                                    direction)) + 1 == MoveRepository.winNumber:
                return 1
        if self.__moveRepository.moveNumber == MoveRepository.dimensionX * MoveRepository.dimensionY:
            return -1
        return 0

    def __count(self, lastMove, direction):
        """
        Counts the signs similar to the last move's in the given direction and returns the result
        :param lastMove: The last move made in the game
        :param direction: The direction to use in the calculation
        :return: The number of similar signs in the given direction
        """
        count = 0
        xCoordinate = lastMove.xCoordinate
        yCoordinate = lastMove.yCoordinate
        xCoordinate += direction[0]
        yCoordinate += direction[1]
        while self.__isValid(xCoordinate, yCoordinate) and self.__moveRepository.getMove(xCoordinate, yCoordinate) is not None \
                and self.__moveRepository.getMove(xCoordinate, yCoordinate).sign == lastMove.sign:
            xCoordinate += direction[0]
            yCoordinate += direction[1]
            count += 1
        return count

    @staticmethod
    def __invert(direction):
        """
        Inverts a direction
        """
        return -direction[0], -direction[1]

    @staticmethod
    def __isValid(xCoordinate, yCoordinate):
        """
        Checks if the given coordinates are valid
        xCoordinate:the x coordinate
        yCoordinate:the y coordinate
        """
        try:
            Validator.validateCoordinates(xCoordinate, yCoordinate)
            return True
        except MoveInvalid:
            return False

    @property
    def moveRepository(self):
        return self.__moveRepository