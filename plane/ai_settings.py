import pygame


class Ai_settings():

    def __init__(self):
        self.attribute_screen()

    def attribute_screen(self):
        self.screen = (480, 700)
        self.bg_cl = (255, 0, 0)
        self.title = '雷电'
        self.background =pygame.image.load('images/background.png')

