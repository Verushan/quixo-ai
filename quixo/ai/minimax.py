from ..logic.agent import Agent
from quixo import Move, Board


class MinimaxAgent(Agent):
    def __init__(self) -> None:
        super().__init__()

    def get_move(self, board: Board) -> Move:
        return super().get_move()
