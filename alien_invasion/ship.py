import pygame

class Ship():

    def __init__(self,screen):
        self.screen =screen

        self.images = pygame.image.load('images/ship.bmp')
        self.rect = self.images.get_rect()
        self.screen_rect = screen.get_rect()
