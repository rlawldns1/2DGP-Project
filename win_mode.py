from pico2d import *
import game_framework
import tournament_mode

image = None

def init():
    global image
    image = load_image('youwin.png')

def finish():
    global image
    del image

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            game_framework.change_mode(tournament_mode)

def draw():
    clear_canvas()
    image.draw(640, 360, 1280, 720)
    update_canvas()

def update():
    pass

def pause():
    pass

def resume():
    pass
