from pico2d import *



open_canvas()

p = load_image('punch_1.png')

for x in range(0,800,5):
    clear_canvas()
    p.draw(400,300)
    update_canvas()
    delay(0.01)

close_canvas()