import pygame
import random

from dino_runner.components.obstacles.cactus import Cactus
from dino_runner.components.obstacles.bird import Birds
from dino_runner.components.power_ups.power_up_manager import PowerUpManager


class ObstacleManager:
    def __init__(self):
        self.obstacles = []
    
    def choice_obstacle(self):
        self.type = random.randint(0, 1)
        self.obstacle = [
            Cactus(),
            Birds(),
        ]
        self.obstacles.append(self.obstacle[self.type])

    def update(self, game):
        if len(self.obstacles) == 0:
            self.choice_obstacle()
    
        for obstacle in self.obstacles:
            obstacle.update(game.game_speed, self.obstacles)
            if game.player.dino_rect.colliderect(obstacle.rect):
                if not game.player.has_power_up:                   
                    pygame.time.delay(500)
                    game.playing = False
                    game.death_count += 1
                    break
                else:                    
                    self.obstacles.remove(obstacle)

    def reset_obstacles(self):
        self.obstacles = []

    def draw(self, screen):
        for obstacle in self.obstacles:
            obstacle.draw(screen)
            