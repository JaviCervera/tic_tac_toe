from copy import deepcopy

from .board import Board
from .client import Client
from .constants import DRAW_GAME, PLAYER_O
from .constants import EMPTY, GRID_SIZE, PLAYER_X
from .movement import Movement
from .player import Player
from .tic_tac_toe_state import TicTacToeState
from .winner import Winner


class TicTacToeGame:
    def __init__(
        self,
        player: Player,
        client: Client,
    ):
        self._state = TicTacToeState(
            board=[[EMPTY] * GRID_SIZE for _ in range(GRID_SIZE)],
            current_player=PLAYER_X,
            winner=None,
        )
        self._player = player
        self._client = client

    @property
    def state(self) -> TicTacToeState:
        return self._state

    @property
    def player(self) -> Player:
        return self._player

    def update(self) -> None:
        received_state = self._client.receive_state()
        while received_state is not None:
            self._state = received_state
            received_state = self._client.receive_state()

    def move(self, movement: Movement) -> bool:
        if self._state.current_player == self._player:
            new_state = self._move_impl(self._state, movement)
            if new_state is not None:
                self._state = new_state
                self._client.send_state(self._state)
                return True
        return False

    def game_over(self) -> bool:
        return self._state.winner is not None

    def close(self) -> None:
        self._client.close()

    def _move_impl(
        self, state: TicTacToeState, movement: Movement
    ) -> TicTacToeState | None:
        if state.board[movement.row][movement.col] != EMPTY or state.winner is not None:
            return None
        board = deepcopy(state.board)
        board[movement.row][movement.col] = state.current_player
        return TicTacToeState(
            board=board,
            current_player=PLAYER_O if state.current_player == PLAYER_X else PLAYER_X,
            winner=self._check_winner(board),
        )

    @staticmethod
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
