import pygame
import sys
import random
from os import path
from colorsys import hsv_to_rgb

pygame.init()
pygame.font.init()
win = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)  # инициализируем окошко
ico = pygame.image.load(path.join('sprites/space2.png'))
pygame.display.set_icon(ico)

win_w = pygame.display.Info().current_w  # ширина
win_h = pygame.display.Info().current_h  # высота

pygame.display.set_caption("Space Ivaders")  # название окошко
FPS = 60  # ну тут всё понятно
clock = pygame.time.Clock()  # сетапим "тикрейт"

myfont = pygame.font.SysFont('Comic Sans MS', 15)  # малый шрифт (для хп)
bigfont = pygame.font.SysFont('Comic Sans MS', 30)  # больший шрифт (для всего)

bg = pygame.image.load(path.join('sprites/0.gif')).convert_alpha()
# инициализация фона и конвертация в правильный формат пикселей
bg = pygame.transform.scale(bg, (win_w, win_h))  # растягиваем на весь экран
bonus_png = pygame.image.load(path.join('sprites/diam.png'))
bonus_dmg_png = pygame.image.load(path.join('sprites/diam_dmg.png'))
bonus_speed_png = pygame.image.load(path.join('sprites/diam_speed.png'))
music_play = 0
pygame.mixer.music.load(path.join('sprites/STS.mp3'))

color = 0
level = 1
score = 0
start_ticks = 0  # переменная для таймера
run = True  # для главного окна
vvod = True  # для окна ввода кол-ва врагов
proigral = False
restart = False
paused = False

textsurface = bigfont.render('', False, (255, 255, 255))
textsurface_timer = bigfont.render('', False, (255, 255, 255))
text_error = myfont.render('', False, (255, 255, 255))
text_lvl = bigfont.render('', False, (255, 255, 255))
text_score = bigfont.render('', False, (255, 255, 255))


def hsv2rgb(h, s, v):
    return tuple(round(i * 255) for i in hsv_to_rgb(h, s, v))


def DrawWindow(chet):
    global animCount, start_ticks, proigral, textsurface, textsurface_timer, level, text_score, color
    score = chet
    win.blit(bg, (0, 0))
    pygame.draw.rect(win, (0, 0, 0), (0, 0, win_w, 45))
    text_lvl = bigfont.render(
        f'level: {level}  score: {score}  bullets: {molodec.bullet_count}   dmg:{molodec.dmg}  speed: {molodec.speed}',
        False,
        (255, 255, 255))
    if color == 360:
        color = 0
    text_name = bigfont.render(r"\\ Donts_'s Space Invaders", False, hsv2rgb(color / 100, 1, 1))
    color += 1
    if not len(vragi) and not proigral:
        if not start_ticks and level:
            start_ticks = pygame.time.get_ticks()
        seconds = (pygame.time.get_ticks() - start_ticks) / 1000
        textsurface = bigfont.render(f'КРОСАВА, ВСЕХ УБЫВ!!!', False, (255, 255, 255))
        textsurface_timer = bigfont.render(f'Время на отдохнуть: {round(4 - seconds, 3)}', False, (255, 255, 255))
        if seconds > 0.1:
            level += 1
            spawn(count)
            start_ticks = 0
            textsurface = bigfont.render('', False, (255, 255, 255))
            textsurface_timer = bigfont.render('', False, (255, 255, 255))

    if molodec.animCount + 1 >= 30:
        molodec.animCount = 0

    if molodec.left:
        win.blit(molodec.walkLeft[molodec.animCount // 5], (molodec.x, molodec.y))
        if not paused:
            molodec.animCount += 1
    elif molodec.right:
        win.blit(molodec.walkRight[molodec.animCount // 5], (molodec.x, molodec.y))
        if not paused:
            molodec.animCount += 1
    else:
        win.blit(molodec.playerStand, (molodec.x, molodec.y))

    for bullet in bullets:
        bullet.draw(win)
    for item in vragi:
        item.Living()
        if not item.move():
            vragi.clear()
            proigral = True

    if len(bonusi):
        for item in bonusi:
            if item.alive:
                win.blit(item.sprite, (item.x, item.y))
                item.move(molodec, item.sprite)

    if proigral:
        textsurface = bigfont.render(f'ТИ ПРОЕГРАФ', False, (255, 255, 255))
        textsurface_timer = bigfont.render('Press F to Restart', False, (255, 255, 255))
        if keys[pygame.K_f]:
            do_restart(molodec)

    if paused:
        textsurface = bigfont.render(f'Пауза. Press P to continue', False, (255, 255, 255))
        pygame.draw.rect(win, (255, 0, 200), (win_w / 2, 300, 400, 45))
    else:
        textsurface = bigfont.render('', False, (255, 255, 255))
    win.blit(textsurface, (win_w / 2, 300))
    win.blit(textsurface_timer, (win_w / 2, 350))
    win.blit(text_lvl, (5, 0))
    win.blit(text_score, (160, 0))
    win.blit(text_name, (win_w / 2 + 20, 0))
    pygame.display.update()


vragi = []
bonusi = []


def do_restart(igrok):
    global proigral, level, textsurface, textsurface_timer, score
    score = 0
    igrok.bullet_count = 1
    igrok.speed = 5
    igrok.dmg = 1
    proigral = 0
    level = 0
    textsurface = bigfont.render(f'', False, (255, 255, 255))
    textsurface_timer = bigfont.render('', False, (255, 255, 255))
    bullets.clear()
    vragi.clear()


def spawn(chislo):
    global vragi
    for i in range(int(chislo)):
        vragi.append(Enemy(i))


class Player:
    def __init__(self):
        self.wight = 60
        self.height = 71
        self.x = 50
        self.y = win_h - self.height - 10
        self.speed = 5
        self.dmg = 1
        self.isJump = False
        self.jumpCount = 10
        self.bullet_count = 1
        self.left = False
        self.right = False
        self.animCount = 0
        self.last_move = 'right'
        self.walkRight = [pygame.image.load(path.join(f'sprites/pygame_right_{i}.png')) for i in range(1, 7)]
        self.walkLeft = [pygame.image.load(path.join(f'sprites/pygame_left_{i}.png')) for i in range(1, 7)]
        self.playerStand = pygame.image.load(path.join('sprites/pygame_idle.png'))

    def move(self, direction):
        if direction == 'left':
            self.x -= self.speed
            self.left = True
            self.right = False
        else:
            self.x += self.speed
            self.left = False
            self.right = True


class Enemy:
    def __init__(self, poryadoc):
        global level
        self.sprite = pygame.image.load(path.join('sprites/space2.png'))
        self.x = 5 + 80 * poryadoc
        self.y = 70
        self.wight = 50
        self.height = 50
        self.speed = level
        self.go = 'right'
        self.alive = True
        self.health = 10 * level
        self.hhealth = self.health  # неизменяемое здоровье
        self.text_hp = myfont.render(f'{self.health}', False, (255, 255, 255))

    def Living(self):
        if self.alive:
            self.text_hp = myfont.render(f'{self.health}', False, (255, 255, 255))
            pygame.draw.rect(win, (0, 0, 0), (self.x, self.y - 25, self.wight, 25))
            pygame.draw.rect(win, hsv2rgb((self.health * 100 / self.hhealth) / 333, 1, 1), (
                self.x + 3, self.y - 23, (self.wight - 5) - (self.wight - (self.wight * self.health) / self.hhealth),
                20))
            win.blit(self.sprite, (self.x, self.y))
            win.blit(self.text_hp, ((self.x + 15), (self.y - 25)))

    def move(self):
        global paused
        if self.alive and not paused:
            if self.go == 'right':
                self.x += self.speed
            else:
                self.x -= self.speed
            if self.x >= win_w - self.wight - 5:
                self.go = 'left'
                self.y += self.speed
            if self.x <= 4:
                self.go = 'right'
                self.y += self.speed
            if self.y >= win_h - self.height - 5:
                self.alive = False
                return False
        return True


class Snaryad:
    def __init__(self, x, y, radius):
        global color
        self.x = x
        self.y = y
        self.radius = radius
        self.collor = (hsv2rgb(random.randint(0, 360) / 100, 1, 1))  # color
        self.vel = 20

    def draw(self, window):
        pygame.draw.circle(window, self.collor, (self.x, self.y), self.radius)


class Bonus:
    def __init__(self, x_vraga, y_vraga, kavo):
        self.x = x_vraga + 25
        self.y = y_vraga + 50
        self.speed = 5
        self.sprite = kavo
        self.alive = True

    def move(self, igrok, kavo):
        self.y += self.speed
        if igrok.x < self.x < igrok.x + igrok.wight and igrok.y < self.y < igrok.y + igrok.height:
            self.alive = False
            if kavo == bonus_png:
                igrok.bullet_count += 1
            elif kavo == bonus_dmg_png:
                igrok.dmg += 1
            elif igrok.speed <= 10:
                igrok.speed += 1


count = ''
while vvod:
    clock.tick(FPS)
    pygame.draw.rect(win, (0, 0, 0), (0, 0, win_w, win_h))
    keys = pygame.key.get_pressed()
    text_vopros = bigfont.render(f'Сколько (от 1 до 17) хочешь врагов?: {count}', False, (255, 255, 255))
    text_about = myfont.render(r'© \\ Donts_   2019', False, (255, 255, 255))
    if color == 100:
        color = 0.0
    text_name = bigfont.render(r"\\ Donts_'s Space Invaders", False, hsv2rgb(color / 100, 1, 1))
    color += 0.5
    textsurface = bigfont.render('Управление: A & D (Стрелки)   Прыжок: Space   Атака: E', False, (255, 255, 255))
    textsurface2 = bigfont.render('Выход: ESC   Рестарт: F  Пауза: P', False, (255, 255, 255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
            vvod = False
            run = False
        elif event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_0 or event.key == pygame.K_KP0) and count:
                count += '0'
            elif event.key == pygame.K_1 or event.key == pygame.K_KP1:
                count += '1'
            elif event.key == pygame.K_2 or event.key == pygame.K_KP2:
                count += '2'
            elif event.key == pygame.K_3 or event.key == pygame.K_KP3:
                count += '3'
            elif event.key == pygame.K_4 or event.key == pygame.K_KP4:
                count += '4'
            elif event.key == pygame.K_5 or event.key == pygame.K_KP5:
                count += '5'
            elif event.key == pygame.K_6 or event.key == pygame.K_KP6:
                count += '6'
            elif event.key == pygame.K_7 or event.key == pygame.K_KP7:
                count += '7'
            elif event.key == pygame.K_8 or event.key == pygame.K_KP8:
                count += '8'
            elif event.key == pygame.K_9 or event.key == pygame.K_KP9:
                count += '9'
            elif event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN:
                try:
                    int(count)
                except ValueError:
                    text_error = bigfont.render('Чет ты перегнул', False, (255, 255, 255))
                else:
                    if 0 <= int(count) <= 17:
                        n = int(count)
                        vvod = False
                    else:
                        text_error = bigfont.render('Чет ты перегнул', False, (255, 255, 255))
    win.blit(text_name, (500, 30))
    win.blit(textsurface, (250, 130))
    win.blit(textsurface2, (250, 170))
    win.blit(text_vopros, (200, 450))
    win.blit(text_error, (200, 500))
    win.blit(text_about, (0, win_h - 30))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_BACKSPACE]:
        if len(count) > 0:
            count = count[:-1]
    pygame.display.update()

bullets = []

molodec = Player()
textsurface = bigfont.render('', False, (255, 255, 255))
pygame.mixer.music.play(-1)
spawn(count)
while run:
    clock.tick(FPS)
    keys = pygame.key.get_pressed()
    if not paused:
        for bullet in bullets:
            if win_h > bullet.y > 60:
                bullet.y -= bullet.vel
                for item in vragi:
                    if item.x < bullet.x < (item.x + item.wight) \
                            and item.y < bullet.y < (item.y + item.height):
                        item.health -= molodec.dmg
                        if item.health <= 0:
                            score += level
                            item.alive = False
                            vragi.pop(vragi.index(item))
                            if random.randint(0, 10) == random.randint(0, 10):
                                bonusi.append(Bonus(item.x, item.y, bonus_png))
                            elif random.randint(0, 100) == random.randint(0, 100):
                                bonusi.append(Bonus(item.x, item.y, bonus_dmg_png))
                            elif random.randint(0, 500) == random.randint(0, 500):
                                bonusi.append(Bonus(item.x, item.y, bonus_speed_png))
                        if bullet in bullets:
                            bullets.pop(bullets.index(bullet))
            elif bullet in bullets:
                bullets.pop(bullets.index(bullet))
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and molodec.x > 5:
            molodec.move('left')
        elif (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and molodec.x < win_w - molodec.wight - 5:
            molodec.move('right')
        else:
            molodec.left = False
            molodec.right = False
            molodec.animCount = 0
        if not molodec.isJump:
            if keys[pygame.K_SPACE]:
                molodec.isJump = True
        else:
            if molodec.jumpCount >= -10:
                if molodec.jumpCount < 0:
                    molodec.y += (molodec.jumpCount ** 2) / 5
                else:
                    molodec.y -= (molodec.jumpCount ** 2) / 5
                molodec.jumpCount -= 0.5
            else:
                molodec.isJump = False
                molodec.jumpCount = 10

        for item in vragi:
            item.move()

        if keys[pygame.K_e]:
            if len(bullets) < 10000:
                for item in range(molodec.bullet_count):
                    bullets.append(
                        Snaryad((round(molodec.x + int(item) * 2)), round(molodec.y + molodec.wight // 2), 2))

    for event in pygame.event.get():
        if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                do_restart(molodec)
            elif event.key == pygame.K_p:
                if not paused:
                    paused = True
                    pygame.mixer.music.pause()
                else:
                    paused = False
                    pygame.mixer.music.unpause()
            elif event.key == pygame.K_m:
                if not music_play:
                    music_play = 1
                    pygame.mixer.music.play(-1)
                else:
                    music_play = 0
                    pygame.mixer.music.stop()

    DrawWindow(score)

pygame.quit()
sys.exit()
