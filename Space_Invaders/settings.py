from random import *
import random
import pygame


class Settings:


    def __init__(self):

        self.alien_points = None
        self.fleet_direction = 1
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.game_bg_color = (71, 0, 145)
        self.menu_bg_color = (0, 0, 0)
        # Ship settings
        self.ship_speed_factor = 1.5
        self.ship_limit = 3
        # Bullet settings
        self.bullet_speed_factor = 3
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 0, 255, 0
        self.alien_bullet_color = 255, 255, 0
        self.bullets_allowed = 10
        # Alien settings
        self.alien_speed_factor = None
        self.fleet_drop_speed = 10
        # How quickly the game speeds up
        self.speedup_scale = 1.08
        # How quickly the alien point value increase
        self.score_scale = 1.5
        self.time = 0
        self.time_of_last_ufo = None
        self.collision_time = 0
        self.collision_points = None
        self.collision_location = None
        self.collision_recent = False
        self.alien_skin_mode = 1
        self.alien_skin_last_change = 0
        self.alien_bullet_interval = random.randrange(2000, 6000, 500)
        self.last_alien_bullet_time = 0
        self.change_sound = pygame.mixer.Sound("sounds/boop.wav")
        self.shoot_sound = pygame.mixer.Sound("sounds/shoot.wav")
        self.explosion = pygame.mixer.Sound("sounds/explosion.wav")
        self.invaderkilled = pygame.mixer.Sound("sounds/invaderkilled.wav")
        self.ufo_speed_factor = random.uniform(0.5, 0.8)
        self.initialize_dynamic_settings()

    def update_skins(self):
        if (self.time - self.alien_skin_last_change) > 400:
            if self.alien_skin_mode == 1:
                self.alien_skin_mode = 2
            else:
                self.alien_skin_mode = 1
            self.alien_skin_last_change = self.time

    @staticmethod
    def log(objectpassed):
        print("Log request" + objectpassed)

    def update_collision(self):
        if (self.time - self.collision_time) > 2500:
            self.collision_time = 0
            self.collision_points = None
            self.collision_location = None
            self.collision_recent = False

    def initialize_dynamic_settings(self):
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = .7
        self.ufo_speed_factor = random.uniform(0.5, 0.8)
        # fleet direction of 1  represents right; -1 represents left.
        self.fleet_direction = 1
        pygame.mixer.set_num_channels(10)
        self.change_sound = pygame.mixer.Sound("sounds/boop.wav")
        self.shoot_sound = pygame.mixer.Sound("sounds/shoot.wav")
        self.explosion = pygame.mixer.Sound("sounds/explosion.wav")
        self.invaderkilled = pygame.mixer.Sound("sounds/invaderkilled.wav")
        # Scoring
        self.alien_points = 50

    def increase_speed(self):
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.ufo_speed_factor *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
