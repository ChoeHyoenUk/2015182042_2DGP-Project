from pico2d import *
from math import *
import threading
import random
import enum
import os

os.chdir('C:\\Users\\levy-\\Desktop\\1\\2DGP\\2015182042_2DGP-Project\\TEXTURE')

open_canvas()
hide_cursor()

gravity = 6.2
M_x, M_y = 0, 0
ground = 85
running = True
frame = 0
d_timer_run = False

# 이미지
cursor = load_image("Cursor.png")
grass = load_image("grass.png")
d_count = load_image("DashCount.png")
d_board = load_image("DashCountBase.png")


class StateList(enum.Enum):
    IDLE = enum.auto()
    RUN = enum.auto()
    DASH = enum.auto()
    DEAD = enum.auto()
    ATK = enum.auto()
    FALL = enum.auto
    PATTERN1 = enum.auto()
    PATTERN2 = enum.auto()
    PATTERN3 = enum.auto()


class Weapon:
    def __init__(self, X, Y, ATK, COOLDOWN, W, H, SWORD_IMAGE, SWING_IMAGE):
        self.x, self.y = 0, 80
        self.draw_x, self.draw_y = 0, 0
        self.move_x, self.move_y = 0, 0
        self.atk = ATK
        self.cooldown = COOLDOWN
        self.H, self.W = H, W
        self.frame = 0
        self.image = load_image(SWORD_IMAGE)
        self.swing_image = load_image(SWING_IMAGE)
        self.angle = 0
        self.isswing = False

    def swing(self):
        if -90 <= self.angle <= 90:
            self.swing_image.clip_composite_draw(self.W * self.frame, 0, self.W, self.H, self.angle / 360 * 2 * math.pi,
                                                 'v',
                                                 self.x + (self.W / 2 * math.cos(self.angle / 360 * 2 * math.pi)),
                                                 self.y + (self.W / 2 * math.sin(self.angle / 360 * 2 * math.pi)),
                                                 self.W + 60, self.H + 35)
        else:
            self.swing_image.clip_composite_draw(self.W * self.frame, 0, self.W, self.H, self.angle / 360 * 2 * math.pi,
                                                 'v',
                                                 self.x + (self.W / 2 * math.cos(self.angle / 360 * 2 * math.pi)),
                                                 self.y + (self.W / 2 * math.sin(self.angle / 360 * 2 * math.pi)),
                                                 self.W + 60, self.H + 35)
        self.frame = (self.frame + 1) % 4

        if self.frame == 0:
            self.isswing = False
        delay(0.02)

    def draw(self):
        global player
        if player.stand_dir == 1:
            self.image.rotate_draw(self.angle / 360 * 2 * pi, self.x, self.y, 25, 50)
        else:
            self.image.composite_draw(self.angle / 360 * 2 * pi, 'v', self.x, self.y, 25, 50)


class Player:

    def __init__(self):
        self.image = load_image("Character_Sheet(32x32).png")

        self.state = StateList.IDLE
        self.dir = 0
        self.stand_dir = 1

        self.speed = 0.7
        self.x, self.y = 400, 85
        self.weapons = Weapon(self.x, self.y, 7, 0.3, 49, 60, "Fire_Sword.png", "Fire_Swing.png")
        self.hp = 100
        self.atk = 7
        self.j_power, self.j_time = 6.5, 0
        self.dash_distance = 0
        self.dash_count = 6
        self.frame = 0
        self.opacity_mode = False

        self.j_pos, self.d_start, self.d_end = None, None, None
        self.isjumping, self.falling, self.attack = False, False, True

    def update(self):
        global gravity
        global ground

        if self.state == StateList.RUN:
            self.x += self.speed * self.dir
            self.x = clamp(20, self.x, 800 - 20)

        elif self.state == StateList.DASH:
            t = self.dash_distance / 100
            self.x = (1 - t) * self.d_start[0] + t * self.d_end[0]
            self.y = (1 - t) * self.d_start[1] + t * self.d_end[1]
            self.dash_distance += 1

            if self.dash_distance > 100:
                self.image.opacify(1)
                self.opacity_mode = False
                self.dash_distance = 0
                self.state = StateList.IDLE
                self.d_start = None
                self.d_end = None
                if self.y > ground:
                    self.falling = True
                    self.j_time = 0

        if self.isjumping:
            self.y = round(self.y + ((-gravity / 2) * self.j_time ** 2 + self.j_power * self.j_time))
            self.j_time += 0.02

            if self.y < self.j_pos:
                self.isjumping = False
                self.state = StateList.IDLE
                self.y = self.j_pos
                self.j_time = 0

        if self.falling:
            self.y = round(self.y + ((-gravity * self.j_time ** 2) / 2))
            self.j_time += 0.02

            if self.y < ground:
                self.falling = False
                self.state = StateList.IDLE
                self.y = ground
                self.j_time = 0

        player.weapons.x = ((20 * cos(player.weapons.angle / 360 * 2 * pi)) + player.x)
        player.weapons.y = (20 * sin(player.weapons.angle / 360 * 2 * pi)) + (player.y - 20)
        self.frame = (self.frame + 1) % 4

    def draw(self):
        if self.state == StateList.IDLE:
            if self.stand_dir == 1:
                if self.falling or self.isjumping:
                    self.image.clip_draw(0, 160, 32, 32, self.x, self.y, 80, 80)
                else:
                    self.image.clip_draw(self.frame * 32, 32, 32, 32, self.x, self.y, 80, 80)
            else:
                if self.falling or self.isjumping:
                    self.image.clip_draw(0, 128, 32, 32, self.x, self.y, 80, 80)
                else:
                    self.image.clip_draw(self.frame * 32, 0, 32, 32, self.x, self.y, 80, 80)

        elif self.state == StateList.RUN:
            if self.stand_dir == 1:
                if self.falling or self.isjumping:
                    self.image.clip_draw(0, 160, 32, 32, self.x, self.y, 80, 80)
                else:
                    self.image.clip_draw(self.frame * 32, 96, 32, 32, self.x, self.y, 80, 80)
            else:
                if self.falling or self.isjumping:
                    self.image.clip_draw(0, 128, 32, 32, self.x, self.y, 80, 80)
                else:
                    self.image.clip_draw(self.frame * 32, 64, 32, 32, self.x, self.y, 80, 80)

        elif self.state == StateList.DASH:
            if player.stand_dir == -1:
                self.image.clip_draw(self.frame * 32, 64, 32, 32, player.x, player.y, 80, 80)
            elif player.stand_dir == 1:
                self.image.clip_draw(self.frame * 32, 96, 32, 32, player.x, player.y, 80, 80)

        elif self.state == StateList.DEAD:
            self.image.clip_draw(0, 192, 32, 32, self.x, self.y, 80, 80)

        if self.weapons.isswing:
            self.weapons.swing()
        self.weapons.draw()


class Skeleton:
    image = None
    Atk_image = None

    def __init__(self):
        self.hp = 60
        self.atk = 7
        self.dir = -1
        self.x, self.y = 600, 90
        self.speed = 1
        self.frame = 0
        self.atk_frame = 0
        self.state = StateList.IDLE
        if Skeleton.image is None:
            Skeleton.image = load_image("Skel(33x30).png")
        if Skeleton.Atk_image is None:
            Skeleton.Atk_image = load_image("SkelAtk(71x48).png")

    '''
    def state_change(self):
        temp = random.randint(-1, 1)
        if temp == -1 or temp == 1:
            self.dir = temp
            self.state = StateList.RUN
        else:
            self.state == StateList.IDLE
    '''

    def update(self):
        if self.state == StateList.ATK:
            self.atk_frame = (self.atk_frame + 1) % 12
            if self.atk_frame == 0:
                self.state = StateList.IDLE

        else:
            if self.state == StateList.RUN:
                self.x += self.speed * self.dir
                self.x = clamp(20, self.x, 800 - 20)
            self.frame = (self.frame + 1) % 6

    def draw(self):
        if self.state == StateList.IDLE:
            if self.dir == -1:
                Skeleton.image.clip_draw(self.frame * 33, 0, 33, 30, self.x, self.y, 33, 90)
            elif self.dir == 1:
                Skeleton.image.clip_draw(self.frame * 33, 30, 33, 30, self.x, self.y, 33, 90)

        elif self.state == StateList.RUN:
            if self.dir == -1:
                Skeleton.image.clip_draw(self.frame * 33, 60, 33, 30, self.x, self.y, 33, 90)
            elif self.dir == 1:
                Skeleton.image.clip_draw(self.frame * 33, 90, 33, 30, self.x, self.y, 33, 90)

        elif self.state == StateList.ATK:
            if self.dir == -1:
                Skeleton.Atk_image.clip_draw(self.atk_frame * 71, 0, 71, 48, self.x - 18, self.y + 30, 71, 144)
            elif self.dir == 1:
                Skeleton.Atk_image.clip_draw(self.atk_frame * 71, 48, 71, 48, self.x + 18, self.y + 30, 70, 144)
            delay(0.02)


class Banshee:
    image = None

    def __init__(self):
        if Banshee.image is None:
            Banshee.image = load_image("Banshee(20x22).png")
        self.hp = 40
        self.x, self.y = random.randint(20, 780), random.randint(400, 500)
        self.dir = 1
        self.state = StateList.IDLE
        self.atk = 5
        self.frame = random.randint(0, 5)
        self.atk_frame = 0

    def update(self):
        global player

        if self.state == StateList.ATK:
            self.atk_frame = (self.atk_frame + 1) % 6
            if self.atk_frame == 0:
                self.state = StateList.IDLE

        else:
            if self.x <= player.x:
                self.dir = 1
            else:
                self.dir = -1
        self.frame = (self.frame + 1) % 6

    def draw(self):
        if self.state == StateList.IDLE:
            if self.dir == 1:
                Banshee.image.clip_draw(self.frame * 20, 0, 20, 22, self.x, self.y, 30, 30)
            elif self.dir == -1:
                Banshee.image.clip_composite_draw(self.frame * 20, 0, 20, 22, 0, 'h', self.x, self.y, 30, 30)
        else:
            if self.dir == 1:
                Banshee.image.clip_draw(self.frame * 20, 22, 20, 22, self.x, self.y, 30, 30)
            elif self.dir == -1:
                Banshee.image.clip_composite_draw(self.frame * 20, 22, 20, 22, 0, 'h', self.x, self.y, 30, 30)


class Banshee_Bullet:
    image = None
    d_image = None

    def __init__(self, x, y, angle):
        if Banshee_Bullet.image is None:
            Banshee_Bullet.image = load_image("BanShee_Bullet(13x16).png")
        if Banshee_Bullet.d_image is None:
            Banshee_Bullet.d_image = load_image("Banshee_Bullet_Del(20x27).png")
        self.atk = 5
        self.r = 0
        self.cen_x, self.cen_y = x, y
        self.x, self.y = 0, 0
        self.angle = angle
        self.frame = 0

    def update(self):
        self.x = (self.r * cos(self.angle / 360 * 2 * pi)) + self.cen_x
        self.y = (self.r * sin(self.angle / 360 * 2 * pi)) + self.cen_y
        self.r += 3
        self.frame = (self.frame + 1) % 4

    def draw(self):
        Banshee_Bullet.image.clip_draw(self.frame * 13, 0, 13, 16, self.x, self.y, 20, 20)


class Belial_LEFT_Hand:
    def __init__(self, hand_image, atk_image, x, y):
        self.image = load_image(hand_image)
        self.atk_image = load_image(atk_image)
        self.laser = load_image("Boss_Laser(320x55).png")
        self.x, self.y = x, y
        self.state = StateList.IDLE
        self.frame = 0

    def update(self):
        if self.state == StateList.PATTERN2:
            if self.frame >= 9:
                self.frame = 0
                self.state = StateList.IDLE
                Berial_Pattern2(1)
            else:
                self.frame += 1

    def draw(self):
        if self.state == StateList.IDLE:
            self.image.draw(self.x, self.y)
        elif self.state == StateList.PATTERN2:
            self.atk_image.clip_draw(self.frame * 70, 0, 70, 80, self.x, self.y)
            if self.frame >= 2:
                self.laser.clip_draw(0, self.frame * 55, 320, 55, self.x + 195, self.y)
            delay(0.02)


class Belial_RIGHT_Hand:
    def __init__(self, hand_image, atk_image, x, y):
        self.image = load_image(hand_image)
        self.atk_image = load_image(atk_image)
        self.laser = load_image("Boss_Laser(320x55).png")
        self.x, self.y = x, y
        self.state = StateList.IDLE
        self.frame = 0

    def update(self):
        if self.state == StateList.PATTERN2:
            if self.frame >= 9:
                self.frame = 0
                self.state = StateList.IDLE
            else:
                self.frame += 1

    def draw(self):
        if self.state == StateList.IDLE:
            self.image.draw(self.x, self.y)
        elif self.state == StateList.PATTERN2:
            self.atk_image.clip_draw(self.frame * 70, 0, 70, 80, self.x, self.y)
            if self.frame >= 2:
                self.laser.clip_composite_draw(0, self.frame * 55, 320, 55, 0, 'h', self.x - 195, self.y, 320, 55)
            delay(0.02)


class Boss_Bullet:
    Atk = 7
    cen_x, cen_y = None, None
    image = None
    d_image = None

    def __init__(self, x, y, angle):
        if (Boss_Bullet.cen_x, Boss_Bullet.cen_y) == (None, None):
            Boss_Bullet.cen_x, Boss_Bullet.cen_y = x, y
        if Boss_Bullet.image is None:
            Boss_Bullet.image = load_image("BossBullet.png")
        if Boss_Bullet.d_image is None:
            Boss_Bullet.d_image = load_image("BossBullet_Del.png")
        self.x, self.y = 0, 0
        self.angle = angle
        self.r = 0

    def update(self):
        self.x = Boss_Bullet.cen_x + (self.r * cos(self.angle / 360 * 2 * pi))
        self.y = Boss_Bullet.cen_y + (self.r * sin(self.angle / 360 * 2 * pi))
        self.r += 1

    def draw(self):
        Boss_Bullet.image.draw(self.x, self.y, 25, 25)


class Boss_Sword:
    Atk = 15
    image = None

    def __init__(self, x):
        global player

        if Boss_Sword.image is None:
            Boss_Sword.image = load_image("BossSword.png")
        self.x, self.y = 300 + x, 500
        self.angle = 0
        self.state = StateList.IDLE
        self.start_x, self.start_y = self.x, self.y
        self. end_x, self.end_y = player.x, player.y - 40
        self.fall_distant = 0

    def update(self):
        global player
        if self.state == StateList.IDLE:
            self.angle = get_angle(self.x, self.y, player.x, player.y) + 90
            self.end_x, self.end_y = player.x, player.y - 40
        elif self.state == StateList.FALL:
            self.x = (1 - self.fall_distant) * self.start_x + self.fall_distant * self.end_x
            self.y = (1 - self.fall_distant) * self.start_y + self.fall_distant * self.end_y
            self.fall_distant += 0.003

    def draw(self):
        Boss_Sword.image.rotate_draw(self.angle/360*2*pi, self.x, self.y, 30, 120)


class Belial:
    def __init__(self):
        self.image = load_image("Boss(70x99).png")
        self.pattern1_image = load_image("Boss_Atk(70x128).png")
        self.Left_Hand = Belial_LEFT_Hand("Boss_LeftHand.png", "Boss_LH_Atk(70x80).png", 200, 200)
        self.Right_Hand = Belial_RIGHT_Hand("Boss_RightHand.png", "Boss_RH_Atk(70x80).png", 600, 200)
        self.hp = 250
        self.x, self.y = 400, 300
        self.frame = 0
        self.state = StateList.IDLE
        self.bullet_count = 0

    def update(self):
        global belial_bullets

        if self.state == StateList.PATTERN1:
            if self.bullet_count < 30:
                belial_bullets.append(Boss_Bullet(410, 270, self.bullet_count * 25))
                self.bullet_count += 1
            self.frame += 1
            self.frame = clamp(0, self.frame, 9)

            if self.bullet_count == 30:
                self.bullet_count = 0
                self.state = StateList.IDLE
        else:
            self.frame = (self.frame + 1) % 10

        self.Left_Hand.update()
        self.Right_Hand.update()

    def draw(self):
        if self.state == StateList.PATTERN1:
            self.pattern1_image.clip_draw(70 * self.frame, 0, 70, 128, self.x, self.y)
        else:
            self.image.clip_draw(70 * self.frame, 0, 70, 90, self.x, self.y)
        self.Left_Hand.draw()
        self.Right_Hand.draw()


def get_angle(start_x, start_y, end_x, end_y):
    dx = end_x - start_x
    dy = end_y - start_y
    return math.atan2(dy, dx) * (180 / math.pi)


def get_distant(x1, y1, x2, y2):
    return sqrt(pow(x2-x1, 2) + pow(y2-y1, 2))


def dash_timer_start():
    global player
    global d_timer_run
    timer = threading.Timer(2, dash_timer_start)

    if player.dash_count < 6:
        if not d_timer_run:
            d_timer_run = True
        else:
            player.dash_count += 1
        timer.start()
    else:
        d_timer_run = False


def attack_timer():
    global player
    player.attack = True


def attack_timer_start(cooldown):
    timer = threading.Timer(cooldown, attack_timer)
    timer.start()


def monster_state_chagne_timer():
    global skul_monster
    skul_monster.state_change()


def LEFT_Laser_Shot():
    global belial

    if not belial.Left_Hand.state == StateList.PATTERN2:
        belial.Left_Hand.state = StateList.PATTERN2


def RIGHT_Laser_Shot():
    global belial

    if not belial.Right_Hand.state == StateList.PATTERN2:
        belial.Right_Hand.state = StateList.PATTERN2


def Berial_Pattern2(hand):
    global belial
    global player

    if hand == -1:
        belial.Left_Hand.x, belial.Left_Hand.y = player.x - 80, player.y
        timer = threading.Timer(0.5, LEFT_Laser_Shot)
        timer.start()
    elif hand == 1:
        belial.Right_Hand.x, belial.Right_Hand.y = player.x + 80, player.y
        timer = threading.Timer(0.5, RIGHT_Laser_Shot)
        timer.start()


def Drop_Sword():
    global belial_sword
    if len(belial_sword) > 0:
        if not belial_sword[0].state == StateList.FALL:
            belial_sword[0].state = StateList.FALL


def handle_events():
    global player
    global running
    global M_x, M_y
    global d_timer_run
    global skul_monster
    global banshee
    global banshee_bullets
    global belial
    global belial_sword
    events = get_events()

    for event in events:
        if event.type == SDL_QUIT:
            running = False

        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False

        # 오른쪽 이동
        elif event.type == SDL_KEYDOWN and event.key == SDLK_d:
            if not player.state == StateList.DASH:
                player.state = StateList.RUN
                player.dir = 1

        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_RIGHT):
            if not skul_monster.state == StateList.ATK:
                skul_monster.state = StateList.RUN
                skul_monster.dir = 1

        # 왼쪽 이동
        elif event.type == SDL_KEYDOWN and event.key == SDLK_a:
            if not player.state == StateList.DASH:
                player.state = StateList.RUN
                player.dir = -1

        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_LEFT):
            if not skul_monster.state == StateList.ATK:
                skul_monster.state = StateList.RUN
                skul_monster.dir = -1

        # 점프
        elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            if not player.state == StateList.DASH and not player.isjumping and not player.falling:
                player.isjumping = True
                player.j_pos = player.y

        # 오른쪽 이동 중 정지
        elif event.type == SDL_KEYUP and event.key == SDLK_a:
            if not player.state == StateList.DASH:
                player.state = StateList.IDLE
                player.dir = 0

        elif (event.type, event.key) == (SDL_KEYUP, SDLK_RIGHT):
            skul_monster.state = StateList.IDLE

        # 왼쪽 이동 중 정지
        elif event.type == SDL_KEYUP and event.key == SDLK_d:
            if not player.state == StateList.DASH:
                player.state = StateList.IDLE
                player.dir = 0

        elif (event.type, event.key) == (SDL_KEYUP, SDLK_LEFT):
            skul_monster.state = StateList.IDLE

        # 사망
        elif event.type == SDL_KEYUP and event.key == SDLK_q:
            if not player.state == StateList.DASH:
                player.hp = 0
                player.state = StateList.DEAD

        # 부활
        elif event.type == SDL_KEYUP and event.key == SDLK_r:
            if not player.state == StateList.DASH:
                player.hp = 100
                player.state = StateList.IDLE
                player.dir = 0

        # 원위치
        elif event.type == SDL_KEYUP and event.key == SDLK_t:
            if not player.state == StateList.DASH:
                player.x, player.y = 400, 85
                player.weapons.x, player.weapons.y = 420, 90
                player.state = StateList.IDLE
                player.dir = 0

        # 마우스 이동
        elif event.type == SDL_MOUSEMOTION:
            M_x, M_y = event.x, 600 - 1 - event.y
            player.weapons.angle = get_angle(player.x, player.y, M_x, M_y)
            if player.x < M_x:
                player.stand_dir = 1
            elif player.x > M_x:
                player.stand_dir = -1

        # 마우스 우클릭(대쉬)
        elif event.type == SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_RIGHT:
            global ground

            if player.dash_count > 0:
                # x축 거리 확인
                if event.x - player.x > 230:
                    end_x = player.x + 230
                elif event.x - player.x < -230:
                    end_x = player.x - 230
                else:
                    end_x = event.x

                # y축 거리 확인
                if (600 - 1 - event.y) - player.y > 230:
                    end_y = player.y + 230
                elif (600 - 1 - event.y) - player.y < -230:
                    end_y = player.y - 230
                elif (600 - 1 - event.y) < ground:
                    end_y = ground
                else:
                    end_y = 600 - 1 - event.y

                player.dash_distance = 0
                player.isjumping, player.falling = False, False
                player.state = StateList.DASH
                player.d_start = (player.x, player.y)
                player.d_end = (end_x, end_y)
                player.dash_count -= 1

                if not d_timer_run:
                    dash_timer_start()

                if not player.opacity_mode:
                    player.opacity_mode = True
                    player.image.opacify(0.5)

            if player.dash_count == 0:
                print("U CAN'T DASH!!")


        # 마우스 좌클릭(공격)
        elif event.type == SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_LEFT:
            if player.attack:
                player.weapons.isswing = True
                player.attack = False
                attack_timer_start(player.weapons.cooldown)
            else:
                print("COOLTIME!!")

        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_KP_0):
            if not skul_monster.state == StateList.ATK:
                skul_monster.state = StateList.ATK

            for monster in banshee:
                if not monster.state == StateList.ATK:
                    monster.state = StateList.ATK
                    for i in range(12):
                        banshee_bullets.append(Banshee_Bullet(monster.x, monster.y, i * 30))

        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_b):
            if not belial.state == StateList.PATTERN1:
                belial.state = StateList.PATTERN1

        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_l):
            Berial_Pattern2(-1)

        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_k):
            if len(belial_sword) == 0:
                for i in range(5):
                    belial_sword.append(Boss_Sword(50 * i))
                timer = threading.Timer(5,Drop_Sword)
                timer.start()


player = Player()
skul_monster = Skeleton()
banshee = [Banshee() for i in range(5)]
belial = Belial()
banshee_bullets = []
belial_bullets = []
belial_sword = []

while running:
    clear_canvas()
    handle_events()

    player.update()

    belial.update()

    if len(belial_bullets) > 0:
        for bullet in belial_bullets:
            if bullet.r > 400:
                belial_bullets.remove(bullet)
            else:
                bullet.update()

    for monster in banshee:
        monster.update()

    skul_monster.update()

    if len(banshee_bullets) > 0:
        for bullet in banshee_bullets:
            if bullet.r > 300:
                banshee_bullets.remove(bullet)
            else:
                bullet.update()

    if len(belial_sword) > 0:
        for sword in belial_sword:
            if get_distant(sword.x, sword.y, sword.end_x, sword.end_y) <= 60:
                belial_sword.remove(sword)
                Drop_Sword()
            else:
                sword.update()

    grass.draw(400, 30)

    d_board.draw(48, 593, 96, 14)

    for n in range(player.dash_count):
        d_count.draw(((n + 1) * 16) - 8, 593, 14, 8)

    belial.draw()

    player.draw()

    if len(belial_bullets) > 0:
        for bullet in belial_bullets:
            bullet.draw()

    for monster in banshee:
        monster.draw()

    skul_monster.draw()

    if len(banshee_bullets) > 0:
        for bullet in banshee_bullets:
            bullet.draw()

    if len(belial_sword) > 0:
        for sword in belial_sword:
            sword.draw()

    cursor.draw(M_x, M_y)

    update_canvas()


close_canvas()
