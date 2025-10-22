import requests

from game.movement import Movement
from game.server import Server
from game.tic_tac_toe_state import TicTacToeState


class RestServer(Server):
    def __init__(self, url: str) -> None:
        self._url = url

    def send_movement(
        self, state: TicTacToeState, movement: Movement
    ) -> TicTacToeState | None:
        response = requests.post(
            self._url,
            json={
                "board": state.board,
                "current_player": state.current_player,
                "winner": state.winner,
                "row": movement.row,
                "col": movement.col,
            },
        )
        if response.status_code == 200:
            return TicTacToeState(
                board=response.json()["board"],
                current_player=response.json()["current_player"],
                winner=response.json()["winner"],
            )
        return None
