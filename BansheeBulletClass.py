from pico2d import *
import math
import game_world


class Banshee_Bullet:
    image = None
    d_image = None

    def __init__(self, x, y, angle):
        if Banshee_Bullet.image is None:
            Banshee_Bullet.image = load_image("BanShee_Bullet(13x16).png")
        if Banshee_Bullet.d_image is None:
            Banshee_Bullet.d_image = load_image("Banshee_Bullet_Del(20x27).png")
        self.atk = 5
        self.r = 0
        self.cen_x, self.cen_y = x, y
        self.x, self.y = 0, 0
        self.angle = angle
        self.frame = 0

    def update(self):
        self.x = (self.r * math.cos(self.angle / 360 * 2 * math.pi)) + self.cen_x
        self.y = (self.r * math.sin(self.angle / 360 * 2 * math.pi)) + self.cen_y
        self.r += 3
        if self.r >= 300:
            game_world.remove_object(self)
        self.frame = (self.frame + 1) % 4

    def draw(self):
        Banshee_Bullet.image.clip_draw(self.frame * 13, 0, 13, 16, self.x, self.y, 20, 20)