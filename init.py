if __name__ == "__main__":
    pass
else:
    import pygame
    from os import path
    from math import e
    pygame.init()
    pygame.font.init()
    win = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    # инициализируем окошко
    ico = pygame.image.load(path.join('sprites/space2.png'))
    pygame.display.set_icon(ico)  # ярлык окошка
    pygame.display.set_caption("Space Ivaders")  # название окошка

    pygame.time.Clock().tick(60)  # FPS

    win_w = pygame.display.Info().current_w  # определение ширины экрана
    win_h = pygame.display.Info().current_h  # определение высоты экрана

    myfont = pygame.font.SysFont('Comic Sans MS', 15)  # малый шрифт (для хп)
    bigfont = pygame.font.SysFont('Comic Sans MS', 30)  # больший шрифт (для всего)

    emptytext = bigfont.render(f'', False, (255, 255, 255))  # инициализация пустого текстового поля

    bg = pygame.image.load(path.join('sprites/0.gif')).convert_alpha()
    # инициализация фона и конвертация в правильный формат пикселей
    bg = pygame.transform.scale(bg, (win_w, win_h))  # растягиваем на весь экран
    player_png = pygame.image.load(path.join('sprites/player.png'))
    enemy_png = pygame.image.load(path.join('sprites/space2.png'))
    bonus_png = pygame.image.load(path.join('sprites/diam.png'))
    bonus_dmg_png = pygame.image.load(path.join('sprites/diam_dmg.png'))
    bonus_speed_png = pygame.image.load(path.join('sprites/diam_speed.png'))
    bonus_hp_png = pygame.image.load(path.join('sprites/diam_hp.png'))
    pygame.mixer.music.load(path.join('sprites/STS.mp3'))
