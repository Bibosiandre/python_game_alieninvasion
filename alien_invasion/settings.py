import pygame
class Settings():
    def __init__(self):
        self.ship_speed = 5.5
        self.ship_limit = 3
        self.alien_speed = 1.0
        self.fleet_drop_speed = 35
        self.fleet_direction = 5
        self.screen_width = 1000
        self.screen_height = 800
        self.images = pygame.image.load("images/bg.bmp")
        self.images = pygame.transform.scale(self.images, (1960, 1100))
        self.bg_color = (230, 230 , 230)
        self.bullet_speed = 2.25
        self.bullet_width = 8
        self.bullet_height = 15
        self.bullet_color = (230, 230, 230)
        self.speedup_scale = 1.1
        self.score_scale = 1.5
        self.initialize_dynamic_settings()
    def initialize_dynamic_settings(self):
        self.ship_speed_factor = 1.5
        self.alien_speed_factor = 2.0
        self.bullet_speed_factor = 3.0
        self.fleet_direction = 5
        self.alien_points = 5
    def increase_speed(self):
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale

