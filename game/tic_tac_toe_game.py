from .tic_tac_toe import (
    EMPTY,
    GRID_SIZE,
    PLAYER_X,
    InvalidMovementError,
    Movement,
    Player,
    TicTacToeMoveFunc,
    TicTacToeReceiveStateFunc,
    TicTacToeSendStateFunc,
    TicTacToeState,
)


class TicTacToeGame:
    def __init__(
        self,
        player: Player,
        move_func: TicTacToeMoveFunc,
        receive_state_func: TicTacToeReceiveStateFunc,
        send_state_func: TicTacToeSendStateFunc,
    ):
        self._state = TicTacToeState(
            board=[[EMPTY] * GRID_SIZE for _ in range(GRID_SIZE)],
            current_player=PLAYER_X,
            winner=None,
        )
        self._player = player
        self._move = move_func
        self._receive_state = receive_state_func
        self._send_state = send_state_func

    @property
    def state(self) -> TicTacToeState:
        return self._state

    @property
    def player(self) -> Player:
        return self._player

    def update(self) -> None:
        received_state = self._receive_state()
        if received_state:
            self._state = received_state

    def move(self, movement: Movement) -> bool:
        if self._state.current_player == self._player:
            try:
                self._state = self._move(self._state, movement)
                self._send_state(self._state)
                return True
            except InvalidMovementError:
                pass
        return False

    def game_over(self) -> bool:
        return self._state.winner is not None
