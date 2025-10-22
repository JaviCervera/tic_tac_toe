from abc import ABC, abstractmethod

from .movement import Movement
from .tic_tac_toe_state import TicTacToeState


class Server(ABC):
    @abstractmethod
    def send_movement(
        self, state: TicTacToeState, movement: Movement
    ) -> TicTacToeState | None:
        pass
