from quixo import RandomAgent, GameManager, Board, Move, Direction, StateInfo

# manager = GameManager()
# agent1 = RandomAgent()
# agent2 = RandomAgent()
# manager.play_match(agent1, agent2)

fen = "X3O/3O1/X3O/X3O/X3O X 0"
board = Board(fen)
board.display()

move = Move(15, Direction.NORTH)

board.make_move(move)
board.display()
board.unmake_move(move)

fen = "X3O/1X3/X3O/X3O/X3O O 0"
board.load_board_as_fen(fen)
board.display()
move = Move(19, Direction.NORTH)
board.make_move(move)
board.display()
