from pico2d import *

running = True

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

open_canvas()

p = load_image('punch_1.png')

frame = 0
dir = 0
x = 400
while running:
    clear_canvas()
    p.clip_draw(frame*128,0,128,128,x,90)
    update_canvas()
    handle_events()
    frame = (frame + 1) % 5
    x += dir * 5
    delay(0.1)

close_canvas()