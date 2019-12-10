from pico2d import *
from BehaviorTree import BehaviorTree, SelectorNode, SequenceNode, LeafNode
import boss_state
import threading

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
        boss_hand.x, boss_hand.y = boss_state.player.x - 80, boss_state.player.y

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
    def __init__(self, hand_image, atk_image, x, y, hand):
        self.image = load_image(hand_image)
        self.atk_image = load_image(atk_image)
        self.laser = load_image("Boss_Laser(320x55).png")
        self.x, self.y = x, y
        self.frame = 0
        self.which_hand = hand
        self.laser_pattern = False

    def laser_shot(self):
        if not self.laser_pattern:
            self.laser_pattern = True
        self.frame += 1
        if self.frame > 8:
            if self.which_hand == -1:
                self.frame = 0
                self.laser_pattern = False
                return 1
            else:
                self.frame = 0
                self.laser_pattern = False
                return 1
        return -1

    def update(self):
        pass

    def draw(self):
        if not self.laser_pattern:
            self.image.draw(self.x, self.y)
        else:
            self.atk_image.clip_draw(self.frame * 70, 0, 70, 80, self.x, self.y)
            if self.frame >= 2:
                if self.which_hand == -1:
                    self.laser.clip_draw(0, self.frame * 55, 320, 55, self.x + 195, self.y)
                else:
                    self.laser.clip_composite_draw(0, self.frame * 55, 320, 55, 0, 'h', self.x - 195, self.y, 320, 55)
