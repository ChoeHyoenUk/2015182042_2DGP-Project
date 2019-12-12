from pico2d import *
from FireSword import FireSword
from Zweihander import Zweihander
import game_framework
import threading
import normal_stage
import boss_stage

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
            player.weapons[i].hitbox_x = (30 * math.cos(0 / 360 * 2 * math.pi)) + player.x
            player.weapons[i].hitbox_y = (30 * math.sin(0 / 360 * 2 * math.pi)) + (player.y - 20)
            player.weapons[i].hitbox_minus_x = (30 * math.cos(180 / 360 * 2 * math.pi)) + player.x
            player.weapons[i].hitbox_minus_y = (30 * math.sin(180 / 360 * 2 * math.pi)) + (player.y - 20)
        player.frame = (player.frame + 4 * (1.0 / 0.5) * game_framework.frame_time) % 4

    @staticmethod
    def draw(player):
        cx, cy = player.x - player.bg.window_left, player.y - player.bg.window_bottom
        if player.stand_dir == 1:
            player.image.clip_draw(int(player.frame) * 32, 32, 32, 32, cx, cy, 60, 60)
        else:
            player.image.clip_draw(int(player.frame) * 32, 0, 32, 32, cx, cy, 60, 60)

        player.weapons[player.selected_weapon].draw()
        if player.weapons[player.selected_weapon].isswing:
            player.weapons[player.selected_weapon].swing()
        player.font.draw(cx - 35, cy + 20, 'HP : %d' % player.hp, (255, 0, 0))


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
        player.x = clamp(0, player.x, player.bg.w)
        player.y = clamp(0, player.y, player.bg.h)
        for i in range(2):
            player.weapons[i].x = (30 * math.cos(player.weapons[i].angle / 360 * 2 * math.pi)) + player.x
            player.weapons[i].y = (30 * math.sin(player.weapons[i].angle / 360 * 2 * math.pi)) + (player.y - 20)
            player.weapons[i].hitbox_x = (30 * math.cos(0 / 360 * 2 * math.pi)) + player.x
            player.weapons[i].hitbox_y = (30 * math.sin(0 / 360 * 2 * math.pi)) + (player.y - 20)
            player.weapons[i].hitbox_minus_x = (30 * math.cos(180 / 360 * 2 * math.pi)) + player.x
            player.weapons[i].hitbox_minus_y = (30 * math.sin(180 / 360 * 2 * math.pi)) + (player.y - 20)
        player.frame = (player.frame + 4 * (1.0 / 0.5) * game_framework.frame_time) % 4
        player.move_sound.play()

    @staticmethod
    def draw(player):
        cx, cy = player.x - player.bg.window_left, player.y - player.bg.window_bottom
        if player.stand_dir == 1:
            player.image.clip_draw(int(player.frame) * 32, 96, 32, 32, cx, cy, 60, 60)
        else:
            player.image.clip_draw(int(player.frame) * 32, 64, 32, 32, cx, cy, 60, 60)

        player.weapons[player.selected_weapon].draw()
        if player.weapons[player.selected_weapon].isswing:
            player.weapons[player.selected_weapon].swing()
        player.font.draw(cx - 35, cy + 20, 'HP : %d' % player.hp, (255, 0, 0))


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
        player.x = clamp(0, player.x, player.bg.w)
        player.y = clamp(0, player.y, player.bg.h)
        for i in range(2):
            player.weapons[i].x = (30 * math.cos(player.weapons[i].angle / 360 * 2 * math.pi)) + player.x
            player.weapons[i].y = (30 * math.sin(player.weapons[i].angle / 360 * 2 * math.pi)) + (player.y - 20)
            player.weapons[i].hitbox_x = (30 * math.cos(0 / 360 * 2 * math.pi)) + player.x
            player.weapons[i].hitbox_y = (30 * math.sin(0 / 360 * 2 * math.pi)) + (player.y - 20)
            player.weapons[i].hitbox_minus_x = (30 * math.cos(180 / 360 * 2 * math.pi)) + player.x
            player.weapons[i].hitbox_minus_y = (30 * math.sin(180 / 360 * 2 * math.pi)) + (player.y - 20)
        player.frame = (player.frame + 4 * (1.0 / 0.5) * game_framework.frame_time) % 4
        player.move_sound.play()

    @staticmethod
    def draw(player):
        cx, cy = player.x - player.bg.window_left, player.y - player.bg.window_bottom
        if player.stand_dir == 1:
            player.image.clip_draw(int(player.frame) * 32, 96, 32, 32, cx, cy, 60, 60)
        else:
            player.image.clip_draw(int(player.frame) * 32, 64, 32, 32, cx, cy, 60, 60)

        player.weapons[player.selected_weapon].draw()
        if player.weapons[player.selected_weapon].isswing:
            player.weapons[player.selected_weapon].swing()
        player.font.draw(cx - 35, cy + 20, 'HP : %d' % player.hp, (255, 0, 0))


class JumpState:
    @staticmethod
    def enter(player, event):
        if not player.jumping:
            player.jumping = True
            player.j_pos = player.y
            player.jump_sound.play()

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
        player.x = clamp(0, player.x, player.bg.w)
        player.y = clamp(0, player.y, player.bg.h)
        player.jump_time += 0.02
        for i in range(2):
            player.weapons[i].x = (30 * math.cos(player.weapons[i].angle / 360 * 2 * math.pi)) + player.x
            player.weapons[i].y = (30 * math.sin(player.weapons[i].angle / 360 * 2 * math.pi)) + (player.y - 20)
            player.weapons[i].hitbox_x = (30 * math.cos(0 / 360 * 2 * math.pi)) + player.x
            player.weapons[i].hitbox_y = (30 * math.sin(0 / 360 * 2 * math.pi)) + (player.y - 20)
            player.weapons[i].hitbox_minus_x = (30 * math.cos(180 / 360 * 2 * math.pi)) + player.x
            player.weapons[i].hitbox_minus_y = (30 * math.sin(180 / 360 * 2 * math.pi)) + (player.y - 20)
        if player.y < player.j_pos:
            player.add_event(COLLIDE)

    @staticmethod
    def draw(player):
        cx, cy = player.x - player.bg.window_left, player.y - player.bg.window_bottom
        if player.stand_dir == 1:
            player.image.clip_draw(0, 160, 32, 32, cx, cy, 60, 60)
        else:
            player.image.clip_draw(0, 128, 32, 32, cx, cy, 60, 60)

        player.weapons[player.selected_weapon].draw()
        if player.weapons[player.selected_weapon].isswing:
            player.weapons[player.selected_weapon].swing()
        player.font.draw(cx - 35, cy + 20, 'HP : %d' % player.hp, (255, 0, 0))


class LeftJumpState:
    @staticmethod
    def enter(player, event):
        if not player.jumping:
            player.jumping = True
            player.j_pos = player.y
            player.jump_sound.play()
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
        player.x = clamp(0, player.x, player.bg.w)
        player.y = clamp(0, player.y, player.bg.h)
        player.jump_time += 0.02
        for i in range(2):
            player.weapons[i].x = (30 * math.cos(player.weapons[i].angle / 360 * 2 * math.pi)) + player.x
            player.weapons[i].y = (30 * math.sin(player.weapons[i].angle / 360 * 2 * math.pi)) + (player.y - 20)
            player.weapons[i].hitbox_x = (30 * math.cos(0 / 360 * 2 * math.pi)) + player.x
            player.weapons[i].hitbox_y = (30 * math.sin(0 / 360 * 2 * math.pi)) + (player.y - 20)
            player.weapons[i].hitbox_minus_x = (30 * math.cos(180 / 360 * 2 * math.pi)) + player.x
            player.weapons[i].hitbox_minus_y = (30 * math.sin(180 / 360 * 2 * math.pi)) + (player.y - 20)
        if player.y < player.j_pos:
            player.add_event(COLLIDE)

    @staticmethod
    def draw(player):
        cx, cy = player.x - player.bg.window_left, player.y - player.bg.window_bottom
        if player.stand_dir == 1:
            player.image.clip_draw(0, 160, 32, 32, cx, cy, 60, 60)
        else:
            player.image.clip_draw(0, 128, 32, 32, cx, cy, 60, 60)

        player.weapons[player.selected_weapon].draw()
        if player.weapons[player.selected_weapon].isswing:
            player.weapons[player.selected_weapon].swing()
        player.font.draw(cx - 35, cy + 20, 'HP : %d' % player.hp, (255, 0, 0))


class RightJumpState:
    @staticmethod
    def enter(player, event):
        if not player.jumping:
            player.jumping = True
            player.j_pos = player.y
            player.jump_sound.play()
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
        player.x = clamp(0, player.x, player.bg.w)
        player.y = clamp(0, player.y, player.bg.h)
        player.jump_time += 0.02
        for i in range(2):
            player.weapons[i].x = (30 * math.cos(player.weapons[i].angle / 360 * 2 * math.pi)) + player.x
            player.weapons[i].y = (30 * math.sin(player.weapons[i].angle / 360 * 2 * math.pi)) + (player.y - 20)
            player.weapons[i].hitbox_x = (30 * math.cos(0 / 360 * 2 * math.pi)) + player.x
            player.weapons[i].hitbox_y = (30 * math.sin(0 / 360 * 2 * math.pi)) + (player.y - 20)
            player.weapons[i].hitbox_minus_x = (30 * math.cos(180 / 360 * 2 * math.pi)) + player.x
            player.weapons[i].hitbox_minus_y = (30 * math.sin(180 / 360 * 2 * math.pi)) + (player.y - 20)
        if player.y < player.j_pos:
            player.add_event(COLLIDE)

    @staticmethod
    def draw(player):
        cx, cy = player.x - player.bg.window_left, player.y - player.bg.window_bottom
        if player.stand_dir == 1:
            player.image.clip_draw(0, 160, 32, 32, cx, cy, 60, 60)
        else:
            player.image.clip_draw(0, 128, 32, 32, cx, cy, 60, 60)

        player.weapons[player.selected_weapon].draw()
        if player.weapons[player.selected_weapon].isswing:
            player.weapons[player.selected_weapon].swing()
        player.font.draw(cx - 35, cy + 20, 'HP : %d' % player.hp, (255, 0, 0))


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
        player.x = clamp(0, player.x, player.bg.w)
        player.y = clamp(0, player.y, player.bg.h)
        player.jump_time += 0.02
        for i in range(2):
            player.weapons[i].x = (30 * math.cos(player.weapons[i].angle / 360 * 2 * math.pi)) + player.x
            player.weapons[i].y = (30 * math.sin(player.weapons[i].angle / 360 * 2 * math.pi)) + (player.y - 20)
            player.weapons[i].hitbox_x = (30 * math.cos(0 / 360 * 2 * math.pi)) + player.x
            player.weapons[i].hitbox_y = (30 * math.sin(0 / 360 * 2 * math.pi)) + (player.y - 20)
            player.weapons[i].hitbox_minus_x = (30 * math.cos(180 / 360 * 2 * math.pi)) + player.x
            player.weapons[i].hitbox_minus_y = (30 * math.sin(180 / 360 * 2 * math.pi)) + (player.y - 20)
        if player.y < 85:
            player.add_event(COLLIDE)

    @staticmethod
    def draw(player):
        cx, cy = player.x - player.bg.window_left, player.y - player.bg.window_bottom
        if player.stand_dir == 1:
            player.image.clip_draw(0, 160, 32, 32, cx, cy, 60, 60)
        else:
            player.image.clip_draw(0, 128, 32, 32, cx, cy, 60, 60)

        player.weapons[player.selected_weapon].draw()
        if player.weapons[player.selected_weapon].isswing:
            player.weapons[player.selected_weapon].swing()
        player.font.draw(cx - 35, cy + 20, 'HP : %d' % player.hp, (255, 0, 0))


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
        player.x = clamp(0, player.x, player.bg.w)
        player.y = clamp(0, player.y, player.bg.h)
        player.jump_time += 0.02
        for i in range(2):
            player.weapons[i].x = (30 * math.cos(player.weapons[i].angle / 360 * 2 * math.pi)) + player.x
            player.weapons[i].y = (30 * math.sin(player.weapons[i].angle / 360 * 2 * math.pi)) + (player.y - 20)
            player.weapons[i].hitbox_x = (30 * math.cos(0 / 360 * 2 * math.pi)) + player.x
            player.weapons[i].hitbox_y = (30 * math.sin(0 / 360 * 2 * math.pi)) + (player.y - 20)
            player.weapons[i].hitbox_minus_x = (30 * math.cos(180 / 360 * 2 * math.pi)) + player.x
            player.weapons[i].hitbox_minus_y = (30 * math.sin(180 / 360 * 2 * math.pi)) + (player.y - 20)
        if player.y < 85:
            player.add_event(COLLIDE)

    @staticmethod
    def draw(player):
        cx, cy = player.x - player.bg.window_left, player.y - player.bg.window_bottom
        if player.stand_dir == 1:
            player.image.clip_draw(0, 160, 32, 32, cx, cy, 60, 60)
        else:
            player.image.clip_draw(0, 128, 32, 32, cx, cy, 60, 60)

        player.weapons[player.selected_weapon].draw()
        if player.weapons[player.selected_weapon].isswing:
            player.weapons[player.selected_weapon].swing()
        player.font.draw(cx - 35, cy + 20, 'HP : %d' % player.hp, (255, 0, 0))


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
        player.x = clamp(0, player.x, player.bg.w)
        player.y = clamp(0, player.y, player.bg.h)
        player.jump_time += 0.02
        for i in range(2):
            player.weapons[i].x = (30 * math.cos(player.weapons[i].angle / 360 * 2 * math.pi)) + player.x
            player.weapons[i].y = (30 * math.sin(player.weapons[i].angle / 360 * 2 * math.pi)) + (player.y - 20)
            player.weapons[i].hitbox_x = (30 * math.cos(0 / 360 * 2 * math.pi)) + player.x
            player.weapons[i].hitbox_y = (30 * math.sin(0 / 360 * 2 * math.pi)) + (player.y - 20)
            player.weapons[i].hitbox_minus_x = (30 * math.cos(180 / 360 * 2 * math.pi)) + player.x
            player.weapons[i].hitbox_minus_y = (30 * math.sin(180 / 360 * 2 * math.pi)) + (player.y - 20)
        if player.y < 85:
            player.add_event(COLLIDE)

    @staticmethod
    def draw(player):
        cx, cy = player.x - player.bg.window_left, player.y - player.bg.window_bottom
        if player.stand_dir == 1:
            player.image.clip_draw(0, 160, 32, 32, cx, cy, 60, 60)
        else:
            player.image.clip_draw(0, 128, 32, 32, cx, cy, 60, 60)

        player.weapons[player.selected_weapon].draw()
        if player.weapons[player.selected_weapon].isswing:
            player.weapons[player.selected_weapon].swing()
        player.font.draw(cx - 35, cy + 20, 'HP : %d' % player.hp, (255, 0, 0))


class DashState:
    @staticmethod
    def enter(player, event):
        if player.timer is None:
            player.timer = threading.Timer(2, player.dash_timer)
            print("timer set")
        if not player.is_dash_timer_run:
            player.is_dash_timer_run = True
            player.timer = threading.Timer(2, player.dash_timer)
            player.timer.start()
            print("timer start")
        player.image.opacify(0.5)
        player.opacity_mode = True
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
            player.opacity_mode = False

    @staticmethod
    def do(player):
        t = player.dash_distance / 100
        player.x = (1 - t) * player.dash_start_position[0] + t * player.dash_end_position[0]
        player.y = (1 - t) * player.dash_start_position[1] + t * player.dash_end_position[1]
        player.x = clamp(0, player.x, player.bg.w)
        player.y = clamp(0, player.y, player.bg.h)
        player.dash_distance += 300 * game_framework.frame_time
        for i in range(2):
            player.weapons[i].x = (30 * math.cos(player.weapons[i].angle / 360 * 2 * math.pi)) + player.x
            player.weapons[i].y = (30 * math.sin(player.weapons[i].angle / 360 * 2 * math.pi)) + (player.y - 20)
            player.weapons[i].hitbox_x = (30 * math.cos(0 / 360 * 2 * math.pi)) + player.x
            player.weapons[i].hitbox_y = (30 * math.sin(0 / 360 * 2 * math.pi)) + (player.y - 20)
            player.weapons[i].hitbox_minus_x = (30 * math.cos(180 / 360 * 2 * math.pi)) + player.x
            player.weapons[i].hitbox_minus_y = (30 * math.sin(180 / 360 * 2 * math.pi)) + (player.y - 20)
        if player.dash_distance > 100:
            player.add_event(MAX_DISTANCE)
        player.frame = (player.frame + 4 * (1.0 / 0.5) * game_framework.frame_time) % 4

    @staticmethod
    def draw(player):
        cx, cy = player.x - player.bg.window_left, player.y - player.bg.window_bottom
        if player.stand_dir == -1:
            player.image.clip_draw(int(player.frame) * 32, 64, 32, 32, cx, cy, 60, 60)
        elif player.stand_dir == 1:
            player.image.clip_draw(int(player.frame) * 32, 96, 32, 32, cx, cy, 60, 60)

        player.weapons[player.selected_weapon].draw()
        player.font.draw(cx - 35, cy + 20, 'HP : %d' % player.hp, (255, 0, 0))


next_state_table = {
    IdleState: {A_DOWN: LeftMoveState, D_DOWN: RightMoveState,
                A_UP: IdleState, D_UP: IdleState,
                SPACE_DOWN: JumpState, RBUTTON_DOWN: DashState,
                LBUTTON_DOWN: IdleState, COLLIDE: IdleState},

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
        self.weapons = [FireSword(self.x, self.y, 3, 0.3, 49, 60, "Fire_Sword.png", "Fire_Swing.png"),
                        Zweihander(self.x, self.y, 15, 0.3, 70, 90, "Zweihander.png", "Swing.png")]
        self.selected_weapon = 0
        self.hp = 100
        self.jump_power, self.jump_time = 6.5, 0
        self.dash_distance = 0
        self.dash_count = 6
        self.frame = 0
        self.opacity_mode = False

        self.jump_start_position, self.dash_start_position, self.dash_end_position = None, None, None
        self.jumping, self.falling, self.attack = False, False, True

        self.timer = None
        self.is_dash_timer_run = False

        self.event_que = []
        self.cur_state.enter(self, None)

        self.move_sound = load_wav('move.wav')
        self.jump_sound = load_wav('jump.wav')
        self.move_sound.set_volume(64)
        self.jump_sound.set_volume(64)
        self.font = load_font('ENCR10B.TTF', 16)

    def get_bb(self):
        return self.x - 15, self.y - 30, self.x + 15, self.y

    def collide(self, b):
        left_a, bottom_a, right_a, top_a = self.get_bb()

        left_b, bottom_b, right_b, top_b = b.get_bb()

        if left_a > right_b: return False
        if right_a < left_b: return False
        if top_a < bottom_b: return False
        if bottom_a > top_b: return False
        return True

    def dash_timer(self):
        if self.dash_count < 6:
            self.dash_count += 1
            if self.dash_count >= 6:
                self.is_dash_timer_run = False
                return
            else:
                self.timer = threading.Timer(2, self.dash_timer)
                self.timer.start()

    def set_background(self, back):
        self.bg = back

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

    def handle_event(self, event):
        cx, cy = self.x - self.bg.window_left, self.y - self.bg.window_bottom

        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)

        elif (event.type, event.button) == (SDL_MOUSEBUTTONDOWN, SDL_BUTTON_LEFT):
            self.add_event(LBUTTON_DOWN)

        elif (event.type, event.button) == (SDL_MOUSEBUTTONDOWN, SDL_BUTTON_RIGHT):
            if self.dash_count > 0:
                # x축 거리 확인
                if event.x - cx > 230:
                    end_x = self.x + 230
                elif event.x - cx < -230:
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
                self.dash_count -= 1
                self.add_event(RBUTTON_DOWN)