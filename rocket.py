
import pygame
import numpy as np
from typing import List
from constants import *
from obstacle import Obstacle
from reward import Reward

class Rocket:
    def __init__(self, DNA : np.ndarray) -> None:
        self.dna: np.ndarray = DNA
        self.position: np.ndarray = np.array([X_SCREEN_SIZE - 100 , Y_SCREEN_SIZE - 150 ], dtype=np.int16)
        self.current_dna_index: int = 0
        self.hit_reward: bool = False
        self.hit_obstacle: bool = False

    def update(self) -> None:
        if self.current_dna_index < len(self.dna) - 1:
            movement_vector : np.ndarray = self.dna[self.current_dna_index]
            self.position += movement_vector
            self.current_dna_index += 1
        else :
            pass

    def draw(self, screen: pygame.Surface, COLOR: Tuple[int, int, int] = ROCKET_COLOR) -> None:
        x: int = self.position[0]
        y: int = self.position[1]
        position: pygame.math.Vector2 = pygame.math.Vector2(x, y)
        pygame.draw.circle(screen, COLOR, position, ROCKET_RADIUS)


    def resolve_collision(self, obstacle: Obstacle) -> None:
        delta = self.position - obstacle.position
        norm = np.linalg.norm(delta)
        if norm == 0:
            return
        normal = delta / norm
        direction = self.dna[self.current_dna_index].astype(np.float32)
        reflected = direction - 2 * np.dot(direction, normal) * normal
        reflected_int = np.sign(reflected).astype(np.int8)
        self.position += reflected_int
        radius_sum = ROCKET_RADIUS + OBSTACLE_RADIUS
        self.position = obstacle.position + normal * (radius_sum + 1)
        self.position = self.position.astype(np.int16)


    def set_hit_reward_flag(self) -> None:
        self.hit_reward = True

    def set_hit_obstacle_flag(self) -> None:
        self.hit_obstacle = True


    def check_collision_with_reward(self, reward: Reward) -> np.bool_:
        reward_position: np.ndarray = reward.position
        current_position: np.ndarray = self.position
        distance : np.float32 = np.linalg.norm(current_position - reward_position)
        return (distance <= (ROCKET_RADIUS + REWARD_RADIUS))

    def check_collision_obstacle(self, obstacle: Obstacle) -> np.bool_:
        obstacle_position: np.ndarray = obstacle.position
        current_position: np.ndarray = self.position
        distance : np.float32 = np.linalg.norm(current_position - obstacle_position)
        return (distance <= (ROCKET_RADIUS + OBSTACLE_RADIUS))


def generate_initial_dna(dna_count: int) -> np.ndarray:
    return np.random.randint(-1, 2, size=(dna_count, 2), dtype=np.int8)



def update_rockets(rockets: List[Rocket], obstacle: Obstacle, reward: Reward) -> None:
    for rocket in rockets:
        if rocket.check_collision_obstacle(obstacle):
            rocket.resolve_collision(obstacle)
            rocket.set_hit_obstacle_flag()
        if rocket.check_collision_with_reward(reward):
            rocket.set_hit_reward_flag()
        rocket.update()

def draw_rockets(rockets: List[Rocket], screen: pygame.Surface) -> None:
    for rocket in rockets:
        rocket.draw(screen)


def create_rockets(dna_count: int = 10, number_of_rockets: int = 10) -> List[Rocket]:
    rockets: List[Rocket] =[]
    for _ in range(number_of_rockets):
        dna: np.ndarray = generate_initial_dna(dna_count)
        new_rocket: Rocket = Rocket(dna)
        rockets.append(new_rocket)
    return rockets
