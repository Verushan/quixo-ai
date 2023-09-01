import numpy as np
from .move import Direction, Move
from .piece import Piece
from enum import IntEnum
from tabulate import tabulate


class StateInfo(IntEnum):
    X_WIN = 0
    O_WIN = 1
    DRAW = 2
    IN_PROGRESS = 3


class Board:
    BOARD_DIM = 5
    BOARD_LEN = 25

    NORTH_ROW_START_INDEX = 20
    SOUTH_ROW_START_INDEX = 0
    EAST_ROW_START_INDEX = 4
    WEST_ROW_START_INDEX = 0

    X_WIN_SUM = BOARD_DIM * Piece.X
    O_WIN_SUM = BOARD_DIM * Piece.O

    STARTING_FEN = "5/5/5/5/5 X 0"

    OUTER_INDICES = np.array(
        [0, 1, 2, 3, 4, 9, 14, 19, 24, 23, 22, 21, 20, 15, 10, 5], dtype=np.uint8
    )

    VALID_MOVES_FOR_INDICES = (
        np.array([Direction.NORTH, Direction.EAST]),
        np.array([Direction.NORTH, Direction.EAST, Direction.WEST]),
        np.array([Direction.NORTH, Direction.EAST, Direction.WEST]),
        np.array([Direction.NORTH, Direction.EAST, Direction.WEST]),
        np.array([Direction.NORTH, Direction.WEST]),
        np.array([Direction.WEST, Direction.NORTH, Direction.SOUTH]),
        np.array([Direction.WEST, Direction.NORTH, Direction.SOUTH]),
        np.array([Direction.WEST, Direction.NORTH, Direction.SOUTH]),
        np.array([Direction.SOUTH, Direction.WEST]),
        np.array([Direction.SOUTH, Direction.EAST, Direction.WEST]),
        np.array([Direction.SOUTH, Direction.EAST, Direction.WEST]),
        np.array([Direction.SOUTH, Direction.EAST, Direction.WEST]),
        np.array([Direction.SOUTH, Direction.EAST]),
        np.array([Direction.EAST, Direction.NORTH, Direction.SOUTH]),
        np.array([Direction.EAST, Direction.NORTH, Direction.SOUTH]),
        np.array([Direction.EAST, Direction.NORTH, Direction.SOUTH]),
    )

    def __init__(self, fen: str = STARTING_FEN):
        self.load_board_as_fen(fen)

    def load_board_as_fen(self, fen: str) -> None:
        fen_parts = fen.split(" ")
        board_str = fen_parts[0]

        self.side_to_play = Piece.X if fen_parts[1] == "X" else Piece.O
        self.move_count = int(fen_parts[2])
        self.board = np.full(
            shape=(Board.BOARD_LEN,), fill_value=Piece.EMPTY, dtype=np.int8
        )

        col = 0
        row = Board.BOARD_DIM - 1

        for c in board_str:
            if c == "/":
                col = 0
                row -= 1
                continue

            if c.isdigit():
                col += int(c)
                continue

            if c == "X":
                self.board[row * Board.BOARD_DIM + col] = Piece.X
            elif c == "O":
                self.board[row * Board.BOARD_DIM + col] = Piece.O
            else:
                self.board[row * Board.BOARD_DIM + col] = Piece.EMPTY

            col += 1

    def _get_end_square(self, move: Move) -> int:
        start_square = move.start_square
        direction = move.direction

        if direction == Direction.NORTH:
            end = Board.NORTH_ROW_START_INDEX + start_square % Board.BOARD_DIM
        elif direction == Direction.SOUTH:
            end = Board.SOUTH_ROW_START_INDEX + start_square % Board.BOARD_DIM
        elif direction == Direction.EAST:
            end = (
                Board.EAST_ROW_START_INDEX
                + start_square // Board.BOARD_DIM * Board.BOARD_DIM
            )
        else:
            end = (
                Board.WEST_ROW_START_INDEX
                + start_square // Board.BOARD_DIM * Board.BOARD_DIM
            )

        return end

    def _update_board(
        self, moving_piece: Piece, start: int, end: int, moving_direction: Direction
    ) -> None:
        step = 0

        if moving_direction == Direction.NORTH or moving_direction == Direction.SOUTH:
            step = Board.BOARD_DIM
        else:
            step = 1

        if moving_direction == Direction.NORTH or moving_direction == Direction.EAST:
            for i in range(start, end, step):
                self.board[i] = self.board[i + step]
        else:
            for i in range(start, end, -step):
                self.board[i] = self.board[i - step]

        self.board[end] = moving_piece

    def _sum_line(self, start, end, step) -> int:
        return self.board[start:end:step].sum()

    def get_state_info(self) -> StateInfo:
        x_line = False
        o_line = False

        for row in range(Board.BOARD_DIM):
            start = row * Board.BOARD_DIM
            end = start + Board.BOARD_DIM

            curr_sum = self._sum_line(start, end, 1)

            if curr_sum == self.X_WIN_SUM:
                x_line = True
            elif curr_sum == self.O_WIN_SUM:
                o_line = True

        for col in range(Board.BOARD_DIM):
            start = col
            end = self.NORTH_ROW_START_INDEX + col + 1

            curr_sum = self._sum_line(start, end, Board.BOARD_DIM)

            if curr_sum == self.X_WIN_SUM:
                x_line = True
            elif curr_sum == self.O_WIN_SUM:
                o_line = True

        # Main diagonal
        start, end = 0, Board.BOARD_LEN
        step = Board.BOARD_DIM + 1
        main_diag_sum = self._sum_line(start, end, step)

        if main_diag_sum == self.X_WIN_SUM:
            x_line = True
        elif main_diag_sum == self.O_WIN_SUM:
            o_line = True

        # Anti diagonal
        start, end = Board.BOARD_DIM - 1, Board.BOARD_LEN - 1
        step = Board.BOARD_DIM - 1
        anti_diag_sum = self._sum_line(start, end, step)

        if anti_diag_sum == self.X_WIN_SUM:
            x_line = True
        elif anti_diag_sum == self.O_WIN_SUM:
            o_line = True

        if x_line and o_line:
            if self.side_to_play == Piece.X:
                return StateInfo.X_WIN
            else:
                return StateInfo.O_WIN

        if x_line:
            return StateInfo.X_WIN

        if o_line:
            return StateInfo.O_WIN

        return StateInfo.IN_PROGRESS

    def make_move(self, move: Move) -> None:
        moving_piece = self.board[move.start_square]

        if moving_piece == Piece.EMPTY:
            moving_piece = self.side_to_play
            move.was_turned = True

        self.move_count += 1
        self.side_to_play = Piece.X if self.side_to_play == Piece.O else Piece.O
        end_square = self._get_end_square(move)
        self._update_board(moving_piece, move.start_square, end_square, move.direction)

    def unmake_move(self, move: Move) -> None:
        self.side_to_play = Piece.X if self.side_to_play == Piece.O else Piece.O
        self.move_count -= 1

        start = move.start_square
        end = self._get_end_square(move)

        moving_piece = self.board[end]
        moving_direction = move.direction

        if move.was_turned:
            moving_piece = Piece.EMPTY
            move.was_turned = False

        if moving_direction == Direction.NORTH:
            self._update_board(moving_piece, end, start, Direction.SOUTH)
        elif moving_direction == Direction.SOUTH:
            self._update_board(moving_piece, end, start, Direction.NORTH)
        elif moving_direction == Direction.EAST:
            self._update_board(moving_piece, end, start, Direction.WEST)
        else:
            self._update_board(moving_piece, end, start, Direction.EAST)

    def generate_valid_moves(self) -> list:
        valid_moves = []

        for index, indice in enumerate(self.OUTER_INDICES):
            piece = self.board[indice]

            if piece == self.side_to_play or piece == Piece.EMPTY:
                for direction in self.VALID_MOVES_FOR_INDICES[index]:
                    valid_moves.append(Move(indice, direction))

        return valid_moves

    def display(self, minimal: bool = False):
        board = np.full((Board.BOARD_DIM, Board.BOARD_DIM), "_", dtype=str)

        for i in range(Board.BOARD_DIM - 1, -1, -1):
            for j in range(Board.BOARD_DIM):
                piece = self.board[i * Board.BOARD_DIM + j]

                if piece == Piece.X:
                    board[i, j] = "X"
                elif piece == Piece.O:
                    board[i, j] = "O"

        print(tabulate(np.flipud(board), tablefmt="fancy_grid", stralign="center"))

        if minimal == False:
            print("Move count:", self.move_count)

            if self.side_to_play == Piece.X:
                print("Side to play: X")
            else:
                print("Side to play: O")

            state_info = self.get_state_info()
            print("Terminal status:", StateInfo(state_info).name)

        print()
