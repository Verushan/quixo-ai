import numpy as np
from .move import Direction, Move
from .piece import Piece

class Board:
    BOARD_DIM = 5
    BOARD_LEN = 25

    NORTH_ROW_START_INDEX = 20;
    SOUTH_ROW_START_INDEX = 0;
    EAST_ROW_START_INDEX = 4;
    WEST_ROW_START_INDEX = 0;

    STARTING_FEN = "5/5/5/5/5 X 0"

    OUTER_INDICES = np.array([
        0, 1, 2, 3, 4, 9, 14, 19, 24, 23, 22, 21, 20, 15, 10, 5],
        dtype=np.uint8
    );

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
        np.array([Direction.EAST, Direction.NORTH, Direction.SOUTH])
    )

    def __init__(self, fen: str = STARTING_FEN):
        self.load_board_as_fen(fen)

    def load_board_as_fen(self, fen: str) -> None:
        fen_parts = fen.split(" ")
        board_str = fen_parts[0]

        self.side_to_play = Piece.X if fen_parts[1] == "X" else Piece.O
        self.move_count = int(fen_parts[2])
        self.board = np.full(
            shape=(Board.BOARD_LEN,),
            fill_value=Piece.EMPTY, 
            dtype=np.int8
        )

        col = 0
        row = Board.BOARD_DIM - 1

        for c in board_str:
            if (c == '/'):
                col = 0
                row -= 1
                continue
            
            if (c.isdigit()):
                col += int(c)
                continue
        
            if (c == 'X'):
                self.board[row * Board.BOARD_DIM + col] = Piece.X
            elif (c == 'O'):
                self.board[row * Board.BOARD_DIM + col] = Piece.O
            else:
                self.board[row * Board.BOARD_DIM + col] = Piece.EMPTY
            
            col += 1

    def _get_end_square(self, move: Move) -> int:
        start_square = move.start_square
        direction = move.direction

        if (direction == Direction.NORTH):
            end = Board.NORTH_ROW_START_INDEX + start_square % Board.BOARD_DIM
        elif (direction == Direction.SOUTH):
            end = Board.SOUTH_ROW_START_INDEX + start_square % Board.BOARD_DIM
        elif (direction == Direction.EAST):
            end = Board.EAST_ROW_START_INDEX + start_square // Board.BOARD_DIM * Board.BOARD_DIM
        else:
            end = Board.WEST_ROW_START_INDEX + start_square // Board.BOARD_DIM * Board.BOARD_DIM

        return end

    def _update_board(self, moving_piece: Piece, move: Move):
        start = move.start_square
        moving_direction = move.direction
        end, step = self._get_end_square(move), 0

        if (moving_direction == Direction.NORTH or moving_direction == Direction.SOUTH):
            step = Board.BOARD_DIM
        else:
            step = 1

        if (moving_direction == Direction.NORTH or moving_direction == Direction.EAST):
            for i in range(start, end, step):
                self.board[i] = self.board[i + step]
        else:
            for i in range(start, end, -step):
                self.board[i] = self.board[i - step]

        self.board[end] = moving_piece

    def _sum_line(self, start, end, step):
        return self.board[start:end:step].sum()

    def is_terminal(self):
        win_sum = 5 * self.side_to_play

        for row in range(Board.BOARD_DIM):
            start = row * Board.BOARD_DIM
            end = start + Board.BOARD_DIM

            if (self._sum_line(start, end, 1) == win_sum):
                return True

        for col in range(Board.BOARD_DIM):
            start = col
            end = self.NORTH_ROW_START_INDEX + col + 1

            if (self._sum_line(start, end, Board.BOARD_DIM) == win_sum):
                return True

        if (self._sum_line(0, Board.BOARD_LEN, Board.BOARD_DIM + 1) == win_sum):
            return True
        
        return self._sum_line(Board.BOARD_DIM - 1, Board.BOARD_LEN - 1, Board.BOARD_DIM - 1) == win_sum

    def make_move(self, move: Move):
        moving_piece = self.board[move.start_square]

        if (moving_piece == Piece.EMPTY):
            moving_piece = self.side_to_play
            move.was_turned = True
        
        self.move_count += 1
        self.side_to_play = Piece.X if self.side_to_play == Piece.O else Piece.O
        self._update_board(moving_piece, move)


    def unmake_move(self, move: Move):
        self.side_to_play = Piece.X if self.side_to_play == Piece.O else Piece.O
        self.move_count -= 1

        start = move.start_square
        end = self._get_end_square(move)

        moving_piece = self.board[end]
        moving_direction = move.direction

        if (moving_direction == Direction.NORTH):
            move.direction = Direction.SOUTH
        elif (moving_direction == Direction.SOUTH):
            move.direction = Direction.NORTH
        elif (moving_direction == Direction.EAST):
            move.direction = Direction.WEST
        else:
            move.direction = Direction.EAST
        
        move.start_square = end

        if (move.was_turned):
            moving_piece = Piece.EMPTY
            move.was_turned = False

        self._update_board(moving_piece, move)
        
        move.start_square = start
        move.direction = moving_direction

    
    def display(self):
        for i in range(Board.BOARD_DIM - 1, -1, -1):
            for j in range(Board.BOARD_DIM):
                piece = self.board[i * Board.BOARD_DIM + j]

                if (piece == Piece.X):
                    print("X", end=" ")
                elif (piece == Piece.O):
                    print("O", end=" ")
                else:
                    print("_", end=" ")
            print()

        print("Move count:", self.move_count)

        if (self.side_to_play == Piece.X):
            print("Side to play: X")
        else:
            print("Side to play: O")