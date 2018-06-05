import sys

import pygame
from bullet import Bullet
from alien import Alien
from time import sleep

def check_keydown_events(event, ai_settings, screen, ship, bullets):
    """respond to key"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()


def fire_bullet(ai_settings, screen, ship, bullets):
    """fire a bullet if the limits are not reached"""
    # create new bullet and add it in group bullets
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def check_keyup_events(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
    

def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens,
                 bullets):
    """respond to keys and mouse events"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)            
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship,
                              aliens, bullets, mouse_x, mouse_y)


def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens,
                      bullets, mouse_x, mouse_y):
    """click play button to start game"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # reset game settings
        ai_settings.initialize_dynamic_settings()
        
        # make mouse invisible
        pygame.mouse.set_visible(False)
        
        #  reset game stats
        stats.reset_stats()
        stats.game_active = True

        # reset scoreboard
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        # empty aliens and bullets group
        aliens.empty()
        bullets.empty()

        # create a new fleet of aliens, ship is in the middle of the screen
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

            

def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets,
                  play_button):
    """update the image on screen and flip to new screen"""
    # redraw the screen each while loop
    screen.fill(ai_settings.bg_color)
    # draw all the bullets after ship and aliens
    for bullet in bullets.sprites():
        bullet.draw_bullet()
        
    ship.blitme()
    aliens.draw(screen)
    sb.show_score()

    # if the game is active, draw play button
    if not stats.game_active:
        play_button.draw_button()
        
    # show the screen
    pygame.display.flip()


def check_high_score(stats, sb):
    """"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()


def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """update the position of the bullets and remove the disappeared bullets"""
    # update position of bullets
    bullets.update()

    # remove the disppearing bullets
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collisions(ai_settings, screen, stats, sb,
                                  ship, aliens, bullets)


def check_bullet_alien_collisions(ai_settings, screen, stats, sb,
                                  ship, aliens, bullets):
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats,sb)
        
    if len(aliens) == 0:
        # if the whole fleet of aliens are destroyed, then upgrade a level
        bullets.empty()
        ai_settings.increase_speed()
        create_fleet(ai_settings, screen, ship, aliens)

        # upgrade a level
        stats.level += 1
        sb.prep_level


def get_number_aliens_x(ai_settings, alien_width):
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height):
    """calculate how many lines of aliens could fit into the screen"""
    available_space_y = (ai_settings.screen_height - (3* alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """create an alien and put it on the current line"""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)
    

def create_fleet(ai_settings, screen, ship, aliens):
    """create a fleet of aliens"""
    # create an alien fleet and calculate how many aliens fit into each line
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)
    
    # create the fleet of aliens
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def check_fleet_edges(ai_settings, aliens):
    """do something when aliens reach the edges"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    """move the fleet down and change direction"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1
    

def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """responds to ship hit by aliens"""
    if stats.ships_left > 0:
        # ship_letf - 1
        stats.ships_left -= 1
        # update scoreboard
        sb.prep_ships()

        # empty alien list and bullets list
        aliens.empty()
        bullets.empty()

        # create a new fleet of aliens; ship is placed in the middle of the screen bottom
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        # pause
        sleep(0.5)
        
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """check if any alien reaches the bottom"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # same as alien hits ship
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
            break


def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """check if the alien reaches the edge and update the fleet position"""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    #check collisions between aliens and ship
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)

    check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets)










 
