import random

from dino_runner.components.obstacles.obstacle import Obstacle

BIRD_HEIGHTS = [100, 250, 300]


class Birds(Obstacle):
    def __init__(self, image):
        self.step_index = 0
        self.type = 0 if self.step_index > 5 else 1
        super().__init__(image, self.type)
        self.rect.y = random.choice(BIRD_HEIGHTS)
        
    def draw(self, screen):
        if self.step_index >= 9:
            self.step_index = 0
        screen.blit(self.image[self.step_index // 5], self.rect)
        self.step_index += 1