from game.client import Client
from game.tic_tac_toe_state import TicTacToeState


class LocalClient(Client):
    def __init__(self) -> None:
        self._queue: list[TicTacToeState] = []
        self._next_index = 0

    def send_state(self, state: TicTacToeState) -> None:
        self._queue.append(state)

    def receive_state(self) -> TicTacToeState | None:
        if self._next_index < len(self._queue):
            self._next_index += 1
            return self._queue[self._next_index - 1]
        return None

    def close(self) -> None:
        pass
