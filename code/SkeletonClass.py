from pico2d import *

IDLE, LEFT_MOVE, RIGHT_MOVE, ATTACK = range(4)


class IdleState:
    @staticmethod
    def enter(skeleton):
        pass

    @staticmethod
    def exit(skeleton):
        pass

    @staticmethod
    def do(skeleton):
        skeleton.frame = (skeleton.frame + 1) % 6
        # add attack-area check later

    @staticmethod
    def draw(skeleton):
        if skeleton.dir == -1:
            Skeleton.image.clip_draw(skeleton.frame * 33, 0, 33, 30, skeleton.x, skeleton.y, 33, 90)
        elif skeleton.dir == 1:
            Skeleton.image.clip_draw(skeleton.frame * 33, 30, 33, 30, skeleton.x, skeleton.y, 33, 90)


class LeftMoveState:
    @staticmethod
    def enter(skeleton):
        skeleton.dir = -1

    @staticmethod
    def exit(skeleton):
        pass

    @staticmethod
    def do(skeleton):
        skeleton.x += skeleton.dir * skeleton.speed
        skeleton.frame = (skeleton.frame + 1) % 6
        # add attack-area check later

    @staticmethod
    def draw(skeleton):
        Skeleton.image.clip_draw(skeleton.frame * 33, 60, 33, 30, skeleton.x, skeleton.y, 33, 90)


class RightMoveState:
    @staticmethod
    def enter(skeleton):
        skeleton.dir = 1

    @staticmethod
    def exit(skeleton):
        pass

    @staticmethod
    def do(skeleton):
        skeleton.x += skeleton.dir * skeleton.speed
        skeleton.frame = (skeleton.frame + 1) % 6
        # add attack-area check later

    @staticmethod
    def draw(skeleton):
        Skeleton.image.clip_draw(skeleton.frame * 33, 60, 33, 30, skeleton.x, skeleton.y, 33, 90)


class AttackState:
    @staticmethod
    def enter(skeleton):
        pass

    @staticmethod
    def exit(skeleton):
        skeleton.atk_frame = 0

    @staticmethod
    def do(skeleton):
        skeleton.atk_frame = (skeleton.atk_frame + 1) % 12
        # if atk_frame is 2~6 collision check with player later
        if skeleton.atk_frame > 11:
            skeleton.add_event(IDLE)

    @staticmethod
    def draw(skeleton):
        if skeleton.dir == -1:
            Skeleton.Atk_image.clip_draw(skeleton.atk_frame * 71, 0, 71, 48, skeleton.x - 18, skeleton.y + 30, 71, 144)
        elif skeleton.dir == 1:
            Skeleton.Atk_image.clip_draw(skeleton.atk_frame * 71, 48, 71, 48, skeleton.x + 18, skeleton.y + 30, 70, 144)


next_state_table = {
    IdleState: {IDLE: IdleState, LEFT_MOVE: LeftMoveState,
                RIGHT_MOVE: RightMoveState, ATTACK: AttackState},

    LeftMoveState: {IDLE: IdleState, LEFT_MOVE: LeftMoveState,
                    RIGHT_MOVE: RightMoveState, ATTACK: AttackState},

    RightMoveState: {IDLE: IdleState, LEFT_MOVE: LeftMoveState,
                     RIGHT_MOVE: RightMoveState, ATTACK: AttackState},

    AttackState: {IDLE: IdleState, LEFT_MOVE: LeftMoveState,
                  RIGHT_MOVE: RightMoveState}
}


class Skeleton:
    image = None
    Atk_image = None

    def __init__(self):
        if Skeleton.image is None:
            Skeleton.image = load_image("Skel(33x30).png")
        if Skeleton.Atk_image is None:
            Skeleton.Atk_image = load_image("SkelAtk(71x48).png")
        self.hp = 60
        self.atk = 7
        self.dir = 1
        self.x, self.y = 600, 90
        self.speed = 1
        self.frame = 0
        self.atk_frame = 0
        self.cur_state = IdleState
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
