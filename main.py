# /// script
# dependencies = [
#     "cffi",
#     "raylib"
# ]
# ///
import asyncio

from pyray import (
    BLUE,
    DARKGRAY,
    RAYWHITE,
    RED,
    KeyboardKey,
    MouseButton,
    begin_drawing,
    clear_background,
    close_window,
    draw_circle,
    draw_line,
    draw_text,
    end_drawing,
    get_mouse_x,
    get_mouse_y,
    init_window,
    is_key_pressed,
    is_mouse_button_pressed,
    set_target_fps,
    window_should_close,
)

from game.tic_tac_toe import (
    DRAW_GAME,
    GRID_SIZE,
    PLAYER_O,
    PLAYER_X,
    Board,
    Movement,
    Player,
    TicTacToeState,
)
from game.move_impl import move_impl
from game.tic_tac_toe_game import TicTacToeGame
from game.receive_state_local import TicTacToeReceiveStateLocal
from game.send_state_local import TicTacToeSendStateLocal

WIDTH, HEIGHT = 600, 600
CELL_SIZE = WIDTH // GRID_SIZE


def draw_board(board: Board):
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            x = col * CELL_SIZE
            y = row * CELL_SIZE
            if board[row][col] == PLAYER_X:
                draw_line(x + 20, y + 20, x + CELL_SIZE - 20, y + CELL_SIZE - 20, RED)
                draw_line(x + CELL_SIZE - 20, y + 20, x + 20, y + CELL_SIZE - 20, RED)
            elif board[row][col] == PLAYER_O:
                draw_circle(
                    x + CELL_SIZE // 2, y + CELL_SIZE // 2, CELL_SIZE // 2 - 20, BLUE
                )


class TicTacToeGameLocal(TicTacToeGame):
    def __init__(self) -> None:
        queue: list[TicTacToeState] = []
        super().__init__(
            PLAYER_X,
            move_impl,
            TicTacToeReceiveStateLocal(queue),
            TicTacToeSendStateLocal(queue),
        )

    def move(self, movement: Movement) -> bool:
        result = super().move(movement)
        if result is True:
            self._player: Player = PLAYER_O if self._player == PLAYER_X else PLAYER_X
        return result


def create_default_game(player: Player | None) -> TicTacToeGame | None:
    return TicTacToeGameLocal()


async def main() -> None:
    game = create_default_game(None)

    init_window(WIDTH, HEIGHT, "Tic Tac Toe")
    set_target_fps(60)

    while not window_should_close():
        if game is None:
            if is_key_pressed(KeyboardKey.KEY_X):
                game = create_default_game(PLAYER_X)
            elif is_key_pressed(KeyboardKey.KEY_O):
                game = create_default_game(PLAYER_O)

            begin_drawing()
            clear_background(RAYWHITE)
            draw_text(
                "Press X to start game",
                WIDTH // 2 - 100,
                HEIGHT // 2 - 20,
                20,
                DARKGRAY,
            )
            draw_text(
                "Press O to join game", WIDTH // 2 - 100, HEIGHT // 2, 20, DARKGRAY
            )
            end_drawing()
        else:
            if not game.game_over():
                game.update()
                if is_mouse_button_pressed(MouseButton.MOUSE_BUTTON_LEFT):
                    mouse_x = get_mouse_x()
                    mouse_y = get_mouse_y()
                    col = mouse_x // CELL_SIZE
                    row = mouse_y // CELL_SIZE
                    if not game.move(Movement(row, col)):
                        print("Invalid movement")

            begin_drawing()
            clear_background(RAYWHITE)
            draw_board(game.state.board)

            if game.game_over():
                if is_mouse_button_pressed(MouseButton.MOUSE_BUTTON_RIGHT):
                    game = create_default_game(None)
                else:
                    if game.state.winner != DRAW_GAME:
                        message = f"Player {'X' if game.state.winner == PLAYER_X else 'O'} wins!"
                    else:
                        message = "It's a draw!"
                    draw_text(message, WIDTH // 2 - 100, HEIGHT // 2 - 20, 20, DARKGRAY)
                    draw_text(
                        "Click right mouse button to reset",
                        WIDTH // 2 - 100,
                        HEIGHT // 2,
                        20,
                        DARKGRAY,
                    )

            end_drawing()
        await asyncio.sleep(0)

    close_window()


asyncio.run(main())
