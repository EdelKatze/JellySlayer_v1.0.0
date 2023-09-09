import pygame as pg
import inspect
from typing import Callable

pg.init()
screen = pg.display.set_mode((1600, 900))
COLOR_INACTIVE = pg.Color('lightskyblue3')
COLOR_ACTIVE = pg.Color('dodgerblue2')
FONT = pg.font.Font(None, 32)


class InputBox:

    def __init__(self, x, y, w, h, name: str, text=''):

        pg.init()
        COLOR_INACTIVE = pg.Color('lightskyblue3')
        FONT = pg.font.Font(None, 32)
        self.rect = pg.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False
        self.name = name
        self.name_surface = FONT.render(name, True, self.color)

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_RETURN:
                    print(self.text)
                elif event.key == pg.K_BACKSPACE and pg.key.get_mods() & pg.KMOD_CTRL:
                    self.text = ''
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif event.key == pg.K_ESCAPE:
                    return 0
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, self.color)

    def rtn_text(self):
        return self.text

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        screen.blit(self.name_surface, (self.rect.x, self.rect.y - 30))
        # Blit the rect.
        pg.draw.rect(screen, self.color, self.rect, 2)


def delete(objects: list, lists_using_objects: list = None):
    clock = pg.time.Clock()
    input_boxes = []
    c=0
    for i in objects:
        name = str(i.__class__) + ", in "+ str(i.stage_pos)
        input_boxes.append(InputBox(100, 40 + (c * 65), 140, 32, name))

        c +=1

    done = False
    while not done:

        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    done = True

            for box in input_boxes:
                box.handle_event(event)

        for box in input_boxes:
            box.update()

        screen.fill((30, 30, 30))
        for box in input_boxes:
            box.draw(screen)

        pg.display.flip()
        clock.tick(30)
    c = 0
    d = 0
    for i in input_boxes:
        if input_boxes[c].text != '':
            objects.pop(d)
            d -= 1
            print(d)
            print(input_boxes[c].text)
        c += 1
        d += 1
    print(objects)
    
    deleted_obj = None # 현재 오류 남. 삭제된 오브젝트를 리스트나 단일 객체로 받아오게 해주셈
    if lists_using_objects is not None:
        for list in lists_using_objects:
            for obj in list:
                if deleted_obj.name == obj.name:
                    list.remove(obj)
    
    return objects

