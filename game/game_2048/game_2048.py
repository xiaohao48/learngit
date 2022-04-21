import pygame


def run_game():
    pygame.init()
    screen = pygame.display.set_mode((600, 500), 0, 32)
    pygame.display.set_caption("hello pygame")
    while True:
        pygame.display.update()


if __name__ == '__main__':
    run_game()
