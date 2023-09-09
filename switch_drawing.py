from conf import Config


class Switch:
    def __init__(self, player_pos: list, stage_size: list, projectile_obj: list, obj: list):
        self.player_pos = player_pos
        self.stage_size = stage_size
        self.projectile_obj = projectile_obj
        self.obj = obj
        self.drawn_obj = []
        self.undrawn_obj = []
        for i in obj:
            out = (i.stage_pos[0] >= self.player_pos[0] + Config.width // 2 + 800 or
                   i.stage_pos[1] >= self.player_pos[1] + Config.height // 2 + 800)
            if not out:
                self.drawn_obj.append(i)
            else:
                self.undrawn_obj.append(i)

    def switch(self):

        x = 0

        for i in self.undrawn_obj:
            out = (abs(i.stage_pos[0] - self.player_pos[0]) >= Config.width // 2 + 800 or
                   abs(i.stage_pos[1] - self.player_pos[1]) >= Config.height // 2 + 800)
            if not out:  # 스테이지 안에 있으면
                obj = self.undrawn_obj.pop(x)
                self.drawn_obj.append(obj)  # 삭제 하고 drawn 에 추가
                x -= 1
            x += 1
        x = 0
        for i in self.drawn_obj:  # 스테이지 밖에 있다면
            out = (abs(i.stage_pos[0] - self.player_pos[0]) >= Config.width // 2 + 800 or
                   abs(i.stage_pos[1] - self.player_pos[1]) >= Config.height // 2 + 800)
            if out:
                obj = self.drawn_obj.pop(x)
                self.undrawn_obj.append(obj)  # 삭제 하고 undrawn 에 추가
                x -= 1
            x += 1
        return self.drawn_obj

    def projectiles(self):
        x = 0
        for i in self.projectile_obj:

            out = (abs(i.stage_pos[0] - self.player_pos[0]) >= Config.width // 2 + 800 or
                   abs(i.stage_pos[1] - self.player_pos[1]) >= Config.height // 2 + 800)
            if out:
                self.projectile_obj.remove(x)  # 얘는 밖에 있으면 얄짤 없음
                x -= 1
            x += 1

    def player_pos_update(self, current_player_pos):
        self.player_pos = current_player_pos

    def objectupdate(self, objs):
        self.drawn_obj = objs