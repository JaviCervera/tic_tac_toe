from dataclasses import dataclass

from .board import Board
from .player import Player
from .winner import Winner


@dataclass(frozen=True)
class TicTacToeState:
    board: Board
    current_player: Player
    winner: Winner
