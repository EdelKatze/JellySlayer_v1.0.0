import pygame as pg

pg.init()


class Image:
    def __init__(self, genre, img_name, img_index=None):
        self.genre = genre
        self.image = None
        if img_index is None:
            self.image = pg.image.load(f'./src/images/{genre}/{img_name}.png').convert_alpha()
        else:
            self.image = pg.image.load(f'./src/images/{genre}/{img_name}{img_index}.png').convert_alpha()


class Images:
    def __init__(self):
        self.image_list = {
            "player": {
                "player_idle": 4,
                "player_run": 4,
                "player_attack": 6,
                "player_light": 3,
                "@": 1
            },
            "entity": {
                "jelly_idle": 1,
                "jelly_run": 1,

                "boss_jelly_idle": 2,
                "boss_jelly_skill1": 11,
                "boss_jelly_skill2": 3,
                "thunder": 5,

                "empty_bar": 1,
                "health": 1,
                "mentality": 1,

                "@": 1,
            },
            "stage": {
                "portal": 3,
                "title": 1,
                "forest_background": 1,
                "forest_platform": 1,
                "@": 1,
            },
        }

        self.images = {}

        for (genre, images) in self.image_list.items():
            for (img_name, max_frames) in images.items():
                if max_frames == 1:
                    self.images[img_name] = [Image(genre, img_name)]
                else:
                    self.images[img_name] = [Image(genre, img_name, i) for i in range(max_frames)]

        for i in self.images:
            print(i)
