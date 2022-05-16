import time

import pygame
from pygame.locals import *
import sys
from math import pi

RED = pygame.Color(255, 0, 0)
BLACK = pygame.Color(0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
version = "v1.05"
FPS = 20


class MainGame():
    window = None
    SCREEN_HEIGHT = 500
    SCREEN_WIDTH = 800

    TANK_P1 = None

    def __init__(self):
        ...

    def startGame(self):
        pygame.display.init()  # 初始化游戏窗口
        MainGame.window = pygame.display.set_mode([MainGame.SCREEN_WIDTH, MainGame.SCREEN_HEIGHT])  # 加载窗口
        pygame.display.set_caption("坦克大战" + version)  # 设置标题

        MainGame.TANK_P1 = Tank(400, 300, 5)

        while True:
            MainGame.window.fill(BLACK)
            MainGame.window.blit(self.getTextSurface(f"剩余敌方坦克5辆{version}"), (5, 5))
            self.getEvent()

            MainGame.TANK_P1.displayTank()
            if not MainGame.TANK_P1.stop:
                MainGame.TANK_P1.move()
            time.sleep(0.02)

            pygame.display.update()

    def endGame(self):
        print("谢谢使用")
        exit()

    def getTextSurface(self, text):
        pygame.font.init()
        font = pygame.font.SysFont('kaiti', 18)
        textSurface = font.render(text, True, RED)
        return textSurface

    def checkEvent(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()

    def getEvent(self):
        eventList = pygame.event.get()
        for event in eventList:
            if event.type == pygame.QUIT:
                self.endGame()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    MainGame.TANK_P1.direction = "U"
                    MainGame.TANK_P1.stop = False
                    print("向上移动")
                elif event.key == pygame.K_DOWN:
                    MainGame.TANK_P1.direction = "D"
                    MainGame.TANK_P1.stop = False
                    print("向下移动")
                elif event.key == pygame.K_LEFT:
                    MainGame.TANK_P1.direction = "L"
                    MainGame.TANK_P1.stop = False
                    print("向左移动")
                elif event.key == pygame.K_RIGHT:
                    MainGame.TANK_P1.direction = "R"
                    MainGame.TANK_P1.stop = False
                    print("向右移动")
                elif event.key == pygame.K_SPACE:
                    print("发射子弹")
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    MainGame.TANK_P1.stop = True


class Tank():
    def __init__(self, left, top, speed):
        self.images = {
            'U': pygame.image.load('img/p1tankU.gif'),
            'D': pygame.image.load('img/p1tankD.gif'),
            'L': pygame.image.load('img/p1tankL.gif'),
            'R': pygame.image.load('img/p1tankR.gif')
        }
        self.direction = 'U'
        self.image = self.images[self.direction]
        self.rect = self.image.get_rect()
        self.rect.left = left
        self.rect.top = top
        self.speed = speed
        self.stop = True

    def move(self):
        if self.direction == "L":
            if self.rect.left > 0:
                self.rect.left -= self.speed
        elif self.direction == "R":
            if self.rect.left + self.rect.height < MainGame.SCREEN_WIDTH:
                self.rect.left += self.speed
        elif self.direction == "U":
            if self.rect.top > 0:
                self.rect.top -= self.speed
        elif self.direction == "D":
            if self.rect.top + self.rect.height < MainGame.SCREEN_HEIGHT:
                self.rect.top += self.speed

    def hitWalls(self):
        ...

    def shot(self):
        ...

    def displayTank(self):
        self.image = self.images[self.direction]
        MainGame.window.blit(self.image, self.rect)


class MyTank(Tank):
    def __init__(self):
        ...

    def hitEnemyTank(self):
        ...


class EnemyTank(Tank):
    def __init__(self):
        ...

    def hitMyTank(self):
        ...


class Bullet():
    def __init__(self):
        ...

    def bulletMove(self):
        ...

    def displayBullet(self):
        ...

    def hitEnemyTank(self):
        ...

    def hitMyTank(self):
        ...

    def hitWalls(self):
        ...


class Wall():
    def __init__(self):
        ...

    def displayWall(self):
        ...


class Explode():
    def __init__(self):
        ...

    def displayExplode(self):
        ...


class Music():
    def __init__(self):
        ...

    def play(self):
        ...


def check_event(x, y):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
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
    font = pygame.font.SysFont('kaiti', 18)
    textSurface = font.render(text, True, RED)
    return textSurface


def run_game():
    pygame.init()
    screen = pygame.display.set_mode((600, 500), 0, 32)
    pygame.display.set_caption('Tank坦克')
    x, y = 0, 0
    image = pygame.image.load('OVO_icon.png')
    font = show_font('tank game坦克')
    fpsClock = pygame.time.Clock()
    imgx = 10
    imgy = 10
    direction = 'right'

    # pygame.draw.line(screen, GREEN, [0, 0], [50, 30], 5)

    while True:
        screen.fill((0, 0, 0))
        x, y = check_event(x, y)
        screen.blit(font, (x + 100, y + 100))
        pygame.draw.line(screen, GREEN, [0, 0], [50, 30], 5)
        pygame.draw.aaline(screen, GREEN, [0, 50], [50, 80], True)
        pygame.draw.lines(screen, WHITE, False, [[0, 80], [50, 90], [200, 80], [220, 30]], 5)
        pygame.draw.rect(screen, RED, [225, 10, 50, 20], 1)
        pygame.draw.ellipse(screen, RED, [225, 10, 50, 20], 2)
        pygame.draw.circle(screen, BLUE, [225, 10], 1, 1)

        screen.blit(image, (imgx, imgy))
        if direction == 'right':
            imgx += 5
            if imgx == 380:
                direction = 'down'
        elif direction == 'down':
            imgy += 5
            if imgy == 300:
                direction = 'left'
        elif direction == 'left':
            imgx -= 5
            if imgx == 10:
                direction = 'up'
        elif direction == 'up':
            imgy -= 5
            if imgy == 10:
                direction = 'right'

        pygame.display.update()
        fpsClock.tick(FPS)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # run_game()
    MainGame().startGame()
