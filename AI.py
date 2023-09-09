import math
import random

class AI:
    def __init__(self):
        self.count = 10
        self.sleep = 100
        self.is_sleep = True
        self.noticed = False
        self.direction = False
        self.det_count = 0

    def determinate(self, ply_pos: list, stg_pos: list):
        if self.det_count <= 0:

            x1 = ply_pos[0]
            x2 = stg_pos[0]
            y1 = ply_pos[1]
            y2 = stg_pos[1]
            dist = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

            if dist < 600:
                self.noticed = True

            else:
                self.noticed = False

            self.det_count = 60
        else:
            self.det_count -= 1

    def moving(self, ply_pos: list, stg_pos: list):
        x1 = ply_pos[0]
        x2 = stg_pos[0]
        y1 = ply_pos[1]
        y2 = stg_pos[1]
        if not self.noticed:

            if self.sleep > 0:
                self.sleep -= 1
                self.is_sleep = True
            elif self.sleep <= 0 < self.count:
                self.count -= 1
                self.is_sleep = False

            elif self.sleep <= 0 and self.count <= 0:
                self.direction = random.randrange(0, 1) == 0
                self.is_sleep = False
                self.count = random.randrange(10, 60)
                self.sleep = random.randrange(60, 200)

        else:
            return x2-x1 <= 0

