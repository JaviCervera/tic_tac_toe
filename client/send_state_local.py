from game.tic_tac_toe import TicTacToeState


class TicTacToeSendStateLocal:
    def __init__(self, queue: list[TicTacToeState]):
        self._queue = queue

    def __call__(self, state: TicTacToeState) -> None:
        self._queue.append(state)
