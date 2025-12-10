from pico2d import *

import game_framework
import game_world
import style_select_mode
import title_mode
import win_mode
import lose_mode
import rest_mode
from player import Player
from cage import Cage
from enemy import Enemy
import tournament_mode

running = True
player = None

time_left = 30
_time_acc = 0.0
time_font = None

style_presets = {
    'striker': (450, 20, 5),
    'grappler': (600, 10, 10),
    'all_rounder': (500, 15, 10)
}

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_mode(title_mode)
        else:
            player.handle_event(event)

def apply_selected_style():
    style = getattr(tournament_mode, 'selected_style', None)
    stats = style_presets.get(style)
    if stats and player:
        player.stats.set_stats(*stats)

def init():
    global running
    global player
    global time_left, _time_acc, time_font
    running = True

    time_left = 30
    _time_acc = 0.0
    time_font = load_font('ENCR10B.TTF', 50)

    cage = Cage()
    game_world.add_object(cage,0)

    if player is None:
        player = Player()
        apply_selected_style()
    else:
        player.stats.full_heal()

    game_world.add_object(player,1)

    cur_match = tournament_mode.match

    # 1번 상대
    if cur_match == 0:
        enemy = Enemy(x=950, y=300,
            max_hp=500, attack_=15, defense=5,
            attack_cooldown_time=1.0,
            idle_image_path='Enemy/dodge.png',
            death_image_path='Enemy/Death.png',
            hurt_image_path='Enemy/hurt.png',
            left_punch_image_path='Enemy/Punch_2.png',
            right_punch_image_path='Enemy/Punch_1.png',
            kick_image_path='Enemy/Kick.png')

    # 2번 상대
    elif cur_match == 1:
        enemy = Enemy(x=950, y=300,
                       max_hp=500, attack_=20, defense=10,
                       attack_cooldown_time=0.8,
                       idle_image_path='Enemy2/dodge.png',
                       death_image_path='Enemy2/Death.png',
                       hurt_image_path='Enemy2/hurt.png',
                       left_punch_image_path='Enemy2/Punch_2.png',
                       right_punch_image_path='Enemy2/Punch_1.png',
                       kick_image_path='Enemy2/Kick.png')


    # 3번 상대
    elif cur_match == 2:
        enemy = Enemy(x=950, y=300,
                       max_hp=500, attack_=25, defense=10,
                       attack_cooldown_time=1.0,
                       idle_image_path='Enemy4/dodge.png',
                       death_image_path='Enemy4/Death.png',
                       hurt_image_path='Enemy4/hurt.png',
                       left_punch_image_path='Enemy4/Punch_2.png',
                       right_punch_image_path='Enemy4/Punch_1.png',
                       kick_image_path='Enemy4/Kick.png')

    enemy.set_target(player)
    game_world.add_object(enemy, 1)

    game_world.collision_pairs.clear()
    game_world.add_collision_pair('player_lp:enemy', player, enemy)
    game_world.add_collision_pair('player_rp:enemy', player, enemy)
    game_world.add_collision_pair('player_kick:enemy', player, enemy)
    game_world.add_collision_pair('enemy_lp:player', enemy, player)
    game_world.add_collision_pair('enemy_rp:player', enemy, player)
    game_world.add_collision_pair('enemy_kick:player', enemy, player)


def update():
    global time_left, _time_acc


    _time_acc += game_framework.frame_time
    while _time_acc >= 1.0 and time_left > 0:
        time_left -= 1
        _time_acc -= 1.0
        if time_left < 0:
            time_left = 0
    if time_left == 0:
        game_framework.push_mode(rest_mode)

    game_world.update()
    game_world.handle_collisions()

    enemies = [obj for obj in game_world.world[1] if isinstance(obj, Enemy)]
    if len(enemies) == 0:
        game_framework.change_mode(win_mode)
    if player.stats.cur_hp == 0:
        game_framework.change_mode(lose_mode)

def draw():
    clear_canvas()
    game_world.render()

    timer_x = 640
    timer_y = 650
    display_text = f'{int(time_left)}'
    time_font.draw(timer_x-20, timer_y, display_text, (255, 255, 255))

    update_canvas()

def finish():
    global time_font
    game_world.clear()
    if time_font:
        del time_font
        time_font = None

def pause():
    pass

def resume():
    global time_left, _time_acc
    time_left = 30
    _time_acc = 0.0