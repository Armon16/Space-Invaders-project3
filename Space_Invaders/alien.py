import pygame
from pygame.sprite import Sprite


class Alien(Sprite):


    def __init__(self, ai_settings, screen, color, pv):
        super(Alien, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        self.health = 4
        self.status = "Healthy"
        self.timeshot = 0
        if color == 'Pink':
            self.image = pygame.image.load('images/pinky1.png')
            self.a_type = 'Pink'
        elif color == 'Blue':
            self.image = pygame.image.load('images/blugu1.png')
            self.a_type = 'Blue'
        else:
            self.image = pygame.image.load('images/green1.png')
            self.a_type = 'Green'
        self.rect = self.image.get_rect()
        # Start each new alien near the top left of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        self.point_value = pv
        # Store the alien's exact position.
        self.x = float(self.rect.x)

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def change_alien(self, mode, ai_settings):
        pygame.mixer.Sound.play(ai_settings.change_sound)
        if mode == 1 and self.status == "Healthy":
            if self.a_type == 'Pink':
                self.image = pygame.image.load('images/pinky1.png')
            elif self.a_type == 'Blue':
                self.image = pygame.image.load('images/blugu1.png')
            else:
                self.image = pygame.image.load('images/green1.png')
        elif mode == 2 and self.status == "Healthy":
            if self.a_type == 'Pink':
                self.image = pygame.image.load('images/pinky2.png')
            elif self.a_type == 'Blue':
                self.image = pygame.image.load('images/blugu2.png')
            else:
                self.image = pygame.image.load('images/green2.png')
        elif self.status == "Shot" and self.health != 0:
            timepassed = ai_settings.time - self.timeshot
            if timepassed < 100:
                self.health = 3
                if self.a_type == 'Pink':
                    self.image = pygame.image.load('images/pink_d_3.png')
                elif self.a_type == 'Blue':
                    self.image = pygame.image.load('images/blue_d_3.png')
                else:
                    self.image = pygame.image.load('images/green_d_3.png')
            elif timepassed < 200:
                self.health = 2
                if self.a_type == 'Pink':
                    self.image = pygame.image.load('images/pink_d_2.png')
                elif self.a_type == 'Blue':
                    self.image = pygame.image.load('images/blue_d_2.png')
                else:
                    self.image = pygame.image.load('images/green_d_2.png')
            elif timepassed < 400:
                self.health = 1
                if self.a_type == 'Pink':
                    self.image = pygame.image.load('images/pink_d_1.png')
                elif self.a_type == 'Blue':
                    self.image = pygame.image.load('images/blue_d_1.png')
                else:
                    self.image = pygame.image.load('images/green_d_1.png')
            elif timepassed < 500:
                pygame.mixer.Channel(3).play(ai_settings.invaderkilled)
                self.health = 0

    def check_edges(self):
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def update(self):
        self.x += (self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction)
        self.rect.x = self.x
