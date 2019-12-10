from pico2d import *
from FireSword import FireSword
from Zweihander import Zweihander
import game_framework

# Player Event
A_DOWN, A_UP, D_DOWN, D_UP, SPACE_DOWN, RBUTTON_DOWN, LBUTTON_DOWN, MAX_DISTANCE, COLLIDE = range(9)

key_event_table = {
    (SDL_KEYDOWN, SDLK_a): A_DOWN,
    (SDL_KEYUP, SDLK_a): A_UP,
    (SDL_KEYDOWN, SDLK_d): D_DOWN,
    (SDL_KEYUP, SDLK_d): D_UP,
    (SDL_KEYDOWN, SDLK_SPACE): SPACE_DOWN,
}


# States

class IdleState:
    @staticmethod
    def enter(player, event):
        if event == LBUTTON_DOWN:
            player.weapons[player.selected_weapon].isswing = True
        else:
            player.move_dir = 0

    @staticmethod
    def exit(player, event):
        pass

    @staticmethod
    def do(player):
        for i in range(2):
            player.weapons[i].x = (30 * math.cos(player.weapons[i].angle / 360 * 2 * math.pi)) + player.x
            player.weapons[i].y = (30 * math.sin(player.weapons[i].angle / 360 * 2 * math.pi)) + (player.y - 20)
        player.frame = (player.frame + 4 * (1.0 / 0.5) * game_framework.frame_time ) % 4

    @staticmethod
    def draw(player):
        if player.stand_dir == 1:
            player.image.clip_draw(int(player.frame) * 32, 32, 32, 32, player.x, player.y, 60, 60)
        else:
            player.image.clip_draw(int(player.frame) * 32, 0, 32, 32, player.x, player.y, 60, 60)

        player.weapons[player.selected_weapon].draw()
        if player.weapons[player.selected_weapon].isswing:
            player.weapons[player.selected_weapon].swing()


class LeftMoveState:
    @staticmethod
    def enter(player, event):
        if event == LBUTTON_DOWN:
            player.weapons[player.selected_weapon].isswing = True
        else:
            player.move_dir = -1

    @staticmethod
    def exit(player, event):
        pass

    @staticmethod
    def do(player):
        player.x += player.speed * player.move_dir * game_framework.frame_time
        for i in range(2):
            player.weapons[i].x = (30 * math.cos(player.weapons[i].angle / 360 * 2 * math.pi)) + player.x
            player.weapons[i].y = (30 * math.sin(player.weapons[i].angle / 360 * 2 * math.pi)) + (player.y - 20)
        player.frame = (player.frame + 4 * (1.0 / 0.5) * game_framework.frame_time ) % 4

    @staticmethod
    def draw(player):
        if player.stand_dir == 1:
            player.image.clip_draw(int(player.frame) * 32, 96, 32, 32, player.x, player.y, 60, 60)
        else:
            player.image.clip_draw(int(player.frame) * 32, 64, 32, 32, player.x, player.y, 60, 60)

        player.weapons[player.selected_weapon].draw()
        if player.weapons[player.selected_weapon].isswing:
            player.weapons[player.selected_weapon].swing()


class RightMoveState:
    @staticmethod
    def enter(player, event):
        if event == LBUTTON_DOWN:
            player.weapons[player.selected_weapon].isswing = True
        else:
            player.move_dir = 1

    @staticmethod
    def exit(player, event):
        pass

    @staticmethod
    def do(player):
        player.x += player.speed * player.move_dir * game_framework.frame_time
        for i in range(2):
            player.weapons[i].x = (30 * math.cos(player.weapons[i].angle / 360 * 2 * math.pi)) + player.x
            player.weapons[i].y = (30 * math.sin(player.weapons[i].angle / 360 * 2 * math.pi)) + (player.y - 20)
        player.frame = (player.frame + 4 * (1.0 / 0.5) * game_framework.frame_time ) % 4

    @staticmethod
    def draw(player):
        if player.stand_dir == 1:
            player.image.clip_draw(int(player.frame) * 32, 96, 32, 32, player.x, player.y, 60, 60)
        else:
            player.image.clip_draw(int(player.frame) * 32, 64, 32, 32, player.x, player.y, 60, 60)

        player.weapons[player.selected_weapon].draw()
        if player.weapons[player.selected_weapon].isswing:
            player.weapons[player.selected_weapon].swing()


class JumpState:
    @staticmethod
    def enter(player, event):
        if not player.jumping:
            player.jumping = True
            player.j_pos = player.y

        if event == LBUTTON_DOWN:
            player.weapons[player.selected_weapon].isswing = True

    @staticmethod
    def exit(player, event):
        if event == COLLIDE:
            player.jumping = False
            player.y = 85
            player.j_pos = None
            player.jump_time = 0

    @staticmethod
    def do(player):
        player.y = player.y + (
                    (-6.2 / 2) * player.jump_time ** 2 + player.jump_power * player.jump_time)  # 6.2 is gravity
        player.jump_time += 0.02
        for i in range(2):
            player.weapons[i].x = (30 * math.cos(player.weapons[i].angle / 360 * 2 * math.pi)) + player.x
            player.weapons[i].y = (30 * math.sin(player.weapons[i].angle / 360 * 2 * math.pi)) + (player.y - 20)
        if player.y < player.j_pos:
            player.add_event(COLLIDE)

    @staticmethod
    def draw(player):
        if player.stand_dir == 1:
            player.image.clip_draw(0, 160, 32, 32, player.x, player.y, 60, 60)
        else:
            player.image.clip_draw(0, 128, 32, 32, player.x, player.y, 60, 60)

        player.weapons[player.selected_weapon].draw()
        if player.weapons[player.selected_weapon].isswing:
            player.weapons[player.selected_weapon].swing()


class LeftJumpState:
    @staticmethod
    def enter(player, event):
        if not player.jumping:
            player.jumping = True
            player.j_pos = player.y
        player.move_dir = -1

        if event == LBUTTON_DOWN:
            player.weapons[player.selected_weapon].isswing = True

    @staticmethod
    def exit(player, event):
        if event == COLLIDE:
            player.jumping = False
            player.y = 85
            player.j_pos = None
            player.jump_time = 0

    @staticmethod
    def do(player):
        player.y = player.y + (
                    (-6.2 / 2) * player.jump_time ** 2 + player.jump_power * player.jump_time)  # 6.2 is gravity
        player.x += player.speed * player.move_dir * game_framework.frame_time
        player.jump_time += 0.02
        for i in range(2):
            player.weapons[i].x = (30 * math.cos(player.weapons[i].angle / 360 * 2 * math.pi)) + player.x
            player.weapons[i].y = (30 * math.sin(player.weapons[i].angle / 360 * 2 * math.pi)) + (player.y - 20)
        if player.y < player.j_pos:
            player.add_event(COLLIDE)

    @staticmethod
    def draw(player):
        if player.stand_dir == 1:
            player.image.clip_draw(0, 160, 32, 32, player.x, player.y, 60, 60)
        else:
            player.image.clip_draw(0, 128, 32, 32, player.x, player.y, 60, 60)

        player.weapons[player.selected_weapon].draw()
        if player.weapons[player.selected_weapon].isswing:
            player.weapons[player.selected_weapon].swing()


class RightJumpState:
    @staticmethod
    def enter(player, event):
        if not player.jumping:
            player.jumping = True
            player.j_pos = player.y
        player.move_dir = 1

        if event == LBUTTON_DOWN:
            player.weapons[player.selected_weapon].isswing = True

    @staticmethod
    def exit(player, event):
        if event == COLLIDE:
            player.jumping = False
            player.y = 85
            player.j_pos = None
            player.jump_time = 0

    @staticmethod
    def do(player):
        player.y = player.y + (
                    (-6.2 / 2) * player.jump_time ** 2 + player.jump_power * player.jump_time)  # 6.2 is gravity
        player.x += player.speed * player.move_dir * game_framework.frame_time
        player.jump_time += 0.02
        for i in range(2):
            player.weapons[i].x = (30 * math.cos(player.weapons[i].angle / 360 * 2 * math.pi)) + player.x
            player.weapons[i].y = (30 * math.sin(player.weapons[i].angle / 360 * 2 * math.pi)) + (player.y - 20)
        if player.y < player.j_pos:
            player.add_event(COLLIDE)

    @staticmethod
    def draw(player):
        if player.stand_dir == 1:
            player.image.clip_draw(0, 160, 32, 32, player.x, player.y, 60, 60)
        else:
            player.image.clip_draw(0, 128, 32, 32, player.x, player.y, 60, 60)

        player.weapons[player.selected_weapon].draw()
        if player.weapons[player.selected_weapon].isswing:
            player.weapons[player.selected_weapon].swing()


class FallState:
    @staticmethod
    def enter(player, event):
        if event == LBUTTON_DOWN:
            player.weapons[player.selected_weapon].isswing = True

    @staticmethod
    def exit(player, event):
        if event == COLLIDE:
            player.jump_time = 0
            player.y = 85  # 85 is y of groung

    @staticmethod
    def do(player):
        player.y = player.y + ((-6.2 * player.jump_time ** 2) / 2)  # 6.2 is gravity
        player.jump_time += 0.02
        for i in range(2):
            player.weapons[i].x = (30 * math.cos(player.weapons[i].angle / 360 * 2 * math.pi)) + player.x
            player.weapons[i].y = (30 * math.sin(player.weapons[i].angle / 360 * 2 * math.pi)) + (player.y - 20)
        if player.y < 85:
            player.add_event(COLLIDE)

    @staticmethod
    def draw(player):
        if player.stand_dir == 1:
            player.image.clip_draw(0, 160, 32, 32, player.x, player.y, 60, 60)
        else:
            player.image.clip_draw(0, 128, 32, 32, player.x, player.y, 60, 60)

        player.weapons[player.selected_weapon].draw()
        if player.weapons[player.selected_weapon].isswing:
            player.weapons[player.selected_weapon].swing()


class LeftFallState:
    @staticmethod
    def enter(player, event):
        player.jump_time = 0
        player.move_dir = -1
        if event == LBUTTON_DOWN:
            player.weapons[player.selected_weapon].isswing = True

    @staticmethod
    def exit(player, event):
        if event == COLLIDE:
            player.jump_time = 0
            player.y = 85  # 85 is y of groung

    @staticmethod
    def do(player):
        player.y = player.y + ((-6.2 * player.jump_time ** 2) / 2)  # 6.2 is gravity
        player.x += player.speed * player.move_dir * game_framework.frame_time
        player.jump_time += 0.02
        for i in range(2):
            player.weapons[i].x = (30 * math.cos(player.weapons[i].angle / 360 * 2 * math.pi)) + player.x
            player.weapons[i].y = (30 * math.sin(player.weapons[i].angle / 360 * 2 * math.pi)) + (player.y - 20)
        if player.y < 85:
            player.add_event(COLLIDE)

    @staticmethod
    def draw(player):
        if player.stand_dir == 1:
            player.image.clip_draw(0, 160, 32, 32, player.x, player.y, 60, 60)
        else:
            player.image.clip_draw(0, 128, 32, 32, player.x, player.y, 60, 60)

        player.weapons[player.selected_weapon].draw()
        if player.weapons[player.selected_weapon].isswing:
            player.weapons[player.selected_weapon].swing()


class RightFallState:
    @staticmethod
    def enter(player, event):
        player.move_dir = 1
        if event == LBUTTON_DOWN:
            player.weapons[player.selected_weapon].isswing = True

    @staticmethod
    def exit(player, event):
        if event == COLLIDE:
            player.jump_time = 0
            player.y = 85  # 85 is y of groung

    @staticmethod
    def do(player):
        player.y = player.y + ((-6.2 * player.jump_time ** 2) / 2)  # 6.2 is gravity
        player.x += player.speed * player.move_dir * game_framework.frame_time
        player.jump_time += 0.02
        for i in range(2):
            player.weapons[i].x = (30 * math.cos(player.weapons[i].angle / 360 * 2 * math.pi)) + player.x
            player.weapons[i].y = (30 * math.sin(player.weapons[i].angle / 360 * 2 * math.pi)) + (player.y - 20)
        if player.y < 85:
            player.add_event(COLLIDE)

    @staticmethod
    def draw(player):
        if player.stand_dir == 1:
            player.image.clip_draw(0, 160, 32, 32, player.x, player.y, 60, 60)
        else:
            player.image.clip_draw(0, 128, 32, 32, player.x, player.y, 60, 60)

        player.weapons[player.selected_weapon].draw()
        if player.weapons[player.selected_weapon].isswing:
            player.weapons[player.selected_weapon].swing()


class DashState:
    @staticmethod
    def enter(player, event):
        player.image.opacify(0.5)
        if event == RBUTTON_DOWN:
            player.dash_distance = 0
            player.dash_count -= 0

    @staticmethod
    def exit(player, event):
        if event == MAX_DISTANCE:
            player.image.opacify(1.0)
            player.dash_distance = 0
            player.dash_start_position = None
            player.dash_end_position = None

    @staticmethod
    def do(player):
        t = player.dash_distance / 100
        player.x = (1 - t) * player.dash_start_position[0] + t * player.dash_end_position[0]
        player.y = (1 - t) * player.dash_start_position[1] + t * player.dash_end_position[1]
        player.dash_distance += 300 * game_framework.frame_time
        for i in range(2):
            player.weapons[i].x = (30 * math.cos(player.weapons[i].angle / 360 * 2 * math.pi)) + player.x
            player.weapons[i].y = (30 * math.sin(player.weapons[i].angle / 360 * 2 * math.pi)) + (player.y - 20)
        if player.dash_distance > 100:
            player.add_event(MAX_DISTANCE)
        player.frame = (player.frame + 4 * (1.0 / 0.5) * game_framework.frame_time ) % 4

    @staticmethod
    def draw(player):
        if player.stand_dir == -1:
            player.image.clip_draw(int(player.frame) * 32, 64, 32, 32, player.x, player.y, 60, 60)
        elif player.stand_dir == 1:
            player.image.clip_draw(int(player.frame) * 32, 96, 32, 32, player.x, player.y, 60, 60)

        player.weapons[player.selected_weapon].draw()


next_state_table = {
    IdleState: {A_DOWN: LeftMoveState, D_DOWN: RightMoveState,
                A_UP: IdleState, D_UP: IdleState,
                SPACE_DOWN: JumpState, RBUTTON_DOWN: DashState,
                LBUTTON_DOWN: IdleState},

    LeftMoveState: {A_DOWN: LeftMoveState, A_UP: IdleState,
                    D_DOWN: RightMoveState, D_UP: LeftMoveState,
                    SPACE_DOWN: LeftJumpState, RBUTTON_DOWN: DashState,
                    LBUTTON_DOWN: LeftMoveState},

    RightMoveState: {D_DOWN: RightMoveState, D_UP: IdleState,
                     A_DOWN: LeftMoveState, A_UP: RightMoveState,
                     SPACE_DOWN: RightJumpState, RBUTTON_DOWN: DashState,
                     LBUTTON_DOWN: RightMoveState},

    JumpState: {A_DOWN: LeftJumpState, D_DOWN: RightJumpState,
                A_UP: JumpState, D_UP: JumpState,
                RBUTTON_DOWN: DashState, SPACE_DOWN: JumpState,
                LBUTTON_DOWN: JumpState, COLLIDE: IdleState},

    LeftJumpState: {A_DOWN: LeftJumpState, A_UP: JumpState,
                    D_DOWN: RightJumpState, D_UP: LeftJumpState,
                    SPACE_DOWN: LeftJumpState, RBUTTON_DOWN: DashState,
                    LBUTTON_DOWN: LeftJumpState, COLLIDE: LeftMoveState},

    RightJumpState: {D_DOWN: RightJumpState, D_UP: JumpState,
                     A_DOWN: LeftJumpState, A_UP: RightJumpState,
                     SPACE_DOWN: RightJumpState, RBUTTON_DOWN: DashState,
                     LBUTTON_DOWN: RightJumpState, COLLIDE: RightMoveState},

    DashState: {D_DOWN: DashState, D_UP: DashState,
                A_DOWN: DashState, A_UP: DashState,
                SPACE_DOWN: DashState, RBUTTON_DOWN: DashState, LBUTTON_DOWN: DashState,
                MAX_DISTANCE: FallState},

    FallState: {A_DOWN: LeftFallState, D_DOWN: RightFallState,
                A_UP: FallState, D_UP: FallState,
                SPACE_DOWN: FallState, RBUTTON_DOWN: DashState,
                LBUTTON_DOWN: FallState, COLLIDE: IdleState},

    LeftFallState: {A_DOWN: LeftFallState, A_UP: FallState,
                    D_DOWN: RightFallState, D_UP: LeftFallState,
                    SPACE_DOWN: LeftFallState, RBUTTON_DOWN: DashState,
                    LBUTTON_DOWN: LeftFallState, COLLIDE: LeftMoveState},

    RightFallState: {D_DOWN: RightFallState, D_UP: FallState,
                     A_DOWN: LeftFallState, A_UP: RightFallState,
                     SPACE_DOWN: RightFallState, RBUTTON_DOWN: DashState,
                     LBUTTON_DOWN: RightFallState, COLLIDE: RightMoveState},
}


class Player:

    def __init__(self):
        self.image = load_image("Character_Sheet(32x32).png")

        self.cur_state = IdleState
        self.move_dir = 0
        self.stand_dir = 1

        self.speed = 150
        self.x, self.y = 15, 85
        self.weapons = [FireSword(self.x, self.y, 7, 0.3, 49, 60, "Fire_Sword.png", "Fire_Swing.png"),
                        Zweihander(self.x, self.y, 7, 0.3, 70, 90, "Zweihander.png", "Swing.png")]
        self.selected_weapon = 0
        self.hp = 100
        self.jump_power, self.jump_time = 6.5, 0
        self.dash_distance = 0
        self.dash_count = 6
        self.frame = 0
        self.opacity_mode = False

        self.jump_start_position, self.dash_start_position, self.dash_end_position = None, None, None
        self.jumping, self.falling, self.attack = False, False, True

        self.event_que = []
        self.cur_state.enter(self, None)

    def update_state(self):
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            self.cur_state = next_state_table[self.cur_state][event]
            self.cur_state.enter(self, event)

    def add_event(self, event):
        self.event_que.insert(0, event)

    def update(self):
        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            self.cur_state = next_state_table[self.cur_state][event]
            self.cur_state.enter(self, event)

    def draw(self):
        self.cur_state.draw(self)
        draw_rectangle(self.x - 15, self.y - 30, self.x + 15, self.y)

    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)

        elif (event.type, event.button) == (SDL_MOUSEBUTTONDOWN, SDL_BUTTON_LEFT):
            self.add_event(LBUTTON_DOWN)

        elif (event.type, event.button) == (SDL_MOUSEBUTTONDOWN, SDL_BUTTON_RIGHT):
            if self.dash_count > 0:
                # x축 거리 확인
                if event.x - self.x > 230:
                    end_x = self.x + 230
                elif event.x - self.x < -230:
                    end_x = self.x - 230
                else:
                    end_x = event.x

                # y축 거리 확인
                if (600 - 1 - event.y) - self.y > 230:
                    end_y = self.y + 230
                elif (600 - 1 - event.y) - self.y < -230:
                    end_y = self.y - 230
                elif (600 - 1 - event.y) < 85:
                    end_y = 85
                else:
                    end_y = 600 - 1 - event.y

                self.dash_start_position = (self.x, self.y)
                self.dash_end_position = (end_x, end_y)

                self.add_event(RBUTTON_DOWN)