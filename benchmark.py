import multiprocessing as mp

from quixo import (
    MinimaxAgent,
    RandomAgent,
    GameManager,
    HumanAgent,
    CenterMinimaxAgent,
    EdgeMinimaxAgent,
    MonteCarloAgent,
    Agent,
    Piece,
)

import numpy as np


class Tournament:
    WIN = 0
    LOSS = 1
    DRAW = 2
    NUM_OUTCOMES = 3

    def __init__(self) -> None:
        self.manager = GameManager(show_ui=False)

    def get_stats(
        self,
        agent_x_index: int,
        agent_o_index: int,
        agent_x: Agent,
        agent_o: Agent,
        output_queue,
    ) -> None:
        value = (0, 0, 0, 0)
        result = self.manager.play_match(agent_x, agent_o)

        if result == Piece.X:
            value = (agent_x_index, Tournament.WIN, agent_o_index, Tournament.LOSS)
        elif result == Piece.O:
            value = (agent_o_index, Tournament.WIN, agent_x_index, Tournament.LOSS)
        else:
            value = (agent_o_index, Tournament.DRAW, agent_x_index, Tournament.DRAW)

        output_queue.put(value)

    def start(self, agents: list) -> dict:
        processes = []
        result_queue = mp.Manager().Queue()

        num_agents = len(agents)

        for x_index, agent_x in enumerate(agents):
            for o_index, agent_o in enumerate(agents):
                if x_index == o_index:
                    continue

                process = mp.Process(
                    target=self.get_stats,
                    args=(x_index, o_index, agent_x, agent_o, result_queue),
                )

                processes.append(process)
                process.start()

        for process in processes:
            process.join()

        stats = np.zeros((num_agents, Tournament.NUM_OUTCOMES))

        while not result_queue.empty():
            value = result_queue.get()
            x_index, x_state, o_index, o_state = value
            stats[x_index, x_state] += 1
            stats[o_index, o_state] += 1

        result = {}

        for index, agent in enumerate(agents):
            win_rate = np.round(
                (stats[index, Tournament.WIN] / stats[index, :].sum()) * 100, 2
            )
            loss_rate = np.round(
                (stats[index, Tournament.LOSS] / stats[index, :].sum()) * 100, 2
            )
            draw_rate = np.round(
                (stats[index, Tournament.DRAW] / stats[index, :].sum()) * 100, 2
            )
            result[agent.get_name()] = "rates [win, loss, draw] [{}%, {}%, {}%]".format(
                win_rate, loss_rate, draw_rate
            )

        return result


def main():
    agents = [
        MinimaxAgent(),
        EdgeMinimaxAgent(),
        CenterMinimaxAgent(),
        MonteCarloAgent(),
    ]

    tournament = Tournament()
    results = tournament.start(agents)

    for key, value in results.items():
        print(key, value)


if __name__ == "__main__":
    main()
