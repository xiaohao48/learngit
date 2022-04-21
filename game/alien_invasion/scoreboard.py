import pygame.font
from pygame.sprite import Group
from ship import Ship


class Scoreboard():
    '''分数榜'''

    def __init__(self, ai_settings, screen, stats):
        self.ai_settings = ai_settings
        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        self.stats = stats

        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont("simHei", 36)
        self.prep_score()
        self.prep_high_score()
        self.prep_ships()

    def prep_score(self):
        rounded_score = int(round(self.stats.score, -1))
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render("总分：" + score_str, True, self.text_color, self.ai_settings.bg_color)
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20
        self.prep_level()

    def prep_high_score(self):
        high_score = int(round(self.stats.high_score, -1))
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render("最高分：" + high_score_str, True, self.text_color,
                                                 self.ai_settings.bg_color)

        self.high_score_image_rect = self.high_score_image.get_rect()
        self.high_score_image_rect.centerx = self.screen_rect.centerx
        self.high_score_image_rect.top = self.score_rect.top

    def show_score(self):
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_image_rect)
        self.screen.blit(self.level_image, self.level_image_rect)
        self.ships.draw(self.screen)

    def prep_level(self):
        self.level_image = self.font.render("LEVEL " + str(self.stats.level), True, self.text_color,
                                            self.ai_settings.bg_color)
        self.level_image_rect = self.level_image.get_rect()
        self.level_image_rect.right = self.score_rect.right
        self.level_image_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_settings, self.screen)
            ship.rect = ship.image.get_rect()
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)
