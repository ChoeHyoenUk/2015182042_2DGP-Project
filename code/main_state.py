import threading
import random
import enum
from pico2d import *
import game_framework
from PlayerClass import Player
from BansheeClass import Banshee

name = "MainState"

os.chdir('C:\\Users\\levy-\\Desktop\\1\\2DGP\\2015182042_2DGP-Project\\TEXTURE')

gravity = 6.2
M_x, M_y = 0, 0
ground = 85
running = True
frame = 0
d_timer_run = False

bg_image = None
grass = None
player = None
skul_monster = None
banshee = []
belial = None
banshee_bullets = []
belial_bullets = []
belial_sword = []
cursor = None
d_count = None
d_board = None


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
        self.x = Boss_Bullet.cen_x + (self.r * math.cos(self.angle / 360 * 2 * math.pi))
        self.y = Boss_Bullet.cen_y + (self.r * math.sin(self.angle / 360 * 2 * math.pi))
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
        self.end_x, self.end_y = player.x, player.y - 40
        self.fall_distant = 0

    def update(self):
        global player
        if self.state == StateList.IDLE:
            self.angle = get_angle(self.x, self.y, player.x, player.y) + 90
            self.end_x, self.end_y = player.x, player.y - 40
        elif self.state == StateList.FALL:
            self.x = (1 - self.fall_distant) * self.start_x + self.fall_distant * self.end_x
            self.y = (1 - self.fall_distant) * self.start_y + self.fall_distant * self.end_y
            self.fall_distant += 0.01

    def draw(self):
        Boss_Sword.image.rotate_draw(self.angle / 360 * 2 * math.pi, self.x, self.y, 30, 120)


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
    return math.sqrt(pow(x2 - x1, 2) + pow(y2 - y1, 2))


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
        timer.cancel()


def attack_timer():
    global player
    player.attack = True


def attack_timer_start(cooldown):
    timer = threading.Timer(cooldown, attack_timer)
    timer.start()


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


def enter():
    global player
    global grass
    global skul_monster
    global banshee
    global belial
    global cursor
    global d_count, d_board
    global bg_image

    player = Player()
    grass = load_image("grass.png")
    skul_monster = Skeleton()
    for i in range(5):
        banshee.append(Banshee())
    belial = Belial()
    cursor = load_image("Cursor.png")
    d_count = load_image("DashCount.png")
    d_board = load_image("DashCountBase.png")
    bg_image = load_image("SubBG-sharedassets7.assets-57.png")


def exit():
    global player
    global grass
    global skul_monster
    global banshee
    global belial

    del player
    del grass
    del skul_monster
    del banshee
    del belial


def pause():
    pass


def resume():
    pass

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
            game_framework.quit()

        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()

        elif event.type == SDL_MOUSEMOTION:
            M_x, M_y = event.x, 600 - 1 - event.y
            player.weapon.angle = get_angle(player.x, player.y, M_x, M_y)
            if player.x < M_x:
                player.stand_dir = 1
            elif player.x > M_x:
                player.stand_dir = -1

        else:
            player.handle_event(event)


def update():
    global player
    global skul_monster
    global banshee
    global belial
    global banshee_bullets
    global belial_bullets
    global belial_sword

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


def draw():
    global player
    global skul_monster
    global banshee
    global belial
    global banshee_bullets
    global belial_bullets
    global belial_sword
    global cursor
    global d_count, d_count

    clear_canvas()
    bg_image.draw(400, 300, 800, 600)
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

    cursor.draw(M_x, M_y, 30, 30)
    update_canvas()