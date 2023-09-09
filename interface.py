import pygame
import pygame_menu
from typing import Callable
from game import Game

pygame.init()

surface = pygame.display.set_mode((1600, 900))


def add_button(menu, title, function: Callable):
    """

    :type function: Function
    """
    menu.add.button(title, function).set_font("./src/fonts/joystix monospace.otf", 30, "GRAY", "WHITE", "GRAY", "GRAY",
                                              [40, 41, 35])
    # 'font_size', 'color', 'selected_color', 'readonly_color', 'readonly_selected_color', and 'background_color'
    return menu


def start_the_game():
    # Do the job here !
    pygame_menu.events.EXIT
    Game.main()


# Create a custom theme
my_theme = pygame_menu.themes.THEME_DARK.copy()
my_theme.title = False  # Hide the menu title
myimage = pygame_menu.baseimage.BaseImage(
    image_path="./src/images/stage/background.png",
    drawing_mode=pygame_menu.baseimage.IMAGE_MODE_FILL,
    drawing_offset=(0, 0)
)
my_theme.background_color = myimage
menu = pygame_menu.Menu(
    height=900,  # Use full-screen
    theme=my_theme,
    title='',
    center_content=False,
    width=1600
)

menu.add.button("Play", start_the_game).set_font("./src/fonts/joystix monospace.otf", 60, "GRAY", "WHITE", "GRAY",
                                                 "GRAY", None).translate(-650, 400)
menu.add.button("Quit", pygame_menu.events.EXIT).set_font("./src/fonts/joystix monospace.otf", 60, "GRAY", "WHITE",
                                                          "GRAY", "GRAY", None).translate(-650, 420)

menu.mainloop(surface)
