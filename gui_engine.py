#   _____ _    _ ______   ______             _
#  / ____| |  | |_   _|  |  ____|           (_)
# | |  __| |  | | | |    | |__   _ __   __ _ _ _ __   ___
# | | |_ | |  | | | |    |  __| | '_ \ / _` | | '_ \ / _ \
# | |__| | |__| |_| |_   | |____| | | | (_| | | | | |  __/
#  \_____|\____/|____|   |______|_| |_|\__, |_|_| |_|\___|
#                                      __/ |
#                                     |___/
# Made By Shkryoav And Arctic Fox
# Giving Credits Will Help Us So Much
# Version: 1.0.3 | Alpha
import datetime
import pygame


class GUI:
    def __init__(self):
        self.elements = []
        self.hiddens = []

    def __str__(self):
        return f"<GUI items={len(self.elements)}>"

    def draw(self, surface):
        returns = {}
        for level, element in sorted(self.elements):
            if element in self.hiddens:
                continue
            data = element.draw(surface)
            if data is not None:
                returns[element] = data
        return returns

    def add_element(self, element, level=0):
        self.elements.append([level, element])

    def hide_element(self, element):
        if element not in self.hiddens:
            self.hiddens.append(element)

    def show_element(self, element):
        if element in self.hiddens:
            self.hiddens.remove(element)


class Box:
    def __init__(self, w, h, x=0, y=0, color=(0, 0, 0), width=0, rounded=0):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = color
        self.width = width
        self.round = rounded

    def __str__(self):
        return f"<Box width={self.rect.w} height={self.rect.h} x={self.rect.x}" \
               f" y={self.rect.y} color= {self.color} draw_type={self.width}>"

    def draw(self, surface):
        max_round = min(self.rect.w, self.rect.h) / 2
        pygame.draw.rect(surface, self.color, self.rect, self.width, self.round if self.round <= max_round else 0)


class BoxButton:
    def __init__(self, w, h, x=0, y=0, color=(255, 255, 255), click_color=None, highlite_color=None, **kwargs):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = color
        self.click_color = click_color
        self.highlite_color = highlite_color
        self.ticks = kwargs.get("ticks") or 50
        self._current_tick = 0
        self._click = False
        self._highlite = False
        self.direct_call = None

    def __str__(self):
        return f"<BoxButton width={self.rect.w} height={self.rect.h} x={self.rect.x}" \
               f" y={self.rect.y} color= {self.color}>"

    def draw(self, surface):
        self.update()
        if self._click:
            pygame.draw.rect(surface, self.click_color, self.rect)
        elif self._highlite:
            pygame.draw.rect(surface, self.highlite_color, self.rect)
        else:
            pygame.draw.rect(surface, self.color, self.rect)
        return {"click": self._click, "highlite": self._highlite}

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_buttons = pygame.mouse.get_pressed(3)
        if self._current_tick != 0:
            self._current_tick -= 1
        else:
            self._click = False

        if self.rect.collidepoint(mouse_pos) and mouse_buttons[0]:
            if self.direct_call is not None and self._click:
                self.direct_call()
            self._click = True
            self._current_tick = self.ticks
        elif self.rect.collidepoint(mouse_pos):
            self._highlite = True
        else:
            self._highlite = False


class ImageButton:
    def __init__(self, x, y, image, clickimage=None, highliteimage=None, **kwargs):
        self.image = image.copy()
        self.rect = self.image.get_rect(x=x, y=y)
        self.click_image = clickimage or image.copy()
        self.highlite_image = highliteimage
        self.ticks = kwargs.get("ticks") or 60
        self.direct_call = None
        self._current_tick = 0
        self._click = False
        self._highlite = False

    def __str__(self):
        return f"<ImageButton width={self.rect.w} height={self.rect.h} x={self.rect.x} y={self.rect.y}>"

    def draw(self, surface):
        self.update()
        if self._click:
            surface.blit(self.click_image, self.rect)
        elif self._highlite and self.highlite_image is not None:
            surface.blit(self.highlite_image, self.rect)
        else:
            surface.blit(self.image, self.rect)
        return {"click": self._click, "highlite": self._highlite}

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_buttons = pygame.mouse.get_pressed(3)
        if self._current_tick != 0:
            self._current_tick -= 1
        else:
            self._click = False

        if self.rect.collidepoint(mouse_pos) and mouse_buttons[0]:
            self._click = True
            self._current_tick = self.ticks
            if self.direct_call is not None:
                self.direct_call()
        elif self.rect.collidepoint(mouse_pos):
            self._highlite = True
        else:
            self._highlite = False


class SysText:
    def __init__(self, x, y, font_name, font_size, text, color=(0, 0, 0), background_color=None, **kwargs):
        self.font = pygame.font.Font(font_name, font_size)
        self.font_size = font_size
        self.text = text.split("\n")
        self.pos = (x, y)
        self.color = color
        self.background_color = background_color
        self.max_width = kwargs.get("max_width") or 0
        self.anti_allias = kwargs.get("anti_allias") or False
        self.transparent = kwargs.get("transparent") or False

    def __str__(self):
        return f"<SysText x={self.pos[0]} y={self.pos[1]} color={self.color} text={self.text}>"

    def draw(self, surface):
        line_movement = 0
        if self.background_color is not None:
            for line in self.text:
                surface.blit(self.font.render(line, self.anti_allias, self.color, self.background_color),
                             (self.pos[0], self.pos[1] + line_movement))
                line_movement += self.font_size + 2
        else:
            for line in self.text:
                surface.blit(self.font.render(line, self.anti_allias, self.color),
                             (self.pos[0], self.pos[1] + line_movement))
                line_movement += self.font_size + 2

    def change_font(self, font_name, font_size):
        self.font = pygame.font.SysFont(font_name, font_size)


class HorizontalSlider:
    def __init__(self, x, y, length, height_bar, fill_color, empty_color, box: Box):
        self.fill_percent = 0
        self.fill_color = fill_color
        self.empty_color = empty_color
        self.click_box = box
        self.click_box.rect.centerx = x
        self.click_box.rect.centery = y + (height_bar / 2)
        self._borders = (x, x+length)
        self._fill_box = pygame.Rect(x, y, 0, height_bar)
        self._empty_box = pygame.Rect(x, y, length, height_bar)
        self._focus = False

    def __str__(self):
        return "<HorizontalSlider>"

    def draw(self, surface):
        self.update()
        pygame.draw.rect(surface, self.empty_color, self._empty_box)
        pygame.draw.rect(surface, self.fill_color, self._fill_box)
        self.click_box.draw(surface)
        return {"focus": self._focus, "percentage": self.fill_percent}

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        buttons = pygame.mouse.get_pressed(3)

        if self.click_box.rect.collidepoint(mouse_pos) and buttons[0]:
            self._focus = True
        elif self._focus and not buttons[0]:
            self._focus = False

        rel = pygame.mouse.get_rel()
        if self._focus:
            if self._borders[0] <= self.click_box.rect.centerx + rel[0] <= self._borders[1]:
                self.click_box.rect.x += rel[0]
                self.fill_percent = (self.click_box.rect.centerx - self._empty_box.x) / self._empty_box.w
            else:
                if rel[0] > 0:
                    self.click_box.rect.centerx = self._empty_box.x + self._empty_box.w
                    self.fill_percent = 1.0
                elif rel[0] < 0:
                    self.click_box.rect.centerx = self._empty_box.x
                    self.fill_percent = 0.0

        self._fill_box.w = self.fill_percent * self._empty_box.w


class TextInput:
    def __init__(self, x, y, w, h, font_name, size, color, **kwargs):
        self.rect = pygame.Rect(x, y, w, h)
        self.font = pygame.font.SysFont(font_name, size)
        self.color = color
        self.delete_after_max = kwargs.get("delete_after_max") or False
        self.scroll_after_max = kwargs.get("scroll_after_max") or False
        self.background_color = kwargs.get("background_color") or None
        self.text = ""
        self._focus = False
        self._key_pressed = False
        self._press_timer = datetime.datetime.now()

    def draw(self, surface):
        self.update()
        if self.background_color is not None:
            pygame.draw.rect(surface, self.background_color, self.rect)
        if self.text == "":
            return {"focus": self._focus, "text": self.text}
        text_surface = self.font.render(self.text, False, self.color)
        if self.scroll_after_max and text_surface.get_width() > self.rect.w:
            sub_area = text_surface.get_rect(x=text_surface.get_width()-self.rect.w, w=self.rect.w)
            text_surface = text_surface.subsurface(sub_area)
        elif self.delete_after_max and text_surface.get_width() > self.rect.w:
            text_surface = text_surface.subsurface(text_surface.get_rect(w=self.rect.w))
        surface.blit(text_surface, self.rect)
        return {"focus": self._focus, "text": self.text}

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        buttons = pygame.mouse.get_pressed(3)
        if self.rect.collidepoint(mouse_pos) and buttons[0]:
            self._focus = True
        elif self._focus and buttons[0] and not self.rect.collidepoint(mouse_pos):
            self._focus = False
        keys = pygame.key.get_pressed()
        if self._focus:
            if not self._key_pressed or (datetime.datetime.now() - self._press_timer).total_seconds() > 0.10:
                if keys[pygame.K_q]: self.text += "q"
                if keys[pygame.K_w]: self.text += "w"
                if keys[pygame.K_e]: self.text += "e"
                if keys[pygame.K_r]: self.text += "r"
                if keys[pygame.K_t]: self.text += "t"
                if keys[pygame.K_y]: self.text += "y"
                if keys[pygame.K_u]: self.text += "u"
                if keys[pygame.K_o]: self.text += "o"
                if keys[pygame.K_p]: self.text += "p"
                if keys[pygame.K_a]: self.text += "a"
                if keys[pygame.K_s]: self.text += "s"
                if keys[pygame.K_d]: self.text += "d"
                if keys[pygame.K_f]: self.text += "f"
                if keys[pygame.K_g]: self.text += "g"
                if keys[pygame.K_h]: self.text += "h"
                if keys[pygame.K_j]: self.text += "j"
                if keys[pygame.K_k]: self.text += "k"
                if keys[pygame.K_l]: self.text += "l"
                if keys[pygame.K_i]: self.text += "i"
                if keys[pygame.K_z]: self.text += "z"
                if keys[pygame.K_x]: self.text += "x"
                if keys[pygame.K_c]: self.text += "c"
                if keys[pygame.K_v]: self.text += "v"
                if keys[pygame.K_b]: self.text += "b"
                if keys[pygame.K_n]: self.text += "n"
                if keys[pygame.K_m]: self.text += "m"
                if keys[pygame.K_SPACE]: self.text += " "
                if keys[pygame.K_RETURN] or keys[pygame.K_ESCAPE]:
                    self._key_pressed = False
                    self._focus = False
                    return
                if keys[pygame.K_BACKSPACE]:
                    self.text = self.text[:-1]
                self._key_pressed = True
                self._press_timer = datetime.datetime.now()
        if not any(keys):
            self._key_pressed = False
            self._press_timer = datetime.datetime.now()


class CheckBox:
    def __init__(self, x, y, w, h, pixel_difference, empty_color, fill_color, **kwargs):
        self.rect = pygame.Rect(x, y, w, h)
        self.pixel_difference = pixel_difference
        self.empty_color = empty_color
        self.fill_color = fill_color
        self._click = False
        self._pressed = False
        self.round = kwargs.get("round") or 0

    def draw(self, surface):
        self.update()
        pygame.draw.rect(surface, self.empty_color, self.rect, 0, self.round)
        if self._click:
            fill_rect = self.rect.copy()
            fill_rect.x += self.pixel_difference
            fill_rect.y += self.pixel_difference
            fill_rect.w -= 2 * self.pixel_difference
            fill_rect.h -= 2 * self.pixel_difference
            pygame.draw.rect(surface, self.fill_color, fill_rect, 0, self.round)
        return {"click": self._click}

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        buttons = pygame.mouse.get_pressed(3)
        if self.rect.collidepoint(mouse_pos) and buttons[0] and not self._pressed:
            self._click = not self._click
            self._pressed = True
        if not buttons[0]:
            self._pressed = False


class InvisibleButton:
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)
        self.direct_call = None
        self._click = False
        self._pressed = False

    def draw(self, surface):
        self.update()
        return {"click": self._click}

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        buttons = pygame.mouse.get_pressed(3)
        if self.rect.collidepoint(mouse_pos) and buttons[0] and not self._pressed:
            self._click = True
            self._pressed = True
            if self.direct_call is not None:
                self.direct_call()

        if not buttons[0]:
            self._pressed = False
            self._click = False
