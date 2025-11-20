from pico2d import *

import game_framework
import game_world
from state_machine import StateMachine

PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 20.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION

# FRAMES_PER_SECOND = FRAMES_PER_ACTION / TIME_PER_ACTION

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
        self.max_hp = 100
        self.cur_hp = self.max_hp
        self.font = load_font('ENCR10B.TTF', 16)

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

        self.state_machine.draw()
        hp_bar_x = 100
        hp_bar_y = 620
        hp_bar_width = 400
        hp_bar_height = 50

        draw_rectangle(hp_bar_x, hp_bar_y, hp_bar_x + hp_bar_width, hp_bar_y + hp_bar_height)

        current_hp_width = (self.cur_hp / self.max_hp) * hp_bar_width
        if current_hp_width > 0:
            draw_rectangle(hp_bar_x, hp_bar_y, hp_bar_x + current_hp_width, hp_bar_y + hp_bar_height, 255,0,0,1,True)

        draw_rectangle(*self.get_bb())

    def handle_event(self, event):
        self.state_machine.handle_state_event(('INPUT', event))

    def get_bb(self):
        if isinstance(self.state_machine.cur_state, Kick):
            if 3 <= self.frame < 4 and not self.state_machine.cur_state.hit:
                kick_offset = 160 * self.face_dir
                kick_x = self.x + kick_offset
                kick_y = self.y - 70
                kick_width = 30
                kick_height = 30
                return (kick_x - kick_width // 2, kick_y - kick_height // 2,
                        kick_x + kick_width // 2, kick_y + kick_height // 2)
        # 왼쪽 펀치 상태
        elif isinstance(self.state_machine.cur_state, LeftPunch):
             if 1 <= self.frame < 3 and not self.state_machine.cur_state.hit:
                return self.state_machine.cur_state.get_lp_bb()

        # 오른쪽 펀치 상태
        elif isinstance(self.state_machine.cur_state, RightPunch):
            if 2 <= self.frame < 5 and not self.state_machine.cur_state.hit:
                return self.state_machine.cur_state.get_rp_bb()

        # 기본 바운딩 박스
        return self.x - 64, self.y - 256, self.x + 64, self.y + 32

    def handle_collision(self, group, other):
        if group == 'player_kick:enemy':
            if isinstance(self.state_machine.cur_state, Kick):
                if not self.state_machine.cur_state.hit:
                    self.state_machine.cur_state.hit = True
        elif group == 'player_lp:enemy':
            if isinstance(self.state_machine.cur_state, LeftPunch):
                if not self.state_machine.cur_state.hit:
                    self.state_machine.cur_state.hit = True
        elif group == 'player_rp:enemy':
            if isinstance(self.state_machine.cur_state, RightPunch):
                if not self.state_machine.cur_state.hit:
                    self.state_machine.cur_state.hit = True


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
        self.player.frame = (self.player.frame + 4 * ACTION_PER_TIME * game_framework.frame_time) % 4

    def draw(self):
        if self.player.face_dir == 1:
            self.player.image.clip_draw(int(self.player.frame) * 128, 0, 128, 128, self.player.x, self.player.y, 512, 512)
        else:
            self.player.image.clip_composite_draw(int(self.player.frame) * 128, 0, 128, 128, 0, 'h', self.player.x, self.player.y, 512, 512)

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
        self.player.frame = (self.player.frame + 12 * ACTION_PER_TIME * game_framework.frame_time) % 12
        self.player.x += self.player.dir * RUN_SPEED_PPS * game_framework.frame_time

    def draw(self):
        if self.player.face_dir == 1:
            self.player.image.clip_draw(int(self.player.frame) * 128, 0, 128, 128, self.player.x, self.player.y, 512, 512)
        else:
            self.player.image.clip_composite_draw(int(self.player.frame) * 128, 0, 128, 128, 0, 'h', self.player.x, self.player.y, 512, 512)

class LeftPunch:
    def __init__(self, player):
        self.player = player
        self.hit = False


    def enter(self, event):
        self.player.image = self.player.left_punch_image
        self.player.frame = 0
        self.player.max_frame = 3
        self.player.wait_time = get_time()
        self.hit = False

    def exit(self, event):
        pass

    def do(self):
        self.player.frame = (self.player.frame + 3 * ACTION_PER_TIME * game_framework.frame_time)
        if self.player.frame >= self.player.max_frame:
            self.player.state_machine.handle_state_event(('TIMEOUT', None))

    def draw(self):
        if self.player.face_dir == 1:
            self.player.image.clip_draw(int(self.player.frame) * 128, 0, 128, 128, self.player.x, self.player.y, 512, 512)
        else:
            self.player.image.clip_composite_draw(int(self.player.frame) * 128, 0, 128, 128, 0, 'h', self.player.x, self.player.y, 512, 512)
        draw_rectangle(*self.get_lp_bb())

    def get_lp_bb(self):
        lp_offset = 120 * self.player.face_dir
        lp_x = self.player.x + lp_offset
        lp_y = self.player.y - 60
        lp_width = 30
        lp_height = 30

        return (lp_x - lp_width // 2, lp_y - lp_height // 2, lp_x + lp_width // 2, lp_y + lp_height // 2)

class RightPunch:
    def __init__(self, player):
        self.player = player
        self.hit = False


    def enter(self, event):
        self.player.image = self.player.right_punch_image
        self.player.frame = 0
        self.player.max_frame = 5
        self.player.wait_time = get_time()
        self.hit = False

    def exit(self, event):
        pass

    def do(self):
        self.player.frame = (self.player.frame + 5 * ACTION_PER_TIME * game_framework.frame_time)
        if self.player.frame >= self.player.max_frame:
            self.player.state_machine.handle_state_event(('TIMEOUT', None))

    def draw(self):
        if self.player.face_dir == 1:
            self.player.image.clip_draw(int(self.player.frame) * 128, 0, 128, 128, self.player.x, self.player.y, 512, 512)
        else:
            self.player.image.clip_composite_draw(int(self.player.frame) * 128, 0, 128, 128, 0, 'h', self.player.x, self.player.y, 512, 512)

        draw_rectangle(*self.get_rp_bb())

    def get_rp_bb(self):
        rp_offset = 140 * self.player.face_dir
        rp_x = self.player.x + rp_offset
        rp_y = self.player.y - 50
        rp_width = 30
        rp_height = 30

        return (rp_x - rp_width // 2, rp_y - rp_height // 2, rp_x + rp_width // 2, rp_y + rp_height // 2)

class Kick:
    def __init__(self, player):
        self.player = player
        self.hit = False


    def enter(self, event):
        self.player.image = self.player.right_kick_image
        self.player.frame = 0
        self.player.max_frame = 5
        self.player.wait_time = get_time()
        self.hit = False

    def exit(self, event):
        pass

    def do(self):
        self.player.frame = (self.player.frame + 5 * ACTION_PER_TIME * game_framework.frame_time)
        if self.player.frame >= self.player.max_frame:
            self.player.state_machine.handle_state_event(('TIMEOUT', None))

    def draw(self):
        if self.player.face_dir == 1:
            self.player.image.clip_draw(int(self.player.frame) * 128, 0, 128, 128, self.player.x, self.player.y, 512, 512)
        else:
            self.player.image.clip_composite_draw(int(self.player.frame) * 128, 0, 128, 128, 0, 'h', self.player.x, self.player.y, 512, 512)

        draw_rectangle(*self.get_kick_bb())

    def get_kick_bb(self):
        kick_offset = 160 * self.player.face_dir
        kick_x = self.player.x + kick_offset
        kick_y = self.player.y - 70
        kick_width = 30
        kick_height = 30

        return (kick_x - kick_width // 2, kick_y - kick_height // 2, kick_x + kick_width // 2, kick_y + kick_height // 2)

