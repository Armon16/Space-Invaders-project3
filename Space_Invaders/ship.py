import pygame
from pygame.sprite import Sprite


class Ship(Sprite):

    def __init__(self, ai_settings, screen):
        super(Ship, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        # Load the ship image and get its rect
        self.image = pygame.image.load('images/ship.png')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        # Start each new ship at the bottom center of the screen.
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        # Store a decimal value for the ship's center.
        self.center = float(self.rect.centerx)
        # Movement flags
        self.moving_right = False
        self.moving_left = False
        self.health = 8
        self.status = "Healthy"
        self.timeshot = 0

    def update(self, ai_settings):
        # Update the ship's center value, not the rect.
        if self.status == "Shot" and self.health != 0:
            timepassed = ai_settings.time - self.timeshot
            if timepassed < 100:
                self.health = 7
                self.image = pygame.image.load('images/ship_d_1.png')
            elif timepassed < 200:
                self.health = 6
                self.image = pygame.image.load('images/ship_d_2.png')
            elif timepassed < 300:
                self.health = 5
                self.image = pygame.image.load('images/ship_d_3.png')
            elif timepassed < 400:
                self.health = 4
                self.image = pygame.image.load('images/ship_d_4.png')
            elif timepassed < 500:
                self.health = 3
                self.image = pygame.image.load('images/ship_d_5.png')
            elif timepassed < 600:
                self.health = 2
                self.image = pygame.image.load('images/ship_d_6.png')
            elif timepassed < 700:
                self.health = 1
                self.image = pygame.image.load('images/ship_d_7.png')
            elif timepassed < 800:
                self.health = 0
        if self.health == 0:
            self.reset()
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor
        # Update the rect object from self.center.
        self.rect.centerx = self.center

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        self.center = self.screen_rect.centerx

    def reset(self):
        self.health = 8
        self.status = "Healthy"
        self.timeshot = 0
        self.image = pygame.image.load('images/ship.png')
