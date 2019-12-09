from pico2d import *
import math


class FireSword:
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
        self.isswing = False

    def swing(self):
        if -90 <= self.angle <= 90:
            self.swing_image.clip_composite_draw(self.W * self.frame, 0, self.W, self.H, self.angle / 360 * 2 * math.pi,
                                                 'v',
                                                 self.x + (self.W / 2 * math.cos(self.angle / 360 * 2 * math.pi)),
                                                 self.y + (self.W / 2 * math.sin(self.angle / 360 * 2 * math.pi)),
                                                 self.W + 60, self.H + 35)
        else:
            self.swing_image.clip_composite_draw(self.W * self.frame, 0, self.W, self.H, self.angle / 360 * 2 * math.pi,
                                                 'v',
                                                 self.x + (self.W / 2 * math.cos(self.angle / 360 * 2 * math.pi)),
                                                 self.y + (self.W / 2 * math.sin(self.angle / 360 * 2 * math.pi)),
                                                 self.W + 60, self.H + 35)
        self.frame = (self.frame + 1) % 4

        if self.frame == 0:
            self.isswing = False

    def draw(self):
        if -90 <= self.angle <= 90:
            self.image.rotate_draw(self.angle / 360 * 2 * math.pi, self.x, self.y, 25, 50)
        else:
            self.image.composite_draw(self.angle / 360 * 2 * math.pi, 'v', self.x, self.y, 25, 50)
