from pico2d import *

# Player Event
A_DOWN, A_UP, D_DOWN, D_UP, SPACE_DOWN, RBUTTON_DOWN, LBUTTON_DOWN, MAX_DISTANCE, COLLIDE = range(9)

key_event_table = {
    (SDL_KEYDOWN, SDLK_a): A_DOWN,
    (SDL_KEYUP, SDLK_a): A_UP,
    (SDL_KEYDOWN, SDLK_d): D_DOWN,
    (SDL_KEYUP, SDLK_d): D_UP,
    (SDL_KEYDOWN, SDLK_SPACE): SPACE_DOWN,
    (SDL_MOUSEBUTTONDOWN, SDL_BUTTON_LEFT): LBUTTON_DOWN,
    (SDL_MOUSEBUTTONDOWN, SDL_BUTTON_RIGHT): RBUTTON_DOWN,
}


# States

class IdleState:
    @staticmethod
    def enter(player, event):
        player.dir = 0

    @staticmethod
    def exit(player, event):
        pass

    @staticmethod
    def do(player):
        player.frame = (player.frame + 1) % 4

    @staticmethod
    def draw(player):
        if player.stand_dir == 1:
            player.image.clip_draw(player.frame * 32, 32, 32, 32, player.x, player.y, 60, 60)
        else:
            player.image.clip_draw(player.frame * 32, 0, 32, 32, player.x, player.y, 60, 60)


class LeftMoveState:
    @staticmethod
    def enter(player, event):
        player.dir = -1

    @staticmethod
    def exit(player, event):
        pass

    @staticmethod
    def do(player):
        player.x += player.speed * player.dir
        player.frame = (player.frame + 1) % 4

    @staticmethod
    def draw(player):
        if player.stand_dir == 1:
            player.image.clip_draw(player.frame * 32, 96, 32, 32, player.x, player.y, 60, 60)
        else:
            player.image.clip_draw(player.frame * 32, 64, 32, 32, player.x, player.y, 60, 60)


class RightMoveState:
    @staticmethod
    def enter(player, event):
        player.dir = 1

    @staticmethod
    def exit(player, event):
        pass

    @staticmethod
    def do(player):
        player.x += player.speed * player.dir
        player.frame = (player.frame + 1) % 4

    @staticmethod
    def draw(player):
        if player.stand_dir == 1:
            player.image.clip_draw(player.frame * 32, 96, 32, 32, player.x, player.y, 60, 60)
        else:
            player.image.clip_draw(player.frame * 32, 64, 32, 32, player.x, player.y, 60, 60)


class JumpState:
    @staticmethod
    def enter(player, event):
        if not player.isjumping:
            player.isjumping = True
            player.j_pos = player.y

    @staticmethod
    def exit(player, event):
        if event == COLLIDE:
            player.isjumping = False
            player.j_pos = None
            player.j_time = 0

    @staticmethod
    def do(player):
        player.y = player.y + ((-6.2 / 2) * player.j_time ** 2 + player.j_power * player.j_time)  # 6.2 is gravity
        player.j_time += 0.02

        if player.y < player.j_pos:
            player.add_event(COLLIDE)

    @staticmethod
    def draw(player):
        if player.stand_dir == 1:
            player.image.draw(0, 160, 32, 32, player.x, player.y, 60, 60)
        else:
            player.image.draw(0, 128, 32, 32, player.x, player.y, 60, 60)


class LeftJumpState:
    @staticmethod
    def enter(player, event):
        if not player.isjumping:
            player.isjumping = True
            player.j_pos = player.y
        player.dir = -1

    @staticmethod
    def exit(player, event):
        if event == COLLIDE:
            player.isjumping = False
            player.j_pos = None
            player.j_time = 0

    @staticmethod
    def do(player):
        player.y = player.y + ((-6.2 / 2) * player.j_time ** 2 + player.j_power * player.j_time)  # 6.2 is gravity
        player.x += player.speed * player.dir
        player.j_time += 0.02

        if player.y < player.j_pos:
            player.add_event(COLLIDE)

    @staticmethod
    def draw(player):
        if player.stand_dir == 1:
            player.image.draw(0, 160, 32, 32, player.x, player.y, 60, 60)
        else:
            player.image.draw(0, 128, 32, 32, player.x, player.y, 60, 60)


class RightJumpState:
    @staticmethod
    def enter(player, event):
        if not player.isjumping:
            player.isjumping = True
            player.j_pos = player.y
        player.dir = 1

    @staticmethod
    def exit(player, event):
        if event == COLLIDE:
            player.isjumping = False
            player.j_pos = None
            player.j_time = 0

    @staticmethod
    def do(player):
        player.y = player.y + ((-6.2 / 2) * player.j_time ** 2 + player.j_power * player.j_time)  # 6.2 is gravity
        player.x += player.speed * player.dir
        player.j_time += 0.02

        if player.y < player.j_pos:
            player.add_event(COLLIDE)

    @staticmethod
    def draw(player):
        if player.stand_dir == 1:
            player.image.draw(0, 160, 32, 32, player.x, player.y, 60, 60)
        else:
            player.image.draw(0, 128, 32, 32, player.x, player.y, 60, 60)


class FallState:
    @staticmethod
    def enter(player, event):
        player.j_time = 0

    @staticmethod
    def exit(player, event):
        if event == COLLIDE:
            player.j_time = 0
            player.y = 85  # 85 is y of groung

    @staticmethod
    def do(player):
        player.y = player.y + ((-6.2 * player.j_time ** 2) / 2)  # 6.2 is gravity
        player.j_time += 0.02

        if player.y < 85:
            player.add_event(COLLIDE)

    @staticmethod
    def draw(player):
        if player.stand_dir == 1:
            player.image.draw(0, 160, 32, 32, player.x, player.y, 60, 60)
        else:
            player.image.draw(0, 128, 32, 32, player.x, player.y, 60, 60)


class LeftFallState:
    @staticmethod
    def enter(player, event):
        player.j_time = 0
        player.dir = -1

    @staticmethod
    def exit(player, event):
        if event == COLLIDE:
            player.j_time = 0
            player.y = 85  # 85 is y of groung

    @staticmethod
    def do(player):
        player.y = player.y + ((-6.2 * player.j_time ** 2) / 2)  # 6.2 is gravity
        player.x += player.speed * player.dir
        player.j_time += 0.02

        if player.y < 85:
            player.add_event(COLLIDE)

    @staticmethod
    def draw(player):
        if player.stand_dir == 1:
            player.image.draw(0, 160, 32, 32, player.x, player.y, 60, 60)
        else:
            player.image.draw(0, 128, 32, 32, player.x, player.y, 60, 60)


class RightFallState:
    @staticmethod
    def enter(player, event):
        player.j_time = 0

    @staticmethod
    def exit(player, event):
        if event == COLLIDE:
            player.j_time = 0
            player.y = 85  # 85 is y of groung

    @staticmethod
    def do(player):
        player.y = player.y + ((-6.2 * player.j_time ** 2) / 2)  # 6.2 is gravity
        player.j_time += 0.02

        if player.y < 85:
            player.add_event(COLLIDE)

    @staticmethod
    def draw(player):
        if player.stand_dir == 1:
            player.image.draw(0, 160, 32, 32, player.x, player.y, 60, 60)
        else:
            player.image.draw(0, 128, 32, 32, player.x, player.y, 60, 60)


class LeftFallState:
    @staticmethod
    def enter(player, event):
        player.j_time = 0
        player.dir = 1

    @staticmethod
    def exit(player, event):
        if event == COLLIDE:
            player.j_time = 0
            player.y = 85  # 85 is y of groung

    @staticmethod
    def do(player):
        player.y = player.y + ((-6.2 * player.j_time ** 2) / 2)  # 6.2 is gravity
        player.x += player.speed * player.dir
        player.j_time += 0.02

        if player.y < 85:
            player.add_event(COLLIDE)

    @staticmethod
    def draw(player):
        if player.stand_dir == 1:
            player.image.draw(0, 160, 32, 32, player.x, player.y, 60, 60)
        else:
            player.image.draw(0, 128, 32, 32, player.x, player.y, 60, 60)


class DashState:
    @staticmethod
    def enter(player, event):
        pass

    @staticmethod
    def exit(player,event):
        pass

    @staticmethod
    def do(player):
        pass

    @staticmethod
    def draw(player):
        pass

    pass


next_state_table = {
    IdleState: {A_DOWN: LeftMoveState, D_DOWN: RightMoveState,
                SPACE_DOWN: JumpState, RBUTTON_DOWN: DashState,
                LBUTTON_DOWN: IdleState},

    LeftMoveState: {A_UP: IdleState, D_DOWN: RightMoveState, D_UP: LeftMoveState,
                    SPACE_DOWN: LeftJumpState, RBUTTON_DOWN: DashState,
                    LBUTTON_DOWN: LeftMoveState},

    RightMoveState: {D_UP: IdleState, A_DOWN: LeftMoveState, A_UP: RightMoveState,
                     SPACE_DOWN: RightJumpState, RBUTTON_DOWN: DashState,
                     LBUTTON_DOWN: RightMoveState},

    JumpState: {A_DOWN: LeftJumpState, D_DOWN: RightJumpState,
                RBUTTON_DOWN: DashState, SPACE_DOWN: JumpState,
                LBUTTON_DOWN: JumpState, COLLIDE: IdleState},

    LeftJumpState: {A_UP: JumpState, D_DOWN: RightJumpState, D_UP: LeftJumpState,
                    SPACE_DOWN: LeftJumpState, RBUTTON_DOWN: DashState,
                    LBUTTON_DOWN: LeftJumpState, COLLIDE: LeftMoveState},

    RightJumpState: {D_UP: JumpState, A_DOWN: LeftJumpState, A_UP: RightJumpState,
                     SPACE_DOWN: LeftJumpState, RBUTTON_DOWN: DashState,
                     LBUTTON_DOWN: RightJumpState, COLLIDE: RightMoveState},

    DashState: {D_DOWN: DashState, D_UP: DashState,
                A_DOWN: DashState, A_UP: DashState,
                SPACE_DOWN: DashState, RBUTTON_DOWN: DashState, LBUTTON_DOWN: DashState,
                MAX_DISTANCE: FallState},

    FallState: {A_DOWN: LeftFallState, D_DOWN: RightFallState,
                SPACE_DOWN: FallState, RBUTTON_DOWN: DashState,
                LBUTTON_DOWN: FallState, COLLIDE: IdleState},

    LeftFallState: {A_UP: FallState, D_DOWN: RightFallState, D_UP: LeftFallState,
                    SPACE_DOWN: LeftFallState, RBUTTON_DOWN: DashState,
                    LBUTTON_DOWN: LeftFallState, COLLIDE: LeftMoveState},

    RightFallState: {D_UP: FallState, A_DOWN: LeftFallState, A_UP: RightFallState,
                     SPACE_DOWN: RightFallState, RBUTTON_DOWN: DashState,
                     LBUTTON_DOWN: RightFallState, COLLIDE: RightMoveState},
}
