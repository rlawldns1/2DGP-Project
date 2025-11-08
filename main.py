from pico2d import *
from player import Player
from cage import Cage

running = True

class Cage:
    def __init__(self):
        self.image = load_image('cagge.jpg')

    def update(self):
        pass

    def draw(self):
        self.image.draw(width/2, height/2)

def reset_world():
    global running
    global world

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
    global running, dir

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                running = False
            elif event.key == SDLK_RIGHT:
                dir += 1
            elif event.key == SDLK_LEFT:
                dir -= 1
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_RIGHT:
                dir -= 1
            elif event.key == SDLK_LEFT:
                dir += 1

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