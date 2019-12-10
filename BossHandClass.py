from pico2d import *
import boss_state
import game_framework


class Boss_Hand:
    def __init__(self, hand_image, atk_image, x, y, hand):
        self.image = load_image(hand_image)
        self.atk_image = load_image(atk_image)
        self.laser = load_image("Boss_Laser(320x55).png")
        self.x, self.y = x, y
        self.frame = 0
        self.which_hand = hand
        self.laser_pattern = False

    def laser_shot(self):
        if not self.laser_pattern:
            self.laser_pattern = True
        self.frame = (self.frame + 9 * (1.0/1.5) * game_framework.frame_time)
        if self.frame > 8:
            self.frame = 0
            self.laser_pattern = False
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
                else:
                    self.laser.clip_composite_draw(0, int(self.frame) * 55, 320, 55, 0, 'h', self.x - 195, self.y, 320, 55)
