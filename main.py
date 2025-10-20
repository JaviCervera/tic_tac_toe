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
    is_mouse_button_pressed,
    set_target_fps,
    window_should_close,
)

from game import (
    Board,
    DRAW_GAME,
    EMPTY,
    GRID_SIZE,
    InvalidMovementError,
    Movement,
    PLAYER_O,
    PLAYER_X,
    TicTacToeState,
    TicTacToeMoveFunc,
    TicTacToeMoveProxy,
)

WIDTH, HEIGHT = 600, 600
CELL_SIZE = WIDTH // GRID_SIZE


def new_state() -> TicTacToeState:
    return TicTacToeState(
        board=[[EMPTY] * GRID_SIZE for _ in range(GRID_SIZE)],
        current_player=PLAYER_X,
        winner=None,
    )


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


def game_over(state: TicTacToeState) -> bool:
    return state.winner is not None


async def main() -> None:
    state: TicTacToeState = new_state()
    move: TicTacToeMoveFunc = TicTacToeMoveProxy("http://127.0.0.1:5000")

    init_window(WIDTH, HEIGHT, "Tic Tac Toe")
    set_target_fps(60)

    while not window_should_close():
        if not game_over(state):
            if is_mouse_button_pressed(MouseButton.MOUSE_BUTTON_LEFT):
                mouse_x = get_mouse_x()
                mouse_y = get_mouse_y()
                col = mouse_x // CELL_SIZE
                row = mouse_y // CELL_SIZE
                try:
                    state = move(state, Movement(row, col))
                except InvalidMovementError as exc:
                    print(exc)

        begin_drawing()
        clear_background(RAYWHITE)
        draw_board(state.board)

        if game_over(state):
            if is_mouse_button_pressed(MouseButton.MOUSE_BUTTON_RIGHT):
                state = new_state()
            message = (
                f"Player {'X' if state.winner == PLAYER_X else 'O'} wins!"
                if state.winner != DRAW_GAME
                else "It's a draw!"
            )
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


# if __name__ == '__main__':
asyncio.run(main())
