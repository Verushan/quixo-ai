from quixo import RandomAgent, GameManager, Board

manager = GameManager()
agent1 = RandomAgent()
agent2 = RandomAgent()
manager.play_match(Board.STARTING_FEN, agent1, agent2)
