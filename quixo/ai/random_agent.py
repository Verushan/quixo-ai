from quixo.logic.board import Board
from quixo.logic.move import Move
from ..logic import Agent, Move
import numpy as np


class RandomAgent(Agent):
    def __init__(self) -> None:
        super().__init__()

    def get_move(self, board: Board) -> Move:
        moves = board.generate_valid_moves()
        move_index = np.random.choice(len(moves))
        return moves[move_index]
