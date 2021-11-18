import sys
import pygame
from settings import Settings
from bullet import Bullet
from alien import Alien
from time import sleep


def check_events(ship, ai_settings, bullets, screen, play_button, stats, aliens, sb):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(play_button, mouse_x, mouse_y, stats, aliens, bullets, ship, ai_settings, screen, sb)
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ship, bullets, ai_settings, screen)

        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)


def check_keydown_events(event, ship, bullets, ai_settings, screen):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    if event.key == pygame.K_LEFT:
        ship.moving_left = True
    if event.key == pygame.K_UP:
        ship.moving_up = True
    if event.key == pygame.K_DOWN:
        ship.moving_down = True

    if event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)

    if event.key == pygame.K_q:
        sys.exit()


def check_keyup_events(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    if event.key == pygame.K_LEFT:
        ship.moving_left = False
    if event.key == pygame.K_UP:
        ship.moving_up = False
    if event.key == pygame.K_DOWN:
        ship.moving_down = False


def check_play_button(play_button, mouse_x, mouse_y, stats, aliens, bullets, ship, ai_settings, screen, sb):
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        stats.reset_stats()
        stats.game_active = True
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        ai_settings.initialize_dynamic_settings()

        rest_aliens(aliens, bullets, ship, ai_settings, screen)
        pygame.mouse.set_visible(False)


def update_screen(ai_settings, screen, ship, bullets, aliens, stats, play_button, sb):
    screen.fill(ai_settings.bg_color)
    sb.show_score()
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.biltme()
    aliens.draw(screen)

    if not stats.game_active:
        play_button.draw_button()
    pygame.display.flip()


def update_bullets(bullets, aliens, ai_settings, screen, ship, stats, sb):
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(ai_settings, screen, aliens, ship, bullets, stats, sb)


def check_bullet_alien_collisions(ai_settings, screen, aliens, ship, bullets, stats, sb):
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()

    if len(aliens) == 0:
        bullets.empty()
        ai_settings.increate_speed()
        stats.level += 1
        sb.prep_level()
        create_fleet(ai_settings, screen, aliens, ship)


def fire_bullet(ai_settings, screen, ship, bullets):
    if len(bullets) < ai_settings.bullet_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def get_number_aliens_x(ai_settings, alien_width):
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height):
    available_space_y = ai_settings.screen_height - 3 * alien_height - ship_height
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    alien.add(aliens)


def create_fleet(ai_settings, screen, aliens, ship):
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def update_aliens(aliens, ai_settings, ship, stats, bullets, screen, sb):
    check_alien_bottom(screen, aliens, ai_settings, stats, bullets, ship, sb)
    check_fleet_edges(aliens, ai_settings)
    aliens.update()
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, aliens, bullets, screen, ship, sb)
    for alien in aliens.copy():
        if alien.rect.top >= ai_settings.screen_height:
            aliens.remove(alien)


# 舰队到达左右边缘
def check_fleet_edges(aliens, ai_settings):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


# 改变舰队的方向
def change_fleet_direction(ai_settings, aliens):
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def ship_hit(ai_settings, stats, aliens, bullets, screen, ship, sb):
    if stats.ships_left > 0:
        stats.ships_left -= 1
        rest_aliens(aliens, bullets, ship, ai_settings, screen)
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)
        check_high_score(stats, sb)


def rest_aliens(aliens, bullets, ship, ai_settings, screen):
    aliens.empty()
    bullets.empty()
    create_fleet(ai_settings, screen, aliens, ship)
    ship.center_ship()


def check_alien_bottom(screen, aliens, ai_settings, stats, bullets, ship, sb):
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings, stats, aliens, bullets, screen, ship, sb)
            break


def check_high_score(stats, sb):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
