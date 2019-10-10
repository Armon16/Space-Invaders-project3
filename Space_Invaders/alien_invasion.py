import pygame
from pygame.sprite import Group
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
import game_functions as gf
from ufo import Ufo


def run_game():
    # Initialize pygame, settings, and screen object.
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Space Invaders")
    # Makes the Play button.
    play_button = Button(ai_settings, screen, "Play Game")
    # Makes the game title.
    titlefont = pygame.font.SysFont('Comic Sans MS', 70)
    game_title = titlefont.render('Alien Invasion', False, (255, 255, 255))
    # Makes the infosheet
    scoresheet = pygame.image.load('images/infosheet.png')
    # Make the High Scores button.
    high_scores_button = Button(ai_settings, screen, "High Scores")
    high_scores_button.make_high_scores_button("High Scores")
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)
    # Make a ship
    ship = Ship(ai_settings, screen)
    bullets = Group()
    aliens = Group()
    albullets = Group() 
    bunkers = Group()
    gf.create_bunkers(ai_settings, screen, bunkers)
    ufo = Ufo(ai_settings, screen)
    ufo.blitme()
    # Create the fleet of aliens.
    gf.create_fleet(ai_settings, screen, ship, aliens)
    # Load sounds
    ai_settings.change_sound = pygame.mixer.Sound("sounds/boop.wav")

    # Start the main loop for the game.
    while True:
        # Check for key presses or mouse clicks
        gf.check_events(ai_settings, screen, stats, sb, play_button, high_scores_button, ship, aliens, bullets, bunkers)
        if stats.game_active:
            ticks = pygame.time.get_ticks()
            ai_settings.time = ticks
            if ai_settings.time >= 13000:
                ai_settings.change_sound = pygame.mixer.Sound("sounds/boop2.wav")
            if ai_settings.time >= 20000:
                ai_settings.change_sound = pygame.mixer.Sound("sounds/boop3.wav")
            # Move the ship left/right
            ship.update(ai_settings)
            # Move bullets and check for alien collisions
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets, albullets, ufo, bunkers)
            # Move the aliens and check for edge collisions
            gf.update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets, bunkers)
            # Move the UFO across
            gf.update_ufo(ai_settings, screen, stats, sb, ship, aliens, bullets, ufo)
            gf.drop_lead(ai_settings, screen, stats, sb, ship, aliens, bullets, albullets, bunkers)
        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, albullets, play_button, high_scores_button, game_title, scoresheet, ufo, bunkers)


run_game()
