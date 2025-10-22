from .client import Client
from .constants import EMPTY, GRID_SIZE, PLAYER_X
from .movement import Movement
from .player import Player
from .server import Server
from .tic_tac_toe_state import TicTacToeState


class TicTacToeGame:
    def __init__(
        self,
        player: Player,
        client: Client,
        server: Server,
    ):
        self._state = TicTacToeState(
            board=[[EMPTY] * GRID_SIZE for _ in range(GRID_SIZE)],
            current_player=PLAYER_X,
            winner=None,
        )
        self._player = player
        self._client = client
        self._server = server

    @property
    def state(self) -> TicTacToeState:
        return self._state

    @property
    def player(self) -> Player:
        return self._player

    def update(self) -> None:
        if self._state.current_player != self._player:
            received_state = self._client.receive_state()
            while received_state is not None:
                self._state = received_state
                received_state = self._client.receive_state()

    def move(self, movement: Movement) -> bool:
        if self._state.current_player == self._player:
            new_state = self._server.send_movement(self._state, movement)
            if new_state is not None:
                self._state = new_state
                self._client.send_state(self._state)
                return True
        return False

    def game_over(self) -> bool:
        return self._state.winner is not None
