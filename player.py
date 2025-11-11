from pico2d import *

import game_framework
from state_machine import StateMachine

PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 20.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

def d_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_d


def d_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_d


def a_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_a


def a_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_a

# 왼쪽 펀치
def u_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_u
# 오른쪽 펀치
def i_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_i
# 왼쪽 발차기
def j_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_j
# 오른쪽 발차기
def k_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_k
# 타임아웃
def time_out(e):
    return e[0] == 'TIMEOUT'

class Player:

    def __init__(self):
        self.x = 400
        self.y = 300
        self.frame = 0
        self.face_dir = 1
        self.idle_image = load_image('Dodge.png')
        self.left_punch_image = load_image('Punch_2.png')
        self.right_punch_image = load_image('Punch_1.png')
        self.walk_image = load_image('Walking.png')
        self.right_kick_image = load_image('Kick.png')

        self.image = self.idle_image

        self.IDLE = Idle(self)
        self.WALK = Walk(self)
        self.LEFT_PUNCH = LeftPunch(self)
        self.RIGHT_PUNCH = RightPunch(self)
        self.KICK = Kick(self)

        self.state_machine = StateMachine(
            self.IDLE,
            {
             self.IDLE: {u_down: self.LEFT_PUNCH, i_down: self.RIGHT_PUNCH, a_down: self.WALK, d_down: self.WALK, k_down: self.KICK},
             self.LEFT_PUNCH: {time_out: self.IDLE},
             self.RIGHT_PUNCH: {time_out: self.IDLE},
             self.WALK: {a_up: self.IDLE, d_up:self.IDLE},
             self.KICK: {time_out:self.IDLE},
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
        self.player.frame = (self.player.frame + 1) % 4
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
        if d_down(event) or a_up(event):
            self.player.dir = self.player.face_dir = 1
        elif a_down(event) or d_up(event):
            self.player.dir = self.player.face_dir = -1


    def exit(self, event):
        pass

    def do(self):
        self.player.frame = (self.player.frame + 1) % 12
        self.player.x += self.player.dir * RUN_SPEED_PPS * game_framework.frame_time

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
        self.player.max_frame = 3
        self.player.wait_time = get_time()

    def exit(self, event):
        pass

    def do(self):
        self.player.frame += 1
        if self.player.frame >= self.player.max_frame:
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
        self.player.max_frame = 5
        self.player.wait_time = get_time()

    def exit(self, event):
        pass

    def do(self):
        self.player.frame += 1
        if self.player.frame >= self.player.max_frame:
            self.player.state_machine.handle_state_event(('TIMEOUT', None))

    def draw(self):
        if self.player.face_dir == 1:
            self.player.image.clip_draw(self.player.frame * 128, 0, 128, 128, self.player.x, self.player.y, 512, 512)
        else:
            self.player.image.clip_composite_draw(self.player.frame * 128, 0, 128, 128, 0, 'h', self.player.x, self.player.y, 512, 512)

class Kick:
    def __init__(self, player):
        self.player = player


    def enter(self, event):
        self.player.image = self.player.right_kick_image
        self.player.frame = 0
        self.player.max_frame = 5
        self.player.wait_time = get_time()

    def exit(self, event):
        pass

    def do(self):
        self.player.frame += 1
        if self.player.frame >= self.player.max_frame:
            self.player.state_machine.handle_state_event(('TIMEOUT', None))

    def draw(self):
        if self.player.face_dir == 1:
            self.player.image.clip_draw(self.player.frame * 128, 0, 128, 128, self.player.x, self.player.y, 512, 512)
        else:
            self.player.image.clip_composite_draw(self.player.frame * 128, 0, 128, 128, 0, 'h', self.player.x, self.player.y, 512, 512)