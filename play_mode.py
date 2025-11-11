from pico2d import *

import game_framework
import game_world
import title_mode
from player import Player
from cage import Cage
from enemy import Enemy

running = True
player = None

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

    running = True

    cage = Cage()
    game_world.add_object(cage,0)

    player = Player()
    game_world.add_object(player,1)

    enemy = Enemy()
    game_world.add_object(enemy,1)

    game_world.add_collision_pair('player_lp:enemy',None, enemy)
    game_world.add_collision_pair('player_rp:enemy', None, enemy)
    game_world.add_collision_pair('player_kick:enemy', None, enemy)


def update():
    game_world.update()
    game_world.handle_collisions()


def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def finish():
    game_world.clear()