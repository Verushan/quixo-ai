from quixo import MinimaxAgent, RandomAgent, GameManager, HumanAgent

fen = "XXOX1/XOO2/OXO1O/XO1XX/XXXOO X 24"
manager = GameManager()
agent1 = HumanAgent()
agent2 = MinimaxAgent()
manager.play_match(agent1, agent2, fen)
