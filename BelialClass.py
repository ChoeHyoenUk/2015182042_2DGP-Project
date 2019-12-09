from pico2d import *
from BossBulletClass import Boss_Bullet
from BossHandClass import Boss_Hand
import boss_state


PATTERN_START, PATTERN_END = range(2)


class IdleState:
    @staticmethod
    def enter(belial):
        pass

    @staticmethod
    def exit(belial):
        pass

    @staticmethod
    def do(belial):
        belial.frame = (belial.frame + 1) % 10
        belial.Left_Hand.update()
        belial.Right_Hand.update()

    @staticmethod
    def draw(belial):
        belial.image.clip_draw(70 * belial.frame, 0, 70, 90, belial.x, belial.y)
        belial.Left_Hand.draw()
        belial.Right_Hand.draw()


class AttackState:
    @staticmethod
    def enter(belial):
        pass

    @staticmethod
    def exit(belial):
        belial.bullet_count = 0

    @staticmethod
    def do(belial):
        if belial.bullet_count < 30:
            boss_state.belial_bullets.append(Boss_Bullet(410, 270, belial.bullet_count * 25))
            belial.bullet_count += 1
        belial.frame += 1
        belial.frame = clamp(0, belial.frame, 9)

        if belial.bullet_count == 30:
            belial.add_event(PATTERN_END)

    @staticmethod
    def draw(belial):
        belial.pattern1_image.clip_draw(70 * belial.frame, 0, 70, 128, belial.x, belial.y)


next_state_table = {
    IdleState: {PATTERN_START: AttackState},
    AttackState: {PATTERN_END: IdleState}
}


class Belial:
    def __init__(self):
        self.image = load_image("Boss(70x99).png")
        self.pattern1_image = load_image("Boss_Atk(70x128).png")
        self.Left_Hand = Boss_Hand("Boss_LeftHand.png", "Boss_LH_Atk(70x80).png", 200, 200)
        self.Right_Hand = Boss_Hand("Boss_RightHand.png", "Boss_RH_Atk(70x80).png", 600, 200)
        self.hp = 250
        self.x, self.y = 400, 300
        self.frame = 0
        self.cur_state = IdleState
        self.bullet_count = 0
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