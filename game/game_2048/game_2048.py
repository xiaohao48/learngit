import sys
import pygame
import time

SCREEN_SIZE = (650, 370)
WHITE = (255, 255, 255)
COLOR_1 = (100, 100, 100)
MARGIN_SIZE = 10
BLOCK_SIZE = 80


class Number2048():
    def __init__(self, matrix_size=(4, 4)):
        self.matrix_size = matrix_size
        self.initialize()

    def initialize(self):
        self.game_matrix = [['null' for _ in range(self.matrix_size[1])] for _ in range(self.matrix_size[0])]

    def shownumber(self):
        ...


def drawGameMatrix(screen, game_matrix):
    for i in range(len(game_matrix)):
        for j in range(len(game_matrix[i])):
            number = game_matrix[i][j]
            # print(number)
            x = MARGIN_SIZE * (j + 1) + BLOCK_SIZE * j
            y = MARGIN_SIZE * (i + 1) + BLOCK_SIZE * i
            pygame.draw.rect(screen, COLOR_1, (x, y, BLOCK_SIZE, BLOCK_SIZE))


def create_rect(screen, bg_color):
    matrix = [[x - y for x in range(0, 3)] for y in range(0, 3)]
    # for m in range(0, 4):
    #     for n in range(0, 4):
    #         # matrix[n][m] = pygame.draw.rect(screen, bg_color, [(m + 1) * 5 + m * 80, (n + 1) * 5 + n * 80, 80, 80])
    #         matrix[n][m] = n * m
    print(matrix)


def run_game():
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE, 0, 32)
    pygame.display.set_caption("game_2048 v1.0.0")
    # image = pygame.image.load('OVO_icon.png')
    num_2048 = [['null' for _ in range(4)] for _ in range(4)]
    # print(num_2048)
    a=1
    print(a)
    while True:
        screen.fill((0, 0, 0))
        check_events()

        drawGameMatrix(screen, num_2048)
        # pygame.draw.rect(screen, WHITE, (5, 100, 100, 100))
        # pygame.draw.rect(screen, WHITE, (110, 100, 100, 100))
        # pygame.draw.rect(screen, WHITE, (215, 100, 100, 100))
        # pygame.draw.rect(screen, WHITE, (320, 100, 100, 100))
        # create_rect(screen, WHITE)

        font = pygame.font.SysFont("kaiti", 20)
        text = font.render("1024", True, (255, 0, 0))
        # textSurface = pygame.font.render('你好，Pygame', True, COLOR_RED)
        screen.blit(text, (250, 150))

        pygame.display.update()


def check_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()


if __name__ == '__main__':
    # game_matrix = [['null' for _ in range(4)] for _ in range(4)]
    # print(game_matrix)
    # print(len(game_matrix))
    run_game()
