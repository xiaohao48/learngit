import sys
import pygame
from settings import Settings
from ship import Ship
import game_functions as gf
from bullet import Bullet
from pygame.sprite import Group
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard


def run_game():
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")
    play_button = Button(ai_settings, screen, "Play")
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)

    ship = Ship(ai_settings, screen)
    bullets = Group()
    aliens = Group()
    # 游戏主循环
    while True:
        gf.check_events(ship, ai_settings, bullets, screen, play_button, stats, aliens, sb)
        if stats.game_active:
            ship.update()
            gf.update_bullets(bullets, aliens, ai_settings, screen, ship, stats, sb)
            gf.update_aliens(aliens, ai_settings, ship, stats, bullets, screen, sb)
        gf.update_screen(ai_settings, screen, ship, bullets, aliens, stats, play_button, sb)


if __name__ == '__main__':
    run_game()
