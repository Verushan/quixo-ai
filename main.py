from quixo import (
    MinimaxAgent,
    RandomAgent,
    GameManager,
    Board,
    Move,
    Direction,
    StateInfo,
)

manager = GameManager()
agent1 = RandomAgent()
agent2 = MinimaxAgent()
manager.play_match(agent1, agent2)
