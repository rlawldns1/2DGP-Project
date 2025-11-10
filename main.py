from pico2d import *

import game_world
from player import Player
from cage import Cage

running = True
player = None

def reset_world():
    global running
    global world
    global player

    running = True

    cage = Cage()
    game_world.add_object(cage)

    player = Player()
    game_world.add_object(player)

def update_world():
    game_world.update()


def render_world():
    clear_canvas()
    game_world.render()
    update_canvas()

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


width = 1280
height = 720
open_canvas(width,height)

dir = 0

reset_world()

while running:
    handle_events()
    update_world()
    render_world()
    delay(0.1)

close_canvas()