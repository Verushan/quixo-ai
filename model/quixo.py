import gym
from gym import spaces
import numpy as np

from .piece import Piece
from .move import Move
from .board import Board

class QuixoEnv(gym.Env):
    FPS = 15
    WINDOW_SIZE = 150

    metadata = {
        "render_modes": ["human", "ansi"], 
        "render_fps": FPS
    }

    def __init__(self, render_mode=None, fen: str = None):
        self.observation_space = spaces.Dict({
            "board": spaces.Box(Piece.X, Piece.EMPTY, shape=(self.BOARD_LEN,), dtype=np.uint8),
            "player": spaces.Discrete(2)
        })

        self.action_space = spaces.Dict({
            "direction": spaces.Discrete(4),
            "square": spaces.Box(0, self.BOARD_LEN - 1, shape=(1,), dtype=np.uint8)
        })

        assert render_mode is None or render_mode in self.metadata["render_modes"]
        
        if (fen is None):
            self.board = Board()
        else:
            self.board = Board(fen)

        self.window = None
        self.clock = None

    def _get_obs(self):
        return {
            "board": self.board.board,
            "player": self.board.side_to_play
        }

    def reset(self):
        super().reset()
        self.board = Board()
        observation = self._get_obs()

        if (self.render_mode == "human"):
            self._render_frame()

        return observation

    def step(self, action):
        move = Move(action["square"], action["direction"])
        self.board.make_move(move)

    def render(self):
        if (self.render_mode == "ansi"):
            self.board.display()
        else:
            self._render_frame()
    
    def _render_frame(self):
        raise NotImplementedError

    def close(self):
        pass