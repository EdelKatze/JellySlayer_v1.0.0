import pygame as pg
from conf import Config
from obj import Object


class EmptyBar(Object):
    def __init__(self, name, init_pos):
        super().__init__(species="interface", name=name, img_name="empty_bar",
                         size=Config.bar_size, init_pos=init_pos)
        self.hitbox = None


class Core(Object):
    def __init__(self, name, img_name, init_pos):
        super().__init__(species="interface", name=name, img_name=img_name,
                         size=Config.bar_size, init_pos=init_pos)
        self.now_percent = 100
        self.hitbox = None
        self.original_img = self.img
        self.font = None
        self.text = None

    def shrinking(self, percentage):
        __percentage = percentage / 100
        self.img = pg.transform.scale(self.original_img, [abs(self.size[0] * __percentage), self.size[1]]).convert_alpha()

    def update(self, player):
        point = player.get_protect_point() / player.max_pp \
            if self.name.split("_")[0] == "protection" \
            else player.get_ap() / player.max_ap

        percentage = round(point * 100)
        # print(percentage)
        if percentage != self.now_percent:
            self.shrinking(percentage)
            self.now_percent = percentage
        Config.screen.blit(self.img, self.pos)
        self.font = pg.font.Font("./src/fonts/joystix monospace.otf", 40)
        self.text = self.font.render(self.name[0] + "P", True, (0, 0, 0)).convert_alpha()
        Config.screen.blit(self.text, [self.pos[0] + self.size[0] + 10, self.pos[1] - 5])


class DisplayBar:
    def __init__(self, name, init_pos):
        self.img_name = "@"
        self.size = (0, 0)
        self.name = name + "_bar"
        
        self.empty_bar = EmptyBar(name + "_empty_bar", init_pos)
        self.core = Core(name + "_core",
                         "health" if name == "protection"
                         else "mentality",
                         init_pos)

    def update(self, player):
        self.empty_bar.update()
        self.core.update(player)
