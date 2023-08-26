from .board import Board
from .move import Move


class Agent:
    def __init__(self) -> None:
        pass

    def get_move(self, board: Board) -> Move:
        raise NotImplementedError
