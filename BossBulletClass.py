from pico2d import *
import game_world


class Boss_Bullet:
    Atk = 7
    cen_x, cen_y = None, None
    image = None
    d_image = None

    def __init__(self, x, y, angle):
        if (Boss_Bullet.cen_x, Boss_Bullet.cen_y) == (None, None):
            Boss_Bullet.cen_x, Boss_Bullet.cen_y = x, y
        if Boss_Bullet.image is None:
            Boss_Bullet.image = load_image("BossBullet.png")
        if Boss_Bullet.d_image is None:
            Boss_Bullet.d_image = load_image("BossBullet_Del.png")
        self.x, self.y = 0, 0
        self.angle = angle
        self.r = 0

    def update(self):
        self.x = Boss_Bullet.cen_x + (self.r * math.cos(self.angle / 360 * 2 * math.pi))
        self.y = Boss_Bullet.cen_y + (self.r * math.sin(self.angle / 360 * 2 * math.pi))
        self.r += 1
        if self.r >= 300:
            game_world.remove_object(self)

    def draw(self):
        Boss_Bullet.image.draw(self.x, self.y, 25, 25)