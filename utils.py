import pygame

import init
from colorsys import hsv_to_rgb


def hsv2rgb(h, s, v):
    return tuple(round(i * 255) for i in hsv_to_rgb(h, s, v))


def switch_music(mute: bool = None):

    if mute is not None:
        if mute:
            init.play_music = False
            pygame.mixer.music.pause()
        else:
            init.play_music = True
            pygame.mixer.music.unpause()
    else:
        if init.play_music:
            init.play_music = False
            pygame.mixer.music.pause()
        else:
            init.play_music = True
            pygame.mixer.music.unpause()

def read_code(path):
    result = ''
    with open(path, encoding='utf-8') as file:
        chars = file.readlines()
        for i in chars:
            try:
                result += chr(int(i, 16))
            except ValueError:
                pass
    return result

def encode_text(text: str):
    for i in text:
        print(hex(ord(i)))
