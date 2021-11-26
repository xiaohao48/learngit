import pygame
import traceback
import sys
from ai_settings import Ai_settings
import game_function as gf
from my_plane import My_plane


def run_game():
    pygame.init()
    ai_settings = Ai_settings()

    screen = pygame.display.set_mode(ai_settings.screen)
    pygame.display.set_caption(ai_settings.title)
    my_plane = My_plane(ai_settings, screen)

    while True:
        gf.check_events(my_plane)
        screen.blit(ai_settings.background, (0, 0))

        my_plane.blitme()
        my_plane.update()

        pygame.display.flip()


if __name__ == '__main__':
    # try:
    #     run_game()
    # except:
    #     traceback.print_exc()
    #     pygame.quit()
    run_game()
