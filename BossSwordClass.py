from pico2d import *
import math
import boss_state

IDLE, FALL = range(2)


class IdleState:
    @staticmethod
    def enter(boss_sword):
        pass

    @staticmethod
    def exit(boss_sword):
        pass

    @staticmethod
    def do(boss_sword):
        boss_sword.angle = boss_state.get_angle(boss_sword.x, boss_sword.y, boss_state.player.x,
                                                boss_state.player.y) + 90
        boss_sword.end_x, boss_sword.end_y = boss_state.player.x, boss_state.player.y - 40

    @staticmethod
    def draw(boss_sword):
        Boss_Sword.image.rotate_draw(boss_sword.angle / 360 * 2 * math.pi, boss_sword.x, boss_sword.y, 30, 120)


class FallState():
    @staticmethod
    def enter(boss_sword):
        pass

    @staticmethod
    def exit(boss_sword):
        pass

    @staticmethod
    def do(boss_sword):
        boss_sword.x = (1 - boss_sword.fall_distant) * boss_sword.start_x + boss_sword.fall_distant * boss_sword.end_x
        boss_sword.y = (1 - boss_sword.fall_distant) * boss_sword.start_y + boss_sword.fall_distant * boss_sword.end_y
        boss_sword.fall_distant += 0.01

    @staticmethod
    def draw(boss_sword):
        Boss_Sword.image.rotate_draw(boss_sword.angle / 360 * 2 * math.pi, boss_sword.x, boss_sword.y, 30, 120)


next_state_table = {IdleState: {FALL: FallState}}


class Boss_Sword:
    Atk = 3
    image = None

    def __init__(self, x):
        if Boss_Sword.image is None:
            Boss_Sword.image = load_image("BossSword.png")
        self.x, self.y = 300 + x, 500
        self.angle = 0
        self.state = 1
        self.start_x, self.start_y = self.x, self.y
        self.end_x, self.end_y = boss_state.player.x, boss_state.player.y - 40
        self.fall_distant = 0

    def update(self):
        if self.state == 1:
            self.angle = boss_state.get_angle(self.x, self.y, boss_state.player.x, boss_state.player.y) + 90
            self.end_x, self.end_y = boss_state.player.x, boss_state.player.y - 40
        else:
            self.x = (1 - self.fall_distant) * self.start_x + self.fall_distant * self.end_x
            self.y = (1 - self.fall_distant) * self.start_y + self.fall_distant * self.end_y
            self.fall_distant += 0.01
            if self.fall_distant >= 1:
                boss_state.belial_sword.remove(self)
                if len(boss_state.belial_sword) > 0:
                    boss_state.belial_sword[0].state = 0

    def draw(self):
        if self.state == 1:
            Boss_Sword.image.rotate_draw(self.angle / 360 * 2 * math.pi, self.x, self.y, 30, 120)
        else:
            Boss_Sword.image.rotate_draw(self.angle / 360 * 2 * math.pi, self.x, self.y, 30, 120)
