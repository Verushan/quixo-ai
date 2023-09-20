from .board import Board, Piece
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
            print(move)

        board.make_move(move)

    def play_match(
        self,
        agent_x: Agent,
        agent_o: Agent,
        fen: str = Board.STARTING_FEN,
        seed=None,
    ) -> tuple:
        np.random.seed(seed)
        board = Board(fen)

        if self.show_ui:
            self.gui.show_board(board.board)

        is_terminal = board.get_winner() != Piece.NONE
        first_agent, second_agent = agent_x, agent_o

        while not is_terminal and board.move_count <= GameManager.MOVE_LIMIT:
            self._process_move(board, first_agent)
            is_terminal = board.get_winner() != Piece.NONE

            if is_terminal:
                break

            self._process_move(board, second_agent)
            is_terminal = board.get_winner() != Piece.NONE

        result = board.get_winner()

        if self.show_ui is False:
            return result, board.move_count

        GameManager.print_outcome(result, first_agent, second_agent)

        while True and self.show_ui:
            for event in pg.event.get():
                if event.type == pg.QUIT or event.type == pg.WINDOWCLOSE:
                    pg.quit()
                    return

            self.gui.show_board(board.board)

        return result, board.move_count

    @staticmethod
    def print_outcome(winner: Piece, agent1: Agent, agent2: Agent) -> None:
        if winner == Piece.NONE:
            print("DRAW!")
        elif winner == Piece.X:
            print(agent1.get_name(), "WINS!")
        elif winner == Piece.O:
            print(agent2.get_name(), "WINS!")
        else:
            print("DRAW BY {} MOVE LIMIT!".format(GameManager.MOVE_LIMIT))
