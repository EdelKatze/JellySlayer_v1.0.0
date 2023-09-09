from obj import Object
from ani import Animation


class Portal(Object):
    def __init__(self, name, img_name, size: list, init_pos: list = None):
        super().__init__("structure", name, img_name, size, init_pos, True)
        self.switch = False
        self.anime_name = "portal"
        self.state.interactive = True
        self.state.can_underthrough = True

    def interact(self):
        self.switch = True

    def update(self):
        self.animation.anime_change(Animation.get_anime(self.anime_name), True)
        super().update()


class Platform(Object):
    def __init__(self, name, size: list, init_pos: list = None):
        super().__init__("structure", name, "forest_platform", size, init_pos)
