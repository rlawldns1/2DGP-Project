from pico2d import *

width = 1280
height = 720

class WelcomeToUFC:
    def __init__(self):
        self.image = load_image('welcome_to_ufc.jpg')
        self.bgm = load_music('sound/welcometotheufc.mp3')
        self.bgm.set_volume(64)
        self.bgm.play(1)

    def update(self):
        pass

    def draw(self):
        self.image.draw(640, 360, 1280, 720)