from copy import deepcopy

from .board import Board
from .constants import DRAW_GAME, EMPTY, GRID_SIZE, PLAYER_O, PLAYER_X
from .movement import Movement
from .tic_tac_toe_state import TicTacToeState
from .winner import Winner


def move(state: TicTacToeState, movement: Movement) -> TicTacToeState | None:
    if state.board[movement.row][movement.col] != EMPTY or state.winner is not None:
        return None
    board = deepcopy(state.board)
    board[movement.row][movement.col] = state.current_player
    return TicTacToeState(
        board=board,
        current_player=PLAYER_O if state.current_player == PLAYER_X else PLAYER_X,
        winner=_check_winner(board),
    )


def _check_winner(board: Board) -> Winner:
    if not any(cell is EMPTY for row in board for cell in row):
        # No empty cells, draw game
        return DRAW_GAME
    for i in range(GRID_SIZE):
        if (board[i][0] == board[i][1] == board[i][2] != EMPTY) or (
            board[0][i] == board[1][i] == board[2][i] != EMPTY
        ):
            return board[i][0] if board[i][0] == board[i][1] else board[0][i]
    if (board[0][0] == board[1][1] == board[2][2] != EMPTY) or (
        board[0][2] == board[1][1] == board[2][0] != EMPTY
    ):
        return board[1][1]
    return None
