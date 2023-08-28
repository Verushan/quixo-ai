from ..logic.agent import Agent
from quixo import Move, Board, StateInfo, Piece


class MinimaxAgent(Agent):
    MAX = 1e6

    def __init__(self) -> None:
        super().__init__()

    def get_move(self, board: Board) -> Move:
        return super().get_move()

    def minimax(self, board: Board, is_maximizing: bool = False):
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

            return result if is_maximizing else -result
