from dataclasses import dataclass

from .constants import GRID_SIZE


@dataclass(frozen=True)
class Movement:
    row: int
    col: int

    def __post_init__(self):
        assert self.row >= 0 and self.row < GRID_SIZE, f"Invalid row {self.row}"
        assert self.col >= 0 and self.col < GRID_SIZE, f"Invalid col {self.col}"
