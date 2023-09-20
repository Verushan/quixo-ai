from ..logic import Agent, Move, Direction, Board, GUI, Piece
import string
import pygame as pg
import numpy as np


class HumanAgent(Agent):
    def __init__(self, use_ui_controls: bool = True) -> None:
        super().__init__()
        self.punctuation_translation = str.maketrans("", "", string.punctuation)
        self.use_ui_controls = use_ui_controls

    def clean_input(self, text: str):
        string = input(text)
        string = string.lower()
        string = string.translate(self.punctuation_translation)
        return string

    def string_to_color(self, direction_str: str):
        try:
            return Direction[direction_str.upper()]
        except KeyError:
            raise ValueError(f"'{direction_str}' is not a valid color")

    def _calculate_move(self, board: Board, direction: Direction) -> Move:
        x, y = pg.mouse.get_pos()
        row = Board.BOARD_DIM - (y // GUI.PIECE_HEIGHT) - 1
        col = x // GUI.PIECE_WIDTH
        square = row * Board.BOARD_DIM + col

        if square in Board.OUTER_INDICES:
            piece = board.board[square]
            piece_index = np.where(Board.OUTER_INDICES == square)[0][0]

            if piece == board.side_to_play or piece == Piece.NONE:
                if direction in Board.VALID_MOVES_FOR_INDICES[piece_index]:
                    return Move(square, direction)
                else:
                    print("INVALID MOVE")
                    return None

    def _get_ui_move(self, board: Board) -> Move:
        current_frame = pg.display.get_surface().copy()
        pg.event.clear()

        while True:
            direction = None

            for event in pg.event.get():
                if event.type == pg.WINDOWFOCUSGAINED:
                    pg.display.get_surface().blit(current_frame, (0, 0))
                    pg.display.update()

                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_w:
                        direction = Direction.NORTH
                    elif event.key == pg.K_s:
                        direction = Direction.SOUTH
                    elif event.key == pg.K_a:
                        direction = Direction.WEST
                    elif event.key == pg.K_d:
                        direction = Direction.EAST

                    if direction != None:
                        move = self._calculate_move(board, direction)

                        if move != None:
                            return move

    def get_move(self, board: Board, time_limit: float) -> Move:
        move = None

        if self.use_ui_controls:
            return self._get_ui_move(board)
        else:
            square = int(self.clean_input("Enter the square index "))
            direction = self.clean_input(
                "Enter a direction to move (NORTH, SOUTH, EAST WEST) "
            )
            direction = self.string_to_color(direction)

            move = Move(square, direction)

        return move

    def get_name(self) -> str:
        return "HumanAgent Agent"
