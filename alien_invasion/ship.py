import pygame
from settings import Settings
import scoreboard
from pygame.sprite import Group
from pygame.sprite import Sprite
class Ship():
    def __init__(self, ai_game):
        super().__init__()
        self.settings = Settings()
        self.ships = Group()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()
        self.images = pygame.image.load('images/ship.bmp')
        self.images = pygame.transform.scale(self.images, (200, 200))
        self.rect = self.images.get_rect()
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
        self.moving_right = False
        self.moving_left = False
    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        self.rect.x = self.x
    def blitme(self):
        self.screen.blit(self.images, self.rect)
