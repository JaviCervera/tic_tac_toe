from abc import ABC, abstractmethod
from typing import Literal


PLAYER_X = 1
PLAYER_O = 2

Player = Literal[PLAYER_X, PLAYER_O]  # type: ignore [valid-type]
Board = list[list[Player|None]]


class TicTacToe(ABC):
    @abstractmethod    
    def reset_game(self) -> bool:
        pass

    @abstractmethod
    def make_move(self, row: int, col: int) -> bool:
        pass

    @abstractmethod
    def check_winner(self) -> Player|None:
        pass

    @abstractmethod
    def get_board(self) -> Board:
        pass

    @abstractmethod
    def get_current_player(self) -> Player:
        pass
