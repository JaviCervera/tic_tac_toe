from dataclasses import dataclass
from typing import Callable, Literal

DRAW_GAME = -1
EMPTY = None
GRID_SIZE = 3
PLAYER_X = 1
PLAYER_O = 2

Player = Literal[PLAYER_X, PLAYER_O]  # type: ignore [valid-type]
Board = list[list[Player | None]]
Winner = Literal[None, Player, DRAW_GAME]


class InvalidPositionError(Exception):
    def __init__(self, pos: int, is_row: bool):
        super().__init__(
            f"The value for {'row' if is_row else 'col'} must be 0, 1 or 2, got {pos}"
        )


@dataclass(frozen=True)
class Movement:
    row: int
    col: int

    def __post_init__(self):
        if self.row < 0 or self.row > 2:
            raise InvalidPositionError(self.row, True)
        if self.col < 0 or self.col > 2:
            raise InvalidPositionError(self.col, False)


@dataclass(frozen=True)
class TicTacToeState:
    board: Board
    current_player: Player
    winner: Winner


class InvalidMovementError(Exception):
    def __init__(self, movement: Movement):
        super().__init__(f"Invalid movement: row {movement.row}, col {movement.col}")


TicTacToeMoveFunc = Callable[[TicTacToeState, Movement], TicTacToeState]
TicTacToeSendStateFunc = Callable[[TicTacToeState], None]
TicTacToeReceiveStateFunc = Callable[[], TicTacToeState | None]
