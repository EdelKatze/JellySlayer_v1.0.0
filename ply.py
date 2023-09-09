import pygame as pg
import time
from math import floor
from conf import Config
from ent import Entity
from ani import Animation

pg.init()


class Player(Entity):
    def __init__(self, img_name, size: list, init_pos: list = None):
        super().__init__("player", "player", img_name, size, init_pos)
        self.max_ap = 100
        self.anima_point = self.max_ap
        self.regen_count = 4
        self.walking_time = 0
        self.walk_speed = 12

        self.attack_damage = 20
        self.lighting_damage = self.attack_damage * 4
        self.is_lighting = False
        self.lighting_cooltime = 0
        self.can_lighting = True

        self.font = pg.font.Font("./src/fonts/joystix monospace.otf", 40)
        self.text = self.font.render(str(), True, (255, 255, 255))

        self.middle_const = self.walk_speed * (800 // self.walk_speed)
    def set_ap(self, mp):
        self.anima_point = mp

    def get_ap(self):
        return self.anima_point

    def plus_ap(self, n: int = 0):
        if not self.is_damage_immune:
            self.set_ap(self.anima_point + n)

    def multiple_ap(self, n: int = 1):
        if not self.is_damage_immune:
            self.set_ap(floor(self.anima_point * n))

    def movement(self):
        if self.can_moving:
            if self.going_direction[0] or self.going_direction[1]:
                self.is_moving = True
                current_time = time.time()

                if current_time - self.walking_time >= 6.6 / self.walk_speed and self.is_on_ground:
                    Config.SOUND.sound_play("Walking")
                    self.walking_time = time.time()
                self.animation.anime_change(Animation.get_anime("player_run"))

                if self.going_direction[0]:
                    self.pos[0] -= self.walk_speed  # Move left

                if self.going_direction[1]:
                    self.pos[0] += self.walk_speed  # Move right

                self.is_idle = False
            else:
                if not self.is_idle:
                    self.animation.current_frame = 0
                    self.is_idle = True
                self.animation.anime_change(Animation.get_anime("player_idle"))
            if self.vertical_speed != 0:
                Config.SOUND.sound_stop("Walking")
            self.rotate()

    def jump(self):
        if self.is_jumping:
            self.is_on_ground = False
            if self.jump_count == self.jump_time:
                # pass
                Config.SOUND.sound_play("Jump")

            if self.jump_count >= -self.jump_time:
                # self.animation.anime_change(Anime(name="player_jump", size=Config.player_size))
                neg = 1
                if self.jump_count < 0:
                    # self.animation.anime_change(Anime(name="player_down", size=Config.player_size))
                    neg = -1
                self.pos[1] -= (self.jump_count ** 2) * neg * self.jump_height_const
                self.stage_pos[1] = self.pos[1]
                # print(self.jump_time_const / self.jump_height_const)
                self.jump_count -= 1
            else:
                self.is_jumping = False
                self.jump_count = self.jump_time
                self.is_on_ground = True

    def light(self):
        if self.is_on_ground:
            self.can_moving = False
            self.is_lighting = True
            self.animation.anime_change(Animation.get_anime("player_light"))

    def manage_dmg(self, taken_dmg=None, screen = None):
        regenerated = False

        # print(taken_dmg, ', ', self.hit_count)
        if taken_dmg is not None:
            if taken_dmg != 0 and self.hit_count <= 0:
                self.hit_count = 50
                self.is_damage_immune = True
                if self.protect_point != 0:
                    self.protect_point -= taken_dmg
                    Config.SOUND.sound_play("Attacked")
                    # print(self.protect_point)
                    if self.protect_point < 0:
                        taken_dmg = abs(self.protect_point)
                        self.protect_point = 0

                if self.protect_point == 0 and self.anima_point:
                    self.anima_point -= taken_dmg

                if self.protect_point == 0 and self.anima_point <= 0:
                    return 0

        if self.hit_count > 0:
            self.hit_count -= 1
            if self.recent_damage is None:
                self.recent_damage = taken_dmg
            if self.recent_damage is not None:
                if self.font is None:

                    self.font = pg.font.Font("./src/fonts/joystix monospace.otf", 40)
                self.text = self.font.render(str(self.recent_damage), True, (255, 255, 255)).convert_alpha()
                # print(self.recent_damage)

                if screen is not None:
                    # print("W")
                    screen.blit(self.text, (self.pos[0] + self.size[0] / 3,
                                            self.pos[1] - self.hit_count_constant ** 2 /
                                            (self.hit_count + self.hit_count_constant)
                                            + self.hit_count_constant / 2))
            # print(self.recent_damage)
        if self.hit_count <= 0:
            self.is_damage_immune = False

        if self.regen_count > 0:
            self.regen_count -= 1
        # print(self.regen_count, ', ', self.protect_point, ', ', self.anima_point)
        if self.regen_count <= 0:

            self.regen_count = 50

            if self.anima_point < self.max_ap:
                self.anima_point += 4

                if self.anima_point > self.max_ap:
                    self.protect_point += self.anima_point - self.max_ap
                    self.anima_point = self.max_ap
                    regenerated = True

            if self.protect_point > self.max_pp:
                self.protect_point = self.max_pp
            if self.anima_point == self.max_ap:
                if self.protect_point <= self.max_pp and not regenerated:
                    self.protect_point += 4

                if self.protect_point > self.max_pp:
                    self.protect_point = self.max_pp

        if self.anima_point <= 0:
            self.anima_point = 0

    def skill_count(self):
        try:
            if self.is_lighting:
                self.lighting_cooltime = 120
            elif not self.is_lighting and self.can_lighting:
                self.lighting_cooltime = 0
            self.lighting_cooltime -= 1

            if self.lighting_cooltime > 0:
                # print("s")
                self.can_lighting = False
            elif self.lighting_cooltime <= 0:
                self.can_lighting = True
        except:
            # print('x')
            self.can_lighting = True

    def knock_back(self, player_stage_pos: list, is_hit: bool, direction):

        if is_hit and not self.is_damage_immune:
            # print("workin again")
            if not direction:  # 왼쪽에 있을떄
                self.horizontal_speed = 15
                self.vertical_speed = -12
            else:
                self.horizontal_speed = -15
                self.vertical_speed = -12

        if self.horizontal_speed > 0:
            self.horizontal_speed -= 1
        if self.horizontal_speed < 0:
            self.horizontal_speed += 1

        self.stage_pos[0] -= self.horizontal_speed
        self.pos[0] -= self.horizontal_speed

        # print(self.horizontal_speed)
