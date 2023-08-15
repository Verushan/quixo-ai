from engine import Board, Move, Direction, QuixoEnv

quixo = QuixoEnv(render_mode="ansi")
quixo.render()
result = quixo.step({
    "square": 0,
    "direction": Direction.NORTH,
})

print(result)

quixo.render()