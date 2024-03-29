import random
import json
from math import e
from ast import literal_eval
from datetime import timedelta


from init import *
from utils import hsv2rgb, switch_music, read_code
from pause import dead, pause
from entities import (Player,
                      Enemy,
                      BossEnemy,
                      Snaryad,
                      EnemySnaryad,
                      BounceEnemySnaryad,
                      BulletBonus,
                      DamageBonus,
                      SpeedBonus,
                      HealthBonus,
                      Shield,
                      Achievement,
                      )

was_bosslvl = False
current_text_list = []
current_text = 0
shieled_obj = None
nitemare_text = False
is_final = False
donts_defence = False
show_game_key = False
final_exit = False
sound_repeat = -1
achievement = None

GAME_KEY = read_code('resources/secret_key.txt')

texts = open('resources/text.json', encoding='utf-8')
text_data = json.load(texts)
texts.close()
boss_texts = text_data['data']['boss_texts']
donts_texts = text_data['data']['donts_texts']
final_texts = text_data['data']['final_texts']


def do_restart(igrok):
    global proigral, level, textsurface, textsurface_timer, score, bosslvl, is_final, bullets, enemy_bullets
    if not bosslvl or is_final:
        bosslvl = False
        is_final = False
        score = proigral = level = 0
        igrok.bullet_count = 1
        igrok.dmg = 1
        textsurface = textsurface_timer = emptytext
        igrok.speed = 1
        igrok.health = 100
        igrok.x = win_w / 2
        bullets.clear()
        enemy_bullets.clear()
        vragi.clear()


def spawn(chislo = None):
    global vragi, level, bosslvl
    if not bosslvl:
        for i in range(int(chislo)):
            vragi.append(Enemy(i, int(level * e)))
    else:
        vragi.append(BossEnemy())


def drawwindow(score):  # прорисовка графики
    global start_ticks, proigral, level, color, bosslvl, nitemare_text, sound_repeat, key_color, achievement, achievement_color
    textsurface_timer = text_score = textsurface = emptytext
    win.blit(bg, (0, 0))
    pygame.draw.rect(win, (0, 0, 0), (0, 0, win_w, 45))

    if color == 360:
        color = 0
    if key_color == 360:
        key_color = 0
    if achievement_color == 360:
        achievement_color = 0
    if nitemare_text:
        output_color = hsv2rgb(color / 100, 1, 1)
    else:
        output_color = (255, 255, 255)

    text_lvl = bigfont.render(f'level: {level}  score: {score}', False, output_color)
    health_text = bigfont.render(f'Health: {molodec.health}', False, (255, 0, 0) if not nitemare_text else output_color)
    bullet_count_text = bigfont.render(f'bullets: {molodec.bullet_count}', False,  (0, 0, 255) if not nitemare_text else output_color)
    dmg_text = bigfont.render(f'dmg:{molodec.dmg}', False, (255, 0, 180) if not nitemare_text else output_color)
    speed_text = bigfont.render(f'speed: {molodec.speed}', False, (0, 255, 0) if not nitemare_text else output_color)
    if not nitemare_text:
        text_name = bigfont.render(r"DDontS's Space Invaders", False, (255,0,255))
    else:
        text_name = bigfont.render(r"DDontS's Space Invaders", False, hsv2rgb(color / 100, 1, 1))
    color += 1
    key_color += 0.01
    achievement_color += 0.1

    if not len(vragi) and not proigral and not paused and not is_final:
        if not start_ticks and level:
            start_ticks = pygame.time.get_ticks()
        seconds = (pygame.time.get_ticks() - start_ticks) / 1000
        textsurface = bigfont.render(f'Wave comleted', False, (255, 255, 255))
        textsurface_timer = bigfont.render(f'Next wave in: {round(4 - seconds, 3)}', False, (255, 255, 255))
        if seconds > 4:
            level += 1
            bosslvl = True if level % 5 == 0 and level != 0 else False
            if not bosslvl and level < 5:
                spawn(17)
            start_ticks = 0
            textsurface = bigfont.render('', False, (255, 255, 255))
            textsurface_timer = bigfont.render('', False, (255, 255, 255))

    if not proigral:
        win.blit(molodec.player, (molodec.x, molodec.y))

    for item in vragi:
        if item.alive:
            if nitemare_text:
                hp_color = hsv2rgb(color / 100, 1, 1)
            else:
                hp_color = (255, 255, 255)
            item.text_hp = myfont.render(f'{item.health}', False, hp_color)
            item.text_hp_shadow = myfont_bigger.render(f'{item.health}', False, (0,0,0))
            pygame.draw.rect(win, (0, 0, 0), (item.x, item.y - 25, item.wight, 25))
            pygame.draw.rect(win, hsv2rgb((item.health * 100 / item.hhealth) / 333, 1, 1), (
                item.x + 3, item.y - 23, (item.wight - 5) - (item.wight - (item.wight * item.health) / item.hhealth),
                20))
            win.blit(item.sprite, (item.x, item.y))
            win.blit(item.text_hp_shadow, ((item.x + item.wight / 3), (item.y - 25)))
            win.blit(item.text_hp, ((item.x + item.wight / 3), (item.y - 25)))

    for bullet in bullets:
        if nitemare_text:
            pygame.draw.circle(win, hsv2rgb(achievement_color / 100, 1, 1), (bullet.x, bullet.y), bullet.radius)
        else:
            pygame.draw.circle(win, bullet.collor, (bullet.x, bullet.y), bullet.radius)

    for bullet in enemy_bullets:
        if nitemare_text:
            pygame.draw.circle(win, hsv2rgb(achievement_color / 100, 1, 1), (bullet.x, bullet.y),
                               bullet.radius)
        else:
            pygame.draw.circle(win, bullet.collor, (bullet.x, bullet.y),
                               bullet.radius)

    try:
        if achievement:
            pygame.draw.rect(win, (100, 100, 100),  (achievement.x-achievement.wight, achievement.y, achievement.wight, achievement.height))
            if is_final:
                achievement_text_color = hsv2rgb(achievement_color / 100, 1, 1)
            else:
                achievement_text_color = (255, 255, 255)
            achievement_text = bigfont.render(achievement.text, False,
                          achievement_text_color)
            win.blit(achievement_text, (achievement.x-achievement.wight, achievement.y))
    except:
        pass

    if len(bonusi):
        for item in bonusi:
            if item.alive:
                win.blit(item.sprite, (item.x, item.y))
                item.move(molodec)

    if shieled_obj:
        win.blit(shieled_obj.sprite, (shieled_obj.x, shieled_obj.y))

    if proigral:
        dead(score)
        do_restart(molodec)
    elif not proigral and len(vragi):
        textsurface = bigfont.render('', False, (255, 255, 255))
    win.blit(textsurface, (win_w / 2, 300))
    win.blit(textsurface_timer, (win_w / 2, 350))
    win.blit(text_lvl, (5, 0))
    win.blit(health_text, (270, 0))
    win.blit(bullet_count_text, (470, 0))
    win.blit(dmg_text, (660, 0))
    win.blit(speed_text, (820, 0))
    win.blit(text_score, (160, 0))
    win.blit(text_name, (win_w - 370, 0))

    if current_text_list and show_text_box and current_text < len(current_text_list):
        pygame.draw.rect(win, (50, 50, 50),
                         (40, win_h - 250, win_w-80, 200))
        sayer_name = bigfont.render(f'{current_text_list[current_text]["sayer"]}', False,
                       literal_eval(current_text_list[current_text]['speaker_color']))
        boss_text = bigfont.render(f'{current_text_list[current_text]["text"]}', False,
                       literal_eval(current_text_list[current_text]["text_color"]))
        about_text = myfont.render(f'Пробел для продолжения', False, (255, 255, 255))
        win.blit(about_text, (1000, win_h - 80))
        win.blit(sayer_name, (50, win_h - 240))
        win.blit(boss_text, (50, win_h - 200))

    if show_game_key:
        pygame.draw.rect(win, (50, 50, 50),(40, win_h - 450, win_w - 80, 200))
        help_text = myfont.render(f'Нажми {5-final_exit} раз пробел, чтобы выйти', False, (255, 255, 255))
        key_text = giantfont.render(f'{GAME_KEY}', False, hsv2rgb(key_color / 100, 1, 1))
        win.blit(key_text, (120, win_h - 440))
        win.blit(help_text, (1000, win_h - 280))

    pygame.display.update()


def boss_level():
    global paused, show_text_box, current_text, current_text_list, nitemare_text
    nitemare_text = True
    show_text_box = True
    current_text_list = boss_texts

    if current_text < len(current_text_list):
        paused = True
        switch_music(mute=True)

    if current_text >= len(current_text_list) and paused:
        show_text_box = False
        paused = False
        switch_music(mute=False)
        pygame.mixer.music.unload()
        pygame.mixer.music.load(path.join('resources/loop.mp3'))
        pygame.mixer.music.play(-1)


def defence_from_boss():
    global paused, show_text_box, current_text, current_text_list, donts_defence
    show_text_box = True
    donts_defence = True
    current_text_list = donts_texts

    if current_text < len(current_text_list):
        paused = True


def final_level():
    global paused, show_text_box, current_text, current_text_list
    show_text_box = True
    paused = True
    current_text_list = final_texts

    if current_text <= len(current_text_list) and paused:
        pygame.mixer.music.unload()
        pygame.mixer.music.load(path.join('resources/buddy.mp3'))
        pygame.mixer.music.play(-1)

achievement_created = False
if __name__ == "__main__":
    pygame.mouse.set_visible(False)
    pause()
    molodec = Player()
    if play_music:
        pygame.mixer.music.play(-1)
    spawn(17)
    while run:
        bosslvl = True if level % 5 == 0 and level != 0 else False
        keys = pygame.key.get_pressed()
        if not paused:
            if len(vragi) == 0 and not achievement_created:
                if not bosslvl:
                    achievement_created = True
                    achievement = Achievement(win_w, win_h,
                                              f'Пройти уровень {level}!')
                else:
                    achievement_created = True
                    achievement = Achievement(win_w, win_h,
                                              f'Пройти игру! И быть солнышком)', 20)
            try:
                if achievement and achievement.is_alive:
                    achievement.move(win_h)
                else:
                    if not is_final:
                        achievement_created = False
                        del achievement
            except:
                pass
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
                                    bonusi.append(BulletBonus(item.x, item.y))
                                elif random.randint(0, 10) == random.randint(0, 10):
                                    bonusi.append(DamageBonus(item.x, item.y))
                                elif bosslvl:
                                    bonusi.append(DamageBonus(item.x, item.y))
                                elif random.randint(0, 5) == random.randint(0, 5):
                                    bonusi.append(HealthBonus(item.x, item.y))
                                elif random.randint(0, 20) == random.randint(0, 20) and molodec.speed <= 2:
                                    bonusi.append(SpeedBonus(item.x, item.y))
                            if bullet in bullets:
                                bullets.pop(bullets.index(bullet))
                elif bullet in bullets:
                    bullets.pop(bullets.index(bullet))
            for enemy_bullet in enemy_bullets:
                enemy_bullet.live()
                if molodec.x < enemy_bullet.x < (molodec.x + molodec.wight) \
                        and molodec.y < enemy_bullet.y < (molodec.y + molodec.height):
                    if shieled_obj:
                        pass
                    elif not bosslvl:
                        molodec.health -= 1
                    elif bosslvl:
                        molodec.health -= 7
                    enemy_bullets.pop(enemy_bullets.index(enemy_bullet))
                if enemy_bullet.y > win_h:
                    enemy_bullets.pop(enemy_bullets.index(enemy_bullet))
            if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and molodec.x > 5:
                molodec.move('left')
                if shieled_obj:
                    shieled_obj.move('left')
            elif (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and molodec.x < win_w - molodec.wight - 5:
                molodec.move('right')
                if shieled_obj:
                    shieled_obj.move('right')

            for item in vragi:
                item.move()

            if keys[pygame.K_e] and not proigral:
                now = datetime.datetime.now()
                two_secs_ago = now - timedelta(seconds=0.75 / molodec.bullet_count)
                if last_shot_time > two_secs_ago:
                    pass
                else:
                    last_shot_time = datetime.datetime.now()
                    bullets.append(Snaryad((molodec.x + molodec.wight // 2), molodec.y, donts_defence))
            for vrag in vragi:
                if (not bosslvl
                        and len(vragi) != 0
                        and random.randint(0, 40) == random.randint(0, 35)
                        and len(enemy_bullets) < 10):
                    enemy_bullets.append(EnemySnaryad(vrag.x + vrag.wight//2, vrag.y + 53))
                if bosslvl:
                    boss_now = datetime.datetime.now()
                    boss_two_secs_ago = boss_now - timedelta(seconds=0.2)
                    if boss_last_shot_time > boss_two_secs_ago:
                        pass
                    else:
                        boss_last_shot_time = datetime.datetime.now()
                        enemy_bullets.append(BounceEnemySnaryad(vrag.x + vrag.wight//2, vrag.y + 53, 'left'))
                        enemy_bullets.append(EnemySnaryad(vrag.x + vrag.wight//2, vrag.y + 53))
                        enemy_bullets.append(BounceEnemySnaryad(vrag.x+ vrag.wight//2, vrag.y + 53, 'right'))

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    do_restart(molodec)
                elif event.key == pygame.K_ESCAPE:
                    pygame.mixer.pause()
                    pause()
                elif event.key == pygame.K_EQUALS:
                    level += 1
                elif event.key == pygame.K_m:
                    switch_music()
                if bosslvl and event.key == pygame.K_SPACE:
                    current_text += 1
                if show_game_key:
                    if event.key == pygame.K_SPACE:
                        final_exit += 1
                    if final_exit >= 5:
                        run = False
            elif event.type == pygame.WINDOWCLOSE:
                run = False
        for item in vragi:
            if molodec.health <= 0 and not bosslvl:
                vragi.clear()
                bullets.clear()
                enemy_bullets.clear()
                proigral = True

        if bosslvl:
            if not was_bosslvl:
                boss_level()
                if len(vragi) < 1:
                    spawn()

            if molodec.health < 1:
                was_bosslvl = True
                current_text = 0
                molodec.health = 1
                defence_from_boss()

        if donts_defence:
            if current_text == 5:
                nitemare_text = False
            if current_text == 8:
                molodec.health = 1000
                molodec.bullet_count = 100
                molodec.dmg = 10000
                molodec.speed = 2
            if current_text == 13:
                shieled_obj = Shield(molodec)
                shieled_obj.speed = 2


        if donts_defence and not vragi and not is_final:
            is_final = True
            current_text = 0

            final_level()

        if current_text >= len(current_text_list):
            show_text_box = False
            paused = False

            if is_final:
                show_game_key = True

        drawwindow(score)

    pygame.quit()
    sys.exit()


#  pyinstaller mygame.spec