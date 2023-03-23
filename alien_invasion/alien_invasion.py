import sys
from time import sleep
import pygame
from pygame import mixer
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien
class AlienInvasion:
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("AlienInvasion")
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()
        self.play_button = Button(self, "Play")
    def _check_play_button(self, mouse_pos):
        if self.play_button.rect.collidepoint(mouse_pos):
            button_clicked = self.play_button.rect.collidepoint(mouse_pos)
            self.settings.initialize_dynamic_settings()
            if button_clicked and not self.stats.game_active:
                pygame.mouse.set_visible(False)
                self.stats.reset_stats()
                self.stats.game_active = True
                self.sb.prep_score()
                self.sb.prep_level()
    def run_game(self):
        self.sound = pygame.mixer_music.load('sounds/sound for bg.ogg')
        self.sound = pygame.mixer_music.play(0, 0.0, 2000)
        while True:
            self._check_events()
            self._update_bullets()
            if self.stats.game_active == True:
                self.ship.update()
                self._update_aliens()
    def _update_bullets(self):
            if not self.aliens:
                self.bullets.empty()
                self._create_fleet()
            self.bullets.update()
            for bullet in self.bullets.copy():
                if bullet.rect.bottom <=0:
                    self.bullets.remove(bullet)
            self._check_bullet_alien_collisions()
    def _check_bullet_alien_collisions(self):
            print(len(self.bullets))
            self._update_screen()
            collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
            self.settings.increase_speed()
            if collisions:
                self.stats.score += self.settings.alien_points
                self.sb.prep_score()
                self.sb.check_high_score()
            for hit in collisions:
                    self.sound = pygame.mixer_music.load('sounds/dead.ogg')
                    self.sound = pygame.mixer_music.play()
    def _check_events(self):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    self._check_play_button(mouse_pos)
                elif event.type == pygame.KEYDOWN:
                    self._check_keydown_events(event)
                elif event.type == pygame.KEYUP:
                    self._check_keyup_events(event)
    def _check_keydown_events(self, event):
                    if event.key == pygame.K_RIGHT:
                        self.ship.moving_right = True
                    if event.key == pygame.K_LEFT:
                        self.ship.moving_left = True
                    elif event.type == pygame.KEYUP:
                        self._check_keyup_event(event)
                    elif event.key == pygame.K_q:
                        sys.exit()
                    elif event.key == pygame.K_RSHIFT:
                        self._fire_bullet()
    def _check_keyup_events(self, event):
                    if event.key == pygame.K_RIGHT:
                        self.ship.moving_right = False
                    if event.key == pygame.K_LEFT:
                        self.ship.moving_left = False
    def _fire_bullet(self):
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
    def _create_fleet(self):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height -
                             (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)
        self.stats.level += 1
        self.sb.prep_level()
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)
    def _create_alien(self, alien_number, row_number):
            alien = Alien(self)
            alien_width, alien_height = alien.rect.size
            alien.x = alien_width + 2 * alien_width * alien_number
            alien.rect.x = alien.x
            alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
            self.aliens.add(alien)
    def _update_aliens(self):
        self._check_fleet_edges()
        self.aliens.update()
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
            print("Paw!!!")
        self._check_aliens_bottom()
    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
    def _change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1
    def _ship_hit(self):
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self.center_ship()
            self.aliens.empty()
            self.bullets.empty()
            self._create_fleet()
            self.game_active = False
            self.sound = pygame.mixer_music.load('sounds/dead_ship.ogg')
            self.sound = pygame.mixer_music.play()
            self.sound = pygame.mixer_music.set_volume(0.2)
            sleep(0.7)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)
    def center_ship(self):
        self.ship.x = float(1920 / 2)
    def _check_aliens_bottom(self):
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break
    def _update_screen(self):
                self.screen.blit( self.settings.images, (-10,-10))
                self.ship.blitme()
                self.aliens.draw(self.screen)
                if not self.stats.game_active:
                    self.play_button.draw_button()
                for bullet in self.bullets.sprites():
                    bullet.draw_bullet()
                self.aliens.draw(self.screen)
                self.sb.show_score()
                pygame.display.flip()
if __name__ == '__main__':
    ai= AlienInvasion()
    ai.run_game()
