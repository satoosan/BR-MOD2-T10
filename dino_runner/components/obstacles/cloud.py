import random

from dino_runner.utils.constants import CLOUD, SCREEN_WIDTH, GAME_SPEED
from dino_runner.components.obstacles.obstacle import Obstacle

class Cloud(Obstacle):
    def __init__(self):
        self.x = SCREEN_WIDTH + random.randint(800, 1000)
        self.y = random.randint(100, 300)
        self.image = CLOUD
        self.width = self.image.get_width()

    def update(self):
        self.x -= GAME_SPEED
        if self.x < -self.width:
            self.x = SCREEN_WIDTH + random.randint(800, 1000)
            self.y = random.randint(100, 300)

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.x, self.y))