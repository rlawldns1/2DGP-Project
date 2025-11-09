from pico2d import *

from player import Player
from cage import Cage

running = True
player = None

def reset_world():
    global running
    global world
    global player

    running = True
    world = []

    cage = Cage()
    world.append(cage)

    player = Player()
    world.append(player)

def update_world():
    for o in world:
        o.update()


def render_world():
    clear_canvas()
    for o in world:
        o.draw()
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