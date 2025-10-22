from game.move import move
from game.movement import Movement
from game.server import Server
from game.tic_tac_toe_state import TicTacToeState


class LocalServer(Server):
    def send_movement(
        self, state: TicTacToeState, movement: Movement
    ) -> TicTacToeState | None:
        return move(state, movement)
