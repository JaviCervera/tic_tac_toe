import logging

from game.movement import Movement
from game.server import Server
from game.tic_tac_toe_state import TicTacToeState


class LoggedServer(Server):
    def __init__(self, wrapped_server: Server, logger: logging.Logger):
        self._server = wrapped_server
        self._logger = logger

    def send_movement(
        self, state: TicTacToeState, movement: Movement
    ) -> TicTacToeState | None:
        new_state = self._server.send_movement(state, movement)
        self._logger.info(
            f"{self._server_type()}.send_movement({state}, {movement}) -> {new_state}"
        )
        return new_state

    def _server_type(self) -> str:
        return type(self._server).__name__
