import requests

from .tic_tac_toe import Board, TicTacToe

class TicTacToeProxy(TicTacToe):
    def __init__(self, url: str):
        self._base_url = url
        self._board: list[list[int]] = []
        self._winner: int|None = None
    
    def reset_game(self) -> bool:
        response = requests.post(f'{self._base_url}/reset')
        if response.status_code == 200:
            self._board = response.json()['board']
            self._winner = response.json()['winner']
            return True
        else:
            return False

    def make_move(self, row: int, col: int) -> bool:
        response = requests.post(f'{self._base_url}/move', json={'row': row, 'col': col})
        if response.status_code == 200:
            result = response.json()
            self._board = result['board']
            self._winner = result['winner']
            return True
        else:
            return False

    def check_winner(self) -> int|None:
        return self._winner

    def get_board(self) -> Board:
        return self._board
