from pico2d import *
import random
from BehaviorTree import BehaviorTree, SelectorNode, SequenceNode, LeafNode
import normal_stage
import game_framework


class Skeleton:
    image = None
    Atk_image = None

    def __init__(self, num):
        if Skeleton.image is None:
            Skeleton.image = load_image("Skel(33x30).png")
        if Skeleton.Atk_image is None:
            Skeleton.Atk_image = load_image("SkelAtk(71x48).png")
        self.hp = 60
        self.attack_power = 7
        self.dir = 1
        self.x, self.y = random.randint(100, 1400), 100
        self.moving_point = None
        self.speed = 75
        self.frame = 0
        self.atk_frame = 0
        self.state = "Idle"
        self.hit_player = False
        self.build_behavior_tree()

    def collide(self, b):
        if self.dir == -1:
            left_a, bottom_a, right_a, top_a = self.x - 54, self.y - 45, self.x - 16, self.y + 45
        else:
            left_a, bottom_a, right_a, top_a = self.x + 16, self.y - 45, self.x + 54, self.y + 45

        left_b, bottom_b, right_b, top_b = b.x - 15, b.y - 30, b.x + 15, b.y

        if left_a > right_b: return False
        if right_a < left_b: return False
        if top_a < bottom_b: return False
        if bottom_a > top_b: return False
        return True

    def attack_collide(self):
        if self.dir == -1:
            left_a, bottom_a, right_a, top_a = (self.x - 18) - 36, (self.y + 30) - 72, (self.x - 18) + 3, (
                        self.y + 30) + 72
        else:
            left_a, bottom_a, right_a, top_a = (self.x + 18) + 3, (self.y + 30) - 72, (self.x + 18) + 36, (
                        self.y + 30) + 72

        left_b, bottom_b, right_b, top_b = normal_stage.player.x - 15, normal_stage.player.y - 30, \
                                           normal_stage.player.x + 15, normal_stage.player.y

        if left_a > right_b: return False
        if right_a < left_b: return False
        if top_a < bottom_b: return False
        if bottom_a > top_b: return False
        return True

    def find_player(self):
        if self.collide(normal_stage.player):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def attack(self):
        if not self.state == "Attack":
            self.state = "Attack"

        self.atk_frame = (self.atk_frame + 12 * (1.0 / 1.5) * game_framework.frame_time)
        # if atk_frame is 2~6 collision check with player later
        if 2 <= self.atk_frame <= 6:
            if self.attack_collide() and not self.hit_player:
                normal_stage.player.hp -= self.attack_power
                self.hit_player = True
                print(normal_stage.player.hp)

        if self.atk_frame >= 12:
            self.state = "Idle"
            self.atk_frame = 0
            self.hit_player = False
            return BehaviorTree.SUCCESS
        self.atk_frame %= 12
        return BehaviorTree.RUNNING

    def get_point(self):
        self.moving_point = random.randint(15, 1500 - 15)
        if self.x > self.moving_point:
            self.dir = -1
        else:
            self.dir = 1
        return BehaviorTree.SUCCESS

    def move_to_point(self):
        if not self.state == "Moving":
            self.state = "Moving"
        self.x += self.dir * self.speed * game_framework.frame_time

        if self.collide(normal_stage.player):
            return BehaviorTree.FAIL

        self.frame = (self.frame + 6 * (1.0 / 0.5) * game_framework.frame_time) % 6
        distance = (self.moving_point - self.x) ** 2
        if distance <= 5:
            self.state = "Idle"
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def build_behavior_tree(self):
        skeleton_attack_node = SequenceNode("Skeleton Attack")
        find_player_node = LeafNode("Find Player", self.find_player)
        attack_node = LeafNode("Attack", self.attack)
        skeleton_attack_node.add_children(find_player_node, attack_node)
        wander_node = SequenceNode("Wander")
        get_point_node = LeafNode("Get Point", self.get_point)
        move_to_point = LeafNode("Move to Point", self.move_to_point)
        wander_node.add_children(get_point_node, move_to_point)
        skeleton_node = SelectorNode("Skeleton")
        skeleton_node.add_children(skeleton_attack_node, wander_node)
        self.bt = BehaviorTree(skeleton_node)

    def update(self):
        self.bt.run()

    def draw(self):
        if self.state == "Idle":
            if self.dir == -1:
                Skeleton.image.clip_draw(int(self.frame) * 33, 0, 33, 30, self.x, self.y, 33, 90)
                draw_rectangle(self.x - 54, self.y - 45, self.x - 16, self.y + 45)
            elif self.dir == 1:
                Skeleton.image.clip_draw(int(self.frame) * 33, 30, 33, 30, self.x, self.y, 33, 90)
                draw_rectangle(self.x + 16, self.y - 45, self.x + 54, self.y + 45)

        elif self.state == "Attack":
            if self.dir == -1:
                Skeleton.Atk_image.clip_draw(int(self.atk_frame) * 71, 0, 71, 48, self.x - 18, self.y + 30, 71, 144)
                draw_rectangle((self.x - 18) - 36, (self.y + 30) - 72, (self.x - 18) + 3, (self.y + 30) + 72)
            elif self.dir == 1:
                Skeleton.Atk_image.clip_draw(int(self.atk_frame) * 71, 48, 71, 48, self.x + 18, self.y + 30, 71, 144)
                draw_rectangle((self.x + 18) + 3, (self.y + 30) - 72, (self.x + 18) + 36, (self.y + 30) + 72)

        else:
            if self.dir == -1:
                Skeleton.image.clip_draw(int(self.frame) * 33, 60, 33, 30, self.x, self.y, 33, 90)
                draw_rectangle(self.x - 54, self.y - 45, self.x - 16, self.y + 45)
            elif self.dir == 1:
                Skeleton.image.clip_draw(int(self.frame) * 33, 90, 33, 30, self.x, self.y, 33, 90)
                draw_rectangle(self.x + 16, self.y - 45, self.x + 54, self.y + 45)
