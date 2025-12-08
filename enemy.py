from pico2d import *
import random

import game_framework
import game_world
from state_machine import StateMachine
from stats import Stats
from player import LeftPunch, RightPunch, Kick
from behavior_tree import *

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

def hurt(e):
    return e[0] == 'HURT'

def attack(e):
    return e[0] == 'ATTACK'

class Enemy:

    def __init__(self):
        self.x = 1200
        self.y = 300
        self.frame = 0
        self.face_dir = -1
        self.stats = Stats(100, 5, 5)
        self.font = load_font('ENCR10B.TTF', 16)

        self.attack_cooldown = 0.0
        self.attack_cooldown_time = 1.0

        ## behavior tree 관련 멤버 변수
        self.target = None

        self.idle_image = load_image('Enemy/dodge.png')
        self.death_image = load_image('Enemy/Death.png')
        self.hurt_image = load_image('Enemy/hurt.png')
        self.left_punch_image = load_image('Enemy/Punch_2.png')
        self.right_punch_image = load_image('Enemy/Punch_1.png')
        self.kick_image = load_image('Enemy/Kick.png')

        self.attacks = [
            {
                'name': 'left_punch',
                'image': self.left_punch_image,
                'damage': 1,
                'range': 50,
                'frame_count': 3
            },
            {
                'name': 'right_punch',
                'image': self.right_punch_image,
                'damage': 1,
                'range': 50,
                'frame_count': 5
            },
            {
                'name': 'kick',
                'image': self.kick_image,
                'damage': 1,
                'range': 70,
                'frame_count': 5
            }
        ]
        self.current_attack = None

        self.image = self.idle_image

        self.IDLE = EnemyIdle(self)
        self.DEATH = EnemyDeath(self)
        self.HURT = EnemyHurt(self)
        self.ATTACK = EnemyAttack(self)


        self.state_machine = StateMachine(
            self.IDLE,
            {
             self.IDLE: {death: self.DEATH, hurt: self.HURT, attack: self.ATTACK},
             self.DEATH: {},
             self.HURT: {time_out: self.IDLE, death: self.DEATH},
             self.ATTACK : {time_out: self.IDLE, death: self.DEATH, hurt: self.HURT},
            }
        )
        self.build_behavior_tree()

    def build_behavior_tree(self):
        has_target = Condition('HasTarget', Enemy.bt_has_target, self)
        chase_target = Action('ChaseTarget', Enemy.bt_chase_target, self)
        in_attack_range = Condition('InAttackRange', Enemy.bt_in_attack_range, self)
        attack_target = Action('AttackTarget', Enemy.attack_target, self)
        chase_sequence = Sequence('ChaseSequence', has_target, chase_target)
        attack_sequence = Sequence('AttackSequence', has_target, in_attack_range, attack_target)


        def idle_func(enemy):
            print('[BT] IdleAction 실행')
            return BehaviorTree.SUCCESS

        idle_action = Action('IdleAction', idle_func, self)

        root = Selector('RootSelector', attack_sequence, chase_sequence, idle_action)

        self.bt = BehaviorTree(root)

    def set_target(self, target):
        self.target = target
        print('Enemy Target : ',target)

    def bt_has_target(self):
        if self.target is None:
            print('Enemy has no target')
            return BehaviorTree.FAIL
        if not hasattr(self.target, 'stats') or not self.target.stats.is_alive():
            print('Enemy target is dead')
            return BehaviorTree.FAIL
        print('Enemy has target')
        return BehaviorTree.SUCCESS

    def bt_chase_target(self):
        if self.target is None:
            return BehaviorTree.FAIL

        dx = self.target.x - self.x

        if abs(dx) < 90:
            return BehaviorTree.SUCCESS

        self.face_dir = 1 if dx > 0 else -1
        self.x += self.face_dir * RUN_SPEED_PPS * game_framework.frame_time

        print(f'[BT] ChaseTarget: x={self.x:.1f}, target_x={self.target.x:.1f}')
        return BehaviorTree.RUNNING

    def bt_in_attack_range(self):
        if self.target is None:
            return BehaviorTree.FAIL

        dx = self.target.x - self.x
        distance = abs(dx)

        attack_range = 100  # 공격 범위
        print(f'[BT] InAttackRange: distance={distance:.1f}, attack_range={attack_range}')
        return BehaviorTree.SUCCESS if distance <= attack_range else BehaviorTree.FAIL


    def attack_target(self):
        if self.target is None:
            return BehaviorTree.FAIL
        if not hasattr(self.target, 'stats') or not self.target.stats.is_alive():
            return BehaviorTree.FAIL

        if self.attack_cooldown > 0.0:
            return BehaviorTree.FAIL

        profile = random.choice(self.attacks)
        payload = {'kind': profile['name'], 'target': self.target}
        self.state_machine.handle_state_event(('ATTACK', payload))

        self.attack_cooldown = self.attack_cooldown_time
        return BehaviorTree.SUCCESS

    def update(self):
        if self.attack_cooldown > 0.0:
            self.attack_cooldown = max(0.0, self.attack_cooldown - game_framework.frame_time)

        if self.stats.cur_hp <= 0 and not isinstance(self.state_machine.cur_state, EnemyDeath):
            self.state_machine.handle_state_event(('DEATH', None))
        self.state_machine.update()

        if hasattr(self, 'bt') and not isinstance(self.state_machine.cur_state, EnemyDeath):
            self.bt.run()


    def draw(self):
        self.state_machine.draw()
        hp_bar_x = 1280-400-100
        hp_bar_y = 620
        hp_bar_width = 400
        hp_bar_height = 50

        # HP 바 배경
        draw_rectangle(hp_bar_x, hp_bar_y, hp_bar_x + hp_bar_width, hp_bar_y + hp_bar_height)

        # 현재 HP에 따른 HP 바
        current_hp_width = (self.stats.cur_hp / self.stats.max_hp) * hp_bar_width
        if current_hp_width > 0:
            draw_rectangle(hp_bar_x, hp_bar_y, hp_bar_x + current_hp_width, hp_bar_y + hp_bar_height, 255,0,0,1,True)

        self.font.draw(self.x - 50, self.y + 150, f'HP: {self.stats.cur_hp}/{self.stats.max_hp}', (255, 255, 0))
        draw_rectangle(*self.get_bb())


    def handle_event(self, event):
        self.state_machine.handle_state_event(('INPUT', event))

    def get_bb(self):
        return self.x - 64, self.y - 256, self.x + 64, self.y + 32

    def handle_collision(self, group, other):
        attack_groups = {
            'player_lp:enemy': LeftPunch,
            'player_rp:enemy': RightPunch,
            'player_kick:enemy': Kick,
        }

        attack_state_cls = attack_groups.get(group)
        if not attack_state_cls:
            return

        cur_state = getattr(other.state_machine, 'cur_state', None)
        if not isinstance(cur_state, attack_state_cls):
            return
        if cur_state.hit:
            return

        cur_state.hit = True
        actual_damage = self.stats.take_damage(other.stats.attack)

        if not self.stats.is_alive():
            self.state_machine.handle_state_event(('DEATH', None))
        else:
            self.state_machine.handle_state_event(('HURT', None))

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
        if self.enemy.frame < self.enemy.max_frame:
            self.enemy.frame = (self.enemy.frame + 5 * ACTION_PER_TIME * game_framework.frame_time)
        else:
            game_world.remove_object(self.enemy)

    def draw(self):
        if self.enemy.face_dir == 1:
            self.enemy.image.clip_draw(int(self.enemy.frame) * 128, 0, 128, 128, self.enemy.x, self.enemy.y, 512, 512)
        else:
            self.enemy.image.clip_composite_draw(int(self.enemy.frame) * 128, 0, 128, 128, 0, 'h', self.enemy.x, self.enemy.y, 512, 512)

class EnemyHurt:
    def __init__(self, enemy):
        self.enemy = enemy

    def enter(self,event):
        self.enemy.image = self.enemy.hurt_image
        self.enemy.frame = 0
        self.enemy.wait_time = get_time()
        self.enemy.dir = 0
        self.enemy.max_frame = 3

    def exit(self, event):
        pass

    def do(self):
        if self.enemy.frame < self.enemy.max_frame:
            self.enemy.frame = (self.enemy.frame + 10 * ACTION_PER_TIME * game_framework.frame_time)
        else:
            self.enemy.state_machine.handle_state_event(('TIMEOUT', None))

    def draw(self):
        if self.enemy.face_dir == 1:
            self.enemy.image.clip_draw(int(self.enemy.frame) * 128, 0, 128, 128, self.enemy.x, self.enemy.y, 512, 512)
        else:
            self.enemy.image.clip_composite_draw(int(self.enemy.frame) * 128, 0, 128, 128, 0, 'h', self.enemy.x, self.enemy.y, 512, 512)

class EnemyAttack:
    def __init__(self, enemy):
        self.enemy = enemy
        self.profile = None

    def enter(self, event):
        payload = event[1] or {}
        kind = payload.get('kind', 'left_punch')

        self.profile = next(
            (p for p in self.enemy.attacks if p['name'] == kind),
            self.enemy.attacks[0]
        )
        self.enemy.current_attack_profile = self.profile

        self.enemy.image = self.profile['image']
        self.enemy.frame = 0
        self.enemy.max_frame = self.profile['frame_count']

        target = payload.get('target')
        if target and hasattr(target, 'stats') and target.stats.is_alive():
            damage = int(self.enemy.stats.attack * self.profile['damage'])
            target.stats.take_damage(damage)

    def exit(self, event):
        self.profile = None
        self.enemy.current_attack_profile = None

    def do(self):
        if self.enemy.frame < self.enemy.max_frame:
            self.enemy.frame += 5 * ACTION_PER_TIME * game_framework.frame_time
        else:
            self.enemy.state_machine.handle_state_event(('TIMEOUT', None))

    def draw(self):
        profile = self.enemy.current_attack_profile or self.enemy.attacks[0]
        src_x = int(self.enemy.frame) * 128
        src_y = 0

        img = profile['image']
        if self.enemy.face_dir == 1:
            img.clip_draw(src_x, src_y, 128, 128,
                          self.enemy.x, self.enemy.y, 512, 512)
        else:
            img.clip_composite_draw(src_x, src_y, 128, 128,
                                    0, 'h',
                                    self.enemy.x, self.enemy.y, 512, 512)