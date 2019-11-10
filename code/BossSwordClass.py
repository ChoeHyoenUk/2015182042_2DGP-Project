from pico2d import *
import math
import main_state

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
        boss_sword.angle = main_state.get_angle(boss_sword.x, boss_sword.y, main_state.player.x,
                                                main_state.player.y) + 90
        boss_sword.end_x, boss_sword.end_y = main_state.player.x, main_state.player.y - 40

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
    Atk = 15
    image = None

    def __init__(self, x):
        if Boss_Sword.image is None:
            Boss_Sword.image = load_image("BossSword.png")
        self.x, self.y = 300 + x, 500
        self.angle = 0
        self.cur_state = IdleState
        self.start_x, self.start_y = self.x, self.y
        self.end_x, self.end_y = main_state.player.x, main_state.player.y - 40
        self.fall_distant = 0
        self.event_que = []
        self.cur_state.enter(self)

    def update_state(self):
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self)
            self.cur_state = next_state_table[self.cur_state][event]
            self.cur_state.enter(self)

    def add_event(self, event):
        self.event_que.insert(0, event)

    def update(self):
        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self)
            self.cur_state = next_state_table[self.cur_state][event]
            self.cur_state.enter(self)

    def draw(self):
        self.cur_state.draw(self)