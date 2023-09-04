from quixo import MinimaxAgent, RandomAgent, GameManager, HumanAgent

manager = GameManager()
agent1 = HumanAgent(input_mode="human")
agent2 = MinimaxAgent()
manager.play_match(agent1, agent2)
