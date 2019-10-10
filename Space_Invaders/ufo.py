import pygame
from pygame.sprite import Sprite
from random import *
import random


class Ufo(Sprite):


    def __init__(self, ai_settings, screen):
        super(Ufo, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        self.image = pygame.image.load('images/red1.png')
        self.rect = self.image.get_rect()
        # Start each new ufo near the top left of the screen.
        self.rect.x = -50
        self.rect.y = self.rect.height
        # Store the alien's exact position.
        self.x = float(self.rect.x)
        self.point_value = None
        self.respawn_rate = None
        self.reset()
        self.active = False

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def check_edges(self):
        screen_rect = self.screen.get_rect()
        if self.rect.left >= screen_rect.right:
            self.reset()
            return True

    def reset(self):
        print("Ufo is out of frame now")
        self.active = False
        self.x = -50
        self.rect.x = self.x
        self.respawn_rate = randint(10000, 16000)
        self.point_value = random.randrange(100, 500, 100)

    def update(self):
        self.check_edges()
        if self.active:
            self.x += self.ai_settings.ufo_speed_factor
            self.rect.x = self.x

    def check_state(self, ai_settings):
        if ai_settings.alien_skin_mode == 1:
            self.image = pygame.image.load('images/red1.png')
        else:
            self.image = pygame.image.load('images/red2.png')
        if ai_settings.time_of_last_ufo is None:
            if ai_settings.time > self.respawn_rate:
                self.active = True
                ai_settings.time_of_last_ufo = ai_settings.time
                print("Time for first ufo")
        elif (ai_settings.time - ai_settings.time_of_last_ufo) > self.respawn_rate:
            self.active = True
            ai_settings.time_of_last_ufo = ai_settings.time
            print("Time for new ufo")
