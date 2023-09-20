import multiprocessing as mp
from collections import defaultdict

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
        value = (0, 0, 0, 0, 0)
        result, move_count = self.manager.play_match(agent_x, agent_o)

        if result == Piece.X:
            value = (
                agent_x_index,
                Tournament.WIN,
                agent_o_index,
                Tournament.LOSS,
                move_count,
            )
        elif result == Piece.O:
            value = (
                agent_o_index,
                Tournament.WIN,
                agent_x_index,
                Tournament.LOSS,
                move_count,
            )
        else:
            value = (
                agent_o_index,
                Tournament.DRAW,
                agent_x_index,
                Tournament.DRAW,
                move_count,
            )

        output_queue.put(value)

    def start(self, agents: list, num_rounds: int) -> dict:
        processes = []
        result_queue = mp.Manager().Queue()

        num_agents = len(agents)

        for _ in range(num_rounds):
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
        game_length_sums = defaultdict(list)

        while not result_queue.empty():
            value = result_queue.get()
            x_index, x_state, o_index, o_state, move_count = value
            x_name = agents[x_index].get_name()
            o_name = agents[o_index].get_name()

            game_length_sums[x_name].append(move_count)
            game_length_sums[o_name].append(move_count)

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
            result[agent.get_name()] = "[{}%, {}%, {}%]".format(
                win_rate, loss_rate, draw_rate
            )

        game_length_stats = defaultdict(str)

        for key, value in game_length_sums.items():
            average = np.average(value)
            variance = np.var(value)

            game_length_stats[key] = "Average move count {}, Variance {}".format(
                np.round(average, 2), np.round(variance, 2)
            )

        return result, game_length_stats


def main():
    num_rounds = 100

    agents = [
        RandomAgent(),
        MinimaxAgent(1),
        EdgeMinimaxAgent(1),
        CenterMinimaxAgent(1),
        MonteCarloAgent(100),
        MinimaxAgent(2),
        EdgeMinimaxAgent(2),
        CenterMinimaxAgent(2),
        MonteCarloAgent(1000),
        MinimaxAgent(3),
        EdgeMinimaxAgent(3),
        CenterMinimaxAgent(3),
        MonteCarloAgent(2000),
        MinimaxAgent(4),
        EdgeMinimaxAgent(4),
        CenterMinimaxAgent(4),
        MonteCarloAgent(3000),
        MonteCarloAgent(4000),
        MonteCarloAgent(5000),
    ]

    tournament = Tournament()
    results, game_length_stats = tournament.start(agents, num_rounds)

    print("Rounds played:", num_rounds)

    for key, value in results.items():
        print(key)
        print("Performance [win, loss, draw]", value)
        print("Game length", game_length_stats[key])
        print()


if __name__ == "__main__":
    main()
