from .board import Board, StateInfo, Piece
from .agent import Agent
from .gui import GUI
import pygame as pg


class GameManager:
    MOVE_LIMIT = 150

    def __init__(self) -> None:
        self.gui = GUI()

    def _process_move(self, board: Board, agent: Agent):
        move = agent.get_move(board)
        self.gui.make_move(board.board, move, board.side_to_play)
        board.make_move(move)
        print(agent.get_name(), "played", move)

    def play_match(
        self, agent_x: Agent, agent_o: Agent, fen: str = Board.STARTING_FEN
    ) -> None:
        board = Board(fen)
        self.gui.update(board.board)

        is_terminal = board.get_state_info() != StateInfo.IN_PROGRESS

        if board.side_to_play == Piece.X:
            first_agent, second_agent = agent_x, agent_o
        else:
            first_agent, second_agent = agent_o, agent_x

        while not is_terminal and board.move_count <= GameManager.MOVE_LIMIT:
            self._process_move(board, first_agent)
            is_terminal = board.get_state_info() != StateInfo.IN_PROGRESS

            if is_terminal:
                break

            self._process_move(board, second_agent)
            is_terminal = board.get_state_info() != StateInfo.IN_PROGRESS

        result = board.get_state_info()
        self.print_outcome(result)

        while True:
            for event in pg.event.get():
                if event == pg.QUIT or event == pg.WINDOWCLOSE:
                    pg.quit()

                self.gui.update(board.board)

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
