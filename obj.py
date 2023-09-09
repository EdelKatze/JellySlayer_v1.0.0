import pygame as pg
import copy
from conf import Config
from ani import Animation

pg.init()


class State:
    def __init__(self, attackable=False, interactive=False, can_be_damaged=False, can_step=False,
                 can_underthrough=False):
        self.attackable = attackable
        self.interactive = interactive
        self.can_be_damaged = can_be_damaged
        self.can_step = can_step
        self.can_underthrough = can_underthrough


structure_state = State(
    attackable=False,
    interactive=True,
    can_be_damaged=False,
    can_step=True,
    can_underthrough=False,
)

jelly_state = State(
    attackable=True,
    interactive=False,
    can_be_damaged=True,
    can_step=False,
    can_underthrough=True,
)

platform_state = State(
    attackable=False,
    interactive=False,
    can_be_damaged=False,
    can_step=True,
    can_underthrough=False,
)

states = {
    "structure": structure_state,
    "jelly": jelly_state,
    "platform": platform_state,
}


class Hitbox:
    def __init__(self, obj):
        self.obj = obj
        self.pos = self.obj.pos
        self.size = self.obj.size
        self.obj_tracking = True
        self.box = pg.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

    def get_hitbox(self):
        return self.box

    def set_hitbox(self, pos=None, size=None):
        if self.obj_tracking:
            self.pos = self.obj.pos[:]
            self.size = self.obj.size[:]
        else:
            if pos is not None:
                self.pos = pos[:]
            if size is not None:
                self.size = size[:]
        self.box.update(self.pos[0], self.pos[1], self.size[0], self.size[1])


class Object:
    def __init__(self, species, name, img_name, size: list, init_pos: list = None, has_anime=False, state="structure"):
        self.species = species  # player, structure(스테이지 기물(벽 등)), background, enemy
        self.name = name
        self.size = size
        self.img_name = img_name
        try:
            self.img = Config.IMAGE.images[self.img_name][0].image.convert_alpha()
        except:
            self.img = Config.IMAGE.images["@"][0].image
        self.img = pg.transform.scale(self.img, self.size)
        self.pos = init_pos if init_pos is not None else [0, Config.height - self.size[1]]
        self.hitbox = Hitbox(self)
        self.stage_pos = list(self.pos)

        self.has_anime = has_anime

        if self.has_anime:
            self.animation = Animation(obj=self, anime=Animation.get_anime(self.img_name))

        if state in states:
            self.state = copy.deepcopy(states[state])
        else:
            self.state = copy.deepcopy(states["structure"])

    def update(self):
        if self.hitbox is not None:
            self.hitbox.set_hitbox()
        if self.has_anime:
            self.animation.animate()
            pg.draw.rect(Config.screen, (255, 0, 0), self.hitbox.box, 2)

        Config.screen.blit(self.img, self.pos)

    def interact(self):
        print(f'{self.name} has been interacted')
