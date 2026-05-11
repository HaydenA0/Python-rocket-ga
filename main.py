import pygame
from typing import List
import numpy as np

from rocket import Rocket, update_rockets, draw_rockets, create_rockets
from obstacle import Obstacle
from reward import Reward
from game import Game
from constants import *


def print_board(rockets: List[Rocket], board: dict[Rocket, np.float32]) -> None:
    for rocket_index in range(len(rockets)):
        rocket: Rocket = rockets[rocket_index]
        score: np.float32 = board[rocket]
        print(f"rocket {rocket_index} score: {score}")

def debug_print(frames: int, FRAME_MAX: int, rockets: List[Rocket], obstacle: Obstacle, fps_count: float)-> None:
    for rocket_index in range(len(rockets)):
        print(f"rocket {rocket_index} current dna index: {rockets[rocket_index].current_dna_index}")

def main() -> None:
    pygame.init()
    screen: pygame.Surface = pygame.display.set_mode((X_SCREEN_SIZE, Y_SCREEN_SIZE))
    pygame.display.set_caption("Rocket Sim")
    clock: pygame.time.Clock = pygame.time.Clock()
    frames: int = 0

    rockets: List[Rocket] = create_rockets(dna_count=FRAME_MAX, number_of_rockets=ROCKETS_COUNT)
    obstacle : Obstacle = Obstacle(np.array([X_SCREEN_SIZE // 2.5, Y_SCREEN_SIZE // 2.5], dtype=np.int16))
    reward : Reward = Reward(np.array([100 , 100 ], dtype=np.int16))
    game: Game = Game(rockets, ROCKETS_COUNT)

    

    while True:
        _: pygame.event.Event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        update_rockets(rockets, obstacle, reward)
        screen.fill(SCREEN_COLOR)

        draw_rockets(rockets, screen)
        obstacle.draw(screen)
        reward.draw(screen)

        pygame.display.flip()
        # clock.tick(60)

        if frames == FRAME_MAX:
            # this is should be done in the game class
            game.fill_score_board(reward)
            board: dict[Rocket, np.float32] = game.get_board()
            print_board(rockets, board)
            new_rockets: List[Rocket] = game.create_new_generation(game.get_best_rockets())
            print(f"new generation created with {len(new_rockets)} rockets")
            print(f"Best score : {game.get_best_score()}")
            print("Now at generation : ", game.current_generation)
            rockets = new_rockets
            frames = 0




        # fps_count = clock.get_fps()

        frames += 1
        # debug_print(frames, FRAME_MAX, rockets, obstacle, fps_count)
        



if __name__ == "__main__":
    main()
