

import pygame
from constants import *
import numpy as np


class Obstacle:
    def __init__(self, position: np.ndarray) -> None:
        self.position: np.ndarray = position

    def draw(self, screen: pygame.Surface) -> None:
        x: np.int16 = self.position[0]
        y: np.int16 = self.position[1]
        pygame.draw.circle(screen, OBSTACLE_COLOR, (x, y), OBSTACLE_RADIUS)

