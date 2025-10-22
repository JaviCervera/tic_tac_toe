from abc import ABC, abstractmethod

from .tic_tac_toe_state import TicTacToeState


class Client(ABC):
    @abstractmethod
    def send_state(self, state: TicTacToeState) -> None:
        pass

    @abstractmethod
    def receive_state(self) -> TicTacToeState | None:
        pass
