import copy
import math
import random

from conf import Config
from typing import Callable
from obj import jelly_state
from ani import Animation


class JellyBoss:
    def __init__(self, boss, player, stage_objects: list, obj_states: list, count: int, jelly: Callable,
                 remote_electro: Callable, around_electro: Callable, tentacle: Callable):
        self.boss = boss
        self.player = player
        self.stage_objects = stage_objects
        self.obj_states = obj_states
        self.count = count
        self.jelly = jelly
        self.remote_electro = remote_electro
        self.around_electro = around_electro
        self.tentacle = tentacle
        self.sleep = 0
        self.is_sleep = False

        self.noticed = False
        self.count = 10
        self.sleep = 100
        self.is_sleep = True
        self.noticed = False
        self.direction = False
        self.det_count = 0

        self.spawn_jelly = None
        self.spawn_tentacle = None
        self.spawn_remote_electro = None

        self.will_use_skill = False

    def jelly_spawn(self):

        if self.will_use_skill:
            self.spawn_jelly.pos[0] = self.spawn_jelly.stage_pos[0] - self.player.stage_pos[
                0] + self.player.middle_const
            print(self.player.stage_pos, self.spawn_jelly.stage_pos)
            print(self.player.pos, self.spawn_jelly.pos)

            self.stage_objects.append(self.spawn_jelly)
            self.obj_states[self.spawn_jelly.name] = jelly_state
            self.will_use_skill = False

            # 평소대로

        else:
            self.spawn_jelly = self.jelly("jelly"f'{self.count}',
                                          Config.jelly_size,
                                          [copy.deepcopy(self.player.pos[0]), self.player.pos[1] + 500])
            self.spawn_jelly.stage_pos[0] = float(self.player.stage_pos[0])

            self.will_use_skill = True

            self.count += 1
            self.animation.anime_change(Animation.get_anime("boss_jelly_skill1"))

    def dash(self):
        if self.will_use_skill:
            self.will_use_skill = False
            pass
        else:
            self.will_use_skill = True

    def electric_around_attack(self):
        if self.will_use_skill:
            electro = self.around_electro("electro"f'{self.count}',
                                          Config.around_electro_size,
                                          [self.boss.pos[0], Config.around_electro_size[0]])
            electro.stage_pos[0] = self.player.stage_pos[0]
            self.stage_objects.append(electro)
            self.obj_states[electro.name] = jelly_state

            self.count += 1
            self.will_use_skill = False
        else:
            self.will_use_skill = True

    def electric_remote_attack(self):

        if self.will_use_skill:
            self.stage_objects.append(self.spawn_remote_electro)
            self.obj_states[self.spawn_remote_electro.name] = jelly_state
            self.will_use_skill = False
        else:
            self.will_use_skill = True
            self.spawn_remote_electro = self.remote_electro("electro"f'{self.count}',
                                                            Config.remote_electro_size,
                                                            [copy.deepcopy(self.player.pos[0]),
                                                             Config.remote_electro_size[1]])
            self.spawn_remote_electro.stage_pos[0] = float(self.player.stage_pos[0])

            self.count += 1

    def tentacle_attack(self):

        if self.will_use_skill:
            self.stage_objects.append(self.spawn_tentacle)
            self.obj_states[self.spawn_tentacle.name] = jelly_state
            self.will_use_skill = False

        else:
            self.spawn_tentacle = self.tentacle("tentacle"f'{self.count}',
                                                Config.tentacle_size,
                                                [copy.deepcopy(self.player.pos[0]), Config.tentacle_size[1]])
            self.spawn_tentacle.stage_pos[0] = self.player.stage_pos[0]
            self.will_use_skill = True
            self.count += 1

    def determinate(self, ply_pos: list, stg_pos: list):
        if self.det_count <= 0:

            x1 = ply_pos[0]
            x2 = stg_pos[0] + self.boss.size[0] / 2
            y1 = ply_pos[1]
            y2 = stg_pos[1]
            dist = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

            if dist < 1200:
                self.noticed = True

            else:
                self.noticed = False

            self.det_count = 60
        else:
            self.det_count -= 1

    def moving(self, ply_pos: list, stg_pos: list):
        x1 = ply_pos[0]
        x2 = stg_pos[0] + self.boss.size[0] / 2
        y1 = ply_pos[1]
        y2 = stg_pos[1]
        if not self.noticed:

            if self.sleep > 0:
                # print("qw")

                self.sleep -= 1
                self.is_sleep = True

            elif self.sleep <= 0 and self.count > 0:
                self.count -= 1
                self.is_sleep = False

            elif self.sleep <= 0 and self.count <= 0:
                self.direction = random.randrange(0, 1) == 0
                self.is_sleep = False
                self.count = random.randrange(10, 60)
                self.sleep = random.randrange(60, 200)

        else:
            return x2 - x1 <= 0
