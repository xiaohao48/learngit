import pygame
import time


class My_plane():
    def __init__(self, ai_settings, screen):
        self.ai_settings = ai_settings
        self.screen = screen

        self.image1 = pygame.image.load('images/me1.png')
        self.image2 = pygame.image.load('images/me2.png')
        self.destroy_image = []
        self.destroy_image.extend([
            pygame.image.load('images/me_destroy_1.png'),
            pygame.image.load('images/me_destroy_2.png')
        ])

        self.rect = self.image1.get_rect()
        self.screen_rect = self.screen.get_rect()

        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        self.switch_image = True
        self.delay = 1000
        self.speed = 1

        self.up = False
        self.down = False
        self.left = False
        self.right = False

    def blitme(self):
        # self.screen.blit(self.image1, self.rect)
        # self.mask = pygame.mask.from_surface(self.image1)

        if not (self.delay % 5):
            self.switch_image = not self.switch_image
        self.delay -= 1
        if not self.delay:
            self.delay = 1000

        if self.switch_image:
            self.screen.blit(self.image1, self.rect)
        else:
            self.screen.blit(self.image2, self.rect)

    def update(self):
        if self.up and self.rect.top > 0:
            self.rect.y -= self.speed
        if self.down and self.rect.bottom < self.screen_rect.bottom:
            self.rect.y += self.speed
        if self.left and self.rect.left > 0:
            self.rect.x -= self.speed
        if self.right and self.rect.right < self.screen_rect.right:
            self.rect.x += self.speed
