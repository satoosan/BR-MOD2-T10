import pygame
import random

from dino_runner.utils.constants import SMALL_CACTUS, LARGE_CACTUS, BIRD
from dino_runner.components.obstacles.cactus import Cactus
from dino_runner.components.obstacles.cactus_large import CactusLarge
from dino_runner.components.obstacles.bird import Birds



class ObstacleManager:
    def __init__(self):
        self.obstacles = []
    
    def choice_obstacle(self):
        self.type = random.randint(0, 2)
        self.obstacle = [
            Cactus(SMALL_CACTUS),
            CactusLarge(LARGE_CACTUS),
            Birds(BIRD),
        ]
        self.obstacles.append(self.obstacle[self.type])

    def update(self, game):
        if len(self.obstacles) == 0:
            self.choice_obstacle()
    
        for obstacle in self.obstacles:
            obstacle.update(game.game_speed, self.obstacles)
            if game.player.dino_rect.colliderect(obstacle.rect):
                pygame.time.delay(500)
                game.playing = False
                break
    
    def draw(self, screen):
        for obstacle in self.obstacles:
            obstacle.draw(screen)
            