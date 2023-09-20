from quixo.logic import Board
from .minimax_agent import MinimaxAgent
from ..logic import Piece, Board
import numpy as np


class EdgeMinimaxAgent(MinimaxAgent):
    def __init__(self, depth: int) -> None:
        super().__init__(depth)

    def evaluate(self, board: Board) -> float:
        evaluation = super().evaluate(board)

        edge_evaluation = 0

        x_edge_piece_count = np.count_nonzero(
            board.board[board.OUTER_INDICES] == Piece.X
        )

        o_edge_piece_count = np.count_nonzero(
            board.board[board.OUTER_INDICES] == Piece.O
        )

        if board.side_to_play == Piece.X:
            edge_evaluation = x_edge_piece_count - o_edge_piece_count
        else:
            edge_evaluation = o_edge_piece_count - x_edge_piece_count

        return evaluation + edge_evaluation

    def get_name(self) -> str:
        return "Edge Minimax Agent Depth " + str(self.depth)
