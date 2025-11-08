from pico2d import *

class Player:
    def __init__(self):
        self.x = 400
        self.y = 300
        self.frame = 0
        self.image = load_image('Walking.png')

    def update(self):
        self.frame = (self.frame + 1) % 12
        self.x += 5

    def draw(self):
        self.image.clip_draw(self.frame * 128, 0, 128, 128, self.x, self.y, 512, 512)