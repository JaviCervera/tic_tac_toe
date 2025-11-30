# /// script
# dependencies = [
#     "cffi",
#     "raylib"
# ]
# ///
import asyncio
import logging

from game.config import Config, load_config
from game.player import Player
from game.tic_tac_toe_game import TicTacToeGame
from game.window_raylib import Window


def init_logger(level: int) -> logging.Logger:
    logger = logging.getLogger(__name__)
    logger.setLevel(level)
    console_handler = logging.StreamHandler()
    formatter = logging.Formatter("%(levelname)s: %(message)s")
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    return logger


def create_local_game(logger: logging.Logger) -> TicTacToeGame:
    from game.local.local_game import LocalGame

    return LocalGame(logger)


def create_remote_game(
    config: Config, player: Player, logger: logging.Logger
) -> TicTacToeGame:
    from game.remote.remote_game import RemoteGame

    return RemoteGame(config, player, logger)


def create_game(
    config: Config, player: Player | None, logger: logging.Logger
) -> TicTacToeGame | None:
    if config.local:
        return create_local_game(logger)
    elif player is None:
        return None
    else:
        return create_remote_game(config, player, logger)


async def main() -> None:
    logger = init_logger(logging.INFO)
    config = load_config("config.json")
    game = create_game(config, None, logger)

    try:
        win = Window()
        while not win.should_close():
            if game is None:
                sel_player = win.selected_player()
                if sel_player:
                    game = create_game(config, sel_player, logger)
                win.draw_welcome_screen()
            else:
                if not game.game_over():
                    game.update()
                    movement = win.selected_movement()
                    if movement:
                        if not game.move(movement):
                            print("Invalid movement")
                win.draw_game_state(game.state, game.player)
                if game.game_over() and win.selected_restart():
                    game.close()
                    game = create_game(config, None, logger)
            await asyncio.sleep(0)
        win.close()
    finally:
        if game is not None:
            game.close()


"""
pygbag is used to run the app on a browser,
and it requires an async main func
"""
asyncio.run(main())
