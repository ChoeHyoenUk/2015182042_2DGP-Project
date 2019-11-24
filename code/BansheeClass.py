from pico2d import *
from BansheeBulletClass import Banshee_Bullet
import map2_state
import random

TimerEvent, AllBulletCreate = range(2)


class IdleState:

    @staticmethod
    def enter(banshee):
        pass

    @staticmethod
    def exit(banshee):
        banshee.frame = 0

    @staticmethod
    def do(banshee):
        if banshee.x > map2_state.player.x:
            banshee.stand_dir = -1
        else:
            banshee.stand_dir = 1
        banshee.frame = (banshee.frame + 1) % 6

    @staticmethod
    def draw(banshee):
        if banshee.stand_dir == 1:
            Banshee.image.clip_draw(banshee.frame * 20, 0, 20, 22, banshee.x, banshee.y, 30, 30)
        elif banshee.stand_dir == -1:
            Banshee.image.clip_composite_draw(banshee.frame * 20, 0, 20, 22, 0, 'h', banshee.x, banshee.y, 30, 30)


class AttackState:
    @staticmethod
    def enter(banshee):
        pass

    @staticmethod
    def exit(banshee):
        banshee.frame = 0

    @staticmethod
    def do(banshee):
        banshee.frame = (banshee.frame + 1) % 6
        if banshee.frame == 5:
            for i in range(12):
                map2_state.banshee_bullets.append(Banshee_Bullet(banshee.x, banshee.y, 30*i))
            banshee.add_event(AllBulletCreate)

    @staticmethod
    def draw(banshee):
        if banshee.stand_dir == 1:
            Banshee.image.clip_draw(banshee.frame * 20, 22, 20, 22, banshee.x, banshee.y, 30, 30)
        elif banshee.stand_dir == -1:
            Banshee.image.clip_composite_draw(banshee.frame * 20, 22, 20, 22, 0, 'h', banshee.x, banshee.y, 30, 30)


next_state_table = {
    IdleState: {TimerEvent: AttackState},
    AttackState: {TimerEvent: AttackState, AllBulletCreate: IdleState}
}


class Banshee:
    image = None

    def __init__(self):
        if Banshee.image is None:
            Banshee.image = load_image("Banshee(20x22).png")
        self.hp = 40
        self.x, self.y = random.randint(20, 780), random.randint(400, 500)
        self.stand_dir = 1
        self.cur_state = IdleState
        self.frame = random.randint(0, 5)
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
