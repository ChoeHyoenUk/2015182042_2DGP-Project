import game_framework
from pico2d import *
import os
import main_state

os.chdir('C:\\Users\\levy-\\Desktop\\1\\2DGP\\2015182042_2DGP-Project\\TEXTURE')

name = "StartState"

bg_image = None
grass = None
charactor = None
dungeon_entrance = None

x = 100
c_frame = 0
e_frame = 0


def enter():
    global bg_image
    global charactor
    global grass
    global dungeon_entrance

    bg_image = load_image('Intro_BankGround.png')
    charactor = load_image('Character_Sheet(32x32).png')
    grass = load_image('grass.png')
    dungeon_entrance = load_image('Enterance(117x85).png')


def exit():
    global bg_image
    global charactor
    global grass
    global dungeon_entrance

    del bg_image
    del charactor
    del grass
    del dungeon_entrance


def update():
    global x, c_frame, e_frame

    if x < 600:
        x += 1
        c_frame = (c_frame + 1) % 4
    else:
        e_frame = e_frame + 1

    if e_frame == 28:
        game_framework.change_state(main_state)


def draw():
    global bg_image
    global charactor
    global grass
    global dungeon_entrance
    global x, c_frame, e_frame

    clear_canvas()

    bg_image.draw(400, 300, 800, 600)
    grass.draw(400, 30)
    if x < 600:
        charactor.clip_draw(c_frame * 32, 96, 32, 32, x, 85, 60, 60)
        x += 1
    else:
        dungeon_entrance.clip_draw(e_frame * 117, 0, 117, 85, x, 100)
        charactor.clip_draw(0, 32, 32, 32, x, 85, 60, 60)

    if e_frame == 28:
        game_framework.change_state(main_state)
    delay(0.02)
    update_canvas()


def handle_events():
    events = get_events()
    pass


def pause(): pass


def resume(): pass
