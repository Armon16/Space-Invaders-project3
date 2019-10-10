import pygame
from pygame.sprite import Sprite


class Bunker(Sprite):


    def __init__(self, ai_settings, screen, xpos):
        super(Bunker, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        self.health = 7
        self.image = pygame.image.load('images/bunker/b_d_7.png')
        self.rect = self.image.get_rect()
        # Start each new alien near the top left of the screen.
        self.rect.x = xpos
        self.rect.y = 700

    def incur_damage(self, bunkers):
        self.health -= 1
        if self.health > 0:
            xpos = self.rect.x
            img_string = 'images/bunker/b_d_' + str(self.health) + '.png'
            self.image = pygame.image.load(img_string)
            self.rect = self.image.get_rect()
            self.rect.x = xpos
            self.rect.y = 700
        else:
            for bunker in bunkers:
                if bunker.health == 0:
                    bunkers.remove(bunker)
