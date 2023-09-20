from ..logic import Agent, Move, Piece, Board
import numpy as np


class MinimaxAgent(Agent):
    MAX = 1e6
    MAX_DEPTH = 3

    def __init__(self, depth: int) -> None:
        super().__init__()
        self.depth = depth

    def _random_best_move(self, moves: list, scores: list) -> Move:
        best_score = np.max(scores)
        best_move_indices = np.where(scores == best_score)[0]
        best_move_index = np.random.choice(best_move_indices)
        return moves[best_move_index]

    def get_move(self, board: Board, time_limit: float) -> Move:
        valid_moves = board.generate_valid_moves()
        alpha, beta = -MinimaxAgent.MAX, MinimaxAgent.MAX
        scores, moves = [], []

        for move in valid_moves:
            board.make_move(move)

            curr_score = self.minimax(
                board=board,
                depth=self.depth - 1,
                alpha=alpha,
                beta=beta,
                is_maximizing=False,
            )

            moves.append(move)
            scores.append(curr_score)
            board.unmake_move(move)

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

    def minimax(
        self,
        board: Board,
        depth: int,
        alpha: int,
        beta: int,
        is_maximizing: bool,
    ):
        winner = board.get_winner()

        if winner != Piece.NONE:
            result = 0

            if board.side_to_play == Piece.X and winner == Piece.O:
                result = -MinimaxAgent.MAX - depth
            elif board.side_to_play == Piece.O and winner == Piece.X:
                result = -MinimaxAgent.MAX - depth
            else:
                result = MinimaxAgent.MAX + depth

            result = result if is_maximizing else -result
            return result

        if depth == 0:
            evaluation = self.evaluate(board)
            result = evaluation if is_maximizing else -evaluation
            return result

        valid_moves = board.generate_valid_moves()

        best_score = 0

        if is_maximizing:
            best_score = -MinimaxAgent.MAX

            for move in valid_moves:
                board.make_move(move)
                curr_score = self.minimax(
                    board=board,
                    depth=depth - 1,
                    alpha=alpha,
                    beta=beta,
                    is_maximizing=False,
                )

                board.unmake_move(move)

                best_score = max(best_score, curr_score)
                alpha = max(alpha, curr_score)

                if beta <= alpha:
                    break

        else:
            best_score = MinimaxAgent.MAX

            for move in valid_moves:
                board.make_move(move)
                curr_score = self.minimax(
                    board=board,
                    depth=depth - 1,
                    alpha=alpha,
                    beta=beta,
                    is_maximizing=True,
                )

                board.unmake_move(move)
                best_score = min(best_score, curr_score)
                beta = min(beta, curr_score)

                if beta <= alpha:
                    break

        return best_score

    def get_name(self) -> str:
        return "MinimaxAgent Agent Depth " + str(self.depth)
