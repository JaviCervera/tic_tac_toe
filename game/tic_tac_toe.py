from abc import ABC, abstractmethod

Board = list[list[int]]

class TicTacToe(ABC):
    @abstractmethod    
    def reset_game(self) -> bool:
        pass

    @abstractmethod
    def make_move(self, row: int, col: int) -> bool:
        pass

    @abstractmethod
    def check_winner(self) -> int|None:
        pass

    @abstractmethod
    def get_board(self) -> Board:
        pass
