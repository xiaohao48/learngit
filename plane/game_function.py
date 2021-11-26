import pygame
import sys


def check_events(my_plane):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            event_keydown(event, my_plane)
        if event.type == pygame.KEYUP:
            event_keyup(event, my_plane)


def event_keydown(event, my_plane):
    if event.key == pygame.K_UP:
        my_plane.up = True
    if event.key == pygame.K_DOWN:
        my_plane.down = True
    if event.key == pygame.K_LEFT:
        my_plane.left = True
    if event.key == pygame.K_RIGHT:
        my_plane.right = True


def event_keyup(event, my_plane):
    if event.key == pygame.K_UP:
        my_plane.up = False
    if event.key == pygame.K_DOWN:
        my_plane.down = False
    if event.key == pygame.K_LEFT:
        my_plane.left = False
    if event.key == pygame.K_RIGHT:
        my_plane.right = False
