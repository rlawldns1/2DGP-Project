from pico2d import *

running = True

class Player:
    def __init__(self):
        self.x = 400
        self.y = 300
        self.frame = 0
        self.dir = 0

def reset_world():
    pass

def update_world():
    pass

def render_world():
    pass

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

p = load_image('Walking.png')
background = load_image('cagge.jpg')

frame = 0
dir = 0
x = 400
while running:
    clear_canvas()
    background.draw(width/2,height/2)
    p.clip_draw(frame*128,0,128,128,x,300,512,512)
    update_canvas()
    handle_events()
    frame = (frame + 1) % 12
    x += dir * 5
    delay(0.1)

close_canvas()