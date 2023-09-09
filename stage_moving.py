from conf import Config
class CameraMoving:
    def __init__(self, screen_player_pos: list, drawn_obj: list, stage_player_pos: list, stage_size: list):
        self.screen_player_pos = screen_player_pos
        self.drawn_obj = drawn_obj
        self.stage_player_pos = stage_player_pos
        self.stage_size = stage_size

    def objectupdate(self, drawn_obj: list, screen_player_pos: list, background, width):
        global player
        x = 0
        for i in drawn_obj:
            if i.name == "player":
                break
            x += 1
        player = drawn_obj.pop(x)

        # print(drawn_obj)
        # print(id(player))
        # print(id(self.screen_player_pos), id(screen_player_pos))
        # print(screen_player_pos, self.screen_player_pos, self.stage_player_pos)
        pos_equal = (self.screen_player_pos[0] == screen_player_pos[0] and
                     self.screen_player_pos[1] == screen_player_pos[1])
        if pos_equal:
            # print(list(drawn_obj))
            drawn_obj.append(player)
            return drawn_obj, screen_player_pos, background

        elif (self.stage_size[0] - 804 < self.stage_player_pos[0] or
              self.stage_player_pos[0] < 804) and screen_player_pos[0] != 804:

            self.stage_player_pos[0] += float(screen_player_pos[0] - self.screen_player_pos[0])
            self.stage_player_pos[1] += float(screen_player_pos[1] - self.screen_player_pos[1])

            self.screen_player_pos[0] = float(screen_player_pos[0])
            self.screen_player_pos[1] = float(screen_player_pos[1])
            if screen_player_pos[0] >= 804 or screen_player_pos[0] <= self.stage_size[0] - 804:
                x = 0
                for i in drawn_obj:
                    drawn_obj[x].pos = [float(drawn_obj[x].pos[0] - screen_player_pos[0] + self.screen_player_pos[0]),
                                        float(drawn_obj[x].pos[1])]
                    x += 1
            drawn_obj.append(player)
            # print("x", self.screen_player_pos, "\n", "y", self.stage_player_pos)
            return drawn_obj, screen_player_pos, background


        else:
            x = 0
            self.stage_player_pos[0] += float(screen_player_pos[0] - self.screen_player_pos[0])
            self.stage_player_pos[1] += float(screen_player_pos[1] - self.screen_player_pos[1])
            self.screen_player_pos = [804, player.pos[1]]

            for i in drawn_obj:
                drawn_obj[x].pos = [float(drawn_obj[x].pos[0] - screen_player_pos[0] + self.screen_player_pos[0]),
                                    float(drawn_obj[x].pos[1])]
                # print(drawn_obj[x].stage_pos)
                # print(drawn_obj[x].pos)

                x += 1
            background.pos[0] = 80 * float(-player.stage_pos[0] + 804) / width

            # print(screen_player_pos[0])
            # print(self.screen_player_pos[0])
            # print("z", self.screen_player_pos, "\n", "w", self.stage_player_pos)

            drawn_obj.append(player)
            self.drawn_obj = drawn_obj

            return self.drawn_obj, list(self.screen_player_pos), background

    def obj_update(self, drawn_obj: list, screen_player_pos: list, background, width, player):
        x = 0
        player_idx = None

        for i, obj in enumerate(drawn_obj):
            if obj.name == "player":
                player_idx = i
                break
            x += 1

        if player is None:
            return drawn_obj, screen_player_pos, background

        middle_const = player.walk_speed * (800 // player.walk_speed)

        if player_idx is not None:
            drawn_obj.pop(player_idx)

        if (
                self.stage_size[0] - middle_const <= self.stage_player_pos[0]
                or self.stage_player_pos[0] <= middle_const
        ):
            screen_player_pos[0] -= abs(screen_player_pos[0] - self.screen_player_pos[0]) % player.walk_speed
            self.stage_player_pos[0] += float(screen_player_pos[0] - self.screen_player_pos[0])
            self.stage_player_pos[1] += float(screen_player_pos[1] - self.screen_player_pos[1])

            for i, obj in enumerate(drawn_obj):
                if self.stage_size[0] <= obj.stage_pos[0] + obj.size[0]:
                    drawn_obj[i].stage_pos[0] = self.stage_size[0] - obj.size[0]
                    drawn_obj[i].pos[0] = 1600 - obj.size[0]
                if obj.stage_pos[0] <= 0:
                    drawn_obj[i].pos[0] = 0

            if (
                    screen_player_pos[0] != self.stage_player_pos[0]
                    or screen_player_pos[0] != self.stage_player_pos[0] - middle_const
            ):
                if self.stage_player_pos[0] + 80 >= self.stage_size[0]:
                    self.screen_player_pos[0] = 1520
                    self.stage_player_pos[0] = self.stage_size[0] - 80
                if self.stage_player_pos[0] <= 0:
                    self.screen_player_pos[0] = 0
                    self.stage_player_pos[0] = 0

                if (
                        screen_player_pos[0]
                        != self.stage_player_pos[0] - middle_const + screen_player_pos[0]
                        and self.stage_player_pos[0] > self.stage_size[0] - middle_const
                ): # 오른쪽 끝에서
                    self.screen_player_pos[0] = self.stage_size[0] - middle_const + screen_player_pos[0]
                    self.stage_player_pos[0] = self.stage_size[0] - Config.width + screen_player_pos[0]

                    background.pos[0] = (80 * float(-self.stage_size[0] + Config.width) / width)
                    for i, obj in enumerate(drawn_obj):
                        drawn_obj[i].pos[0] = float(drawn_obj[i].stage_pos[0] + Config.width - self.stage_size[0])

                elif (
                        screen_player_pos[0] != self.stage_player_pos[0]
                        and self.stage_player_pos[0] <= self.stage_size[0] - 2 * middle_const
                ): # 왼쪽 끝에서
                    self.screen_player_pos[0] = screen_player_pos[0]
                    self.stage_player_pos[0] = screen_player_pos[0]
                    background.pos[0] = 0
                    for i, obj in enumerate(drawn_obj):
                        drawn_obj[i].pos[0] = float(drawn_obj[i].stage_pos[0])

            self.screen_player_pos[0] = float(screen_player_pos[0])
            self.screen_player_pos[1] = float(screen_player_pos[1])

            if middle_const <= screen_player_pos[0] <= self.stage_size[0] - middle_const:
                for i, obj in enumerate(drawn_obj):
                    drawn_obj[i].pos[0] = float(drawn_obj[i].pos[0] - screen_player_pos[0] + self.screen_player_pos[0])

            drawn_obj.append(player)
            return drawn_obj, screen_player_pos, background
        elif (
                self.screen_player_pos[0] == screen_player_pos[0]
                and self.screen_player_pos[1] == screen_player_pos[1]
        ):
            drawn_obj.append(player)
            return drawn_obj, screen_player_pos, background
        else:
            for i, obj in enumerate(drawn_obj):
                drawn_obj[i].pos[0] = float(drawn_obj[i].stage_pos[0] - player.stage_pos[0] + middle_const)

            screen_player_pos[0] -= abs(screen_player_pos[0] - self.screen_player_pos[0]) % player.walk_speed
            self.stage_player_pos[0] += float(screen_player_pos[0] - self.screen_player_pos[0])
            self.stage_player_pos[1] += float(screen_player_pos[1] - self.screen_player_pos[1])
            self.screen_player_pos = [middle_const, player.pos[1]]

            background.pos[0] = 80 * float(-player.stage_pos[0] + middle_const) / width

            drawn_obj.append(player)
            self.drawn_obj = drawn_obj

            return self.drawn_obj, list(self.screen_player_pos), background
