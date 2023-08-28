from .board import Board, StateInfo, Piece
from .agent import Agent
import time


class GameManager:
    MOVE_LIMIT = 150
    DELAY = 1

    def __init__(self) -> None:
        pass

    def play_match(
        self, agent_x: Agent, agent_o: Agent, fen: str = Board.STARTING_FEN
    ) -> None:
        board = Board(fen)
        is_terminal = board.get_state_info() != StateInfo.IN_PROGRESS

        if board.side_to_play == Piece.X:
            first_agent, second_agent = agent_x, agent_o
        else:
            first_agent, second_agent = agent_o, agent_x

        while not is_terminal and board.move_count <= GameManager.MOVE_LIMIT:
            first_agent_move = first_agent.get_move(board)
            print(first_agent_move)
            board.make_move(first_agent_move)
            board.display()
            time.sleep(GameManager.DELAY)

            is_terminal = board.get_state_info() != StateInfo.IN_PROGRESS

            if is_terminal:
                break

            second_agent_move = second_agent.get_move(board)
            print(second_agent_move)
            board.make_move(second_agent_move)
            board.display()
            time.sleep(GameManager.DELAY)
            is_terminal = board.get_state_info() != StateInfo.IN_PROGRESS

        result = board.get_state_info()
        self.print_outcome(result)

    @staticmethod
    def print_outcome(state_info: StateInfo) -> None:
        if state_info == StateInfo.DRAW:
            print("DRAW!")
        elif state_info == StateInfo.X_WIN:
            print("X WINS!")
        elif state_info == StateInfo.O_WIN:
            print("O WINS!")
        else:
            print("GAME IN PROGRESS!")
