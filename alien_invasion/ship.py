import pygame


class Ship():

    def __init__(self, screen):
        self.screen = screen

        self.images = pygame.image.load('images/ship.bmp')
        self.rect = self.images.get_rect()
        self.screen_rect = screen.get_rect()

        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

    def biltme(self):
        self.screen.blit(self.images, self.rect)



