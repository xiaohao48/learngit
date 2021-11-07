import sys
import pygame
from settings import Settings
from ship import Ship
import game_functions as gf
from bullet import Bullet
from pygame.sprite import Group
from alien import Alien


def run_game():
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    ship = Ship(ai_settings, screen)

    bullets = Group()
    aliens = Group()
    gf.create_fleet(ai_settings, screen, aliens, ship)

    while True:
        gf.check_events(ship, ai_settings, bullets, screen)
        ship.update()
        bullets.update()

        gf.update_bullets(bullets, aliens)

        gf.update_screen(ai_settings, screen, ship, bullets, aliens)


run_game()
