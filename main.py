import pygame
import time
import random
import math
from gui_engine import GUI, SysText, ImageButton

pygame.init()

screen = pygame.display.set_mode((600, 800), vsync=1)
pygame.display.set_caption("Type Fast!")
icon = pygame.image.load("assets/ship.png")
icon.set_colorkey((255, 255, 255))
pygame.display.set_icon(icon)

clock = pygame.time.Clock()
font_20 = pygame.font.Font("fonts/Pixeled.ttf", 20)
score_font = pygame.font.Font("fonts/upheavtt.ttf", 50)

pygame.mixer.music.load("sounds/music.mp3")
pygame.mixer.music.play(-1)
explosion_sound = pygame.mixer.Sound("sounds/explosion.wav")
shoot_sound = pygame.mixer.Sound("sounds/shoot.wav")

game_over = False
wave = 0
spawn_timer = 3
on_wave_text = False
on_screen_middle = False
wave_text_pos = [0, 0]
spawn_period = False

class Background:
    def __init__(self):
        self.image = pygame.transform.scale(pygame.image.load("assets/bg.jpg"), (600, 400))
        self.index = 0

    def draw(self, surface):
        surface.blit(self.image, (0, self.index - 400))
        surface.blit(self.image, (0, self.index))
        surface.blit(self.image, (0, self.index + 400))
        if game_over:
            return
        self.index += 60 * dt
        if self.index >= 400:
            self.index = 0


background = Background()


class Player:
    def __init__(self):
        self.image = pygame.transform.scale(pygame.image.load("assets/ship.png"), (64, 64))
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect(x=600 // 2 - self.image.get_width() // 2, y=700)
        self.bullets = []
        self.target = None
        self.score = 0

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        for bullet in self.bullets:
            bullet.draw(surface)
            bullet.update()

    def shoot(self, target):
        self.bullets.append(Bullet(target))


class Target:
    def __init__(self):
        self.image = pygame.transform.scale(pygame.image.load("assets/target.png"), (32, 32))
        self.image.set_colorkey((255, 255, 255))
        self.pos = pygame.Vector2((random.randint(-32, 632), -50))
        self.rect = self.image.get_rect(center=self.pos)
        self.radian = 0
        self.typed = ""
        with open("keys.txt") as f:
            self.text = random.choice(f.read().split("\n")).lower()
            self.live = len(self.text)

    def draw(self, surface):
        global target
        surface.blit(self.image, self.pos)
        if self.typed == self.text:
            return
        if self.typed == "":
            render_text = font_20.render(self.text, False, (255, 255, 255))
        else:
            render_text_typed = font_20.render(self.typed, False, (252, 144, 3))
            render_text_empty = font_20.render(self.text[len(self.typed):], False, (255, 255, 255))
            render_text = pygame.Surface((render_text_empty.get_width() + render_text_typed.get_width(),
                                          render_text_empty.get_height())).convert_alpha()
            render_text.set_colorkey((0, 0, 0))
            render_text.blit(render_text_typed, (0, 0))
            render_text.blit(render_text_empty, (render_text_typed.get_width(), 0))
        x, y = self.pos.x + 16, self.pos.y + 16
        y -= render_text.get_height()
        if y < 0:
            y = 10
        if x - render_text.get_width() // 2 < 0:
            x = render_text.get_width() // 2
        if x > screen.get_width() - render_text.get_width() // 2:
            x = screen.get_width() - render_text.get_width() // 2
        surface.blit(render_text, (x - render_text.get_width() // 2, y - render_text.get_height() // 2))

    def update(self, player):
        if game_over:
            return
        self.radian = math.atan2(player.rect.centery-(self.pos.y + 16),
                                 player.rect.centerx-(self.pos.x+16))
        dx = math.cos(self.radian)
        dy = math.sin(self.radian)
        self.pos.x += dx * (70*dt)
        self.pos.y += dy * (70*dt)
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y


class Bullet:
    def __init__(self, target):
        self.image = pygame.image.load("assets/bullet.png")
        self.pos = pygame.Vector2((300, 700))
        self.rect = self.image.get_rect(center=self.pos)
        self.radian = 0
        self.target = target

    def draw(self, surface):
        surface.blit(self.image, self.pos)

    def update(self):
        if game_over:
            return
        self.radian = math.atan2(self.target.rect.centery-self.pos.y, self.target.rect.centerx-self.pos.x)
        dx = math.cos(self.radian)
        dy = math.sin(self.radian)
        self.pos.x += dx * (400 * dt)
        self.pos.y += dy * (400 * dt)
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y


def menu():
    global background, dt
    # Start Button Images
    start_button_image = pygame.transform.scale(pygame.image.load("assets/start.png"), (64 * 4, 32 * 4))
    start_button_image.set_colorkey((0, 0, 0))
    # Start Button Pressed Images
    start_button_pressed_image = pygame.transform.scale(pygame.image.load("assets/start_pressed.png"), (64 * 4, 32 * 4))
    start_button_pressed_image.set_colorkey((0, 0, 0))
    # Exit Button Images
    exit_button_image = pygame.transform.scale(pygame.image.load("assets/exit.png"), (64 * 4, 32 * 4))
    exit_button_image.set_colorkey((0, 0, 0))
    # Exit Button Pressed Images
    exit_button_pressed_image = pygame.transform.scale(pygame.image.load("assets/exit_pressed.png"), (64 * 4, 32 * 4))
    exit_button_pressed_image.set_colorkey((0, 0, 0))
    # Sound On Icon
    sound_on_image = pygame.transform.scale(pygame.image.load("assets/sound.png"), (32, 32))
    sound_on_image.set_colorkey((0, 0, 0))
    # Sound Mute Icon
    sound_mute_image = pygame.transform.scale(pygame.image.load("assets/mute.png"), (32, 32))
    sound_mute_image.set_colorkey((0, 0, 0))
    # Sound Button Rect
    sound_rect = pygame.Rect(0, screen.get_height() - sound_on_image.get_height(), 32, 32)

    # Buttons X Pos
    button_x = screen.get_width() // 2 - start_button_image.get_width() // 2

    # Elements
    tick = 300
    main_text_element = SysText(58, 120, "fonts/upheavtt.ttf", 90, "Type Fast!", (255, 255, 255))
    start_button = ImageButton(button_x, 300, start_button_image, start_button_pressed_image, ticks=80)
    exit_button = ImageButton(button_x, 500, exit_button_image, exit_button_pressed_image, ticks=80)

    # Gui
    gui = GUI()
    gui.add_element(start_button, 2)
    gui.add_element(exit_button, 1)
    gui.add_element(main_text_element)

    prev_time = time.time()

    sound_on = True
    clicked_button = None
    while True:
        now = time.time()
        dt = now - prev_time
        prev_time = now
        background.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                button = event.button
                if button == 1:
                    if sound_rect.collidepoint(event.pos):
                        sound_on = not sound_on
                        if not sound_on:
                            pygame.mixer.music.set_volume(0)
                            shoot_sound.set_volume(0)
                            explosion_sound.set_volume(0)
                        else:
                            pygame.mixer.music.set_volume(1)
                            shoot_sound.set_volume(1)
                            explosion_sound.set_volume(1)
        data = gui.draw(screen)

        if tick != 300:
            tick -= 1
        if tick == 0 and clicked_button == "start":
            break
        elif tick == 0 and clicked_button == "exit":
            pygame.quit()
            return

        if data[start_button]["click"] and tick == 300:
            tick -= 1
            clicked_button = "start"
        elif data[exit_button]["click"] and tick == 300:
            tick -= 1
            clicked_button = "exit"

        if sound_on:
            screen.blit(sound_on_image, sound_rect)
        else:
            screen.blit(sound_mute_image, sound_rect)
        pygame.display.update()
    main()


dt = 0


def new_wave():
    global wave, on_wave_text, spawn_timer
    wave += 1
    on_wave_text = True
    spawn_timer -= 0.2


def wave_text():
    global wave, wave_text_pos, dt, on_screen_middle, on_wave_text, spawn_period
    render = font_20.render(f"Wave {wave}", False, (255, 255, 255))
    wave_text_pos[0] = screen.get_width() // 2 - render.get_width() // 2
    if not on_screen_middle:
        wave_text_pos[1] += 800 * dt
    else:
        wave_text_pos[1] += dt * 50
    screen.blit(render, wave_text_pos)
    if wave_text_pos[1] >= screen.get_height() // 2 - render.get_height() // 2 and not on_screen_middle:
        on_screen_middle = True
    elif on_screen_middle and wave_text_pos[1] > 450:
        on_screen_middle = False
    if wave_text_pos[1] > screen.get_height():
        on_screen_middle = False
        on_wave_text = False
        wave_text_pos[1] = 0
        spawn_period = True


def main():
    global dt, background, targets, game_over, spawn_timer, spawn_period
    prev_time = time.time()
    last_spawn = time.time()
    added = 0
    player = Player()
    targets = []
    game_over_text = score_font.render("Game Over!", False, (255, 255, 255), (0, 0, 0))
    while True:
        now = time.time()
        dt = now - prev_time
        prev_time = now
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN and not game_over:
                if player.target is None:
                    typed = ""
                    if event.key == pygame.K_q: typed = "q"
                    if event.key == pygame.K_w: typed = "w"
                    if event.key == pygame.K_e: typed = "e"
                    if event.key == pygame.K_r: typed = "r"
                    if event.key == pygame.K_t: typed = "t"
                    if event.key == pygame.K_y: typed = "y"
                    if event.key == pygame.K_u: typed = "u"
                    if event.key == pygame.K_i: typed = "i"
                    if event.key == pygame.K_o: typed = "o"
                    if event.key == pygame.K_p: typed = "p"
                    if event.key == pygame.K_a: typed = "a"
                    if event.key == pygame.K_s: typed = "s"
                    if event.key == pygame.K_d: typed = "d"
                    if event.key == pygame.K_f: typed = "f"
                    if event.key == pygame.K_g: typed = "g"
                    if event.key == pygame.K_h: typed = "h"
                    if event.key == pygame.K_j: typed = "j"
                    if event.key == pygame.K_k: typed = "k"
                    if event.key == pygame.K_l: typed = "l"
                    if event.key == pygame.K_z: typed = "z"
                    if event.key == pygame.K_x: typed = "x"
                    if event.key == pygame.K_c: typed = "c"
                    if event.key == pygame.K_v: typed = "v"
                    if event.key == pygame.K_b: typed = "b"
                    if event.key == pygame.K_n: typed = "n"
                    if event.key == pygame.K_m: typed = "m"
                    filtered = list(filter(lambda tg: tg.text.startswith(typed) and tg.typed=="", targets))
                    if not filtered:
                        continue
                    if len(filtered) == 1:
                        player.target = filtered[0]
                        player.shoot(filtered[0])
                    else:
                        max_distance = 99999999999999
                        selected = None
                        for target in filtered:
                            distance = math.hypot(target.rect.x-player.rect.x, target.rect.y-player.rect.y)
                            if distance <= max_distance:
                                max_distance = distance
                                selected = target
                        player.target = selected
                        player.shoot(selected)
                    shoot_sound.play()
                    player.target.typed += typed

                else:
                    typed = ""
                    if event.key == pygame.K_q: typed = "q"
                    if event.key == pygame.K_w: typed = "w"
                    if event.key == pygame.K_e: typed = "e"
                    if event.key == pygame.K_r: typed = "r"
                    if event.key == pygame.K_t: typed = "t"
                    if event.key == pygame.K_y: typed = "y"
                    if event.key == pygame.K_u: typed = "u"
                    if event.key == pygame.K_i: typed = "i"
                    if event.key == pygame.K_o: typed = "o"
                    if event.key == pygame.K_p: typed = "p"
                    if event.key == pygame.K_a: typed = "a"
                    if event.key == pygame.K_s: typed = "s"
                    if event.key == pygame.K_d: typed = "d"
                    if event.key == pygame.K_f: typed = "f"
                    if event.key == pygame.K_g: typed = "g"
                    if event.key == pygame.K_h: typed = "h"
                    if event.key == pygame.K_j: typed = "j"
                    if event.key == pygame.K_k: typed = "k"
                    if event.key == pygame.K_l: typed = "l"
                    if event.key == pygame.K_z: typed = "z"
                    if event.key == pygame.K_x: typed = "x"
                    if event.key == pygame.K_c: typed = "c"
                    if event.key == pygame.K_v: typed = "v"
                    if event.key == pygame.K_b: typed = "b"
                    if event.key == pygame.K_n: typed = "n"
                    if event.key == pygame.K_m: typed = "m"
                    selected = player.target
                    if selected.text[len(selected.typed)] == typed:
                        player.shoot(selected)
                        selected.typed += typed
                        shoot_sound.play()
                        if selected.text == selected.typed:
                            player.target = None

        background.draw(screen)
        player.draw(screen)
        if game_over:
            score_text = score_font.render(f"Score: {player.score}", False, (255, 255, 255), (0, 0, 0))
            screen.blit(game_over_text, (screen.get_width() // 2 - game_over_text.get_width() // 2,
                                         screen.get_height() // 2 - game_over_text.get_height() // 2))
            screen.blit(score_text, (screen.get_width() // 2 - game_over_text.get_width() // 2,
                                     screen.get_height() // 2 - game_over_text.get_height() // 2 +
                                     game_over_text.get_height()))
        if on_wave_text:
            wave_text()
        for target in targets:
            target.draw(screen)
            target.update(player)
            if target.rect.colliderect(player.rect):
                game_over = True
            for bullet in filter(lambda bl: bl.target == target, player.bullets):
                if bullet.target == target and target.rect.colliderect(bullet.rect):
                    player.bullets.remove(bullet)
                    target.live -= 1
                    if target.live <= 0:
                        targets.remove(target)
                        explosion_sound.play()
                        player.score += 1
                        if player.target == target:
                            player.target = None
        pygame.display.update()
        if spawn_period and not game_over:
            if added == wave * 2:
                spawn_period = False
                added = 0
            if time.time() - last_spawn > spawn_timer:
                targets.append(Target())
                last_spawn = time.time()
                added += 1
        if len(targets) == 0 and not on_wave_text and not spawn_period and not game_over:
            new_wave()

if __name__ == '__main__':
    menu()
