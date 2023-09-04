from ..logic import Agent, Move, Direction, Board, GUI, Piece
import string
import pygame as pg
import numpy as np


class HumanAgent(Agent):
    def __init__(self, input_mode: str = "human") -> None:
        super().__init__()
        self.input_mode = input_mode
        self.punctuation_translation = str.maketrans("", "", string.punctuation)

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

    def get_ui_move(self, board: Board) -> Move:
        while True:
            direction = None

            for event in pg.event.get():
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
                        x, y = pg.mouse.get_pos()
                        row = Board.BOARD_DIM - (y // GUI.PIECE_HEIGHT) - 1
                        col = x // GUI.PIECE_WIDTH
                        square = row * Board.BOARD_DIM + col
                        print("Square index", square)

                        if square in Board.OUTER_INDICES:
                            piece = board.board[square]
                            piece_index = np.where(Board.OUTER_INDICES == square)[0][0]

                            if piece == board.side_to_play or piece == Piece.EMPTY:
                                if (
                                    direction
                                    in Board.VALID_MOVES_FOR_INDICES[piece_index]
                                ):
                                    return Move(square, direction)
                                else:
                                    print("INVALID MOVE")

    def get_move(self, board: Board) -> Move:
        move = None

        if self.input_mode == "human":
            return self.get_ui_move(board)
        else:
            square = int(self.clean_input("Enter the square index "))
            direction = self.clean_input(
                "Enter a direction to move (NORTH, SOUTH, EAST WEST) "
            )
            direction = self.string_to_color(direction)

            move = Move(square, direction)
        return move

    def get_name(self) -> str:
        return "Human Agent"
