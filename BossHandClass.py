from pico2d import *
import boss_stage
import game_framework


class Boss_Hand:
    def __init__(self, hand_image, atk_image, x, y, hand):
        self.image = load_image(hand_image)
        self.atk_image = load_image(atk_image)
        self.laser = load_image("Boss_Laser(320x55).png")
        self.x, self.y = x, y
        self.laser_atk = 15
        self.frame = 0
        self.which_hand = hand
        self.hit_player = False
        self.laser_pattern = False

    def attack_collide(self):
        if self.which_hand == -1:
            left_a, bottom_a, right_a, top_a = (self.x + 195) - 160, self.y - 27.5, (self.x + 195) + 160, self.y + 27.5
        else:
            left_a, bottom_a, right_a, top_a = (self.x - 195) - 160, self.y - 27.5, (self.x - 195) + 160, self.y + 27.5

        left_b, bottom_b, right_b, top_b = boss_stage.player.x - 15, boss_stage.player.y - 30, \
                                           boss_stage.player.x + 15, boss_stage.player.y

        if left_a > right_b: return False
        if right_a < left_b: return False
        if top_a < bottom_b: return False
        if bottom_a > top_b: return False
        return True

    def laser_shot(self):
        if not self.laser_pattern:
            self.laser_pattern = True
        self.frame = (self.frame + 9 * (1.0 / 1.5) * game_framework.frame_time)

        if self.frame >= 2:
            if self.attack_collide() and not self.hit_player:
                self.hit_player = True
                boss_stage.player.hp -= self.laser_atk
                print(boss_stage.player.hp)

        if self.frame > 8:
            self.frame = 0
            self.laser_pattern = False
            self.hit_player = False
            return 1

        self.frame %= 9
        return -1

    def update(self):
        pass

    def draw(self):
        if not self.laser_pattern:
            self.image.draw(self.x, self.y)
        else:
            self.atk_image.clip_draw(int(self.frame) * 70, 0, 70, 80, self.x, self.y)
            if self.frame >= 2:
                if self.which_hand == -1:
                    self.laser.clip_draw(0, int(self.frame) * 55, 320, 55, self.x + 195, self.y)
                    draw_rectangle((self.x + 195) - 160, self.y - 27.5, (self.x + 195) + 160, self.y + 27.5)
                else:
                    self.laser.clip_composite_draw(0, int(self.frame) * 55, 320, 55, 0, 'h', self.x - 195, self.y, 320,
                                                   55)
                    draw_rectangle((self.x - 195) - 160, self.y - 27.5, (self.x - 195) + 160, self.y + 27.5)