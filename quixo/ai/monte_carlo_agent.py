from quixo.logic.board import Board
from quixo.logic.move import Move
from ..logic import Agent, Move, Piece, Board
import numpy as np


class Node:
    pass


class Node:
    def __init__(self, move: Move, parent: Node = None) -> None:
        self.evaluation = 0
        self.visited = 0
        self.move = move
        self.parent = parent
        self.children = []


class MonteCarloAgent(Agent):
    MAX = 1e6
    C = np.sqrt(2)
    SIMULATION_MOVE_LIMIT = 100

    def __init__(self, num_iterations: int) -> None:
        super().__init__()
        self.root = Node(None)
        self.num_iterations = num_iterations

    def _get_ucb(self, node: Node) -> float:
        if node.visited == 0:
            return MonteCarloAgent.MAX

        exploitation = node.evaluation / node.visited
        exploration = MonteCarloAgent.C * np.sqrt(
            np.log(node.parent.visited) / node.visited
        )

        return exploitation + exploration

    def _get_best_child(self, node: Node) -> Node:
        best_child = None
        best_score = 0

        for child in node.children:
            curr_score = self._get_ucb(child)

            if best_child is None or curr_score > best_score:
                best_child = child
                best_score = curr_score

        return best_child

    def _select_node(self, board: Board) -> tuple:
        curr = self.root
        moves = []

        while len(curr.children) > 0:
            best_child = self._get_best_child(curr)

            board.make_move(best_child.move)
            moves.append(best_child.move)

            curr = best_child

        return curr, moves

    def _expand_node(self, node: Node, board: Board) -> None:
        if board.get_winner() != Piece.NONE:
            return node

        valid_moves = board.generate_valid_moves()

        for move in valid_moves:
            move_node = Node(move, node)
            node.children.append(move_node)

        return np.random.choice(node.children)

    def _get_random_move(self, board: Board) -> Move:
        blank_pieces = board.board[Board.OUTER_INDICES] == Piece.NONE
        curr_player_pieces = board.board[Board.OUTER_INDICES] == board.side_to_play

        valid_indices = np.where(blank_pieces | curr_player_pieces)[0]
        index = np.random.choice(valid_indices)

        start_square = Board.OUTER_INDICES[index]
        direction = np.random.choice(Board.VALID_MOVES_FOR_INDICES[index])

        return Move(start_square, direction)

    def _simulate(self, board: Board) -> int:
        moves = []
        move_count = 0

        is_in_progress = board.get_winner() == Piece.NONE

        while move_count <= MonteCarloAgent.SIMULATION_MOVE_LIMIT and is_in_progress:
            move = self._get_random_move(board)
            board.make_move(move)
            moves.append(move)

            is_in_progress = board.get_winner() == Piece.NONE
            move_count += 1

        result = board.get_winner()

        for move in reversed(moves):
            board.unmake_move(move)

        if result == Piece.NONE:
            return 0

        if result != board.side_to_play:
            return 1

        return -1

    def _backpropagate(self, expanded_node: Node, outcome: int) -> None:
        curr = expanded_node

        while curr.parent != None:
            curr.visited += 1
            curr.evaluation += outcome
            outcome = -outcome
            curr = curr.parent

        curr.visited += 1

    def _perform_iteration(self, board: Board):
        selected_node, moves = self._select_node(board)

        if board.get_winner() == Piece.NONE:
            expanded_node = self._expand_node(selected_node, board)
            board.make_move(expanded_node.move)
            simulated_outcome = self._simulate(board)
            board.unmake_move(expanded_node.move)
            self._backpropagate(expanded_node, simulated_outcome)
        else:
            simulated_outcome = self._simulate(board)
            self._backpropagate(selected_node, simulated_outcome)

        for move in reversed(moves):
            board.unmake_move(move)

    def get_move(self, board: Board, time_limit: float) -> Move:
        self.root = Node(None)

        for _ in range(self.num_iterations):
            self._perform_iteration(board)

        def win_visit_ratio(node: Node) -> float:
            return node.visited

        best_node = max(self.root.children, key=win_visit_ratio)
        return best_node.move

    def get_name(self) -> str:
        return "Monte Carlo Agent " + str(self.num_iterations) + " iterations"
