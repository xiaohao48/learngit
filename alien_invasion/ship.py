import pygame


class Ship():

    def __init__(self, ai_settings, screen):
        self.screen = screen
        self.ai_settings = ai_settings

        self.images = pygame.image.load('images/ship.bmp')
        self.rect = self.images.get_rect()
        self.screen_rect = screen.get_rect()

        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

        self.center = float(self.rect.centerx)
        self.y = float(self.screen_rect.bottom) - self.rect.height

    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        elif self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor
        if self.moving_up and self.rect.top > 0:
            self.y -= self.ai_settings.ship_speed_factor
        elif self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.ai_settings.ship_speed_factor

        self.rect.centerx = self.center
        self.rect.y = self.y

    def biltme(self):
        self.screen.blit(self.images, self.rect)

    def center_ship(self):
        self.center = self.screen_rect.centerx
        self.y = float(self.screen_rect.bottom) - self.rect.height
