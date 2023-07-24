"""
Resources initialisation
"""
import sys
import datetime

if __name__ == "__main__":
    sys.exit()

import pygame
from os import path

pygame.init()
pygame.font.init()
win = pygame.display.set_mode((1366, 768), pygame.WINDOWMOVED)
# инициализируем окошко
ico = pygame.image.load(path.join('resources/space2.png'))
pygame.display.set_icon(ico)  # ярлык окошка
pygame.display.set_caption("Space Ivaders")  # название окошка
pygame.time.Clock().tick(60)  # FPS
win_w = pygame.display.Info().current_w  # определение ширины экрана
win_h = pygame.display.Info().current_h  # определение высоты экрана
myfont = pygame.font.SysFont('Comic Sans MS', 15)  # малый шрифт (для хп)
myfont_bigger = pygame.font.SysFont('Comic Sans MS', 17)  # малый шрифт (для хп)
bigfont = pygame.font.SysFont('Comic Sans MS', 30)  # больший шрифт (для всего)
giantfont = pygame.font.SysFont('Comic Sans MS', 100)  # больший шрифт (для всего)
emptytext = bigfont.render(f'', False, (255, 255, 255))  # инициализация пустого текстового поля
bg = pygame.image.load(path.join('resources/0.gif')).convert_alpha()
# инициализация фона и конвертация в правильный формат пикселей
bg = pygame.transform.scale(bg, (win_w, win_h))  # растягиваем на весь экран
player_png = pygame.image.load(path.join('resources/player.png'))
shield_png = pygame.image.load(path.join('resources/shield.png'))
enemy_png = pygame.image.load(path.join('resources/space2.png'))
enemy_boss_png = pygame.image.load(path.join('resources/boss.png'))
bonus_png = pygame.image.load(path.join('resources/diam.png'))
bonus_dmg_png = pygame.image.load(path.join('resources/diam_dmg.png'))
bonus_speed_png = pygame.image.load(path.join('resources/diam_speed.png'))
bonus_hp_png = pygame.image.load(path.join('resources/diam_hp.png'))
pygame.mixer.music.load(path.join('resources/STS.mp3'))


color = key_color = achievement_color = score = start_ticks = 0  # переменная для таймера
level = 1
bosslvl = False
run = True
proigral = restart = paused = False
show_text_box = False
vragi = []
bonusi = []
bullets = []
enemy_bullets = []
last_shot_time = datetime.datetime.now()
boss_last_shot_time = datetime.datetime.now()

play_music = True
