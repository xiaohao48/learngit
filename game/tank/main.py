import pygame

COLOR_RED = (255, 0, 0)


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


def check_event(x, y):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x -= 10
            elif event.key == pygame.K_RIGHT:
                x += 10
            elif event.key == pygame.K_UP:
                y -= 10
            elif event.key == pygame.K_DOWN:
                y += 10
    return x, y

def show_font(text):
    font = pygame.font.SysFont('arial', 18)
    textSurface=font.render(text,True,COLOR_RED)
    return textSurface


def run_game():
    pygame.init()
    screen = pygame.display.set_mode((600, 500), 0, 32)
    pygame.display.set_caption('Tank')
    x, y = 0, 0
    image = pygame.image.load('OVO_icon.png')
    font = show_font('tank game')

    while True:
        screen.fill((0, 0, 0))
        x, y = check_event(x, y)
        screen.blit(font,(x+100,y+100))

        screen.blit(image, (x, y))
        pygame.display.update()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    run_game()
