from pico2d import *

import game_framework
from state_machine import StateMachine

PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 20.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION

# FRAMES_PER_SECOND = FRAMES_PER_ACTION / TIME_PER_ACTION

# 타임아웃
def time_out(e):
    return e[0] == 'TIMEOUT'

def death(e):
    return e[0] == 'DEATH'

class Enemy:

    def __init__(self):
        self.x = 1200
        self.y = 300
        self.frame = 0
        self.face_dir = -1
        self.max_hp = 100
        self.cur_hp = self.max_hp
        self.font = load_font('ENCR10B.TTF', 16)

        self.idle_image = load_image('Enemy/dodge.png')
        self.death_image = load_image('Enemy/Death.png')
        # self.punch_image = load_image('EnemyPunk/punch.png')
        # self.walk_image = load_image('EnemyPunk/walk.png')
        # self.kick_image = load_image('EnemyPunk/kick.png')

        self.image = self.idle_image

        self.IDLE = EnemyIdle(self)
        self.DEATH = EnemyDeath(self)
        # self.WALK = EnemyWalk(self)
        # self.PUNCH = EnemyPunch(self)
        # self.KICK = EnemyKick(self)

        self.state_machine = StateMachine(
            self.IDLE,
            {
             self.IDLE: {death: self.DEATH},
             self.DEATH: {},
             # self.PUNCH: {},
             # self.WALK: {},
             # self.KICK: {},
            }
        )

    def update(self):
        if self.cur_hp <= 0 and not isinstance(self.state_machine.cur_state, EnemyDeath):
            self.state_machine.handle_state_event(('DEATH', None))
        self.state_machine.update()


    def draw(self):
        self.state_machine.draw()
        hp_bar_x = 1280-400-100
        hp_bar_y = 620
        hp_bar_width = 400
        hp_bar_height = 50

        # HP 바 배경
        draw_rectangle(hp_bar_x, hp_bar_y, hp_bar_x + hp_bar_width, hp_bar_y + hp_bar_height)

        # 현재 HP에 따른 HP 바
        current_hp_width = (self.cur_hp / self.max_hp) * hp_bar_width
        draw_rectangle(hp_bar_x, hp_bar_y, hp_bar_x + current_hp_width, hp_bar_y + hp_bar_height)

        self.font.draw(self.x - 50, self.y + 50, f'(Time : {get_time():.2f})', (255, 255, 0))
        self.font.draw(self.x - 50, self.y + 150, f'HP: {self.cur_hp}/{self.max_hp}', (255, 255, 0))
        draw_rectangle(*self.get_bb())


    def handle_event(self, event):
        self.state_machine.handle_state_event(('INPUT', event))

    def get_bb(self):
        return self.x - 64, self.y - 256, self.x + 64, self.y + 32

    def handle_collision(self, group, other):
        if group == 'player_lp:enemy' or group == 'player_rp:enemy' or group == 'player_kick:enemy':
            self.cur_hp -= 5

        if self.cur_hp <= 0:
            self.cur_hp = 0

class EnemyIdle:
    def __init__(self, enemy):
        self.enemy = enemy

    def enter(self,event):
        self.enemy.image = self.enemy.idle_image
        self.enemy.frame = 0
        self.enemy.wait_time = get_time()
        self.enemy.dir = 0

    def exit(self, event):
        pass

    def do(self):
        self.enemy.frame = (self.enemy.frame + 4 * ACTION_PER_TIME * game_framework.frame_time) % 4

    def draw(self):
        if self.enemy.face_dir == 1:
            self.enemy.image.clip_draw(int(self.enemy.frame) * 128, 0, 128, 128, self.enemy.x, self.enemy.y, 512, 512)
        else:
            self.enemy.image.clip_composite_draw(int(self.enemy.frame) * 128, 0, 128, 128, 0, 'h', self.enemy.x, self.enemy.y, 512, 512)

class EnemyDeath:
    def __init__(self, enemy):
        self.enemy = enemy

    def enter(self,event):
        self.enemy.image = self.enemy.death_image
        self.enemy.frame = 0
        self.enemy.wait_time = get_time()
        self.enemy.dir = 0
        self.enemy.max_frame = 5

    def exit(self, event):
        pass

    def do(self):
        self.enemy.frame = (self.enemy.frame + 5 * ACTION_PER_TIME * game_framework.frame_time)

    def draw(self):
        if self.enemy.face_dir == 1:
            self.enemy.image.clip_draw(int(self.enemy.frame) * 128, 0, 128, 128, self.enemy.x, self.enemy.y, 512, 512)
        else:
            self.enemy.image.clip_composite_draw(int(self.enemy.frame) * 128, 0, 128, 128, 0, 'h', self.enemy.x, self.enemy.y, 512, 512)
