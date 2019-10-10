import sys
import pygame
from bullet import Bullet
from alien import Alien
from random import *
import random
from bunkers import Bunker


def check_high_score(stats, sb):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
        scoresheet = open('scoresheet.txt', 'w')
        scoresheet.write(str(stats.high_score))
        scoresheet.close()


def check_events(ai_settings, screen, stats, sb, play_button, high_scores_button, ship, aliens, bullets, bunkers):
    ai_settings.log(str(bunkers))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)
            check_high_scores_button(ai_settings, screen, stats, sb, high_scores_button, ship, aliens, bullets, mouse_x, mouse_y)


def check_high_scores_button(ai_settings, screen, stats, sb, high_scores_button, ship, aliens, bullets, mouse_x, mouse_y):
    ai_settings.log(str(screen))
    ai_settings.log(str(sb))
    ai_settings.log(str(ship))
    ai_settings.log(str(aliens))
    ai_settings.log(str(bullets))
    button_clicked = high_scores_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        stats.game_active = False
        stats.high_score_active = True


def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # Reset the game settings.
        ai_settings.initialize_dynamic_settings()
        ai_settings.change_sound = pygame.mixer.Sound("sounds/boop.wav")
        ai_settings.time = 0
        # Hide the mouse cursor.
        pygame.mouse.set_visible(False)
        # Reset the game statistics.
        stats.reset_stats()
        stats.game_active = True
        stats.high_score_active = False
        # Reset the scoreboard images.
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()
        # Empty the list of aliens and bullets.
        aliens.empty()
        bullets.empty()
        # Create a new fleet and center the ship.
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()


def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, albullets, play_button, high_scores_button, game_title, scoresheet, ufo, bunkers):
    # Redraw the screen during each pass through the loop.
    if not stats.game_active:
        screen.fill(ai_settings.menu_bg_color)
        play_button.draw_button()
        screen.blit(game_title, (440, 150))
        if not stats.high_score_active:
            high_scores_button.draw_button()
            screen.blit(scoresheet, (440, 250))
        if stats.high_score_active:
            font = pygame.font.SysFont('Comic Sans MS', 50)
            hs = font.render('High Score:', False, (255, 255, 255))
            hs_score = font.render(str(stats.high_score), False, (255, 255, 255))
            screen.blit(hs, (330, 375))
            screen.blit(hs_score, (700, 375))
    else:
        screen.fill(ai_settings.game_bg_color)

        # Draw the score information.
        sb.show_score()
        ship.blitme()
        aliens.draw(screen)
        ufo.blitme()
        bunkers.draw(screen)
        ai_settings.update_skins()
        for alien in aliens:
            alien.change_alien(ai_settings.alien_skin_mode, ai_settings)
        # Redraw all bullets behind ship and aliens.
        for bullet in bullets.sprites():
            bullet.draw_bullet()
        # Redraw all alien bullets behind ship and aliens.
        for albullet in albullets.sprites():
            albullet.draw_bullet()
        ai_settings.update_collision() # Make a label for bullet-ufo collisions
        if ai_settings.collision_recent:
            font2 = pygame.font.SysFont('Comic Sans MS', 50)
            col_label_p = font2.render('+', False, (255, 255, 0))
            col_label = font2.render(str(ai_settings.collision_points), False, (255, 255, 0))
            screen.blit(col_label_p, (ai_settings.collision_location, 50))
            screen.blit(col_label, (ai_settings.collision_location+25, 50))
    # Make the most recently drawn screen visible.
    pygame.display.flip()


def check_keydown_events(event, ai_settings, screen, ship, bullets):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
        pygame.mixer.Channel(1).play(ai_settings.shoot_sound)
    elif event.key == pygame.K_ESCAPE:
        sys.exit()


def fire_bullet(ai_settings, screen, ship, bullets):
    # Create a new bullet and add it to the bullets group.
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def fire_alien_bullet(ai_settings, screen, ship, albullets, aliens):
    # Create a new bullet and add it to the albullets group.
    new_bullet = Bullet(ai_settings, screen, ship)
    lower = random.randrange(100, 600, 50)
    upper = random.randrange(600, 1200, 50)
    x = None
    y = None
    ai_settings.log(str(x))
    ai_settings.log(str(y))
    for alien in aliens:
        if lower <= alien.rect.x <= upper:
            x = alien.rect.x
            y = alien.rect.bottom
            new_bullet.make_alien_bullet(ai_settings, x, y)
            albullets.add(new_bullet)
            break


def check_keyup_events(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets, albullets, ufo, bunkers):
    # Update bullet positions.
    bullets.update()
    for albullet in albullets:
        albullet.update_alien_style()
    # Get rid of the user bullets that have disappeared.
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    # Get rid of the alien bullets that have disappeared.
    for albullet in albullets.copy():
        if albullet.rect.top >= 800:
            albullets.remove(albullet)
    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets, ufo)
    check_bullet_ufo_collisions(ai_settings, screen, stats, sb, ship, ufo, bullets, albullets, bunkers)
    check_albullet_collisions(ai_settings, screen, stats, sb, ship, ufo, albullets, aliens, bunkers)


def check_albullet_collisions(ai_settings, screen, stats, sb, ship, ufo, albullets, aliens, bunkers):
    ai_settings.log(str(ufo))
    ship_collisions = pygame.sprite.spritecollideany(ship, albullets)
    bunker_collisions = pygame.sprite.groupcollide(albullets, bunkers, True, False)
    if ship_collisions:
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, albullets, bunkers)
    if bunker_collisions:
        for member in bunker_collisions.values():
            member[0].incur_damage(bunkers)


def drop_lead(ai_settings, screen, stats, sb, ship, aliens, bullets, albullets, bunkers):
    ai_settings.log(str(stats))
    ai_settings.log(str(sb))
    ai_settings.log(str(bullets))
    ai_settings.log(str(bunkers))
    if ai_settings.time - ai_settings.last_alien_bullet_time >= ai_settings.alien_bullet_interval:
        print("Drop lead")
        ai_settings.last_alien_bullet_time = ai_settings.time
        fire_alien_bullet(ai_settings, screen, ship, albullets, aliens)
    else:
        ai_settings.last_alien_bullet_time += 1


def check_bullet_ufo_collisions(ai_settings, screen, stats, sb, ship, ufo, bullets, albullets, bunkers):
    ai_settings.log(str(screen))
    ai_settings.log(str(ship))
    ai_settings.log(str(albullets))
    # Remove any bullets and aliens that have collided.
    collision = pygame.sprite.spritecollideany(ufo, bullets)
    bunker_collisions = pygame.sprite.groupcollide(bullets, bunkers, True, False)
    if collision:
        ai_settings.collision_time = ai_settings.time
        ai_settings.collision_points = ufo.point_value
        ai_settings.collision_location = ufo.rect.x
        ai_settings.collision_recent = True
        ufo.reset()
        stats.score += ufo.point_value
        sb.prep_score()
        check_high_score(stats, sb)
    if bunker_collisions:
        for member in bunker_collisions.values():
            member[0].incur_damage(bunkers)


def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets, ufo):
    # Remove any bullets and aliens that have collided.
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, False)
    if collisions:
        for member in collisions.values():
            stats.score += member[0].point_value
            member[0].status = "Shot"
            member[0].timeshot = ai_settings.time
            sb.prep_score()
        check_high_score(stats, sb)
    if len(aliens) == 0:
        # If the entire fleet is destroyed, start a new level.
        ufo.reset()
        bullets.empty()
        ai_settings.increase_speed()
        # Increase level.
        stats.level += 1
        sb.prep_level()
        create_fleet(ai_settings, screen, ship, aliens)


def get_number_aliens_x(ai_settings, alien_width):
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height):
    available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    color = None
    pv = 0
    ai_settings.log(str(pv))
    ai_settings.log(str(color))
    if row_number < 2:
        color = 'Pink'
        pv = 10
    elif row_number < 4:
        color = 'Blue'
        pv = 20
    else:
        color = 'Green'
        pv = 40
    alien = Alien(ai_settings, screen, color, pv)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_bunkers(ai_settings, screen, bunkers):
    number_of_bunkers = 5
    for each in range(number_of_bunkers):
        xpos = each * 200 + 130
        bunker = Bunker(ai_settings, screen, xpos)
        bunkers.add(bunker)


def create_fleet(ai_settings, screen, ship, aliens):
    # Create an alien and find the number of aliens in a row.
    alien = Alien(ai_settings, screen, 'Pink', 0)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)
    # Create the fleet of aliens.
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def check_fleet_edges(ai_settings, aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets, bunkers):
    ship.status = "Shot"
    ship.timeshot = ai_settings.time
    pygame.mixer.Channel(2).play(ai_settings.explosion)
    if stats.ships_left > 0:
        # Decrement ships_left.
        stats.ships_left -= 1
        # Update scoreboard.
        sb.prep_ships()
        # Empty the list of aliens and bullets.
        aliens.empty()
        bullets.empty()
        # Create a new fleet and center the ship.
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
    else:
        ai_settings.time = 0
        stats.game_active = False
        stats.high_scores_active = False
        pygame.mouse.set_visible(True)
        create_bunkers(ai_settings, screen, bunkers)


def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets, bunkers):
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Treat this the same as if the ship got hit.
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets, bunkers)
            break


def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets, bunkers):
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    # Look for alien-ship collisions.
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets, bunkers)
    bunker_collisions = pygame.sprite.groupcollide(aliens, bunkers, True, False)
    if bunker_collisions:
        for member in bunker_collisions.values():
            member[0].incur_damage(bunkers)
    # Look for aliens hitting the bottom of the screen.
    check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets, bunkers)
    for alien in aliens:
        if alien.health == 0:
            aliens.remove(alien)


def update_ufo(ai_settings, screen, stats, sb, ship, aliens, bullets, ufo):
    ai_settings.log(str(screen))
    ai_settings.log(str(stats))
    ai_settings.log(str(sb))
    ai_settings.log(str(ship))
    ai_settings.log(str(aliens))
    ai_settings.log(str(bullets))
    ufo.check_state(ai_settings)
    ufo.update()
