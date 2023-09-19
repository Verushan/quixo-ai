from quixo.logic import Board
from .minimax_agent import MinimaxAgent
from ..logic import Piece, Board
import numpy as np


class CenterMinimaxAgent(MinimaxAgent):
    CENTER_INDICES = np.array([6, 7, 8, 11, 12, 13, 16, 17, 18])

    def __init__(self) -> None:
        super().__init__()

    def evaluate(self, board: Board) -> float:
        evaluation = super().evaluate(board)

        center_evaluation = 0

        x_centre_count = np.count_nonzero(
            board.board[CenterMinimaxAgent.CENTER_INDICES] == Piece.X
        )

        o_centre_count = np.count_nonzero(
            board.board[CenterMinimaxAgent.CENTER_INDICES] == Piece.O
        )

        if board.side_to_play == Piece.X:
            center_evaluation = x_centre_count - o_centre_count
        else:
            center_evaluation = o_centre_count - x_centre_count

        return evaluation + center_evaluation

    def get_name(self) -> str:
        return "Centre Dominance Minimax Agent"
