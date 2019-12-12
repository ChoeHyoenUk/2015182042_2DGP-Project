from pico2d import *
from BansheeBulletClass import Banshee_Bullet
from BehaviorTree import BehaviorTree, SelectorNode, SequenceNode, LeafNode
import normal_stage
import game_world
import random
import threading
import game_framework


class Banshee:
    image = None

    def __init__(self, x):
        if Banshee.image is None:
            Banshee.image = load_image("Banshee(20x22).png")
        self.hp = 30
        self.x, self.y = x, random.randint(300, 350)
        self.stand_dir = 1
        self.frame = random.randint(0, 5)
        self.can_attack = True
        self.timer = None
        self.attacking = False
        self.hit = False
        self.font = load_font('ENCR10B.TTF', 16)
        self.build_behavior_tree()

    def set_background(self, back):
        self.bg = back

    def get_bb(self):
        return self.x - 15, self.y - 15, self.x + 15, self.y + 15

    def set_can_attack(self):
        self.can_attack = True

    def cooltime_check(self):
        if self.can_attack:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def attack(self):
        if not self.attacking:
            self.frame = 0
            self.attacking = True

        self.frame = (self.frame + 6 * (1.0 / 0.5) * game_framework.frame_time)
        if self.frame >= 6:
            for i in range(12):
                game_world.add_object(Banshee_Bullet(self.x, self.y, 30 * i), 1)
            self.can_attack = False
            self.attacking = False
            self.timer = threading.Timer(5, self.set_can_attack)
            self.timer.start()
            return BehaviorTree.SUCCESS
        self.frame %= 6
        return BehaviorTree.RUNNING

    def change_dir(self):
        if self.x > normal_stage.player.x:
            self.stand_dir = -1
        else:
            self.stand_dir = 1
        self.frame = (self.frame + 6 * (1.0 / 0.5) * game_framework.frame_time) % 6
        return BehaviorTree.SUCCESS

    def build_behavior_tree(self):
        banshee_attck = SequenceNode("Banshee Attack")
        cooltime_check_node = LeafNode("Cooltime Check", self.cooltime_check)
        create_bullets = LeafNode("Create Bullets", self.attack)
        banshee_attck.add_children(cooltime_check_node, create_bullets)
        change_dir_node = LeafNode("Change Dir", self.change_dir)
        banshee_node = SelectorNode("Banshee")
        banshee_node.add_children(banshee_attck, change_dir_node)
        self.bt = BehaviorTree(banshee_node)

    def update(self):
        self.bt.run()
        if self.hp <= 0:
            normal_stage.monsters.remove(self)
            game_world.remove_object(self)

    def draw(self):
        cx, cy = self.x - self.bg.window_left, self.y - self.bg.window_bottom
        if self.attacking:
            if self.stand_dir == 1:
                Banshee.image.clip_draw(int(self.frame) * 20, 22, 20, 22, cx, cy, 30, 30)
            elif self.stand_dir == -1:
                Banshee.image.clip_composite_draw(int(self.frame) * 20, 22, 20, 22, 0, 'h', cx, cy, 30, 30)

        else:
            if self.stand_dir == 1:
                Banshee.image.clip_draw(int(self.frame) * 20, 0, 20, 22, cx, cy, 30, 30)
            elif self.stand_dir == -1:
                Banshee.image.clip_composite_draw(int(self.frame) * 20, 0, 20, 22, 0, 'h', cx, cy, 30, 30)
        self.font.draw(cx - 35, cy + 20, 'HP : %d' % self.hp, (255, 0, 0))