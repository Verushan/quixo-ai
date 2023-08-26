from engine import Direction, QuixoEnv, Board

quixo = QuixoEnv(render_mode="ansi")
quixo.render()

action = {
    "square": 0,
    "direction": Direction.NORTH,
}

observation, reward, is_terminal = quixo.step(action)

print("Feedback after taking action")

board = Board()
board.board = observation["board"]
board.side_to_play = observation["player"]
board.move_count = quixo.board.move_count

board.display()

print(reward)
print(is_terminal)