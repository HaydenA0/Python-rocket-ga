
import pygame
from constants import *
import numpy as np


class Reward:
    def __init__(self, position: np.ndarray) -> None:
        self.position: np.ndarray = position
        self.reward: int = 0

    def draw(self, screen: pygame.Surface) -> None:
        x: np.int16 = self.position[0]
        y: np.int16 = self.position[1]
        pygame.draw.circle(screen, REWARD_COLOR, (x, y), REWARD_RADIUS)
