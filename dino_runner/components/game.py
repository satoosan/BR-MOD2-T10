import pygame
import random

from dino_runner.utils.constants import *
from dino_runner.components.dinosaur import Dinosaur
from dino_runner.components.obstacles.obstacle_manager import ObstacleManager
from dino_runner.components.obstacles.cloud import Cloud
from dino_runner.components.power_ups.power_up_manager import PowerUpManager


FONT_STYLE = "freesansbold.ttf"


# CONSTANTS
SCORE = 0

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.playing = False
        self.running = False

        self.score_now = SCORE
        self.best_score = SCORE
        self.death_count = 0
        self.game_speed = GAME_SPEED

        self.x_pos_bg = 0
        self.y_pos_bg = 380

        self.player = Dinosaur()
        self.cloud = Cloud()
        self.obstacle_manager = ObstacleManager()
        self.power_up_manager = PowerUpManager()

    def execute(self):
        self.running = True
        while self.running:
            if not self.playing:
                self.show_menu()

        pygame.display.quit()
        pygame.quit()

    def run(self):
        # Game loop: events - update - draw
        self.playing = True
        self.obstacle_manager.reset_obstacles()
        self.score_now = SCORE
        self.game_speed = GAME_SPEED
        self.power_up_manager.reset_power_ups()
        while self.playing:
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running= False
                
    def update(self):
        user_input = pygame.key.get_pressed() # Pega a tecla pressionada
        self.player.update(user_input)
        self.cloud.update()
        self.obstacle_manager.update(self)
        
        self.update_score()
        self.power_up_manager.update(self.score_now, self.game_speed, self.player)

    def update_score(self):
        
        self.score_now += 1
        if self.score_now % 100 == 0:
            self.game_speed += 2

        if self.score_now >= self.best_score:
            self.best_score = self.score_now - 1

    def draw(self):
        self.clock.tick(FPS) # Ele calculará quantos milissegundos se passaram desde a chamada anterior
        self.screen.fill((255, 255, 255)) # Preencher a tela
        self.draw_background()
        self.cloud.draw(self.screen)
        self.player.draw(self.screen)
        self.obstacle_manager.draw(self.screen)
        self.draw_message(f"SCORE: {self.score_now}", 21,  1000,  50, (0, 0, 0))
        self.draw_power_up_time()
        self.power_up_manager.draw(self.screen)
        pygame.display.update()
        pygame.display.flip() # Atualize a superfície de exibição completa para a tela

    def draw_background(self):
        image_width = BG.get_width()
        self.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg)) # Enfileira as imagens
        self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
        if self.x_pos_bg <= -image_width:
            self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
            self.x_pos_bg = 0
        self.x_pos_bg -= self.game_speed
    
    def draw_power_up_time(self):
        if self.player.has_power_up:
            time_to_show = round((self.player.power_up_time - pygame.time.get_ticks()) / 1000, 2)
            if time_to_show >= 0:
                self.draw_message(
                    f"{self.player.type.capitalize()} enabled for {time_to_show} seconds",
                    30,
                    SCREEN_WIDTH // 2,
                    (SCREEN_HEIGHT // 2) + 150,
                    (0, 0, 0))
            else:
                self.player.has_power_up = False
                self.player.type = DEFAULT_TYPE
    
    def draw_message(self, msg, size, width, height, color):
        font = pygame.font.Font(FONT_STYLE, size)
        text = font.render(msg, True, color)
        text_rect = text.get_rect()
        text_rect.center = (width, height)
        self.screen.blit(text, text_rect)

    def draw_home_screen(self):
        self.draw_message("Welcome to the game!", 50, self.half_screen_width, self.half_screen_height-100, (0, 0, 0))
        self.draw_message("Press any key to start", 25, self.half_screen_width, self.half_screen_height-30, (0, 0, 0))
        self.draw_message("Developed by Guilherme Kimura", 15, self.half_screen_width+380, self.half_screen_height+280, (128, 128, 128))
        self.draw_message("How to play", 18, self.half_screen_width+395, self.half_screen_height+120,(0, 0, 0))
        self.draw_icon(TUTORIAL, self.half_screen_width-150, self.half_screen_height)
        self.draw_icon(KEYS_ICON, self.half_screen_width+345, self.half_screen_height+150)
        self.draw_icon(FEET, self.half_screen_width-60, self.half_screen_height-240)
    
    def draw_end_screen(self):
        self.draw_message("Press any key to start", 20, self.half_screen_width+20, self.half_screen_height+60, (128, 128, 128))
        self.draw_message(f"SCORE TOTAL: {self.score_now-1}", 18, self.half_screen_width+390, self.half_screen_height-225, (128, 128, 128))
        self.draw_message(f"BEST SCORE: {self.best_score}", 22, self.half_screen_width+400, self.half_screen_height-200, (0, 0, 0))
        self.draw_message(f"DEATH TOTAL: {self.death_count}", 18, self.half_screen_width+385, self.half_screen_height-160, (0, 0, 0))
        self.draw_message("How to play", 18, self.half_screen_width+395, self.half_screen_height+120,(0, 0, 0))
        
        self.draw_icon(GAME_OVER, self.half_screen_width-160, self.half_screen_height)
        self.draw_icon(RESET, self.half_screen_width-20, self.half_screen_height+80)
        self.draw_icon(ICON, self.half_screen_width-20, self.half_screen_height-140)
        self.draw_icon(DEATH_ICON, self.half_screen_width+280, self.half_screen_height-175)
        self.draw_icon(KEYS_ICON, self.half_screen_width+345, self.half_screen_height+150)
        self.draw_icon(AWARD_ICON, self.half_screen_width+280, self.half_screen_height-215)
    
    def draw_icon(self, icon_image, icon_width, icon_height):
        self.screen.blit(icon_image, (icon_width, icon_height))

    def handle_events_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            elif event.type == pygame.KEYDOWN: # não confuda: K_DOWN
                self.run()

    def show_menu(self):
        self.screen.fill((255, 255, 255))
        self.half_screen_height = SCREEN_HEIGHT // 2
        self.half_screen_width = SCREEN_WIDTH // 2
        
        if self.death_count == 0:
            self.draw_home_screen()
        else:
            self.draw_end_screen()
            
        pygame.display.update()
        self.handle_events_menu()
