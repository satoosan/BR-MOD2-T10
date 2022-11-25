import pygame

from dino_runner.utils.constants import BG, ICON, RUNNING, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS, DEATH_ICON, KEYS_ICON, AWARD_ICON
from dino_runner.components.dinosaur import Dinosaur
from dino_runner.components.obstacles.obstacle_manager import ObstacleManager

FONT_STYLE = "freesansbold.ttf"


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.playing = False
        self.running = False
        self.score_now = 0
        self.best_score = 0
        self.death_count = 0
        self.game_speed = 20
        self.x_pos_bg = 0
        self.y_pos_bg = 380
        self.player = Dinosaur()
        self.obstacle_manager = ObstacleManager()

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
        self.score_now = 0
        self.game_speed = 20
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
        self.obstacle_manager.update(self)
        self.update_score()

    def update_score(self):
        
        self.score_now += 1
        if self.score_now % 100 == 0:
            self.game_speed += 5

        if self.score_now >= self.best_score:
            self.best_score = self.score_now

    def draw(self):
        self.clock.tick(FPS) # Ele calculará quantos milissegundos se passaram desde a chamada anterior
        self.screen.fill((255, 255, 255)) # Preencher a tela
        self.draw_background()
        self.player.draw(self.screen)
        self.obstacle_manager.draw(self.screen)
        self.draw_message(f"SCORE: {self.score_now}", 21,  1000,  50, (0, 0, 0))
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
    
    def draw_message(self, msg, size, width, height, color):
        font = pygame.font.Font(FONT_STYLE, size)
        text = font.render(msg, True, color)
        text_rect = text.get_rect()
        text_rect.center = (width, height)
        self.screen.blit(text, text_rect)
    
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
        self.aux = True
        self.screen.fill((255, 255, 255))
        half_screen_height = SCREEN_HEIGHT // 2
        half_screen_width = SCREEN_WIDTH // 2

        if self.death_count == 0:
            self.draw_message("Welcome to the game!", 50, half_screen_width, half_screen_height-100, (0, 0, 0))
            self.draw_message("Press any key to start", 25, half_screen_width, half_screen_height, (0, 0, 0))
            self.draw_icon(KEYS_ICON, half_screen_width-195, half_screen_height)
            self.draw_message("Developed by Guilherme Kimura", 15, half_screen_width+380, half_screen_height+280, (128, 128, 128))
        else:
            self.draw_message("GAME OVER", 50, half_screen_width+20, half_screen_height, (255, 0, 0))
            self.draw_message("Press any key to start", 20, half_screen_width+20, half_screen_height+75, (128, 128, 128))
            self.draw_message(f"SCORE TOTAL: {self.score_now}", 18, half_screen_width+390, half_screen_height-225, (128, 128, 128))
            self.draw_message(f"BEST SCORE: {self.best_score}", 22, half_screen_width+400, half_screen_height-200, (0, 0, 0))
            self.draw_message(f"DEATH TOTAL: {self.death_count}", 18, half_screen_width+385, half_screen_height-160, (0, 0, 0))
            
            self.draw_icon(ICON, half_screen_width-20, half_screen_height-140)
            self.draw_icon(DEATH_ICON, half_screen_width+280, half_screen_height-175)
            self.draw_icon(KEYS_ICON, half_screen_width-170, half_screen_height+70)
            self.draw_icon(AWARD_ICON, half_screen_width+285, half_screen_height-210)
            
        pygame.display.update()
        self.handle_events_menu()
