import pygame as pg

pg.init()


class Sound:
    def __init__(self, genre, sound_name):
        self.genre = genre
        self.sound = pg.mixer.Sound(f'./src/sounds/{genre}/{sound_name}.wav')


class Sounds:
    def __init__(self):
        self.sound_list = {
            "effect": [
                "Attacked",
                "Enemy_death",
                "Jump",
                "Portal_movement",
                "Walking",
                "@",
            ],
            "background": [
                "Forest",
                "JellyPy",
                "JellyPy_loop",
                "@",
            ],
            "system": [
                "Alarm",
                "Selecting_complete",
                "Selecting",
                "@",
            ],
        }


        self.sounds = {}

        for (genre, sounds) in self.sound_list.items():
            for sound_name in sounds:
                self.sounds[sound_name] = Sound(genre, sound_name)

        self.background_is_playing = {sound_name: False for sound_name in self.sound_list["background"]}

    def sound_play(self, sound_name, loops: int = 0, maxtime: int = 0, fade_ms: int = 0):
        try:
            self.sounds[sound_name].sound.play(loops=loops, maxtime=maxtime, fade_ms=fade_ms)
        except:
            self.sounds["@"].sound.play(loops=loops, maxtime=maxtime, fade_ms=fade_ms)
        if loops == -1:
            self.background_is_playing[sound_name] = True

    def sound_stop(self, sound_name):
        self.sounds[sound_name].sound.stop()
        self.background_is_playing[sound_name] = False
