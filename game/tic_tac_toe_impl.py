from .tic_tac_toe import Board, TicTacToe

GRID_SIZE = 3
EMPTY = 0
PLAYER_X = 1
PLAYER_O = 2

class TicTacToeImpl(TicTacToe):
    def __init__(self):
        self.reset_game()

    def reset_game(self) -> bool:
        self._board: Board = [[EMPTY] * GRID_SIZE for _ in range(GRID_SIZE)]
        self._current_player = PLAYER_X
        self._winner: int|None = None
        return True

    def make_move(self, row: int, col: int) -> bool:
        if self._board[row][col] == EMPTY and self._winner is None:
            self._board[row][col] = self._current_player
            self._winner = self.check_winner()
            self._current_player = PLAYER_O if self._current_player == PLAYER_X else PLAYER_X
            return True
        return False

    def check_winner(self) -> int|None:
        for i in range(GRID_SIZE):
            if (self._board[i][0] == self._board[i][1] == self._board[i][2] != EMPTY) or \
                (self._board[0][i] == self._board[1][i] == self._board[2][i] != EMPTY):
                return self._board[i][0] if self._board[i][0] != EMPTY else self._board[0][i]
        if (self._board[0][0] == self._board[1][1] == self._board[2][2] != EMPTY) or \
            (self._board[0][2] == self._board[1][1] == self._board[2][0] != EMPTY):
            return self._board[1][1]
        return None

    def get_board(self) -> Board:
        return self._board
