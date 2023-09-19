from quixo import (
    MinimaxAgent,
    RandomAgent,
    GameManager,
    HumanAgent,
    CenterMinimaxAgent,
    EdgeMinimax,
    StateInfo,
    Agent,
)

agent1 = HumanAgent()
agent2 = MinimaxAgent()
gm = GameManager()

gm.play_match(agent1, agent2)
