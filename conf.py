from pygame import display
from sfx import Sounds
from img import Images


class Config:
    width, height = 1600, 900  # 창 크기
    screen = display.set_mode((width, height))
    fps = 60

    SOUND = Sounds()
    IMAGE = Images()

    frame_multiple_constant = 10
    initial_animation_runtime = 1 / frame_multiple_constant

    smc = 6  # size_multiple_constant

    player_width = 20 * smc
    player_height = 30 * smc
    player_size = [player_width, player_height]
    player_attack = [44 * smc, 40 * smc]
    player_light = [70 * smc, 29 * smc]

    light_length = 70 * smc
    light_size = [light_length, 29 * smc]

    jelly_size = [47 * smc // 2, 39 * smc // 2]
    boss_jelly_size = [274 * smc // 2, 154 * smc // 2]
    boss_jelly_skill1_size = boss_jelly_size  # [304 * smc // 2, 171 * smc // 2]
    boss_jelly_skill2_size = boss_jelly_size  # [309 * smc // 2, 223 * smc // 2]
    tentacle_size = [30 * smc, 150 * smc]
    thunder_size = [84 * smc, 100 * smc]
    remote_electro_size = [22 * smc, 40 * smc]

    platform_size = [22 * smc, 12 * smc]

    bar_size = [65 * smc, 7 * smc]

    around_electro_size = [70 * smc, 150 * smc]



    image_prefer = {
        "player_idle": 1,
        "player_run": 1,
        "player_attack": 2,
        "player_light": 3,

        "portal": 1,

        "background": 0,
        "Forest_floating_platform": 0,

        "boss_jelly_idle": 1,
        "boss_jelly_skill1": 2,
        "boss_jelly_skill2": 3,

        "jelly_idle": 1,
        "jelly_run": 1,
    }

    anime_lists = {
        "player": [
            "player_idle",
            "player_run",
            "player_attack",
            "player_light",
        ],

        "enemy": {
            "jelly_idle",
            "jelly_run",

            "boss_jelly_idle",
            "boss_jelly_skill1",
            "boss_jelly_skill2"
        },

        "structure": [
            "portal",
        ]
    }
