from enum import IntEnum


class Direction(IntEnum):
    NORTH = 0
    SOUTH = 1
    EAST = 2
    WEST = 3


class Move:
    def __init__(self, start_square: int, direction: Direction) -> None:
        self.start_square = start_square
        self.direction = direction
        self.was_turned = False

    def __repr__(self) -> str:
        str_direction = Direction(self.direction).name

        return f"{self.start_square} {str_direction}"
