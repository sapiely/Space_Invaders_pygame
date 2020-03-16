import sys
import random
from colorsys import hsv_to_rgb
from init import *


class Entity:  # инициализации главного класса
    wight = height = speed = x = y = 0

    def move(self, direction):
        if direction == 'left':
            self.x -= self.speed
        else:
            self.x += self.speed


class Player(Entity):
    def __init__(self):
        self.wight = 50
        self.height = 30
        self.x = 50
        self.y = win_h - self.height - 10
        self.speed = 5
        self.dmg = 1
        self.bullet_count = 1
        self.health = 100
        self.player = player_png


class Enemy(Entity):
    alive = True

    def __init__(self, poryadoc):
        global level
        self.sprite = enemy_png
        self.type = "Enemy"
        self.x = 5 + 80 * poryadoc
        self.y = 70
        self.wight = 50
        self.height = 50
        self.speed = level % 20
        self.go = 'right'
        self.health = int(level * e ** 0.5)*8
        self.hhealth = self.health  # неизменяемое здоровье
        self.text_hp = myfont.render(f'{self.health}', False, (255, 255, 255))

    def living(self):
        if self.alive:
            self.text_hp = myfont.render(f'{self.health}', False, (255, 255, 255))
            pygame.draw.rect(win, (0, 0, 0), (self.x, self.y - 25, self.wight, 25))
            pygame.draw.rect(win, hsv2rgb((self.health * 100 / self.hhealth) / 333, 1, 1), (
                self.x + 3, self.y - 23, (self.wight - 5) - (self.wight - (self.wight * self.health) / self.hhealth),
                20))
            win.blit(self.sprite, (self.x, self.y))
            win.blit(self.text_hp, ((self.x + self.wight / 3), (self.y - 25)))

    def move(self):
        def switch():
            if self.go == 'left':
                self.go = 'right'
            else:
                self.go = 'left'
            self.y += 10
        global paused
        if self.alive and not paused:
            if self.go == 'right':
                self.x += self.speed
            else:
                self.x -= self.speed
            if self.x >= win_w - self.wight - 5 and self.type != "Boss":
                switch()
            if self.x <= 4:
                switch()
            if self.y >= win_h - self.height - 5:
                self.alive = False
                return False
        return True


class BossEnemy(Enemy):
    def __init__(self):
        self.sprite = pygame.image.load(path.join('sprites/boss.png'))
        self.type = "Boss"
        self.wight = 100
        self.height = 50
        self.x = win_w + 150
        self.y = 70
        self.speed = int(level * 0.7) % 20
        self.go = "left"
        self.health = int(level * e ** 0.6) * 10
        self.hhealth = self.health


class Snaryad(Entity):
    def __init__(self, x, y):
        global color
        self.type = 'friendly'
        self.x = x
        self.y = y
        self.radius = 2
        self.collor = (hsv2rgb(random.randint(0, 360) / 100, 1, 1))  # color
        self.vel = 20

    def draw(self, window):
        pygame.draw.circle(window, self.collor, (self.x, self.y), self.radius)

    def live(self):
        self.y -= self.vel


class EnemySnaryad(Snaryad):
    def __init__(self, x, y):
        Snaryad.__init__(self, x, y)
        self.type = 'enemy'
        self.radius = 4
        self.collor = hsv2rgb(1, 1, 1)
        self.vel = -10


class Bonus(Entity):
    def __init__(self, x_vraga, y_vraga, vid):
        self.speed = 5
        self.alive = True
        self.x = x_vraga + 25
        self.y = y_vraga + 50
        self.sprite = vid

    def move(self, igrok):
        self.y += self.speed
        if igrok.x < self.x < igrok.x + igrok.height and igrok.y < self.y < igrok.y + igrok.wight:
            self.alive = False
            self.check(igrok)

    def check(self, igrok):
        pass


class BulletBonus(Bonus):
    def check(self, igrok):
        igrok.bullet_count += 1


class DamageBonus(Bonus):
    def check(self, igrok):
        igrok.dmg += 1


class SpeedBonus(Bonus):
    def check(self, igrok):
        if igrok.speed <= 10:
            igrok.speed += 1


class HealthBonus(Bonus):
    def check(self, player):
        player.health += 10


def hsv2rgb(h, s, v):
    return tuple(round(i * 255) for i in hsv_to_rgb(h, s, v))


def drawwindow(score):
    global start_ticks, proigral, level, color
    textsurface_timer = text_score = textsurface = emptytext
    win.blit(bg, (0, 0))
    pygame.draw.rect(win, (0, 0, 0), (0, 0, win_w, 45))
    text_lvl = bigfont.render(
        f'level: {level}  score: {score}  Health: {molodec.health}  bullets: {molodec.bullet_count}   dmg:{molodec.dmg} '
        f' speed: {molodec.speed}', False, (255, 255, 255))
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
        if seconds > 4:
            spawn(17)
            start_ticks = 0
            textsurface = bigfont.render('', False, (255, 255, 255))
            textsurface_timer = bigfont.render('', False, (255, 255, 255))

    if not proigral:
        win.blit(molodec.player, (molodec.x, molodec.y))

    for bullet in bullets:
        bullet.draw(win)
    for item in vragi:
        item.living()
        if not item.move() or molodec.health <= 0:
            vragi.clear()
            bullets.clear()
            proigral = True

    if len(bonusi):
        for item in bonusi:
            if item.alive:
                win.blit(item.sprite, (item.x, item.y))
                item.move(molodec)

    if proigral:
        textsurface = bigfont.render('ТИ ПРОЕГРАФ', False, (255, 255, 255))
        textsurface_timer = bigfont.render('Press F to Restart', False, (255, 255, 255))

        if keys[pygame.K_f]:
            do_restart(molodec)

    if paused and not proigral:
        textsurface = bigfont.render(f'Пауза. Press P to continue', False, (255, 255, 255))
        pygame.draw.rect(win, (255, 0, 200), (win_w / 2, 300, 400, 45))
    elif not proigral and len(vragi):
        textsurface = bigfont.render('', False, (255, 255, 255))
    win.blit(textsurface, (win_w / 2, 300))
    win.blit(textsurface_timer, (win_w / 2, 350))
    win.blit(text_lvl, (5, 0))
    win.blit(text_score, (160, 0))
    win.blit(text_name, (win_w - 410, 0))
    pygame.display.update()


def do_restart(igrok):
    global proigral, level, textsurface, textsurface_timer, score
    score = proigral = level = 0
    igrok.bullet_count = igrok.dmg = 1
    textsurface = textsurface_timer = emptytext
    igrok.speed = 5
    igrok.health = 100
    bullets.clear()
    vragi.clear()


def spawn(chislo):
    global vragi, level, bosslvl
    level += 1
    bosslvl = True if level % 5 == 0 else False
    if not bosslvl:
        for i in range(int(chislo)):
            vragi.append(Enemy(i))
    else:
        vragi.append(BossEnemy())


if __name__ == "__main__":
    color = score = start_ticks = 0  # переменная для таймера
    level = 0
    bosslvl = False
    run = True
    proigral = restart = paused = False
    vragi = []
    bonusi = []
    bullets = []

    molodec = Player()
    music_play = True
    pygame.mixer.music.play(-1)
    spawn(17)
    while run:

        keys = pygame.key.get_pressed()
        if not paused:
            for bullet in bullets:
                if win_h > bullet.y > 60:
                    bullet.live()
                    for item in vragi:
                        if item.x < bullet.x < (item.x + item.wight) \
                                and item.y < bullet.y < (item.y + item.height):
                            item.health -= molodec.dmg
                            if item.health <= 0:
                                if item.type == "Enemy":
                                    score += level
                                else:
                                    score += level * 2
                                item.alive = False
                                vragi.pop(vragi.index(item))
                                if random.randint(0, 10) == random.randint(0, 10):
                                    bonusi.append(BulletBonus(item.x, item.y, bonus_png))
                                elif random.randint(0, 100) == random.randint(0, 100):
                                    bonusi.append(DamageBonus(item.x, item.y, bonus_dmg_png))
                                elif bosslvl:
                                    bonusi.append(DamageBonus(item.x, item.y, bonus_dmg_png))
                                elif random.randint(0, 110) == random.randint(0, 110):
                                    bonusi.append(HealthBonus(item.x, item.y, bonus_hp_png))
                                elif random.randint(0, 500) == random.randint(0, 500):
                                    bonusi.append(SpeedBonus(item.x, item.y, bonus_speed_png))
                            if bullet in bullets:
                                bullets.pop(bullets.index(bullet))
                    if bullet.type == 'enemy' and molodec.x < bullet.x < (molodec.x + molodec.wight) \
                            and molodec.y < bullet.y < (molodec.y + molodec.height):
                        molodec.health -= 1
                elif bullet in bullets:
                    bullets.pop(bullets.index(bullet))
            if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and molodec.x > 5:
                molodec.move('left')
            elif (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and molodec.x < win_w - molodec.wight - 5:
                molodec.move('right')

            for item in vragi:
                item.move()

            if keys[pygame.K_e]:
                if len(bullets) < 10000:
                    for item in range(molodec.bullet_count):
                        bullets.append(
                            Snaryad((round(molodec.x + int(item * 0.3))), round(molodec.y + molodec.wight // 2)))

            if len(vragi) != 0 and bosslvl and random.randint(0, 5) == 1:
                bullets.append(EnemySnaryad(vragi[0].x + 50, vragi[0].y + 53))

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
                        music_play = True
                        pygame.mixer.music.play(-1)
                    else:
                        music_play = False
                        pygame.mixer.music.stop()
                elif event.key == pygame.K_KP_PLUS:
                    level += 1
        drawwindow(score)

    pygame.quit()
    sys.exit()
