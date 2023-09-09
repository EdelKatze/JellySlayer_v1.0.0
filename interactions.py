import pygame as pg

pg.init()
screen = pg.display.set_mode((1600, 900))

class Text_play:
    def __init__(self, text_info: list):
        self.text_info = text_info
        self.list_count = 0
        self.text_count = 0
        self.text = ''
        self.Font = pg.font.Font("./src/fonts/joystix monospace.otf", 32, )
        self.rect = pg.Rect(0, 0, 1400, 800)
        self.color = pg.Color('white')
        self.clock = pg.time.Clock()
        self.check = True
        self.text_surface = None
    def text_update(self):
        if len(self.text_info) == self.list_count and not self.is_next:
            self.check = False
        elif len(self.text_info[self.list_count]) == self.text_count:
            self.text_count = 0
            self.list_count += 1
            self.is_next = True
            while self.is_next:
                # print("SS")
                for event in pg.event.get():
                    if event.type == pg.KEYDOWN:
                        if event.key == pg.K_z:
                            self.is_next = False
        else:
            self.text_count += 1
            self.text = self.text_info[self.list_count][0:self.text_count]
            # print(self.text)
            self.text_surface = self.Font.render(self.text, True, self.color)

    def main(self, background):
        done = True
        while done:
            screen.fill((30, 30, 30))
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    done = False

                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        done = False
            self.text_update()
            screen.blit(background.img, background.pos)
            screen.blit(self.text_surface, (self.rect.x, self.rect.y))
            pg.draw.rect(screen, self.color, self.rect, -1)


            if self.list_count > len(self.text_info):
                self.list_count -= 1


            pg.display.flip()
            self.clock.tick(15)
            done = self.check
