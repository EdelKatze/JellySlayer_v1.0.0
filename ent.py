import random
from typing import Callable

import pygame as pg
from math import floor
from conf import Config
from obj import Object
from ani import Animation
from AI import AI
from BossAI import JellyBoss


class Entity(Object):
    def __init__(self, species, name, img_name, size: list, init_pos: list = None, state=None):
        super().__init__(species, name, img_name, size, init_pos, True, state if state is not None else "structure")
        self.text = None
        self.font = None
        self.anime_list = Config.anime_lists[self.species]

        self.jump_height_const = 0.3
        self.jump_time_const = 0.7
        self.jump_time = self.jump_time_const * 20
        self.is_jumping = False
        self.jump_count = self.jump_time
        self.is_on_ground = True
        self.vertical_speed = 0

        self.direction = True  # False is left, True is right
        self.going_direction = [False, False]  # [0] is left, [1] is right
        self.is_moving = False
        self.is_idle = True
        self.walk_speed = 6
        self.can_moving = True

        self.is_attacking = False
        self.attack_damage = 0

        self.max_pp = 100
        self.hit_count_constant = 120
        self.protect_point = self.max_pp

        self.hit_count = 0
        self.is_damage_immune = False
        self.is_hit = False

        self.AI = AI()

        self.recent_damage = None
        self.check_falling = False
        self.horizontal_speed = 0
        self.font = pg.font.Font("./src/fonts/joystix monospace.otf", 40)

    def set_protect_point(self, protect_point):
        self.protect_point = protect_point

    def get_protect_point(self):
        return self.protect_point

    def plus_protect_point(self, n: int = 0):
        if not self.is_damage_immune:
            self.set_protect_point(self.protect_point + n)

    def multiple_protect_point(self, n: int = 1):
        if not self.is_damage_immune:
            self.set_protect_point(floor(self.protect_point * n))

    def manage_dmg(self, taken_dmg=None, screen=None):
        if taken_dmg is not None:
            if taken_dmg != 0 and self.hit_count <= 0:
                self.hit_count = self.hit_count_constant
                self.is_damage_immune = True
                if self.protect_point != 0:
                    self.protect_point -= taken_dmg
                    if self.protect_point < 0:
                        self.protect_point = 0

        if self.hit_count > 0:
            self.hit_count -= 1
            if self.recent_damage is None and taken_dmg is not None:
                self.recent_damage = taken_dmg
            if self.recent_damage is not None:
                if self.font is None:
                    self.font = pg.font.Font("./src/fonts/joystix monospace.otf", 40)

                self.text = self.font.render(str(self.recent_damage), True, (255, 255, 255)).convert_alpha()

                if screen is not None:
                    # print("W")
                    screen.blit(self.text, (self.pos[0] + self.size[0] / 3,
                                            self.pos[1] - self.hit_count_constant ** 2 /
                                            (self.hit_count + self.hit_count_constant)
                                            + self.hit_count_constant / 2))

        if self.hit_count <= 0:
            self.is_damage_immune = False
            self.recent_damage = None
        if self.protect_point > self.max_pp:
            self.protect_point = self.max_pp

    def movement(self):
        if (self.going_direction[0] or self.going_direction[1]) and self.can_moving:
            self.is_moving = True
            self.animation.anime_change(Animation.get_anime(f'{"_".join(self.img_name.split("_")[:-1])}_run'))

            if self.going_direction[0]:
                self.pos[0] -= self.walk_speed  # Move left
                self.stage_pos[0] -= self.walk_speed

            if self.going_direction[1]:
                self.pos[0] += self.walk_speed  # Move right
                self.stage_pos[0] += self.walk_speed

            self.is_idle = False
            self.rotate()
        else:
            if not self.is_idle:
                self.animation.current_frame = 0
                self.is_idle = True
            self.animation.anime_change(Animation.get_anime(f'{"_".join(self.img_name.split("_")[:-1])}_idle'))

    def rotate(self, force_change=False):
        direction_is_different = self.direction is True and self.going_direction[0] or \
                                 self.direction is False and self.going_direction[1]
        if direction_is_different or force_change:
            self.direction = not self.direction
            for anime in self.anime_list:
                for i in range(Config.IMAGE.image_list[self.animation.anime.genre][anime]):
                    Config.IMAGE.images[anime][i].image = pg.transform.flip(Config.IMAGE.images[anime][i].image, True, False)

    def update(self):
        self.hitbox.set_hitbox()
        self.animation.animate()
        pg.draw.rect(Config.screen, (255, 0, 0), self.hitbox.box, 2)
        if self.direction:
            Config.screen.blit(self.img, self.animation.apply_offset(1))
            pg.draw.rect(Config.screen, (255, 0, 0), self.img.get_rect(topleft=self.animation.apply_offset(1)), 2)
        else:
            Config.screen.blit(self.img, self.animation.apply_offset(0))
            pg.draw.rect(Config.screen, (255, 0, 0), self.img.get_rect(topleft=self.animation.apply_offset(0)), 2)

    def jumping(self):
        if self.vertical_speed == 0:
            Config.SOUND.sound_play("Jump")
            self.vertical_speed = -(self.jump_count * self.jump_height_const) ** 2

    def falling(self, objects: list, count: int, objects_states: list):
        if self.name == "player":
            pass

        self.check_falling = False
        if self.stage_pos[1] >= Config.height - self.size[1] and self.vertical_speed >= 0:
            self.stage_pos[1] = Config.height - self.size[1]
            self.pos[1] = Config.height - self.size[1]
            self.vertical_speed = 0
            self.check_falling = True

        else:
            for i in range(len(objects) - count):
                if objects[count + i].name == "test":
                    pass

                if ((objects[count + i] is not self) and
                        self.hitbox.box.colliderect(objects[count + i].hitbox.box)):  # 충돌시
                    if (objects_states[objects[count + i].name].can_step
                            and not objects_states[self.name].can_step
                            and self.stage_pos[1] + self.size[1] >= objects[count + i].stage_pos[1]
                            and (objects[count + i].stage_pos[1] + objects[count + i].size[1]
                                 >= self.stage_pos[1] + self.size[1])
                            and not objects[count + i].stage_pos[1] < self.stage_pos[1]
                            and self.vertical_speed >= 0):
                        self.vertical_speed = 0
                        self.pos[1] = float(objects[count + i].pos[1] - self.size[1] + 2)
                        self.stage_pos[1] = float(self.pos[1])
                        self.check_falling = True
                        break
                else:
                    pass
            if not self.check_falling:
                for i in range(3):
                    if self.stage_pos[1] >= Config.height - self.size[1] and self.vertical_speed >= 0:
                        pass
                    else:
                        self.pos[1] += self.vertical_speed
                        self.stage_pos[1] = float(self.pos[1])
                        self.vertical_speed += 0.515625
                        if self.vertical_speed >= 12:
                            self.vertical_speed = 12

    def stop_going(self, objects: list, count: int, objects_states: list):
        for i in range(len(objects) - count):
            # count부터 len(objects)까지 반복
            if ((objects[count + i] is not self) and
                    self.hitbox.box.colliderect(objects[count + i].hitbox.box)):  # 충돌시
                '''
                1. 상대방이 can_through가 아닐것
                2. 상대방과 충돌하되 더 위에 있지 않을것
                '''
                obj_state = objects_states[objects[count + i].name]
                obj = objects[count + i]
                # print(obj.stage_pos[1] - obj.size[1] <= self.pos[1] - self.vertical_speed)
                '''
                1. (위)pos에 size 더한값이 self.pos에서 vertical_speed더한 값보다 작거나 같으면 안됨
                2. (아래)pos가 self.pos에서 self.size 빼고 vertcal_speed 더한값보다 크거나같으면 안됨
                '''
                '''
                [obj.stage_pos[1], obj.stage_pos[1] + obj.size[1]](y interval of obj)
                 ∩ [self.stage_pos[1], self.stage_pos[1] + self.size](y interval of self)
                != empty set
                
                -> 
                obj interval의 하한이 self interval의 상한보다 아래에 존재하고 
                obj interval의 상한이 self interval의 하한보다 위에 존재해야한다.
                
                -> 
                obj.stage_pos[1] : 상한
                obj.stage_pos[1] + obj.size[1]: 하한
                이하생략
                
                -> 
                obj.stage_pos[1] + obj.size[1] > self.stage_pos[1] and 
                obj.stage_pos[1] < self.stage_pos[1] + self.size[1]
                '''
                if (not obj_state.can_underthrough
                        and (obj.stage_pos[1] + obj.size[1] >= self.stage_pos[1] and
                             obj.stage_pos[1] < self.stage_pos[1] + self.size[1] - 2)):

                    if self.stage_pos[0] <= obj.stage_pos[0] + obj.size[0] <= self.stage_pos[0] + self.size[0] \
                            and (self.going_direction[0] or abs(self.horizontal_speed) > 0) \
                            and self.check_falling:
                        # self가 obj오른쪽에서 부닻혔을때
                        self.stage_pos[0] = float(obj.stage_pos[0] + obj.size[0])
                        self.pos[0] = float(obj.pos[0] + obj.size[0])

                    elif (obj.stage_pos[0] <= self.stage_pos[0] + self.size[0]
                          and (obj.stage_pos[0] + obj.size[0] >= self.stage_pos[0] + self.size[0])
                          and (self.going_direction[1] or abs(self.horizontal_speed) > 0)
                          and self.check_falling):
                        # self가 obj왼쪽에서 부닻혔을때
                        self.stage_pos[0] = float(obj.stage_pos[0] - self.size[0])
                        self.pos[0] = float(obj.pos[0] - self.size[0])

                    elif obj.stage_pos[1] + obj.size[1] > round(self.stage_pos[1]) > obj.stage_pos[1] \
                            and self.vertical_speed < 0:
                        self.vertical_speed = 0
                        self.stage_pos[1] = obj.stage_pos[1] + obj.size[1]
                        self.pos[1] = obj.stage_pos[1] + obj.size[1]

    def attack(self):
        self.is_attacking = True
        self.animation.anime_change(Animation.get_anime(f"{self.species}_attack"))

    def knock_back(self, player_stage_pos: list, is_hit: bool, direction):
        if self.horizontal_speed is None:
            self.horizontal_speed = 0

        if is_hit:
            if self.recent_damage is None:
                self.recent_damage = 10

            if not direction:  # 왼쪽에 있을떄
                self.horizontal_speed = self.recent_damage
                self.vertical_speed = -12
            else:
                self.horizontal_speed = -self.recent_damage
                self.vertical_speed = -12

        if self.horizontal_speed > 0:
            self.horizontal_speed -= 1
        if self.horizontal_speed < 0:
            self.horizontal_speed += 1

        self.pos[0] -= self.horizontal_speed
        self.stage_pos[0] -= self.horizontal_speed



class Jelly(Entity):
    def __init__(self, name, size: list, init_pos: list = None):
        super().__init__("enemy", name, "jelly_idle", size, init_pos, "jelly")
        self.max_pp = 75
        self.attack_damage = 10

        self.dash_count = 0
        self.dash_count_const = 60
        self.dash_cooltime = 0
        self.dash_cooltime_const = 100
        self.dash_distance_const = 30
        self.dash_vertical_const = 6



    def determinate(self, ply_pos: list):

        previous_noticed = self.AI.noticed
        self.AI.determinate(ply_pos, self.stage_pos)

        if self.AI.noticed and self.can_moving:
            # 플레이어가 근처에 있을때
            if self.AI.noticed is not previous_noticed and abs(self.vertical_speed) > 0:
                self.dash_count = self.dash_count_const  # 준비 시간

            elif self.dash_count > 0:
                self.dash_count -= 1

            elif self.dash_cooltime <= 0:  # 대시 쿨타임
                if self.AI.moving(ply_pos, self.stage_pos):
                    self.horizontal_speed -= self.dash_distance_const

                else:
                    self.horizontal_speed += self.dash_distance_const

                self.vertical_speed -= self.dash_vertical_const
                self.dash_cooltime = self.dash_cooltime_const

            else:
                if self.AI.moving(ply_pos, self.stage_pos):
                    self.going_direction[1] = True
                    self.going_direction[0] = False
                else:
                    self.going_direction[1] = False
                    self.going_direction[0] = True

        else:
            self.AI.moving(ply_pos, self.stage_pos)
            if self.AI.is_sleep:
                self.going_direction = [False, False]

            elif self.AI.direction:
                self.going_direction[1] = True

            else:
                self.going_direction[0] = True

        if self.dash_cooltime <= 0:
            self.dash_cooltime = 0
        elif self.dash_cooltime > 0:
            self.dash_cooltime -= 1


class BossJelly(Entity):
    def __init__(self, name, size: list, init_pos: list, player, stage_objects: list, obj_states: list, count: int, jelly: Callable,
                 remote_electro: Callable, around_electro: Callable, tentacle: Callable):
        super().__init__("enemy", name, "boss_jelly_idle", size, init_pos, "jelly")

        self.max_pp = 75
        self.attack_damage = 10

        self.hit_count_constant = 10

        self.dash_count = 0
        self.dash_count_const = 60
        self.dash_cooltime = 0
        self.dash_cooltime_const = 300
        self.dash_distance_const = 30
        self.dash_vertical_const = 6
        self.player = player
        self.stage_objects = stage_objects
        self.obj_states = obj_states
        self.count = count
        self.jelly = jelly
        self.remote_electro = remote_electro
        self.around_electro = around_electro
        self.tentacle = tentacle
        self.boss = self
        self.next_skill = None
        self.will_use_skill = False

        self.AI = JellyBoss(self, player, stage_objects, obj_states, count, jelly,
                 remote_electro, around_electro, tentacle)

        self.skill_list = [JellyBoss.jelly_spawn, JellyBoss.electric_around_attack,
                           JellyBoss.electric_remote_attack, JellyBoss.tentacle_attack, JellyBoss.dash]
        self.max_pp = 1000
        self.protect_point = self.max_pp

        self.can_moving = False

        self.state.can_be_damaged = False

    def determinate(self, ply_pos: list):
        # rint(self.protect_point)
        previous_noticed = self.AI.noticed
        self.AI.determinate(ply_pos, self.stage_pos)

        if self.AI.noticed and self.can_moving:
            # 플레이어가 근처에 있을때
            if self.AI.noticed is not previous_noticed and abs(self.vertical_speed) > 0:
                self.dash_count = self.dash_count_const  # 준비 시간

            elif self.dash_count > 0:
                self.dash_count -= 1

            elif self.dash_cooltime <= 0 and self.next_skill is None:  # 대시 쿨타임
                self.next_skill = self.skill_list[random.randrange(0, 5)]

                self.next_skill(self)

                print(self.next_skill)

                self.dash_cooltime = self.dash_cooltime_const

            elif self.dash_cooltime <= 0 and self.next_skill is not None:
                self.next_skill(self)
                print(self.next_skill)
                self.next_skill = None

            else:
                if self.AI.moving(ply_pos, self.stage_pos):
                    self.going_direction[1] = True
                    self.going_direction[0] = False
                else:
                    self.going_direction[1] = False
                    self.going_direction[0] = True

        else:
            self.AI.moving(ply_pos, self.stage_pos)
            if self.AI.is_sleep:
                self.going_direction = [False, False]

            elif self.AI.direction:
                self.going_direction[1] = True

            else:
                self.going_direction[0] = True

        if self.dash_cooltime <= 0:
            self.dash_cooltime = 0
        elif self.dash_cooltime > 0:
            self.dash_cooltime -= 1

    def knock_back(self, player_stage_pos: list, is_hit: bool, direction):
        pass
