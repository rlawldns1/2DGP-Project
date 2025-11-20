from pico2d import *

import game_framework
import game_world
import title_mode
from player import Player
from cage import Cage
from enemy import Enemy

running = True
player = None

time_left = 60
_time_acc = 0.0
time_font = None

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_mode(title_mode)
        else:
            player.handle_event(event)

def init():
    global running
    global world
    global player
    global time_left, _time_acc, time_font
    running = True

    time_left = 60
    _time_acc = 0.0
    time_font = load_font('ENCR10B.TTF', 50)

    cage = Cage()
    game_world.add_object(cage,0)

    player = Player()
    game_world.add_object(player,1)

    enemy = Enemy()
    game_world.add_object(enemy,1)

    game_world.add_collision_pair('player_lp:enemy', player, enemy)
    game_world.add_collision_pair('player_rp:enemy', player, enemy)
    game_world.add_collision_pair('player_kick:enemy', player, enemy)


def update():
    global time_left, _time_acc

    game_world.update()
    game_world.handle_collisions()

    _time_acc += game_framework.frame_time
    while _time_acc >= 1.0 and time_left > 0:
        time_left -= 1
        _time_acc -= 1.0
        if time_left < 0:
            time_left = 0

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