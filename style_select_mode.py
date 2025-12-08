from pico2d import *
import game_framework
import play_mode
import title_mode

image = None
font = None

buttons = {
    'striker': (260, 150, 800, 150),
    'grappler': (260, 330, 800, 150),
    'all_rounder': (260, 480, 800, 150)
}

selected = False


def init():
    global image, font, selected
    selected = False
    image = load_image('스타일 선택.png')
    font = load_font('ENCR10B.TTF', 20)


def finish():
    global image, font
    del image
    del font


def point_in_rect(px, py, rect):
    rx, ry, rw, rh = rect
    left = rx - rw // 2
    right = rx + rw // 2
    bottom = ry - rh // 2
    top = ry + rh // 2
    return left <= px <= right and bottom <= py <= top


def apply_style(style_type):
    global selected
    player = getattr(play_mode, 'player', None)
    if not player:
        return

    if style_type == 'striker':
        player.stats.max_hp(450)
        player.stats.attack(20)
        player.stats.defense(5)
    elif style_type == 'grappler':
        player.stats.max_hp(550)
        player.stats.attack(10)
        player.stats.defense(15)
    elif style_type == 'all_rounder':
        player.stats.max_hp(500)
        player.stats.attack(15)
        player.stats.defense(10)

    selected = True


def handle_events():
    global selected

    if selected:  # 이미 업그레이드했으면 이벤트 무시
        return

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_mode(title_mode)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            game_framework.pop_mode()
        elif event.type == SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_LEFT:
            mx, my = event.x, 720 - event.y

            if point_in_rect(mx, my, buttons['striker']):
                apply_style('striker')
                selected = True
                game_framework.pop_mode()
            elif point_in_rect(mx, my, buttons['grappler']):
                apply_style('grappler')
                selected = True
                game_framework.pop_mode()
            elif point_in_rect(mx, my, buttons['all_rounder']):
                apply_style('all_rounder')
                selected = True
                game_framework.pop_mode()



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
