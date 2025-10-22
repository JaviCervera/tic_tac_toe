from game.constants import PLAYER_O, PLAYER_X
from game.movement import Movement
from game.player import Player
from game.tic_tac_toe_game import TicTacToeGame
from .local_client import LocalClient
from .local_server import LocalServer


class LocalGame(TicTacToeGame):
    def __init__(self) -> None:
        super().__init__(PLAYER_X, LocalClient(), LocalServer())

    def move(self, movement: Movement) -> bool:
        result = super().move(movement)
        if result is True:
            self._player: Player = PLAYER_O if self._player == PLAYER_X else PLAYER_X
        return result
