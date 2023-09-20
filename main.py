from quixo import (
    MinimaxAgent,
    RandomAgent,
    GameManager,
    HumanAgent,
    CenterMinimaxAgent,
    EdgeMinimaxAgent,
    MonteCarloAgent,
    Agent,
)

agent1 = MinimaxAgent()
agent2 = MonteCarloAgent()
gm = GameManager()

gm.play_match(agent1, agent2)
