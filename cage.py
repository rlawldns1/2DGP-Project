from pico2d import *

width = 1280
height = 720

class Cage:
    def __init__(self):
        self.image = load_image('cagge.jpg')

    def update(self):
        pass

    def draw(self):
        self.image.draw(width/2, height/2)