from quixo_game import Board, Move, Direction, QuixoEnv

quixo = QuixoEnv(render_mode="ansi")
quixo.render()
result = quixo.step({
    "square": 20,
    "direction": Direction.EAST,
})

print(result)

quixo.render()