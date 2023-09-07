from ..logic import Agent, Move, Piece, Board, StateInfo
import numpy as np


class MinimaxAgent(Agent):
    MAX = 1e6

    def __init__(self) -> None:
        super().__init__()

    def _random_best_move(self, moves: list, scores: list) -> Move:
        best_score = np.max(scores)
        best_move_indices = np.where(scores == best_score)[0]
        best_move_index = np.random.choice(best_move_indices)
        return moves[best_move_index]

    def get_move(self, board: Board) -> Move:
        valid_moves = board.generate_valid_moves()
        moves = []
        scores = []

        for move in valid_moves:
            board.make_move(move)

            curr_score = self.minimax(
                board=board,
                depth=2,
                is_maximizing=False,
            )

            board.unmake_move(move)

            scores.append(curr_score)
            moves.append(move)

        return self._random_best_move(moves, scores)

    def evaluate(self, board: Board) -> float:
        evaluation = 0

        x_piece_count = np.count_nonzero(board.board == Piece.X)
        o_piece_count = np.count_nonzero(board.board == Piece.O)

        if board.side_to_play == Piece.X:
            evaluation += x_piece_count - o_piece_count
        else:
            evaluation += o_piece_count - x_piece_count

        return evaluation

    def minimax(self, board: Board, depth: int, is_maximizing: bool = False):
        state_info = board.get_state_info()

        if state_info == StateInfo.DRAW:
            return 0

        if state_info != StateInfo.IN_PROGRESS:
            result = 0

            if board.side_to_play == Piece.X and state_info == StateInfo.X_WIN:
                result = MinimaxAgent.MAX
            elif board.side_to_play == Piece.O and state_info == StateInfo.O_WIN:
                result = MinimaxAgent.MAX
            else:
                result = -MinimaxAgent.MAX

            return result - depth if is_maximizing else -result + depth

        if depth == 0:
            evaluation = self.evaluate(board)
            return evaluation if is_maximizing else -evaluation

        valid_moves = board.generate_valid_moves()

        best_score = 0

        if is_maximizing:
            best_score = -MinimaxAgent.MAX

            for move in valid_moves:
                board.make_move(move)
                curr_score = self.minimax(
                    board=board,
                    depth=depth - 1,
                    is_maximizing=False,
                )
                board.unmake_move(move)
                best_score = max(best_score, curr_score)
        else:
            best_score = MinimaxAgent.MAX

            for move in valid_moves:
                board.make_move(move)
                curr_score = self.minimax(
                    board=board,
                    depth=depth - 1,
                    is_maximizing=True,
                )
                board.unmake_move(move)
                best_score = min(best_score, curr_score)

        return best_score

    def get_name(self) -> str:
        return "Minimax Agent"
