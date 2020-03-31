import pygame
import pygameMenu
from init import win, win_h, win_w
volume = 100


def pause():
    COLOR_BLACK = (0, 0, 0)
    COLOR_WHITE = (255, 255, 255)
    MENU_BACKGROUND_COLOR = (123, 160, 91)
    WINDOW_SIZE = (win_w, win_h)
    def Pass():
        pass
    font1 = 'sprites/bebas.ttf'
    font2 = 'sprites/8bit.ttf'
    about_menu = pygameMenu.TextMenu(surface=win, bgfun=Pass,
                                     color_selected=COLOR_WHITE,
                                     font=font1,
                                     font_color=COLOR_BLACK,
                                     font_size_title=30,
                                     font_title=font2,
                                     menu_color=MENU_BACKGROUND_COLOR,
                                     menu_color_title=COLOR_WHITE,
                                     menu_height=int(WINDOW_SIZE[1] * 0.5),
                                     menu_width=int(WINDOW_SIZE[0] * 0.3),
                                     onclose=pygameMenu.events.DISABLE_CLOSE,
                                     option_shadow=False,
                                     text_color=COLOR_BLACK,
                                     text_fontsize=20,
                                     title='ABOUT',
                                     window_height=WINDOW_SIZE[1],
                                     window_width=WINDOW_SIZE[0],
                                     mouse_enabled=False,
                                     mouse_visible=False
                                     )

    about_menu.add_line(f'Space        Invader')
    about_menu.add_line(r'© 2020\\ Donts_')
    about_menu.add_line(pygameMenu.locals.TEXT_NEWLINE)
    about_menu.add_option('Return to menu', pygameMenu.events.BACK)
    main_menu = pygameMenu.Menu(surface=win, bgfun=Pass,
                                color_selected=COLOR_WHITE,
                                font=font1,
                                font_color=COLOR_BLACK,
                                font_size=30,
                                menu_alpha=50,
                                font_title=font1,
                                menu_color=MENU_BACKGROUND_COLOR,
                                menu_height=int(WINDOW_SIZE[1] * 0.5),
                                menu_width=int(WINDOW_SIZE[0] * 0.3),
                                onclose=pygameMenu.events.DISABLE_CLOSE,
                                option_shadow=False,
                                title='MAIN MENU',
                                window_height=WINDOW_SIZE[1],
                                window_width=WINDOW_SIZE[0],
                                mouse_enabled=False,
                                mouse_visible=False
                                )

    def music_selector(_, value):
        global volume
        volume = value
        pygame.mixer.music.set_volume(volume/100)

    help_menu = pygameMenu.TextMenu(surface=win, bgfun=Pass,
                                    color_selected=COLOR_WHITE,
                                    font=font1,
                                    font_color=COLOR_BLACK,
                                    font_size_title=30,
                                    font_title=font2,
                                    menu_color=MENU_BACKGROUND_COLOR,
                                    menu_color_title=COLOR_WHITE,
                                    menu_height=int(WINDOW_SIZE[1] * 0.5),
                                    menu_width=int(WINDOW_SIZE[0] * 0.3),
                                    onclose=pygameMenu.events.DISABLE_CLOSE,
                                    option_shadow=False,
                                    text_color=COLOR_BLACK,
                                    text_fontsize=20,
                                    title='HELP',
                                    window_height=WINDOW_SIZE[1],
                                    window_width=WINDOW_SIZE[0],
                                    mouse_enabled=False,
                                    mouse_visible=False
                                    )
    help_menu.add_line("[A]+[D]  or  [Arrows]  to  walk")
    help_menu.add_line("[E]  to  fire")

    help_menu.add_option('Return to menu', pygameMenu.events.BACK)
    main_menu.add_option('Play', main_menu.disable)
    main_menu.add_selector("Music: ", [(str(x), x) for x in range(0, 101, 10)], default=volume//10, onchange=music_selector)
    main_menu.add_option('Help', help_menu)
    main_menu.add_option('About', about_menu)
    main_menu.add_option('Quit', pygameMenu.events.EXIT)
    main_menu.mainloop(pygame.event.get())
