from pico2d import *
import game_framework
import play_mode
import title_mode
from welcometoufc import WelcomeToUFC

image = None
p = None
e1 = e2 = e3 = e4 = e5 = e6 = e7 = None
match = 0
selected_style = None
ufc = None
ufc_timer = 0.0

def init():
    global image, p, e1, e2, e3, e4, e5, e6, e7, match, ufc_timer
    image = load_image('tournament.png')
    p = load_image('profile/player.png')
    e1 = load_image('profile/enemy1.png')
    e2 = load_image('profile/enemy2.png')
    e3 = load_image('profile/enemy3.png')
    e4 = load_image('profile/enemy4.png')
    e5 = load_image('profile/enemy5.png')
    e6 = load_image('profile/enemy6.png')
    e7 = load_image('profile/enemy7.png')
    ufc = None
    ufc_timer = 0.0


def finish():
    global image, p, e1, e2, e3, e4, e5, e6, e7, ufc, ufc_timer
    del image, p, e1, e2, e3, e4, e5, e6, e7, ufc_timer
    if ufc:
        del ufc



def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE and match < 4:
            game_framework.change_mode(play_mode)

def draw():
    clear_canvas()
    image.draw(640, 360, 1280, 720)

    if match == 0:
        p.draw(190,120,100,100)
        e1.draw(320,120,100,100)
        e2.draw(450,120,100,100)
        e3.draw(580,120,100,100)
        e4.draw(710,120,100,100)
        e5.draw(840,120,100,100)
        e6.draw(970,120,100,100)
        e7.draw(1100,120,100,100)
    elif match == 1:
        p.draw(190, 120, 100, 100)
        e1.draw(320, 120, 100, 100)
        e2.draw(450, 120, 100, 100)
        e3.draw(580, 120, 100, 100)
        e4.draw(710, 120, 100, 100)
        e5.draw(840, 120, 100, 100)
        e6.draw(970, 120, 100, 100)
        e7.draw(1100, 120, 100, 100)
        p.draw(255,290,100,100)
        e2.draw(515,290,100,100)
        e4.draw(765,290,100,100)
        e6.draw(1025,290,100,100)
    elif match == 2:
        p.draw(190, 120, 100, 100)
        e1.draw(320, 120, 100, 100)
        e2.draw(450, 120, 100, 100)
        e3.draw(580, 120, 100, 100)
        e4.draw(710, 120, 100, 100)
        e5.draw(840, 120, 100, 100)
        e6.draw(970, 120, 100, 100)
        e7.draw(1100, 120, 100, 100)
        p.draw(255, 290, 100, 100)
        e2.draw(515, 290, 100, 100)
        e4.draw(765, 290, 100, 100)
        e6.draw(1025, 290, 100, 100)
        p.draw(385,460,100,100)
        e4.draw(895,460,100,100)
    elif match == 3:
        p.draw(190, 120, 100, 100)
        e1.draw(320, 120, 100, 100)
        e2.draw(450, 120, 100, 100)
        e3.draw(580, 120, 100, 100)
        e4.draw(710, 120, 100, 100)
        e5.draw(840, 120, 100, 100)
        e6.draw(970, 120, 100, 100)
        e7.draw(1100, 120, 100, 100)
        p.draw(255, 290, 100, 100)
        e2.draw(515, 290, 100, 100)
        e4.draw(765, 290, 100, 100)
        e6.draw(1025, 290, 100, 100)
        p.draw(385, 460, 100, 100)
        e4.draw(895, 460, 100, 100)
        p.draw(640,650,100,100)


    elif match == 4:
        ufc.draw()

    update_canvas()

def update():
    global  match, ufc, ufc_timer
    if match == 3:
        ufc_timer += 0.01
        if ufc_timer > 3:
            match = 4
            ufc = WelcomeToUFC()
            ufc_timer = 0.0
    if ufc:
        ufc.update()

def pause():
    pass

def resume():
    pass
