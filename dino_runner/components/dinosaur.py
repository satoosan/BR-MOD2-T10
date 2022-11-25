import pygame
from pygame.sprite import Sprite

from dino_runner.utils.constants import *

X_POS = 80
Y_POS = 310
Y_POS_DUCK = 340
Y_POS_GODZILLA = 15
JUMP_VEL = 8.5

DUCK_IMG = {DEFAULT_TYPE: DUCKING, SHIELD_TYPE: DUCKING_SHIELD, HAMMER_TYPE: DUCKING_HAMMER}
JUMP_IMG = {DEFAULT_TYPE: JUMPING, SHIELD_TYPE: JUMPING_SHIELD, HAMMER_TYPE: JUMPING_HAMMER}
RUN_IMG = {DEFAULT_TYPE: RUNNING, SHIELD_TYPE: RUNNING_SHIELD, HAMMER_TYPE: RUNNING_HAMMER}
GODZILLA_IMG = {GODZILLA_TYPE: RUNNING_GODZILLA}

class Dinosaur(Sprite):
    def __init__(self):
        self.type = DEFAULT_TYPE
        self.image = RUN_IMG[self.type][0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = X_POS
        self.dino_rect.y = Y_POS
        self.step_index = 0
        self.jump_vel = JUMP_VEL
        self.dino_run = True
        self.dino_jump = False
        self.dino_duck = False
        self.setup_state()

    def setup_state(self):
        self.has_power_up = False
        self.nuclear = False
        self.hammer = False
        self.shield = False
        self.show_text = False
        self.shield_time_up = 0

    def run(self):
        self.image = RUN_IMG[self.type][self.step_index // 5] if self.type != "godzilla" else GODZILLA_IMG[self.type][self.step_index // 5]
        self.dino_rect.x = X_POS
        self.dino_rect.y = Y_POS if self.type != "godzilla" else Y_POS_GODZILLA
        self.step_index += 1

    def duck(self):
        self.image = DUCK_IMG[self.type][self.step_index // 5] if self.type != "godzilla" else GODZILLA_IMG[self.type][self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = X_POS 
        self.dino_rect.y = Y_POS_DUCK if self.type != "godzilla" else Y_POS_GODZILLA
        self.step_index += 1
        self.dino_duck = False

    def jump(self):
        self.image = JUMP_IMG[self.type] if self.type != "godzilla" else GODZILLA_IMG[self.type][self.step_index // 5]
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        
        if self.jump_vel < -JUMP_VEL:
            self.dino_rect.y = Y_POS if self.type != "godzilla" else Y_POS_GODZILLA
            self.dino_jump = False
            self.jump_vel = JUMP_VEL

    def update(self, user_input):
        if self.dino_run:
            self.run()
        elif self.dino_jump:
            self.jump()
        elif self.dino_duck:
            self.duck()

        if user_input[pygame.K_UP]:
            if not self.dino_jump:
                self.dino_jump = True
                self.dino_duck = False
                self.dino_run = False
        elif user_input[pygame.K_DOWN]:
            if not self.dino_jump:
                self.dino_jump = False
                self.dino_duck = True
                self.dino_run = False
        elif not self.dino_jump:
            self.dino_jump = False
            self.dino_duck = False
            self.dino_run = True

        if self.step_index >= 10:
            self.step_index = 0

    def draw(self, screen):
        screen.blit(self.image, (self.dino_rect.x, self.dino_rect.y))