

from typing import List
from rocket import Rocket
from reward import Reward
from constants import *
import numpy as np


class Game:
    def __init__(self, rockets: List[Rocket], population_size: int) -> None:
        self.current_generation: int = 0
        self.population_size: int = population_size
        self.rockets: List[Rocket] = rockets
        self.board : dict[Rocket, np.float32] = {}

    def fill_score_board(self, reward: Reward) -> None:
        self.board: dict[Rocket, np.float32] = {}
        rockets: List[Rocket] = self.rockets
        for rocket_index in range(len(rockets)):
            rocket: Rocket = rockets[rocket_index]
            distance : np.float32  = np.linalg.norm(rocket.position - reward.position)
            score: np.float32 = 1 / (distance + 1)
            if rocket.hit_reward:
                score *= 10
            if rocket.hit_obstacle:
                score /= 10
            self.board[rocket] = score

    def get_best_rockets(self, number_of_rockets: int = 10) -> List[Rocket]:
        sorted_rockets = sorted(
            self.board.items(),
            key=lambda item: item[1],
            reverse=True 
        )
        return [rocket for rocket, _ in sorted_rockets[:number_of_rockets]]

    def get_board(self) -> dict[Rocket, np.float32]:
        return self.board

    def new_population(self, best_rockets: List[Rocket],) -> List[Rocket]:
        number_of_best_rockets: int = len(best_rockets)
        output: List[Rocket] = [Rocket(r.dna) for r in best_rockets]
        while len(output) < self.population_size:
            father_index: int = np.random.randint(0, number_of_best_rockets)
            mother_index: int = np.random.randint(0, number_of_best_rockets)
            while mother_index == father_index:
                mother_index = np.random.randint(0, number_of_best_rockets)
            new_rocket: Rocket = born_rocket(best_rockets[father_index], best_rockets[mother_index])
            output.append(new_rocket)
        return output

    def create_new_generation(self, best_rockets: List[Rocket],) -> List[Rocket]:
        new_population: List[Rocket] = self.new_population(best_rockets)
        self.rockets = new_population
        self.current_generation += 1
        return new_population

    def get_best_score(self) -> np.float32:
        best_rockets: List[Rocket] = self.get_best_rockets()
        return self.board[best_rockets[0]]


        


def born_rocket(father: Rocket, mother: Rocket) -> Rocket:
    father_dna: np.ndarray = father.dna
    mother_dna: np.ndarray = mother.dna


    split = np.random.randint(0, len(father_dna))

    child_dna = np.vstack((
        father_dna[:split],
        mother_dna[split:]
    ))

    mutation_mask = np.random.rand(len(child_dna)) < MUTATION_RATE

    new_genes = np.random.randint(-1, 2, size=(mutation_mask.sum(), 2), dtype=np.int32)

    child_dna[mutation_mask] = new_genes

    return Rocket(child_dna)
