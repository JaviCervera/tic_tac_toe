import pyray as rl

from .board import Board
from .constants import DRAW_GAME, GRID_SIZE, PLAYER_O, PLAYER_X
from .movement import Movement
from .player import Player
from .tic_tac_toe_state import TicTacToeState


class Window:
    WIDTH, HEIGHT = 600, 600
    CELL_SIZE = WIDTH // GRID_SIZE

    def __init__(self):
        rl.set_trace_log_level(rl.TraceLogLevel.LOG_NONE)
        rl.init_window(self.WIDTH, self.HEIGHT, "Tic Tac Toe")
        rl.set_target_fps(60)

    def should_close(self) -> bool:
        return rl.window_should_close()

    def selected_player(self) -> Player | None:
        if rl.is_key_pressed(rl.KeyboardKey.KEY_X):
            return PLAYER_X
        elif rl.is_key_pressed(rl.KeyboardKey.KEY_O):
            return PLAYER_O
        return None

    def draw_welcome_screen(self) -> None:
        rl.begin_drawing()
        rl.clear_background(rl.RAYWHITE)
        rl.draw_text(
            "Press X to start game",
            self.WIDTH // 2 - 100,
            self.HEIGHT // 2 - 20,
            20,
            rl.DARKGRAY,
        )
        rl.draw_text(
            "Press O to join game",
            self.WIDTH // 2 - 100,
            self.HEIGHT // 2,
            20,
            rl.DARKGRAY,
        )
        rl.end_drawing()

    def selected_movement(self) -> Movement | None:
        if rl.is_mouse_button_pressed(rl.MouseButton.MOUSE_BUTTON_LEFT):
            mouse_x = rl.get_mouse_x()
            mouse_y = rl.get_mouse_y()
            col = mouse_x // self.CELL_SIZE
            row = mouse_y // self.CELL_SIZE
            return Movement(row, col)
        return None

    def selected_restart(self) -> bool:
        return rl.is_mouse_button_pressed(rl.MouseButton.MOUSE_BUTTON_RIGHT)

    def draw_game_state(self, state: TicTacToeState, local_player: Player) -> None:
        rl.begin_drawing()
        rl.clear_background(rl.RAYWHITE)
        self._draw_board(state.board)

        if state.winner is not None:
            if state.winner != DRAW_GAME:
                message = f"Player {self._player_str(state.winner)} wins!"
            else:
                message = "It's a draw!"
            rl.draw_text(
                message, self.WIDTH // 2 - 100, self.HEIGHT // 2 - 20, 20, rl.DARKGRAY
            )
            rl.draw_text(
                "Click right mouse button to reset",
                self.WIDTH // 2 - 100,
                self.HEIGHT // 2,
                20,
                rl.DARKGRAY,
            )
        else:
            message = f"Player: {self._player_str(local_player)} -- Turn: {self._player_str(state.current_player)}"
            rl.draw_text(
                message,
                (self.WIDTH - rl.measure_text(message, 20)) // 2,
                self.HEIGHT - 32,
                20,
                rl.DARKGRAY,
            )
        rl.end_drawing()

    def close(self) -> None:
        rl.close_window()

    def _draw_board(self, board: Board):
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                x = col * self.CELL_SIZE
                y = row * self.CELL_SIZE
                if board[row][col] == PLAYER_X:
                    rl.draw_line(
                        x + 20,
                        y + 20,
                        x + self.CELL_SIZE - 20,
                        y + self.CELL_SIZE - 20,
                        rl.RED,
                    )
                    rl.draw_line(
                        x + self.CELL_SIZE - 20,
                        y + 20,
                        x + 20,
                        y + self.CELL_SIZE - 20,
                        rl.RED,
                    )
                elif board[row][col] == PLAYER_O:
                    rl.draw_circle(
                        x + self.CELL_SIZE // 2,
                        y + self.CELL_SIZE // 2,
                        self.CELL_SIZE // 2 - 20,
                        rl.BLUE,
                    )

    @staticmethod
    def _player_str(player: Player) -> str:
        return "X" if player == PLAYER_X else "O"
