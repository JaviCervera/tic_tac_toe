import logging

from ..client import Client
from ..tic_tac_toe_state import TicTacToeState


class LoggedClient(Client):
    def __init__(self, wrapped_client: Client, logger: logging.Logger):
        self._client = wrapped_client
        self._logger = logger

    def send_state(self, state: TicTacToeState) -> None:
        self._logger.info(f"{self._client_type()}.send_state({state})")
        self._client.send_state(state)

    def receive_state(self) -> TicTacToeState | None:
        state = self._client.receive_state()
        msg = f"{self._client_type()}.receive_state() -> {state}"
        if state is not None:
            self._logger.info(msg)
        else:
            self._logger.debug(msg)
        return state

    def close(self) -> None:
        self._logger.info(f"{self._client_type()}.close()")
        self._client.close()

    def _client_type(self) -> str:
        return type(self._client).__name__
