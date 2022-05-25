import time
import pygame
from pygame.locals import *
import sys
import random

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
    EnemyTank_count = 5
    EnemyTank_list = []
    Bullet_list = []
    Explode_list = []
    Enemy_bullet_list = []
    Wall_list = []

    def __init__(self):
        ...

    def startGame(self):
        pygame.display.init()  # 初始化游戏窗口
        MainGame.window = pygame.display.set_mode([MainGame.SCREEN_WIDTH, MainGame.SCREEN_HEIGHT])  # 加载窗口
        pygame.display.set_caption("坦克大战" + version)  # 设置标题

        self.createMyTank()
        self.createEnemyTank()
        self.createWalls()

        while True:
            MainGame.window.fill(BLACK)
            MainGame.window.blit(self.getTextSurface(f"剩余敌方坦克5辆{version}"), (5, 5))
            self.getEvent()

            if MainGame.TANK_P1 and MainGame.TANK_P1.live:
                MainGame.TANK_P1.displayTank()
            else:
                del MainGame.TANK_P1
                MainGame.TANK_P1 = None
            if MainGame.TANK_P1 and not MainGame.TANK_P1.stop:
                MainGame.TANK_P1.move()
                MainGame.TANK_P1.hitWalls()
                MainGame.TANK_P1.hitEnemyTank()

            self.blitWalls()
            self.blitEnemyTank()
            self.blitBullet()
            self.blitEnemyBullet()
            self.displayExplodes()

            time.sleep(0.02)

            pygame.display.update()

    def endGame(self):
        print("谢谢使用")
        exit()

    def getTextSurface(self, text):
        # 插入文字
        pygame.font.init()
        font = pygame.font.SysFont('kaiti', 18)
        textSurface = font.render(text, True, RED)
        return textSurface

    def createMyTank(self):
        MainGame.TANK_P1 = MyTank(400, 300, 5)
        music = Music('img/start.wav')
        music.play()

    def createEnemyTank(self):
        top = 100
        speed = random.randint(3, 6)
        for i in range(MainGame.EnemyTank_count):
            left = random.randint(1, 7)
            eTank = EnemyTank(left * 100, top, speed)
            MainGame.EnemyTank_list.append(eTank)

    def blitEnemyTank(self):
        for eTank in MainGame.EnemyTank_list:
            if eTank.live:
                eTank.displayTank()
                eTank.randMove()
                eTank.hitWalls()
                eTank.hitMyTank()
                eBullet = eTank.shot()
                if eBullet:
                    MainGame.Enemy_bullet_list.append(eBullet)
            else:
                MainGame.EnemyTank_list.remove(eTank)

    def blitBullet(self):
        for bullet in MainGame.Bullet_list:
            if bullet.live:
                bullet.displayBullet()
                bullet.bulletMove()
                bullet.hitEnemyTank()
                bullet.hitWalls()
            else:
                MainGame.Bullet_list.remove(bullet)

    def blitEnemyBullet(self):
        for eBullet in MainGame.Enemy_bullet_list:
            if eBullet.live:
                eBullet.displayBullet()
                eBullet.bulletMove()
                eBullet.hitWalls()
                if MainGame.TANK_P1:
                    eBullet.hitMyTank()
            else:
                MainGame.Enemy_bullet_list.remove(eBullet)

    def displayExplodes(self):
        for explode in MainGame.Explode_list:
            if explode.live:
                explode.displayExplode()
            else:
                MainGame.Explode_list.remove(explode)

    def createWalls(self):
        for i in range(6):
            wall = Wall(130 * i, 240)
            MainGame.Wall_list.append(wall)

    def blitWalls(self):
        for wall in MainGame.Wall_list:
            if wall.live:
                wall.displayWall()
            else:
                MainGame.Wall_list.remove(wall)

    def getEvent(self):
        eventList = pygame.event.get()
        for event in eventList:
            if event.type == pygame.QUIT:
                self.endGame()
            if event.type == pygame.KEYDOWN:
                if MainGame.TANK_P1 and MainGame.TANK_P1.live:
                    if event.key == pygame.K_UP:
                        MainGame.TANK_P1.direction = "U"
                        MainGame.TANK_P1.stop = False
                        # print("向上移动")
                    elif event.key == pygame.K_DOWN:
                        MainGame.TANK_P1.direction = "D"
                        MainGame.TANK_P1.stop = False
                        # print("向下移动")
                    elif event.key == pygame.K_LEFT:
                        MainGame.TANK_P1.direction = "L"
                        MainGame.TANK_P1.stop = False
                        # print("向左移动")
                    elif event.key == pygame.K_RIGHT:
                        MainGame.TANK_P1.direction = "R"
                        MainGame.TANK_P1.stop = False
                        # print("向右移动")
                    elif event.key == pygame.K_SPACE:
                        # print("发射子弹")
                        m = Bullet(MainGame.TANK_P1)
                        MainGame.Bullet_list.append(m)
                        music = Music('img/fire.wav')
                        music.play()
            if event.type == pygame.KEYUP:
                if (
                        event.key == pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT) and MainGame.TANK_P1:
                    MainGame.TANK_P1.stop = True


class BaseItem(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)


class Tank(BaseItem):
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
        self.live = True
        self.oldLeft = self.rect.left
        self.oldTop = self.rect.top

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
        for wall in MainGame.Wall_list:
            if pygame.sprite.collide_rect(self, wall):
                self.stay()

    def shot(self):
        ...

    def displayTank(self):
        self.image = self.images[self.direction]
        MainGame.window.blit(self.image, self.rect)

    def stay(self):
        self.rect.left = self.oldLeft
        self.rect.top = self.oldTop


class MyTank(Tank):
    def __init__(self, left, top, speed):
        super(MyTank, self).__init__(left, top, speed)

    def hitEnemyTank(self):
        for eTank in MainGame.EnemyTank_list:
            if pygame.sprite.collide_rect(eTank, self):
                self.stay()


class EnemyTank(Tank):
    def __init__(self, left, top, speed):
        # super(EnemyTank,self).__init__(left,top,speed)
        Tank.__init__(self, left, top, speed)
        self.images = {
            "U": pygame.image.load('img/enemy1U.gif'),
            "D": pygame.image.load('img/enemy1D.gif'),
            "L": pygame.image.load('img/enemy1L.gif'),
            "R": pygame.image.load('img/enemy1R.gif')
        }
        self.direction = self.randDirection()
        self.image = self.images[self.direction]
        self.rect = self.image.get_rect()
        self.rect.left = left
        self.rect.top = top
        self.speed = speed
        self.stop = True
        self.step = 50
        # self.live = True

    def randDirection(self):
        num = random.randint(1, 4)
        directions = {
            1: "U",
            2: "D",
            3: "L",
            4: "R"
        }
        return directions[num]

    def hitMyTank(self):
        if MainGame.TANK_P1 and MainGame.TANK_P1.live:
            if pygame.sprite.collide_rect(MainGame.TANK_P1, self):
                self.stay()

    def randMove(self):
        if self.step == 0:
            self.direction = self.randDirection()
            self.step = 50
        else:
            self.move()
            self.step -= 1

    def shot(self):
        num = random.randint(1, 1000)
        if num <= 20:
            return Bullet(self)


class Bullet(BaseItem):
    def __init__(self, tank):
        self.image = pygame.image.load('img/enemymissile.gif')
        self.deriction = tank.direction
        self.rect = self.image.get_rect()
        if self.deriction == 'U':
            self.rect.left = tank.rect.left + tank.rect.width / 2 - self.rect.width / 2
            self.rect.top = tank.rect.top - self.rect.height
        elif self.deriction == 'D':
            self.rect.left = tank.rect.left + tank.rect.width / 2 - self.rect.width / 2
            self.rect.top = tank.rect.top + tank.rect.height
        elif self.deriction == 'L':
            self.rect.left = tank.rect.left - self.rect.width
            self.rect.top = tank.rect.top + tank.rect.height / 2 - self.rect.height / 2
        elif self.deriction == 'R':
            self.rect.left = tank.rect.left + tank.rect.width
            self.rect.top = tank.rect.top + tank.rect.height / 2 - self.rect.height / 2
        self.speed = 7
        self.live = True

    def bulletMove(self):
        if self.deriction == 'U':
            if self.rect.top > 0:
                self.rect.top -= self.speed
            else:
                self.live = False
        elif self.deriction == 'D':
            if self.rect.top + self.rect.height < MainGame.SCREEN_HEIGHT:
                self.rect.top += self.speed
            else:
                self.live = False
        elif self.deriction == 'L':
            if self.rect.left > 0:
                self.rect.left -= self.speed
            else:
                self.live = False
        elif self.deriction == 'R':
            if self.rect.left + self.rect.width < MainGame.SCREEN_WIDTH:
                self.rect.left += self.speed
            else:
                self.live = False

    def displayBullet(self):
        MainGame.window.blit(self.image, self.rect)

    def hitEnemyTank(self):
        for eTank in MainGame.EnemyTank_list:
            if pygame.sprite.collide_rect(eTank, self):
                explode = Explode(eTank)
                MainGame.Explode_list.append(explode)
                self.live = False
                eTank.live = False

    def hitMyTank(self):
        if pygame.sprite.collide_rect(self, MainGame.TANK_P1):
            explode = Explode(MainGame.TANK_P1)
            MainGame.Explode_list.append(explode)
            self.live = False
            MainGame.TANK_P1.live = False

    def hitWalls(self):
        for wall in MainGame.Wall_list:
            if pygame.sprite.collide_rect(self, wall):
                wall.hp -= 1
                self.live = False
                if wall.hp == 0:
                    wall.live = False


class Wall():
    def __init__(self, left, top):
        self.image = pygame.image.load('img/steels.gif')
        self.rect = self.image.get_rect()
        self.rect.left = left
        self.rect.top = top
        self.live = True
        self.hp = 3

    def displayWall(self):
        MainGame.window.blit(self.image, self.rect)


class Explode():
    def __init__(self, tank):
        self.rect = tank.rect
        self.step = 0
        self.images = [
            pygame.image.load('img/blast0.gif'),
            pygame.image.load('img/blast1.gif'),
            pygame.image.load('img/blast2.gif'),
            pygame.image.load('img/blast3.gif'),
            pygame.image.load('img/blast4.gif')
        ]
        self.image = self.images[self.step]
        self.live = True

    def displayExplode(self):
        if self.step < len(self.images):
            MainGame.window.blit(self.image, self.rect)
            self.image = self.images[self.step]
            self.step += 1
        else:
            self.live = False
            self.step = 0


class Music():
    def __init__(self, fileName):
        self.fileName = fileName
        pygame.mixer.init()
        pygame.mixer.music.load(self.fileName)

    def play(self):
        pygame.mixer.music.play()


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
