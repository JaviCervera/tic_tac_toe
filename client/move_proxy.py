import requests

from game.tic_tac_toe import InvalidMovementError, Movement, TicTacToeState


class TicTacToeMoveProxy:
    def __init__(self, url: str):
        self._base_url = url

    def __call__(self, state: TicTacToeState, movement: Movement) -> TicTacToeState:
        response = requests.post(
            f"{self._base_url}/move",
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
        else:
            raise InvalidMovementError(movement)
