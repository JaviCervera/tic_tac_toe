from .tic_tac_toe import TicTacToeState


class TicTacToeReceiveStateLocal:
    def __init__(self, queue: list[TicTacToeState]):
        self._queue = queue
        self._next_index = 0

    def __call__(self) -> TicTacToeState | None:
        if self._next_index < len(self._queue):
            self._next_index += 1
            return self._queue[self._next_index - 1]
        return None
