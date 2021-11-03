import sys
import pygame
from settings import Settings
from bullet import Bullet


def check_events(ship,ai_settings,bullets,screen):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ship,ai_settings,screen,bullets)

        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)


def check_keydown_events(event, ship,bullets,ai_settings,screen):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    if event.key == pygame.K_LEFT:
        ship.moving_left = True
    if event.key == pygame.K_SPACE:
        new_bullet = Bullet(ai_settings,screen,ship,bullets)
        bullets.add(new_bullet)


def check_keyup_events(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    if event.key == pygame.K_LEFT:
        ship.moving_left = False




def update_screen(ai_settings, screen, ship,bullets):
    screen.fill(ai_settings.bg_color)
    ship.biltme()

    for bullet in bullets.sprites():
        bullet.draw_bullet()
    pygame.display.flip()
