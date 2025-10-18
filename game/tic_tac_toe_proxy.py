import requests

from .tic_tac_toe import Board, Player, TicTacToe, Winner

class TicTacToeProxy(TicTacToe):
    def __init__(self, url: str):
        self._base_url = url
        response = requests.get(f'{self._base_url}/board')
        if response.status_code == 200:
            self._board: Board = response.json()['board']
            self._winner: Winner = response.json()['winner']
            self._current_player: Player = response.json()['current_player']
        else:
            raise RuntimeError("Can't get game board from the server. Is it running?")
    
    def reset_game(self) -> bool:
        response = requests.post(f'{self._base_url}/reset')
        if response.status_code == 200:
            self._board = response.json()['board']
            self._winner = response.json()['winner']
            self._current_player = response.json()['current_player']
            return True
        else:
            return False

    def make_move(self, row: int, col: int) -> bool:
        response = requests.post(f'{self._base_url}/move', json={'row': row, 'col': col})
        if response.status_code == 200:
            self._board = response.json()['board']
            self._winner = response.json()['winner']
            self._current_player = response.json()['current_player']
            return True
        else:
            return False

    def check_winner(self) -> Winner:
        return self._winner

    def get_board(self) -> Board:
        return self._board

    def get_current_player(self) -> Player:
        return self._current_player
