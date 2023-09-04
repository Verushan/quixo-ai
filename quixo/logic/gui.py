from .board import Board
from .move import Move
from .piece import Piece
import pygame as pg
from pygame import gfxdraw
import numpy as np


class GUI:
    WIDTH = 800
    HEIGHT = 800
    WINDOW_TITLE = "Quixo AI"
    BACKGROUND_COLOR = (76, 86, 106)
    PIECE_COLOR = (143, 188, 187)
    PIECE_OUTLINE_WIDTH = 5
    PIECE_OUTLINE_CORNER_RADIUS = 10
    PIECE_WIDTH = WIDTH // Board.BOARD_DIM
    PIECE_HEIGHT = HEIGHT // Board.BOARD_DIM

    def __init__(self) -> None:
        pg.init()
        self.screen = pg.display.set_mode((GUI.WIDTH, GUI.HEIGHT))
        pg.display.set_caption(GUI.WINDOW_TITLE)

    def _draw_piece_outline(self, pos: tuple):
        rect = pg.Rect(*pos, GUI.PIECE_WIDTH, GUI.PIECE_HEIGHT)

        pg.draw.rect(
            self.screen,
            GUI.PIECE_COLOR,
            rect,
            GUI.PIECE_OUTLINE_WIDTH,
            GUI.PIECE_OUTLINE_CORNER_RADIUS,
        )

    def _draw_thick_line(self, p1: np.ndarray, p2: np.ndarray):
        length = np.linalg.norm(p1 - p2)
        thickness = 10
        center = (p1 + p2) / 2
        angle = np.arctan2(p1[1] - p2[1], p1[0] - p2[0])

        upper_left = (
            center[0] + (length / 2) * np.cos(angle) - (thickness / 2) * np.sin(angle),
            center[1] + (thickness / 2) * np.cos(angle) + (length / 2) * np.sin(angle),
        )

        upper_right = (
            center[0] - (length / 2) * np.cos(angle) - (thickness / 2) * np.sin(angle),
            center[1] + (thickness / 2) * np.cos(angle) - (length / 2) * np.sin(angle),
        )

        lower_left = (
            center[0] + (length / 2) * np.cos(angle) + (thickness / 2) * np.sin(angle),
            center[1] - (thickness / 2) * np.cos(angle) + (length / 2) * np.sin(angle),
        )

        lower_right = (
            center[0] - (length / 2) * np.cos(angle) + (thickness / 2) * np.sin(angle),
            center[1] - (thickness / 2) * np.cos(angle) - (length / 2) * np.sin(angle),
        )

        gfxdraw.aapolygon(
            self.screen,
            (upper_left, upper_right, lower_right, lower_left),
            GUI.PIECE_COLOR,
        )

        gfxdraw.filled_polygon(
            self.screen,
            (upper_left, upper_right, lower_right, lower_left),
            GUI.PIECE_COLOR,
        )

    def _draw_x(self, pos: tuple):
        self._draw_piece_outline(pos)

        padding = 20
        top_left = np.array(pos) + padding

        bottom_right = (
            np.array([top_left[0] + GUI.PIECE_WIDTH, top_left[1] + GUI.PIECE_HEIGHT])
            - 2 * padding
        )

        self._draw_thick_line(top_left, bottom_right)

        top_right = np.array([pos[0] + GUI.PIECE_WIDTH - padding, pos[1] + padding])

        bottom_left = np.array([pos[0] + padding, pos[1] + GUI.PIECE_HEIGHT - padding])

        self._draw_thick_line(bottom_left, top_right)

    def _draw_o(self, pos):
        self._draw_piece_outline(pos)
        radius = 60
        outline_thickness = 10
        pos = (pos[0] + (GUI.PIECE_WIDTH // 2), pos[1] + (GUI.PIECE_HEIGHT // 2))

        gfxdraw.filled_circle(self.screen, *pos, radius, GUI.PIECE_COLOR)
        gfxdraw.aacircle(self.screen, *pos, radius, GUI.PIECE_COLOR)

        gfxdraw.filled_circle(
            self.screen, *pos, radius - outline_thickness, GUI.BACKGROUND_COLOR
        )

        gfxdraw.aacircle(
            self.screen, *pos, radius - outline_thickness, GUI.BACKGROUND_COLOR
        )

    def _draw_board(self, board: np.ndarray, custom_pos: np.ndarray = None):
        self.screen.fill(GUI.BACKGROUND_COLOR)

        for index, piece in enumerate(board):
            row = index // Board.BOARD_DIM
            col = index % Board.BOARD_DIM
            pos = (
                GUI.PIECE_WIDTH * col,
                (Board.BOARD_DIM - row - 1) * GUI.PIECE_HEIGHT,
            )

            if piece == Piece.X:
                self._draw_x(pos)
            elif piece == Piece.O:
                self._draw_o(pos)
            else:
                self._draw_piece_outline(pos)

    def make_move(move: Move):
        pass

    def update(self, board: np.ndarray):
        self._draw_board(board)
        pg.display.update()
