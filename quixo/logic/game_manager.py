from .board import Board, StateInfo, Piece
from .agent import Agent
from .gui import GUI
import pygame as pg
import numpy as np


class GameManager:
    MOVE_LIMIT = 100
    TIME_LIMIT_IN_SECONDS = 1.0

    def __init__(self, show_ui: bool = True) -> None:
        self.show_ui = show_ui

        if show_ui:
            self.gui = GUI()

    def _process_move(self, board: Board, agent: Agent):
        move = agent.get_move(board, GameManager.TIME_LIMIT_IN_SECONDS)

        if self.show_ui:
            self.gui.make_move(board.board, move, board.side_to_play)

        board.make_move(move)
        print(move)

    def play_match(
        self,
        agent_x: Agent,
        agent_o: Agent,
        fen: str = Board.STARTING_FEN,
        seed=None,
    ) -> StateInfo:
        np.random.seed(seed)
        board = Board(fen)

        if self.show_ui:
            self.gui.show_board(board.board)

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

        if self.show_ui is False:
            return result if result != StateInfo.IN_PROGRESS else StateInfo.DRAW

        GameManager.print_outcome(result, first_agent, second_agent)

        while True and self.show_ui:
            for event in pg.event.get():
                if event.type == pg.QUIT or event.type == pg.WINDOWCLOSE:
                    pg.quit()
                    return

            self.gui.show_board(board.board)

        return result if result != StateInfo.IN_PROGRESS else StateInfo.DRAW

    @staticmethod
    def print_outcome(state_info: StateInfo, agent1: Agent, agent2: Agent) -> None:
        if state_info == StateInfo.DRAW:
            print("DRAW!")
        elif state_info == StateInfo.X_WIN:
            print(agent1.get_name(), "WINS!")
        elif state_info == StateInfo.O_WIN:
            print(agent2.get_name(), "WINS!")
        else:
            print("DRAW BY {} MOVE LIMIT!".format(GameManager.MOVE_LIMIT))
