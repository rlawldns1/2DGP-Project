from pico2d import *

from state_machine import StateMachine

def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT


def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT


def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT


def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT
# 왼쪽 펀치
def d_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_d
# 오른쪽 펀치
def f_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_f
# 왼쪽 발차기
def j_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_j
# 오른쪽 발차기
def k_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_k
# 타임아웃 - 3분정도.
def time_out(e):
    return e[0] == 'TIMEOUT'

class Player:

    def __init__(self):
        self.x = 400
        self.y = 300
        self.frame = 0
        self.face_dir = 1
        self.idle_image = load_image('Idle.png')
        self.left_punch_image = load_image('Punch_2.png')
        self.right_punch_image = load_image('Punch_1.png')
        self.walk_image = load_image('Walking.png')

        self.image = self.idle_image

        self.IDLE = Idle(self)
        self.WALK = Walk(self)
        self.LEFT_PUNCH = LeftPunch(self)
        self.RIGHT_PUNCH = RightPunch(self)

        self.state_machine = StateMachine(
            self.IDLE,
            {
             self.IDLE: {d_down: self.LEFT_PUNCH, f_down: self.RIGHT_PUNCH, left_down: self.WALK, right_down: self.WALK},
             self.LEFT_PUNCH: {time_out: self.IDLE},
             self.RIGHT_PUNCH: {time_out: self.IDLE},
             self.WALK: {left_up: self.IDLE, right_up:self.IDLE},
            }
        )

    def update(self):
        self.state_machine.update()

    def draw(self):
        self.state_machine.draw()

    def handle_event(self, event):
        self.state_machine.handle_state_event(('INPUT', event))

class Idle:
    def __init__(self, player):
        self.player = player

    def enter(self,event):
        self.player.image = self.player.idle_image
        self.player.frame = 0
        self.player.wait_time = get_time()
        self.player.dir = 0

    def exit(self, event):
        pass

    def do(self):
        self.player.frame = (self.player.frame + 1) % 1
        if get_time() - self.player.wait_time > 1.0:
            self.player.state_machine.handle_state_event(('TIMEOUT', None))
        pass

    def draw(self):
        if self.player.face_dir == 1:
            self.player.image.clip_draw(self.player.frame * 128, 0, 128, 128, self.player.x, self.player.y, 512, 512)
        else:
            self.player.image.clip_composite_draw(self.player.frame * 128, 0, 128, 128, 0, 'h', self.player.x, self.player.y, 512, 512)

class Walk:
    def __init__(self, player):
        self.player = player

    def enter(self,event):
        self.player.image = self.player.walk_image
        self.player.frame = 0
        self.player.wait_time = get_time()
        self.player.dir = 0
        if right_down(event) or left_up(event):
            self.player.dir = self.player.face_dir = 1
        elif left_down(event) or right_up(event):
            self.player.dir = self.player.face_dir = -1


    def exit(self, event):
        pass

    def do(self):
        self.player.frame = (self.player.frame + 1) % 12
        self.player.x += self.player.dir * 5

    def draw(self):
        if self.player.face_dir == 1:
            self.player.image.clip_draw(self.player.frame * 128, 0, 128, 128, self.player.x, self.player.y, 512, 512)
        else:
            self.player.image.clip_composite_draw(self.player.frame * 128, 0, 128, 128, 0, 'h', self.player.x, self.player.y, 512, 512)

class LeftPunch:
    def __init__(self, player):
        self.player = player


    def enter(self, event):
        self.player.image = self.player.left_punch_image
        self.player.frame = 0
        self.player.wait_time = get_time()

    def exit(self, event):
        pass

    def do(self):
        self.player.frame = (self.player.frame + 1) % 3
        if get_time() - self.player.wait_time > 1.0:
            self.player.state_machine.handle_state_event(('TIMEOUT', None))

    def draw(self):
        if self.player.face_dir == 1:
            self.player.image.clip_draw(self.player.frame * 128, 0, 128, 128, self.player.x, self.player.y, 512, 512)
        else:
            self.player.image.clip_composite_draw(self.player.frame * 128, 0, 128, 128, 0, 'h', self.player.x, self.player.y, 512, 512)

class RightPunch:
    def __init__(self, player):
        self.player = player


    def enter(self, event):
        self.player.image = self.player.right_punch_image
        self.player.frame = 0
        self.player.wait_time = get_time()

    def exit(self, event):
        pass

    def do(self):
        self.player.frame = (self.player.frame + 1) % 5
        if get_time() - self.player.wait_time > 1.0:
            self.player.state_machine.handle_state_event(('TIMEOUT', None))

    def draw(self):
        if self.player.face_dir == 1:
            self.player.image.clip_draw(self.player.frame * 128, 0, 128, 128, self.player.x, self.player.y, 512, 512)
        else:
            self.player.image.clip_composite_draw(self.player.frame * 128, 0, 128, 128, 0, 'h', self.player.x, self.player.y, 512, 512)