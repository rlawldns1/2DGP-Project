from pico2d import *

class Player:

    def __init__(self):
        self.x = 400
        self.y = 300
        self.frame = 0
        self.face_dir = 1
        self.image = load_image('Walking.png')
        self.WALKING = Walking(self)
        self.state_machine = StateMachine(self.WALKING)

    def update(self):
        self.state_machine.update()

    def draw(self):
        self.state_machine.draw()

class Walking:
    def __init__(self, player):
        self.player = player

    def enter(self):
        pass

    def exit(self):
        pass

    def do(self):
        self.player.frame = (self.player.frame + 1) % 12
        pass

    def draw(self):
        if self.player.face_dir == 1:
            self.player.image.clip_draw(self.player.frame * 128, 0, 128, 128, self.player.x, self.player.y, 512, 512)
        else:
            self.player.image.clip_composite_draw(self.player.frame * 128, 0, 128, 128, 0, 'h', self.player.x, self.player.y, 512, 512)

class LeftPunch:
    def __init__(self, player):
        self.player = player

    def enter(self):
        self.player.dir = 0

    def exit(self):
        pass

    def do(self):
        self.player.frame = (self.player.frame + 1) % 5

    def draw(self):
        if self.player.face_dir == 1:
            self.player.image.clip_draw(self.player.frame * 128, 128, 128, 128, self.player.x, self.player.y, 512, 512)
        else:
            self.player.image.clip_composite_draw(self.player.frame * 128, 128, 128, 128, 0, 'h', self.player.x, self.player.y, 512, 512)

class StateMachine:
    def __init__(self, start_state=None):
        self.cur_state = start_state

    def update(self):
        self.cur_state.do()

    def draw(self):
        self.cur_state.draw()