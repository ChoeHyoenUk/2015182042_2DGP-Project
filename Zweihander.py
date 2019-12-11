from pico2d import *
import math
import game_framework
import normal_stage
import boss_stage


class Zweihander:
    def __init__(self, X, Y, ATK, COOLDOWN, W, H, SWORD_IMAGE, SWING_IMAGE):
        self.atk = ATK
        self.cooldown = COOLDOWN
        self.H, self.W = H, W
        self.frame = 0
        self.image = load_image(SWORD_IMAGE)
        self.swing_image = load_image(SWING_IMAGE)
        self.angle = 0
        self.x = (30 * math.cos(self.angle / 360 * 2 * math.pi)) + X
        self.y = (30 * math.sin(self.angle / 360 * 2 * math.pi)) + (Y - 20)
        self.hitbox_x, self.hitbox_y = self.x, self.y
        self.hitbox_minus_x = (30 * math.cos(180 / 360 * 2 * math.pi)) + X
        self.hitbox_minus_y = (30 * math.sin(180 / 360 * 2 * math.pi)) + (Y - 20)
        self.swing_sound = load_wav('fire_swing.wav')
        self.swing_sound.set_volume(32)
        self.sound_play = True
        self.isswing = False
        self.in_boss_stage = False


    def set_background(self, back):
        self.bg = back

    def attack_collide(self, monster):
        if -90 <= self.angle <= 90:
            left_a, bottom_a, right_a, top_a = self.hitbox_x - 17.5, self.hitbox_y - 55, \
                                               self.hitbox_x + 95, self.hitbox_y + 75
        else:
            left_a, bottom_a, right_a, top_a = self.hitbox_minus_x - 95, self.hitbox_minus_y - 55, \
                                               self.hitbox_minus_x + 17.5, self.hitbox_minus_y + 75

        left_b, bottom_b, right_b, top_b = monster.get_bb()

        if left_a > right_b: return False
        if right_a < left_b: return False
        if top_a < bottom_b: return False
        if bottom_a > top_b: return False
        return True

    def swing(self):
        cx, cy = self.x - self.bg.window_left, self.y - self.bg.window_bottom
        if self.sound_play:
            self.swing_sound.play()
            self.sound_play = False

        if -90 <= self.angle <= 90:
            self.swing_image.clip_composite_draw(self.W * int(self.frame), 0, self.W, self.H, self.angle / 360 * 2 * math.pi,
                                                 'v',
                                                 cx + (self.W / 2 * math.cos(self.angle / 360 * 2 * math.pi)),
                                                 cy + (self.W / 2 * math.sin(self.angle / 360 * 2 * math.pi)),
                                                 self.W + 60, self.H + 35)
        else:
            self.swing_image.clip_composite_draw(self.W * int(self.frame), 0, self.W, self.H, self.angle / 360 * 2 * math.pi,
                                                 'v',
                                                 cx + (self.W / 2 * math.cos(self.angle / 360 * 2 * math.pi)),
                                                 cy + (self.W / 2 * math.sin(self.angle / 360 * 2 * math.pi)),
                                                 self.W + 60, self.H + 35)

        if not self.in_boss_stage:
            for m in normal_stage.monsters:
                if self.attack_collide(m) and not m.hit:
                    m.hp -= self.atk
                    m.hit = True
        else:
            for m in boss_stage.monsters:
                if self.attack_collide(m) and not m.hit:
                    m.hp -= self.atk
                    print(m.hp)
                    m.hit = True

        self.frame = (self.frame + 4 * (1.0 / 0.5) * game_framework.frame_time)

        if self.frame >= 4:
            self.isswing = False
            if not self.in_boss_stage:
                for m in normal_stage.monsters:
                    m.hit = False
            else:
                for m in boss_stage.monsters:
                    m.hit = False
            self.sound_play = True

        self.frame %= 4

    def draw(self):
        cx, cy = self.x - self.bg.window_left, self.y - self.bg.window_bottom
        if -90 <= self.angle <= 90:
            self.image.rotate_draw(self.angle / 360 * 2 * math.pi, cx, cy, 25, 50)
        else:
            self.image.composite_draw(self.angle / 360 * 2 * math.pi, 'v', cx, cy, 25, 50)
