from pico2d import *


class BackGround:
    def __init__(self):
        self.image = load_image('BackGround_Image.png')

    def update(self):
        pass

    def draw(self):
        self.image.draw(750, 300)