import random
import pygame

from dino_runner.utils.constants import HAMMER_TYPE, SHIELD_TYPE, GODZILLA_TYPE
from dino_runner.components.power_ups.power_skill import Skill


class PowerUpManager:
    def __init__(self):
        self.power_ups = []
        self.when_appears = 0

    def choice_power_up(self):
        self.type = 0
        self.power_up = [
            Skill()
        ]
        self.power_ups.append(self.power_up[self.type])

    def generate_power_up(self, score):
        if len(self.power_ups) == 0 and self.when_appears == score:
            self.when_appears += random.randint(200, 300) 
            self.choice_power_up()

    def update(self, score, game_speed, player):
        self.generate_power_up(score)
        
        for power_up in self.power_ups:
            power_up.update(game_speed, self.power_ups)
            if player.dino_rect.colliderect(power_up.rect):
                power_up.start_time = pygame.time.get_ticks()
                if power_up.type == HAMMER_TYPE:
                    player.hammer =  True
                    player.shield = False
                    player.nuclear = False
                elif power_up.type == SHIELD_TYPE:
                    player.shield = True
                    player.hammer = False
                    player.nuclear = False
                elif power_up.type == GODZILLA_TYPE:
                    player.nuclear = True
                    player.hammer = False
                    player.shiled = False
                player.has_power_up = True
                player.type = power_up.type
                player.power_up_time = power_up.start_time + (power_up.duration * 1000)
                self.power_ups.remove(power_up)

    def draw(self, screen):
        for power_up in self.power_ups:
            power_up.draw(screen)

    def reset_power_ups(self):
        self.power_ups = []
        self.when_appears = random.randint(200, 300)