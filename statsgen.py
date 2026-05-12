import json
from pathlib import Path
from typing import List, Dict

import numpy as np
import matplotlib.pyplot as plt

from rocket import Rocket, update_rockets, create_rockets
from obstacle import Obstacle
from reward import Reward
from game import Game
from constants import *






frames_count = np.arange(100, 2000, 200)
rocket_count = np.arange(100, 1000, 100)

max_generation = 20
OUTPUT_FILE = Path("experiment_results.json")






def run_simulation(
    frame_max: int,
    rockets_count: int,
    max_generation: int
) -> float:

    rockets: List[Rocket] = create_rockets(
        dna_count=frame_max,
        number_of_rockets=rockets_count
    )

    obstacle = Obstacle(
        np.array(
            [X_SCREEN_SIZE // 2.5, Y_SCREEN_SIZE // 2.5],
            dtype=np.int16,
        )
    )

    reward = Reward(
        np.array([100, 100], dtype=np.int16)
    )

    game = Game(rockets, rockets_count)

    frames = 0

    while game.current_generation < max_generation:

        update_rockets(rockets, obstacle, reward)

        frames += 1

        if frames == frame_max:

            game.fill_score_board(reward)

            rockets = game.create_new_generation(
                game.get_best_rockets()
            )

            frames = 0

    return float(game.get_best_score())






def load_existing_results() -> Dict:
    if OUTPUT_FILE.exists():
        print("Loading existing results...")
        with open(OUTPUT_FILE, "r") as f:
            return json.load(f)
    return {}


def save_results(data: Dict) -> None:
    with open(OUTPUT_FILE, "w") as f:
        json.dump(data, f, indent=4)






def run_experiment():

    results = load_existing_results()

    for frame_max in frames_count:
        frame_key = str(frame_max)

        if frame_key not in results:
            results[frame_key] = {}

        for rockets in rocket_count:
            rocket_key = str(rockets)


            if rocket_key in results[frame_key]:
                print(
                    f"Skipping frames={frame_max}, rockets={rockets}"
                )
                continue

            print(
                f"Running simulation "
                f"(frames={frame_max}, rockets={rockets})"
            )

            score = run_simulation(
                frame_max,
                rockets,
                max_generation,
            )

            results[frame_key][rocket_key] = score


            save_results(results)

    return results






def plot_results(results: Dict):

    heatmap = np.zeros(
        (len(frames_count), len(rocket_count))
    )

    for i, frame_max in enumerate(frames_count):
        for j, rockets in enumerate(rocket_count):

            heatmap[i, j] = results[str(frame_max)][str(rockets)]

    plt.figure(figsize=(10, 6))

    plt.imshow(
        heatmap,
        origin="lower",
        aspect="auto",
        extent=[
            rocket_count[0],
            rocket_count[-1],
            frames_count[0],
            frames_count[-1],
        ],
    )

    plt.colorbar(label="Best Score")

    plt.xlabel("Rocket Count")
    plt.ylabel("Frame Count")
    plt.title("Rocket Evolution Hyperparameter Search")

    plt.show()






if __name__ == "__main__":

    results = run_experiment()

    plot_results(results)
