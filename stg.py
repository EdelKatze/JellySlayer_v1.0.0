import copy
from conf import Config
from obj import Object
from ent import BossJelly, Jelly
from str import Portal, Platform


class Stage:
    def __init__(self, name, size, bg, bgms, floor, objs, stage_size, init_pos=None):
        self.name = name
        self.size = size
        self.bg = bg
        self.bgms = bgms
        self.floor = floor
        self.objs = objs
        self.obj_states = {state.name: state.state for state in self.objs}
        self.stage_size = stage_size

        self.objs.insert(0,
                         Object(
                             species="background",
                             name=self.bg,
                             img_name=self.bg,
                             size=self.size,
                             init_pos=init_pos if init_pos is not None else [0, Config.height - self.size[1]],
                         )
                         )

    @staticmethod
    def check_collide(obj):
        return obj[0].hitbox.box.colliderect(obj[1].hitbox.box)


stage_multiple = 1
stages = {
    "forest": Stage(
        name="forest_stage",
        size=[Config.width * stage_multiple * 1.7, Config.height * stage_multiple],  # 배경 이미지 크기
        stage_size=[3000, 900],  # 이동 가능한 스테이지 크기
        bg="forest_background",
        bgms={
            "general": "Forest",
            "low_mentality": "Forest_low_mentality",
            "boss": "Forest_boss_theme",
        },
        floor=None,
        objs=[
            Portal(
                name="portal",
                img_name="portal",
                size=Config.player_size,
                init_pos=[Config.width - Config.player_width + 1000, Config.height - Config.player_height],
            ),

        ],
    ),
}
