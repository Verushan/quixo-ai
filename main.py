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

agent1 = HumanAgent()
agent2 = MonteCarloAgent(100)
gm = GameManager()

gm.play_match(agent1, agent2)
