import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):


    def __init__(self, ai_settings, screen, ship):
        super(Bullet, self).__init__()
        self.screen = screen
        # Create a bullet 
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width, ai_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top
        self.y = float(self.rect.y)
        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor

    def make_alien_bullet(self, ai_settings, x, y):
        self.rect.centerx = x
        self.rect.top = y
        self.y = float(self.rect.y)
        self.color = ai_settings.alien_bullet_color

    def update(self):
        self.y -= self.speed_factor
        self.rect.y = self.y

    def update_alien_style(self):
        self.y += self.speed_factor
        self.rect.y = self.y

    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
