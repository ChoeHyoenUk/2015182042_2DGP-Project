from pico2d import *
import main_state

PATTERN_START, PATTERN_END = range(2)


class IdleState:
    @staticmethod
    def enter(boss_hand):
        pass

    @staticmethod
    def exit(boss_hand):
        pass

    @staticmethod
    def do(boss_hand):
        pass

    @staticmethod
    def draw(boss_hand):
        boss_hand.image.draw(boss_hand.x, boss_hand.y)


class AttackState:
    @staticmethod
    def enter(boss_hand):
        boss_hand.x, boss_hand.y = main_state.player.x - 80, main_state.player.y

    @staticmethod
    def exit(boss_hand):
        boss_hand.frame = 0

    @staticmethod
    def do(boss_hand):
        boss_hand.frame += 1
        if boss_hand.frame >= 9:
            boss_hand.add_event(PATTERN_END)

    @staticmethod
    def draw(boss_hand):
        boss_hand.atk_image.clip_draw(boss_hand.frame * 70, 0, 70, 80, boss_hand.x, boss_hand.y)
        if boss_hand.frame >= 2:
            boss_hand.laser.clip_draw(0, boss_hand.frame * 55, 320, 55, boss_hand.x + 195, boss_hand.y)


next_state_table = {
    IdleState: {PATTERN_START: AttackState},
    AttackState: {PATTERN_END: IdleState}
}


class Boss_Hand:
    def __init__(self, hand_image, atk_image, x, y):
        self.image = load_image(hand_image)
        self.atk_image = load_image(atk_image)
        self.laser = load_image("Boss_Laser(320x55).png")
        self.x, self.y = x, y
        self.cur_state = IdleState
        self.frame = 0
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