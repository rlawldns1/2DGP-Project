from pico2d import *

import game_world
from player import Player
from cage import Cage

running = True
player = None

def handle_events():
    global running

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        else:
            if player is not None:
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

def update():
    game_world.update()

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def finish():
    pass