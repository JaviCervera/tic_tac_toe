import logging

from game.constants import PLAYER_X
from game.movement import Movement
from game.tic_tac_toe_game import TicTacToeGame
from .local_client import LocalClient
from ..logged.logged_client import LoggedClient


class LocalGame(TicTacToeGame):
    def __init__(self, logger: logging.Logger) -> None:
        super().__init__(PLAYER_X, LoggedClient(LocalClient(), logger))

    def move(self, movement: Movement) -> bool:
        result = super().move(movement)
        self._player = self.state.current_player
        return result
