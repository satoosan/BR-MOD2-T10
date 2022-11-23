import random

from dino_runner.utils.constants import BIRD
from dino_runner.components.obstacles.obstacle import Obstacle

BIRD_HEIGHTS = [100, 250, 300]


class Birds(Obstacle):
    def __init__(self):
        self.step_index = 0
        super().__init__(BIRD, 0)
        self.rect.y = random.choice(BIRD_HEIGHTS)
        
    def draw(self, screen):
        if self.step_index >= 9:
            self.step_index = 0
        screen.blit(self.image[self.step_index // 5], self.rect)
        self.step_index += 1