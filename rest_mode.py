from pico2d import *
import game_framework
import play_mode
import title_mode

image = None
font = None

buttons = {
    'attack': (620, 450, 400, 100),
    'defense': (620, 300, 400, 100),
    'hp': (620, 150, 400, 100)
}

upgraded = False


def init():
    global image, font, upgraded
    upgraded = False
    image = load_image('resttime.png')
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


def apply_upgrade(upgrade_type):
    global upgraded, upgrade_msg
    player = getattr(play_mode, 'player', None)
    if not player:
        return

    if upgrade_type == 'attack':
        player.stats.upgrade_attack(5)
    elif upgrade_type == 'defense':
        player.stats.upgrade_defense(5)
    elif upgrade_type == 'hp':
        player.stats.upgrade_hp(20)

    upgraded = True


def handle_events():
    global upgraded

    if upgraded:  # 이미 업그레이드했으면 이벤트 무시
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

            if point_in_rect(mx, my, buttons['attack']):
                apply_upgrade('attack')
                upgraded = True
                game_framework.pop_mode()
            elif point_in_rect(mx, my, buttons['defense']):
                apply_upgrade('defense')
                upgraded = True
                game_framework.pop_mode()
            elif point_in_rect(mx, my, buttons['hp']):
                apply_upgrade('hp')
                upgraded = True
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
