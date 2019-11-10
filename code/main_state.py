import threading
import enum
from pico2d import *
import game_framework
from PlayerClass import Player
from BansheeClass import Banshee
from SkeletonClass import Skeleton
from BelialClass import Belial

name = "MainState"

M_x, M_y = 0, 0
running = True
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
    PATTERN1 = enum.auto()
    PATTERN2 = enum.auto()
    PATTERN3 = enum.auto()


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
    bg_image = load_image("BackGround_Image.png")


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
    bg_image.draw(700, 300)
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