import multiprocessing

from ..quixo import (
    MinimaxAgent,
    RandomAgent,
    GameManager,
    HumanAgent,
    CenterMinimaxAgent,
    EdgeMinimax,
    StateInfo,
    Agent,
)

import numpy as np

WIN = 0
LOSS = 1
DRAW = 2


manager = GameManager(show_ui=False)


def get_stats(
    agent_x_index: int,
    agent_o_index: int,
    agent_x: Agent,
    agent_o: Agent,
    output_queue,
):
    value = (0, 0, 0, 0)
    result = manager.play_match(agent_x, agent_o)

    if result == StateInfo.X_WIN:
        value = (agent_x_index, WIN, agent_o_index, LOSS)
    elif result == StateInfo.O_WIN:
        value = (agent_o_index, WIN, agent_x_index, LOSS)
    else:
        value = (agent_o_index, DRAW, agent_x_index, DRAW)

    output_queue.put(value)


processes = []
result_queue = multiprocessing.Manager().Queue()


agents = [MinimaxAgent(), EdgeMinimax(), CenterMinimaxAgent()]
num_agents = len(agents)

total_matches = 100
num_outcomes = 3

for match in range(total_matches):
    for x_index, agent_x in enumerate(agents):
        for o_index, agent_o in enumerate(agents):
            if x_index == o_index:
                continue

            process = multiprocessing.Process(
                target=get_stats,
                args=(x_index, o_index, agent_x, agent_o, result_queue),
            )

            processes.append(process)
            process.start()

for process in processes:
    process.join()

stats = np.zeros((num_agents, num_outcomes))

while not result_queue.empty():
    value = result_queue.get()
    x_index, x_state, o_index, o_state = value
    stats[x_index, x_state] += 1
    stats[o_index, o_state] += 1


for index, agent in enumerate(agents):
    win_rate = (stats[index, WIN] / stats[index, :].sum()) * 100
    loss_rate = (stats[index, LOSS] / stats[index, :].sum()) * 100
    draw_rate = (stats[index, DRAW] / stats[index, :].sum()) * 100
    print(
        agent.get_name(),
        "rates [win, loss, draw] [{}%, {}%, {}%]".format(
            win_rate, loss_rate, draw_rate
        ),
    )
