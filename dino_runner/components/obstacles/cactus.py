import random

from dino_runner.utils.constants import LARGE_CACTUS, SMALL_CACTUS
from dino_runner.components.obstacles.obstacle import Obstacle

CACTUS = [
   (LARGE_CACTUS, 300),
   (SMALL_CACTUS, 325),
]


class Cactus(Obstacle):
    def __init__(self):
        image, cactus_pos = CACTUS[random.randint(0, 1)]
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = cactus_pos