# /// script
# dependencies = [
#     "cffi",
#     "raylib"
# ]
# ///
import asyncio

from pyray import *

from game import Board, DRAW_GAME, Player, PLAYER_O, PLAYER_X, TicTacToe, TicTacToeImpl, TicTacToeProxy

WIDTH, HEIGHT = 600, 600
GRID_SIZE = 3
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
                draw_circle(x + CELL_SIZE // 2, y + CELL_SIZE // 2, CELL_SIZE // 2 - 20, BLUE)


def game_over(game: TicTacToe) -> bool:
    return game.check_winner() is not None


async def main() -> None:
    game: TicTacToe = TicTacToeImpl()  # Proxy('http://127.0.0.1:5000')
    
    init_window(WIDTH, HEIGHT, 'Tic Tac Toe')
    set_target_fps(60)

    while not window_should_close():
        if not game_over(game):
            if is_mouse_button_pressed(MouseButton.MOUSE_BUTTON_LEFT):
                mouse_x = get_mouse_x()
                mouse_y = get_mouse_y()
                
                col = mouse_x // CELL_SIZE
                row = mouse_y // CELL_SIZE

                game.make_move(row, col)
        
        begin_drawing()
        clear_background(RAYWHITE)
        draw_board(game.get_board())

        if game_over(game):
            if is_mouse_button_pressed(MouseButton.MOUSE_BUTTON_RIGHT):
                game.reset_game()
            message = f'Player {"X" if game.check_winner() == PLAYER_X else "O"} wins!' if game.check_winner() != DRAW_GAME else "It's a draw!"
            draw_text(message, WIDTH // 2 - 100, HEIGHT // 2 - 20, 20, DARKGRAY)
            draw_text('Click right mouse button to reset', WIDTH // 2 - 100, HEIGHT // 2, 20, DARKGRAY)

        end_drawing()
        await asyncio.sleep(0)

    close_window()


# if __name__ == '__main__':
asyncio.run(main())
