import random
from datetime import timedelta

from init import *
from utils import hsv2rgb

class Entity:  # инициализации главного класса
    wight = height = speed = x = y = 0

    def move(self, direction):
        if direction == 'left':
            self.x -= self.speed
        else:
            self.x += self.speed


class Achievement:
    wight = 500
    height = 50
    speed = 0.25
    text = ''
    is_alive = True


    def __init__(self, x, y, text, life_time=10):
        pygame.mixer.Channel(0).play(
            pygame.mixer.Sound('resources/achievement.mp3'))
        self.life_time_limit = life_time
        self.delete_in = datetime.datetime.now() + timedelta(seconds=self.life_time_limit)
        self.x = x
        self.y = y
        self.text = text

    def move(self, game_height):
        born_time = datetime.datetime.now()
        if born_time < self.delete_in:
            if self.y > game_height - 100:
                self.y -= self.speed
        else:
            if self.y < game_height + 50:
                self.y += self.speed
            elif born_time < (self.delete_in + timedelta(seconds=2)):
                self.is_alive = False


class Player(Entity):
    def __init__(self):
        self.wight = 50
        self.height = 30
        self.x = 50
        self.y = win_h - self.height - 10
        self.speed = 1
        self.dmg = 1
        self.bullet_count = 1
        self.health = 50
        self.player = player_png

class Shield(Player):
    def __init__(self, player: Player):
        super().__init__()
        self.wight = player.wight
        self.height = player.height
        self.x = player.x -15
        self.y = player.y - 15
        self.sprite = shield_png
        self.scale_spite()

    def scale_spite(self):
        bigger_img = pygame.transform.scale(self.sprite, (80, 80))
        self.sprite = bigger_img


class Enemy(Entity):
    alive = True

    def __init__(self, poryadoc, health=1):
        global level
        self.sprite = enemy_png
        self.type = "Enemy"
        self.x = 5 + 80 * poryadoc
        self.y = 70
        self.wight = 50
        self.height = 50
        self.speed = level % 50 / 10
        self.go = 'right'
        self.health = health
        self.hhealth = self.health  # неизменяемое здоровье
        self.text_hp = myfont.render(f'{self.health}', False, (255, 255, 255))

    def move(self):
        def switch():
            if self.go == 'right':
                self.go = 'left'
            else:
                self.go = 'right'
            if self.type == "Enemy":
                self.y += 10

        if self.alive:
            if self.go == 'right':
                self.x += self.speed
            else:
                self.x -= self.speed
            if self.go == "lefty":
                pass
            elif self.x >= win_w - self.wight - 5:
                switch()
            if self.x <= 4:
                switch()
            elif self.y >= win_h - self.height - 5:
                self.alive = False
                return False
        return True


class BossEnemy(Enemy):
    def __init__(self):
        super().__init__(1)
        self.sprite = enemy_boss_png
        self.type = "Boss"
        self.wight = 100
        self.height = 50
        self.x = win_w - 150
        self.y = 70
        self.speed = int(level * 0.7) % 20
        self.speed = 1.5
        self.go = "lefty"
        self.health = 1000000
        self.hhealth = self.health


class Snaryad(Entity):
    def __init__(self, x, y):
        global color
        self.type = 'friendly'
        self.x = x
        self.y = y
        self.radius = 10
        self.collor = (hsv2rgb(random.randint(0, 360) / 100, 1, 1))  # color
        self.vel = 100
        self.speed = 0.4

    def live(self):
        self.y -= self.speed


class EnemySnaryad(Snaryad):
    def __init__(self, x, y):
        Snaryad.__init__(self, x, y)
        self.type = 'enemy'
        self.radius = 7
        self.collor = hsv2rgb(1, 1, 1)
        self.vel = -10

    def live(self):
        self.y += self.speed


class BounceEnemySnaryad(EnemySnaryad):

    direction = 'left'
    speed = 1

    def __init__(self, x, y, direction):
        super().__init__(x, y)
        self.direction = direction

    def live(self):
        self.y += self.speed / 3
        if self.direction == 'left':
            self.x -= self.speed
        else:
            self.x += self.speed
        if self.x <= 0:
            self.direction = 'right'
        if self.x >= win_w:
            self.direction = 'left'


class Bonus(Entity):
    sprite = bonus_png
    def __init__(self, x_vraga, y_vraga):
        self.speed = 0.4
        self.alive = True
        self.x = x_vraga + 25
        self.y = y_vraga + 50

        self.scale_spite()
        self.size_x = self.sprite.get_size()[0]+15
        self.size_y = self.sprite.get_size()[1]+15

    def scale_spite(self):
        size = self.sprite.get_size()
        bigger_img = pygame.transform.scale(self.sprite, (int(size[0])*2, int(size[1])*2))
        self.sprite = bigger_img

    def move(self, igrok):
        self.y += self.speed
        if igrok.x < self.x < igrok.x + igrok.wight and igrok.y < self.y < igrok.y + igrok.height:
            self.alive = False
            self.check(igrok)

    def check(self, igrok):
        pass


class BulletBonus(Bonus):
    sprite = bonus_png

    def check(self, igrok):
        igrok.bullet_count += 1


class DamageBonus(Bonus):
    sprite = bonus_dmg_png
    def check(self, igrok):
        igrok.dmg += 1


class SpeedBonus(Bonus):
    sprite = bonus_speed_png
    def check(self, igrok):
        if igrok.speed <= 2:
            igrok.speed += 0.1
            igrok.speed = round(igrok.speed, 1)


class HealthBonus(Bonus):
    sprite = bonus_hp_png
    def check(self, player):
        player.health += 10