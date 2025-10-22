from typing import Literal

from .constants import DRAW_GAME
from .player import Player

Winner = Literal[None, Player, DRAW_GAME]
