import pygame as pg
import time
import copy
from conf import Config

pg.init()


class Anime:
    def __init__(self, name, size,
                 runtime=Config.initial_animation_runtime,
                 fmc: int = Config.frame_multiple_constant,
                 offset_left=(0, 0), offset_right=(0, 0),
                 start_func=None,
                 middle_func=None,
                 end_func=None,
                 frame_func=None):

        self.name = name
        self.size = size
        self.runtime = runtime
        self.fmc = fmc
        self.offset = {
            "left": [offset_left[0] * Config.smc, offset_left[1] * Config.smc],
            "right": [offset_right[0] * Config.smc, offset_right[1] * Config.smc],
        }
        self.start_func = start_func
        self.middle_func = middle_func
        self.end_func = end_func
        self.frame_func = frame_func

        self.genre = Config.IMAGE.images[self.name][0].genre
        self.max_frame = Config.IMAGE.image_list[self.genre][self.name]
        self.current_frame = 0
        self.last_image_change_time = time.time()


class Animation:
    def __init__(self, obj, anime):
        self.obj = obj
        self.anime = anime
        self.offset = anime.offset
        self.size = anime.size

    def image_change(self, img_name, current_frame=0):
        self.obj.img_name = img_name
        self.obj.img = Config.IMAGE.images[self.obj.img_name][current_frame].image
        self.obj.img = pg.transform.scale(self.obj.img, self.anime.size).convert_alpha()

    def anime_change(self, given_anime, anime_force_change=False):
        if self.anime is None:
            self.anime = given_anime
            self.offset = given_anime.offset
            self.size = given_anime.size

        elif self.anime.name != given_anime.name:
            given_anime_prefer = Config.image_prefer[given_anime.name]
            current_anime_prefer = Config.image_prefer[self.anime.name]
            if given_anime_prefer >= current_anime_prefer or anime_force_change:
                self.anime = given_anime
                self.offset = given_anime.offset
                self.size = given_anime.size

    def animate(self):
        if self.anime is not None:
            max_frame = self.anime.max_frame * self.anime.fmc
            raw_frame = self.anime.current_frame
            current_frame = raw_frame // self.anime.fmc
            now = time.time()

            time_per_frame = self.anime.runtime / max_frame
            time_since_last_frame_change = now - self.anime.last_image_change_time

            if time_since_last_frame_change >= time_per_frame:
                if raw_frame == 0:
                    self.execute_start_func()
                if raw_frame < max_frame:
                    self.image_change(self.anime.name, current_frame)
                    self.anime.last_image_change_time = now
                    self.execute_frame_func()
                    if current_frame < self.anime.max_frame:
                        if self.anime.name == "player_light" and raw_frame == (current_frame + 1) * self.anime.fmc - 1:
                            self.execute_middle_func(current_frame)
                    self.anime.current_frame += 1
                elif raw_frame == max_frame:
                    self.execute_end_func()
                    self.anime = None

    def execute_start_func(self):
        if self.anime.start_func is not None:
            self.anime.start_func()

    def execute_middle_func(self, current_frame):
        middle_func = self.anime.middle_func
        if middle_func is not None and \
                current_frame < len(middle_func) and \
                callable(middle_func[current_frame]):
            middle_func[current_frame]()

    def execute_end_func(self):
        if self.anime.end_func is not None:
            self.anime.end_func()

    def execute_frame_func(self):
        if self.anime.frame_func is not None:
            self.anime.frame_func()


    def apply_offset(self, lr):
        if lr == 1:
            result = [self.obj.pos[0] - self.offset["right"][0],
                      self.obj.pos[1] - self.offset["right"][1]]
        else:
            result = [self.obj.pos[0] - self.offset["left"][0],
                      self.obj.pos[1] - self.offset["left"][1]]
        return result

    @staticmethod
    def get_anime(anime_name):
        return copy.deepcopy(animes[anime_name])


animes = {
    "player_idle": Anime(name="player_idle", size=Config.player_size),
    "player_run": Anime(name="player_run", size=Config.player_size),

    "portal": Anime(name="portal", size=Config.player_size),
    # "number_idle": Anime(name="number_idle", size=Config.player_size),
    # "number_run": Anime(name="number_run", size=Config.player_size),

    "jelly_idle": Anime(name="jelly_idle", size=Config.jelly_size),
    "jelly_run": Anime(name="jelly_run", size=Config.jelly_size),

    "boss_jelly_idle": Anime(name="boss_jelly_idle", size=Config.boss_jelly_size),
    "boss_jelly_skill1": Anime(name="boss_jelly_skill1", size=Config.boss_jelly_skill1_size, fmc=3),
    "boss_jelly_skill2": Anime(name="boss_jelly_skill2", size=Config.boss_jelly_skill2_size, fmc=3),
    "boss_jelly_run": Anime(name="boss_jelly_idle", size=Config.boss_jelly_skill2_size, fmc=3),
    "thunder": Anime(name="thunder", size=Config.thunder_size),
}
