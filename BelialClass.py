from pico2d import *
from BossBulletClass import Boss_Bullet
from BossHandClass import Boss_Hand
from BossSwordClass import Boss_Sword
from BehaviorTree import BehaviorTree, SelectorNode, SequenceNode, LeafNode
import threading
import boss_stage
import game_world
import game_framework


class Belial:
    def __init__(self):
        self.image = load_image("Boss(70x99).png")
        self.pattern1_image = load_image("Boss_Atk(70x128).png")
        self.Left_Hand = Boss_Hand("Boss_LeftHand.png", "Boss_LH_Atk(70x80).png", 200, 200, -1)
        self.Right_Hand = Boss_Hand("Boss_RightHand.png", "Boss_RH_Atk(70x80).png", 600, 200, 1)
        self.hp = 250
        self.x, self.y = 400, 300
        self.frame = 0
        self.bullet_count = 0
        self.hit = False
        self.bullet_pattern_check = False
        self.laser_pattern_check = False
        self.sword_pattern_check = False
        self.bullet_pattern_timer = None
        self.laser_pattern_timer = None
        self.left_laser_shot_func_call_timer = None
        self.right_laser_shot_func_call_timer = None
        self.sword_pattern_timer = None
        self.is_bullet_pattern_timer_run = False
        self.is_laser_pattern_timer_run = False
        self.is_left_laser_shot_func_called = False
        self.is_right_laser_shot_func_called = False
        self.is_sword_pattern_timer_run = False
        self.build_behavior_tree()

    def bullet_pattern_timer_func(self):
        self.is_bullet_pattern_timer_run = False
        self.bullet_pattern_check = True

    def laser_pattern_timer_func(self):
        self.is_laser_pattern_timer_run = False
        self.laser_pattern_check = True

    def call_left_laser_shot_func(self):
        if not self.is_left_laser_shot_func_called:
            self.Left_Hand.x, self.Left_Hand.y = boss_stage.player.x - 80, boss_stage.player.y
        return BehaviorTree.SUCCESS

    def call_right_laser_shot_func(self):
        if not self.is_right_laser_shot_func_called:
            self.Right_Hand.x, self.Right_Hand.y = boss_stage.player.x + 80, boss_stage.player.y
        return BehaviorTree.SUCCESS

    def bullet_pattern_cooltime_check(self):
        if self.bullet_pattern_check:
            return BehaviorTree.SUCCESS
        else:
            if not self.is_bullet_pattern_timer_run:
                self.is_bullet_pattern_timer_run = True
                self.bullet_pattern_timer = threading.Timer(5, self.bullet_pattern_timer_func)
                self.bullet_pattern_timer.start()
            return BehaviorTree.FAIL

    def laser_pattern_cooltime_check(self):
        if self.laser_pattern_check:
            return BehaviorTree.SUCCESS
        else:
            if not self.is_laser_pattern_timer_run:
                self.is_laser_pattern_timer_run = True
                self.laser_pattern_timer = threading.Timer(7, self.laser_pattern_timer_func)
                self.laser_pattern_timer.start()
            return BehaviorTree.FAIL

    def sword_pattern_cooltime_check(self):
        if len(boss_stage.belial_sword) == 0:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def bullet_pattern(self):
        if self.bullet_count < 30:
            game_world.add_object(Boss_Bullet(410, 270, self.bullet_count * 25), 1)
            self.bullet_count += 1
        self.frame += 1
        self.frame = clamp(0, self.frame, 9)

        if self.bullet_count == 30:
            self.bullet_pattern_check = False
            self.is_bullet_pattern_timer_run = True
            self.bullet_count = 0
            self.bullet_pattern_timer = threading.Timer(5, self.bullet_pattern_timer_func)
            self.bullet_pattern_timer.start()
            return BehaviorTree.SUCCESS
        return BehaviorTree.RUNNING

    def left_laser_shot(self):
        if self.Left_Hand.laser_shot() == -1:
            return BehaviorTree.RUNNING
        return BehaviorTree.SUCCESS

    def right_laser_shot(self):
        if self.Right_Hand.laser_shot() == -1:
            return BehaviorTree.RUNNING
        self.laser_pattern_check = False
        self.is_laser_pattern_timer_run = True
        self.laser_pattern_timer = threading.Timer(7, self.laser_pattern_timer_func)
        self.laser_pattern_timer.start()
        return BehaviorTree.SUCCESS

    def create_sword(self):
        for i in range(5):
            boss_stage.belial_sword.append(Boss_Sword(60*i))
        boss_stage.sword_drop_timer = threading.Timer(3, boss_stage.Drop_Sword)
        boss_stage.sword_drop_timer.start()
        return BehaviorTree.SUCCESS

    def idle(self):
        self.frame = (self.frame + 10 * (1.0/1.0) * game_framework.frame_time) % 10
        return BehaviorTree.SUCCESS

    def build_behavior_tree(self):
        bullet_pattern_node = SequenceNode("Bullet Pattern")
        bullet_pattern_cooltime_check_node = LeafNode("B-CoolTime Check", self.bullet_pattern_cooltime_check)
        create_bullet_node = LeafNode("Create Bullet", self.bullet_pattern)
        bullet_pattern_node.add_children(bullet_pattern_cooltime_check_node, create_bullet_node)

        laser_pattern_node = SequenceNode("Laser Pattern")
        laser_pattern_cooltime_check_node = LeafNode("L-CoolTime Check", self.laser_pattern_cooltime_check)
        lefthand_move_node = LeafNode("LeftHand Move", self.call_left_laser_shot_func)
        left_laser_shot_node = LeafNode("Left Laser Shot", self.left_laser_shot)
        righthand_move_node = LeafNode("RightHand Move", self.call_right_laser_shot_func)
        right_laser_shot_node = LeafNode("Right Laser Shot", self.right_laser_shot)
        laser_pattern_node.add_children(laser_pattern_cooltime_check_node, lefthand_move_node, left_laser_shot_node,
                                        righthand_move_node, right_laser_shot_node)

        sword_pattern_node = SequenceNode("Sword Pattern")
        sword_pattern_cooltime_check_node = LeafNode("S-CoolTime Check", self.sword_pattern_cooltime_check)
        create_sword_node = LeafNode("Create Sword", self.create_sword)
        sword_pattern_node.add_children(sword_pattern_cooltime_check_node, create_sword_node)

        idle_node = LeafNode("Idle", self.idle)

        belial_node = SelectorNode("Belial")
        belial_node.add_children(bullet_pattern_node, laser_pattern_node, sword_pattern_node, idle_node)
        self.bt = BehaviorTree(belial_node)

    def update(self):
        self.bt.run()
        if self.hp <= 0:
            boss_stage.monsters.remove(self)
            game_world.remove_object(self)

    def draw(self):
        self.image.clip_draw(70 * int(self.frame), 0, 70, 90, self.x, self.y)
        self.Left_Hand.draw()
        self.Right_Hand.draw()
        draw_rectangle(self.x - 35, self.y - 45, self.x + 35, self.y + 45)