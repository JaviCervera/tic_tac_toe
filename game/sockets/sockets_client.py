import socket

from ..board import Board
from ..client import Client
from ..constants import GRID_SIZE
from ..tic_tac_toe_state import TicTacToeState
from .packet_stream import PacketStream


class SocketsClient(Client):
    def __init__(self, host: str, port: int):
        self._client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._client.connect((host, port))
        self._stream = PacketStream(self._client)

    def send_state(self, state: TicTacToeState) -> None:
        self._client.send(self._state_to_bytes(state))

    def receive_state(self) -> TicTacToeState | None:
        packet = self._stream.read_packet()
        if packet is None:
            return None
        return self._bytes_to_state(packet)

    def close(self) -> None:
        self._client.close()

    @staticmethod
    def _state_to_bytes(state: TicTacToeState) -> bytes:
        arr: list[int] = []
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                cell = state.board[i][j]
                arr.append(cell if cell is not None else 0)
        arr.append(state.current_player)
        arr.append(state.winner or 0)
        return bytes(arr)

    @staticmethod
    def _bytes_to_state(data: bytes) -> TicTacToeState:
        board: Board = []
        for i in range(GRID_SIZE):
            board.append([])
            for j in range(GRID_SIZE):
                cell = data[i * GRID_SIZE + j]
                board[i].append(cell if cell != 0 else None)
        return TicTacToeState(
            board=board,
            current_player=data[9],
            winner=data[10] if data[10] != 0 else None,
        )
