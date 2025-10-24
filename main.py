# /// script
# dependencies = [
#     "cffi",
#     "raylib"
# ]
# ///
import asyncio
import logging

import pyray as rl

from client.config import Config, load_config
from client.logged_client import LoggedClient
from client.logged_server import LoggedServer
from game.board import Board
from game.constants import DRAW_GAME, GRID_SIZE, PLAYER_O, PLAYER_X
from game.movement import Movement
from game.player import Player
from game.tic_tac_toe_game import TicTacToeGame

WIDTH, HEIGHT = 600, 600
CELL_SIZE = WIDTH // GRID_SIZE


def init_logger(level: int) -> logging.Logger:
    logger = logging.getLogger(__name__)
    logger.setLevel(level)
    console_handler = logging.StreamHandler()
    formatter = logging.Formatter("%(levelname)s: %(message)s")
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    return logger


def player_str(player: Player) -> str:
    return "X" if player == PLAYER_X else "O"


def draw_board(board: Board):
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            x = col * CELL_SIZE
            y = row * CELL_SIZE
            if board[row][col] == PLAYER_X:
                rl.draw_line(
                    x + 20, y + 20, x + CELL_SIZE - 20, y + CELL_SIZE - 20, rl.RED
                )
                rl.draw_line(
                    x + CELL_SIZE - 20, y + 20, x + 20, y + CELL_SIZE - 20, rl.RED
                )
            elif board[row][col] == PLAYER_O:
                rl.draw_circle(
                    x + CELL_SIZE // 2, y + CELL_SIZE // 2, CELL_SIZE // 2 - 20, rl.BLUE
                )


def create_local_game(logger: logging.Logger) -> TicTacToeGame:
    from client.local_game import LocalGame

    return LocalGame(logger)


def create_server_game(
    config: Config, player: Player, logger: logging.Logger
) -> TicTacToeGame:
    from client.kafka_client import KafkaClient
    from client.rest_server import RestServer

    return TicTacToeGame(
        player,
        LoggedClient(KafkaClient(config.kafka_url, config.kafka_topic), logger),
        LoggedServer(RestServer(config.server_url), logger),
    )


def create_game(
    config: Config, player: Player | None, logger: logging.Logger
) -> TicTacToeGame | None:
    if config.local:
        return create_local_game(logger)
    elif player is None:
        return None
    else:
        return create_server_game(config, player, logger)


async def main() -> None:
    logger = init_logger(logging.INFO)
    config = load_config("config.json")
    game = create_game(config, None, logger)

    rl.set_trace_log_level(rl.TraceLogLevel.LOG_NONE)
    rl.init_window(WIDTH, HEIGHT, "Tic Tac Toe")
    rl.set_target_fps(60)

    while not rl.window_should_close():
        if game is None:
            if rl.is_key_pressed(rl.KeyboardKey.KEY_X):
                game = create_game(config, PLAYER_X, logger)
            elif rl.is_key_pressed(rl.KeyboardKey.KEY_O):
                game = create_game(config, PLAYER_O, logger)

            rl.begin_drawing()
            rl.clear_background(rl.RAYWHITE)
            rl.draw_text(
                "Press X to start game",
                WIDTH // 2 - 100,
                HEIGHT // 2 - 20,
                20,
                rl.DARKGRAY,
            )
            rl.draw_text(
                "Press O to join game", WIDTH // 2 - 100, HEIGHT // 2, 20, rl.DARKGRAY
            )
            rl.end_drawing()
        else:
            if not game.game_over():
                game.update()
                if rl.is_mouse_button_pressed(rl.MouseButton.MOUSE_BUTTON_LEFT):
                    mouse_x = rl.get_mouse_x()
                    mouse_y = rl.get_mouse_y()
                    col = mouse_x // CELL_SIZE
                    row = mouse_y // CELL_SIZE
                    if not game.move(Movement(row, col)):
                        print("Invalid movement")

            rl.begin_drawing()
            rl.clear_background(rl.RAYWHITE)
            draw_board(game.state.board)

            if game.game_over():
                if rl.is_mouse_button_pressed(rl.MouseButton.MOUSE_BUTTON_RIGHT):
                    game = create_game(config, None, logger)
                else:
                    if game.state.winner != DRAW_GAME:
                        message = f"Player {player_str(game.state.winner)} wins!"
                    else:
                        message = "It's a draw!"
                    rl.draw_text(
                        message, WIDTH // 2 - 100, HEIGHT // 2 - 20, 20, rl.DARKGRAY
                    )
                    rl.draw_text(
                        "Click right mouse button to reset",
                        WIDTH // 2 - 100,
                        HEIGHT // 2,
                        20,
                        rl.DARKGRAY,
                    )
            else:
                message = f"Player: {player_str(game.player)} -- Turn: {player_str(game.state.current_player)}"
                rl.draw_text(
                    message,
                    (WIDTH - rl.measure_text(message, 20)) // 2,
                    HEIGHT - 32,
                    20,
                    rl.DARKGRAY,
                )

            rl.end_drawing()
        await asyncio.sleep(0)

    rl.close_window()


asyncio.run(main())
