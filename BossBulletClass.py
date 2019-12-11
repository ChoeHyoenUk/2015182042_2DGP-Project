from pico2d import *
import game_world
import game_framework
import boss_stage


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

    def attack_collide(self):
        left_a, bottom_a, right_a, top_a = self.x - 6.5, self.y - 6.5, self.x + 6.5, self.y + 6.5

        left_b, bottom_b, right_b, top_b = boss_stage.player.x - 15, boss_stage.player.y - 30, \
                                           boss_stage.player.x + 15, boss_stage.player.y

        if left_a > right_b: return False
        if right_a < left_b: return False
        if top_a < bottom_b: return False
        if bottom_a > top_b: return False
        return True

    def update(self):
        self.x = Boss_Bullet.cen_x + (self.r * math.cos(self.angle / 360 * 2 * math.pi))
        self.y = Boss_Bullet.cen_y + (self.r * math.sin(self.angle / 360 * 2 * math.pi))
        self.r += 150 * game_framework.frame_time

        if self.attack_collide():
            boss_stage.player.hp -= Boss_Bullet.Atk
            print(boss_stage.player.hp)
            game_world.remove_object(self)

        if self.r >= 300:
            game_world.remove_object(self)

    def draw(self):
        Boss_Bullet.image.draw(self.x, self.y, 25, 25)
        draw_rectangle(self.x - 12.5, self.y - 12.5, self.x + 12.5, self.y + 12.5)
