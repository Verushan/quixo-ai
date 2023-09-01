from ..logic import Agent, Move, Direction, Board
import string


class HumanAgent(Agent):
    def __init__(self) -> None:
        super().__init__()
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

    def get_move(self, board: Board) -> Move:
        square = int(self.clean_input("Enter the square index "))
        direction = self.clean_input(
            "Enter a direction to move (NORTH, SOUTH, EAST WEST) "
        )
        direction = self.string_to_color(direction)

        move = Move(square, direction)
        return move

    def get_name(self) -> str:
        return "Human Agent"
