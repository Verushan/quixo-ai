from quixo import RandomAgent, GameManager, Board

manager = GameManager()
agent1 = RandomAgent()
agent2 = RandomAgent()
manager.play_match(agent1, agent2)
